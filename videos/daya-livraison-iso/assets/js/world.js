// The isometric seaside world. One orthographic camera travels one continuous town;
// every object's state is a pure function of HyperFrames time (hf-seek), so any frame
// can be rendered in any order.
import * as THREE from "../vendor/three.module.min.js";
import { mergeGeometries } from "../vendor/BufferGeometryUtils.js";
import { RoundedBoxGeometry } from "../vendor/RoundedBoxGeometry.js";
import { clamp, lerp, inv, seg, env, pop, E, back, rng, track, hop, TAU, DEG } from "./util.js";
import { PAL } from "./palette.js";
import * as TX from "./textures.js";
import * as M from "./models.js";

const W = 1080;
const H = 1920;
const ASPECT = W / H;
const ISO_EL = 35.264;

// ---------------------------------------------------------------- key times
export const T = {
  SW: 4.6, // match cut: phone map → real island
  SHOP: 10.6,
  DEPART: 18.65,
  ARRIVE_A: 21.2,
  LEAVE_A: 24.45,
  ARRIVE_B: 26.3,
  LEAVE_B: 28.7,
  END_RUN: 31.4,
};

// ---------------------------------------------------------------- renderer
const canvas = document.getElementById("gl");
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true, preserveDrawingBuffer: true });
renderer.setPixelRatio(1);
renderer.setSize(W, H, false);
renderer.setClearColor(0x000000, 0);
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.NoToneMapping;

const scene = new THREE.Scene();
const cam = new THREE.OrthographicCamera(-1, 1, 1, -1, 1, 400);
const rtCam = new THREE.OrthographicCamera(-1, 1, 1, -1, 1, 400);
const rt = new THREE.WebGLRenderTarget(1080, 1920, { samples: 4 });
rt.texture.colorSpace = THREE.SRGBColorSpace;

const hemi = new THREE.HemisphereLight(0xfff1e0, 0x9cc7d8, 1.85);
scene.add(hemi);
const sun = new THREE.DirectionalLight(0xfff0d8, 2.55);
sun.castShadow = true;
sun.shadow.mapSize.set(2048, 2048);
sun.shadow.bias = -0.0004;
sun.shadow.normalBias = 0.03;
scene.add(sun, sun.target);
const SUN_DIR = new THREE.Vector3(-0.42, 1, 0.62).normalize();

// ---------------------------------------------------------------- camera math
function camDir(azDeg, elDeg) {
  const az = azDeg * DEG,
    el = elDeg * DEG;
  return new THREE.Vector3(Math.cos(el) * Math.cos(az), Math.sin(el), Math.cos(el) * Math.sin(az));
}
function camBasis(azDeg, elDeg) {
  const d = camDir(azDeg, elDeg);
  const right = new THREE.Vector3(d.z, 0, -d.x).normalize();
  const up = new THREE.Vector3().crossVectors(d, right).normalize();
  return { d, right, up };
}
function applyCam(c, s) {
  const d = camDir(s.az, s.el);
  c.position.set(s.tx + d.x * 150, s.ty + d.y * 150, s.tz + d.z * 150);
  c.up.set(0, 1, 0);
  c.lookAt(s.tx, s.ty, s.tz);
  const vw = s.vh * ASPECT;
  c.left = -vw / 2;
  c.right = vw / 2;
  c.top = s.vh * s.fy;
  c.bottom = -s.vh * (1 - s.fy);
  c.near = 1;
  c.far = 420;
  c.updateProjectionMatrix();
}
const shot = (tx, ty, tz, vh, az = 45, el = ISO_EL, fy = 0.56) => ({ tx, ty, tz, vh, az, el, fy });
function blend(a, b, p) {
  return {
    tx: lerp(a.tx, b.tx, p),
    ty: lerp(a.ty, b.ty, p),
    tz: lerp(a.tz, b.tz, p),
    vh: Math.exp(lerp(Math.log(a.vh), Math.log(b.vh), p)),
    az: lerp(a.az, b.az, p),
    el: lerp(a.el, b.el, p),
    fy: lerp(a.fy, b.fy, p),
  };
}
// keys: [time, shotFn(t) | shot, ease arriving at this key]
function camTrack(keys) {
  const fn = (k, t) => (typeof k === "function" ? k(t) : k);
  return (t) => {
    if (t <= keys[0][0]) return fn(keys[0][1], t);
    for (let i = 1; i < keys.length; i++) {
      if (t <= keys[i][0]) {
        const p = (keys[i][2] || E.inOut3)(inv(keys[i - 1][0], keys[i][0], t));
        return blend(fn(keys[i - 1][1], t), fn(keys[i][1], t), p);
      }
    }
    return fn(keys[keys.length - 1][1], t);
  };
}

// ---------------------------------------------------------------- shared state
const sprites = [];
let CUR_VH = 40; // current frame's view height (wide vs close marker styles)
const tickers = []; // (t) => void, ambient + scripted motion
let tex, prints, spr;
let staticRoot;
const W_ = {}; // named world handles (houses, van, people…)

function makeSprite(map, px, { aspect = 1, center = [0.5, 0.5] } = {}) {
  const m = new THREE.SpriteMaterial({ map, transparent: true, depthTest: false, depthWrite: false });
  const s = new THREE.Sprite(m);
  s.center.set(center[0], center[1]);
  s.renderOrder = 30;
  s.userData = { px, aspect, k: 0 };
  scene.add(s);
  sprites.push(s);
  return s;
}
function updateSprites(vh) {
  const zoomK = clamp(Math.pow(30 / vh, 0.45), 0.7, 1.25);
  for (const s of sprites) {
    const k = ((s.userData.px * vh) / H) * s.userData.k * (s.userData.fixed ? 1 : zoomK);
    s.visible = k > 1e-4 && s.material.opacity > 0.003;
    s.scale.set(Math.max(k, 1e-4) * s.userData.aspect, Math.max(k, 1e-4), 1);
  }
}

// ---------------------------------------------------------------- path helper
function buildPath(corners, R = 1.5, lane = 0.55) {
  const raw = [];
  const P = corners.map(([x, z]) => new THREE.Vector2(x, z));
  raw.push(P[0].clone());
  for (let i = 1; i < P.length - 1; i++) {
    const a = P[i].clone().sub(P[i - 1]).normalize();
    const b = P[i + 1].clone().sub(P[i]).normalize();
    const s0 = P[i].clone().addScaledVector(a, -R);
    const s1 = P[i].clone().addScaledVector(b, R);
    raw.push(s0);
    for (let k = 1; k < 12; k++) {
      const u = k / 12;
      const x = (1 - u) * (1 - u) * s0.x + 2 * (1 - u) * u * P[i].x + u * u * s1.x;
      const y = (1 - u) * (1 - u) * s0.y + 2 * (1 - u) * u * P[i].y + u * u * s1.y;
      raw.push(new THREE.Vector2(x, y));
    }
    raw.push(s1);
  }
  raw.push(P[P.length - 1].clone());
  // densify straight runs, then offset to the right-hand lane
  const dense = [];
  for (let i = 0; i < raw.length - 1; i++) {
    const a = raw[i],
      b = raw[i + 1];
    const n = Math.max(1, Math.ceil(a.distanceTo(b) / 0.5));
    for (let k = 0; k < n; k++) dense.push(a.clone().lerp(b, k / n));
  }
  dense.push(raw[raw.length - 1].clone());
  const pts = dense.map((p, i) => {
    const q = dense[Math.min(i + 1, dense.length - 1)];
    const o = dense[Math.max(i - 1, 0)];
    const tg = q.clone().sub(o).normalize();
    // right of heading (x,z) with y up = (-tz, tx)
    return new THREE.Vector2(p.x - tg.y * lane, p.y + tg.x * lane);
  });
  const cum = [0];
  for (let i = 1; i < pts.length; i++) cum.push(cum[i - 1] + pts[i].distanceTo(pts[i - 1]));
  const len = cum[cum.length - 1];
  function at(s) {
    s = clamp(s, 0, len);
    let lo = 0,
      hi = cum.length - 1;
    while (hi - lo > 1) {
      const mid = (lo + hi) >> 1;
      if (cum[mid] <= s) lo = mid;
      else hi = mid;
    }
    const u = (s - cum[lo]) / Math.max(1e-6, cum[hi] - cum[lo]);
    const p = pts[lo].clone().lerp(pts[hi], u);
    const tg = pts[hi].clone().sub(pts[lo]).normalize();
    return { x: p.x, z: p.y, tx: tg.x, tz: tg.y };
  }
  function nearest(x, z, minS = -1) {
    let best = 0,
      bd = 1e9;
    for (let i = 0; i < pts.length; i++) {
      if (cum[i] < minS) continue;
      const d = (pts[i].x - x) ** 2 + (pts[i].y - z) ** 2;
      if (d < bd) {
        bd = d;
        best = i;
      }
    }
    return cum[best];
  }
  return { at, nearest, len, pts, cum };
}

// ================================================================= BUILD
async function build() {
  await Promise.all([
    document.fonts.load(`900 80px ${TX.FONT_D}`),
    document.fonts.load(`800 80px ${TX.FONT_D}`),
    document.fonts.load(`700 80px ${TX.FONT_D}`),
    document.fonts.load(`500 80px ${TX.FONT_D}`),
  ]);
  prints = TX.printTextures();
  spr = TX.spriteTextures();
  tex = {
    sign: TX.signTexture("daya_na990", { size: 118 }),
    vanSide: TX.signTexture("daya_na990", { bg: null, size: 128, sub: "Livraison à domicile", h: 300 }),
    topper: (() => {
      const { c, g } = TX.canvas(256, 256);
      g.fillStyle = "#FFFFFF";
      g.beginPath();
      g.arc(128, 128, 120, 0, TAU);
      g.fill();
      g.fillStyle = PAL.coral;
      TX.heartPath(g, 128, 120, 160);
      g.fill();
      return TX.tex(c);
    })(),
    sticker: TX.stickerTexture(),
    awning: TX.stripeTexture(PAL.coral, "#FFFFFF", 12, 512, 64, true),
    parasolA: TX.stripeTexture(PAL.coral, "#FFFFFF", 12, 512, 32, true),
    parasolB: TX.stripeTexture(PAL.teal, "#FFFFFF", 12, 512, 32, true),
    parasolC: TX.stripeTexture(PAL.sun, "#FFFFFF", 12, 512, 32, true),
    towelA: TX.stripeTexture(PAL.coral, PAL.sun, 6, 64, 256, false),
    towelB: TX.stripeTexture(PAL.teal, "#FFFFFF", 6, 64, 256, false),
    dash: TX.dashTexture(),
    pageBg: (() => {
      // mirrors #bg (radial-gradient 120% 75% at 50% 42%) + the sun glow, for the phone map pass
      const { c, g } = TX.canvas(1080, 1920);
      g.save();
      g.translate(540, 806.4);
      g.scale(1296 / 1440, 1);
      const gr = g.createRadialGradient(0, 0, 0, 0, 0, 1440);
      gr.addColorStop(0, "#FFF6EC");
      gr.addColorStop(0.48, "#FFE3D2");
      gr.addColorStop(1, "#FFC4AB");
      g.fillStyle = gr;
      g.fillRect(-2000, -2000, 4000, 4000);
      g.restore();
      const sg = g.createRadialGradient(890, 160, 0, 890, 160, 693);
      sg.addColorStop(0, "rgba(255,214,110,0.85)");
      sg.addColorStop(0.38, "rgba(255,214,110,0.32)");
      sg.addColorStop(0.68, "rgba(255,214,110,0)");
      g.fillStyle = sg;
      g.fillRect(0, 0, 1080, 1920);
      return TX.tex(c, { mips: false });
    })(),
    mapMask: TX.roundMask(600, 1067, 26),
  };

  staticRoot = new THREE.Group();
  scene.add(staticRoot);
  buildIsland();
  buildTown();
  buildShop();
  buildVanAndRoute();
  buildPeople();
  buildPhone();
  buildMarkers();
  mergeStatic();
}

// ---------------------------------------------------------------- island
function buildIsland() {
  const S = staticRoot;
  // water body (cross-section) + animated surface
  M.box(42, 2.7, 42, "#22ADBF", { x: 2.5, y: -1.85, z: 2.5, r: 0, parent: scene, cast: false });
  const wg = new THREE.PlaneGeometry(42, 42, 48, 48);
  wg.rotateX(-Math.PI / 2);
  const water = new THREE.Mesh(
    wg,
    new THREE.MeshStandardMaterial({ color: PAL.sea, roughness: 0.28, metalness: 0.0, flatShading: true, transparent: true, opacity: 0.95 }),
  );
  water.position.set(2.5, -0.5, 2.5);
  water.receiveShadow = true;
  scene.add(water);
  const base = wg.attributes.position.array.slice();
  tickers.push((t) => {
    const a = wg.attributes.position.array;
    for (let i = 0; i < a.length; i += 3) {
      const x = base[i] + 2.5,
        z = base[i + 2] + 2.5;
      a[i + 1] = base[i + 1] + 0.07 * Math.sin(x * 0.55 + t * 1.7) + 0.05 * Math.sin(z * 0.47 - t * 1.25) + 0.03 * Math.sin((x + z) * 0.9 + t * 2.3);
    }
    wg.attributes.position.needsUpdate = true;
  });
  // sand shelf (beach) and the town plateau, with visible strata on the cut sides
  M.mesh(new THREE.BoxGeometry(32.5, 3.0, 32.5), [M.mat(PAL.sandDeep), M.mat(PAL.sandDeep), M.mat(PAL.sand), M.mat(PAL.sandDeep), M.mat(PAL.sandDeep), M.mat(PAL.sandDeep)], {
    x: 2.25,
    y: -1.62,
    z: 2.25,
    parent: S,
    cast: false,
  });
  M.mesh(new THREE.BoxGeometry(27, 0.42, 27), [M.mat(PAL.grassDeep), M.mat(PAL.grassDeep), M.mat(PAL.pave), M.mat(PAL.grassDeep), M.mat(PAL.grassDeep), M.mat(PAL.grassDeep)], {
    x: -0.5,
    y: -0.21,
    z: -0.5,
    parent: S,
    cast: false,
  });
  M.mesh(new THREE.BoxGeometry(26.9, 2.7, 26.9), M.mat(PAL.soil), { x: -0.5, y: -1.77, z: -0.5, parent: S, cast: false });
  // shoreline foam that laps in and out
  const foamM = new THREE.MeshBasicMaterial({ color: PAL.foam, transparent: true, opacity: 0.8 });
  const foams = [];
  for (let k = 0; k < 2; k++) {
    const fx = M.mesh(new THREE.BoxGeometry(0.35, 0.04, 32.5), foamM.clone(), { x: 18.6, y: -0.42, z: 2.25, parent: scene, cast: false });
    const fz = M.mesh(new THREE.BoxGeometry(32.9, 0.04, 0.35), foamM.clone(), { x: 2.25, y: -0.42, z: 18.6, parent: scene, cast: false });
    foams.push([fx, fz, k]);
  }
  tickers.push((t) => {
    for (const [fx, fz, k] of foams) {
      const ph = t * 1.4 + k * Math.PI;
      const o = 0.25 + 0.45 * (0.5 + 0.5 * Math.sin(ph));
      fx.position.x = 18.55 + o;
      fz.position.z = 18.55 + o;
      fx.material.opacity = fz.material.opacity = 0.35 + 0.5 * (0.5 - 0.5 * Math.sin(ph));
    }
  });
  // promenade sea wall
  for (const [x, z, w, d] of [
    [13.05, -6.5, 0.22, 15],
    [13.05, 9.5, 0.22, 7],
    [-7.5, 13.05, 13, 0.22],
    [8.0, 13.05, 10, 0.22],
  ])
    M.box(w, 0.32, d, "#FFFFFF", { x, y: 0.16, z, parent: S, r: 0.05 });
}

// ---------------------------------------------------------------- town
function buildTown() {
  const S = staticRoot;
  const road = M.mat(PAL.road);
  const roads = [
    // [x0,x1,z0,z1]
    [-14, 11.8, -1.2, 1.2], // H
    [-1.2, 1.2, -14, 11.8], // V
    [9.4, 11.8, -14, 11.8], // C
    [-14, 11.8, 9.4, 11.8], // S
  ];
  for (const [x0, x1, z0, z1] of roads) M.mesh(new THREE.BoxGeometry(x1 - x0, 0.06, z1 - z0), road, { x: (x0 + x1) / 2, y: 0.03, z: (z0 + z1) / 2, parent: S, cast: false });
  // dashed centre lines, skipping junctions
  const near = (v, list) => list.some((c) => Math.abs(v - c) < 2.0);
  const dash = M.mat(PAL.roadLine);
  for (let x = -13.4; x < 11; x += 1.3) {
    if (!near(x, [0, 10.6])) {
      M.mesh(new THREE.BoxGeometry(0.62, 0.02, 0.1), dash, { x, y: 0.065, z: 0, parent: S, cast: false });
      M.mesh(new THREE.BoxGeometry(0.62, 0.02, 0.1), dash, { x, y: 0.065, z: 10.6, parent: S, cast: false });
    }
  }
  for (let z = -13.4; z < 11; z += 1.3) {
    if (!near(z, [0, 10.6])) {
      M.mesh(new THREE.BoxGeometry(0.1, 0.02, 0.62), dash, { x: 0, y: 0.065, z, parent: S, cast: false });
      M.mesh(new THREE.BoxGeometry(0.1, 0.02, 0.62), dash, { x: 10.6, y: 0.065, z, parent: S, cast: false });
    }
  }
  // zebra crossings
  for (const [cx, cz, alongX] of [
    [-2.0, 0, false],
    [0, 2.0, true],
    [8.8, 0, false],
    [10.6, 8.6, true],
  ]) {
    for (let k = -2; k <= 2; k++) {
      if (alongX) M.mesh(new THREE.BoxGeometry(0.34, 0.02, 1.2), dash, { x: cx + k * 0.48, y: 0.066, z: cz, parent: S, cast: false });
      else M.mesh(new THREE.BoxGeometry(1.2, 0.02, 0.34), dash, { x: cx, y: 0.066, z: cz + k * 0.48, parent: S, cast: false });
    }
  }
  // lawns inside the blocks
  const lawn = M.mat(PAL.grass);
  for (const [x0, x1, z0, z1] of [
    [2.0, 8.6, -13.2, -2.0],
    [2.0, 8.6, 2.0, 8.6],
    [-13.2, -2.0, 2.0, 8.6],
    [-13.2, -10.6, -13.2, -2.0],
    [-10.6, -2.0, -13.2, -9.9],
  ])
    M.mesh(new THREE.BoxGeometry(x1 - x0, 0.08, z1 - z0), lawn, { x: (x0 + x1) / 2, y: 0.04, z: (z0 + z1) / 2, parent: S, cast: false });

  // houses — door on +z (yaw 0) or +x (yaw π/2)
  const defs = {
    N1: { x: 4.3, z: -4.6, yaw: 0, w: 3.4, d: 3.4, wall: PAL.white, roof: PAL.roofCoral, roofType: "gable", door: PAL.teal, shutter: PAL.teal, seed: 2, awning: null },
    N3: { x: 2.9, z: -10.4, yaw: 0, w: 2.8, d: 3.0, h: 2.3, floors: 2, wall: PAL.wallButter, roof: PAL.roofTeal, roofType: "hip", door: PAL.coral, shutter: PAL.coral, seed: 5 },
    N2: { x: 6.3, z: -9.6, yaw: Math.PI / 2, w: 3.2, d: 3.4, wall: PAL.wallMint, roof: PAL.coral, roofType: "flat", door: PAL.coral, shutter: PAL.roofTerra, seed: 7 },
    A: { x: 5.3, z: 2.9, yaw: Math.PI / 2, w: 3.0, d: 3.2, wall: PAL.wallPeach, roof: PAL.roofTerra, roofType: "gable", door: PAL.teal, shutter: PAL.teal, seed: 3, awning: PAL.teal, hingeRight: true },
    B: { x: 2.8, z: 6.2, yaw: 0, w: 3.0, d: 3.0, wall: PAL.white, roof: PAL.roofTeal, roofType: "gable", door: PAL.coral, shutter: PAL.coral, seed: 11, awning: PAL.coral },
    S1: { x: -3.8, z: 4.8, yaw: Math.PI / 2, w: 3.2, d: 3.2, wall: PAL.wallMint, roof: PAL.roofCoral, roofType: "gable", door: PAL.sun, shutter: PAL.sun, seed: 13 },
    S2: { x: -8.8, z: 6.6, yaw: 0, w: 3.4, d: 3.0, h: 2.3, floors: 2, wall: PAL.wallPeach, roof: PAL.coral, roofType: "flat", door: PAL.teal, shutter: PAL.teal, seed: 17 },
  };
  W_.houses = {};
  for (const [name, o] of Object.entries(defs)) {
    const h = M.house(o);
    h.group.position.set(o.x, 0, o.z);
    h.group.rotation.y = o.yaw;
    scene.add(h.group);
    h.group.updateMatrixWorld(true);
    h.name = name;
    h.doorW = h.doorstep.clone().applyMatrix4(h.group.matrixWorld);
    h.bellW = h.bell.clone().applyMatrix4(h.group.matrixWorld);
    h.topW = new THREE.Vector3(o.x, h.top + (o.roofType === "flat" ? 0.4 : o.roofType === "hip" ? 1.3 : 1.15), o.z);
    // the door hinge stays live; the rest of the house merges into the static mesh
    h.group.remove(h.hinge);
    staticAdopt(h.group);
    const hw = new THREE.Group();
    hw.position.copy(h.group.position);
    hw.rotation.copy(h.group.rotation);
    hw.add(h.hinge);
    scene.add(hw);
    hw.updateMatrixWorld(true);
    h.hingeParent = hw;
    W_.houses[name] = h;
  }

  // swimming pool in the SW block
  M.box(5.2, 0.26, 2.4, "#FFFFFF", { x: -8.6, y: 0.13, z: 2.95, parent: S, r: 0.08 });
  M.mesh(new THREE.BoxGeometry(4.7, 0.05, 1.9), new THREE.MeshStandardMaterial({ color: "#5FE0E6", roughness: 0.15 }), { x: -8.6, y: 0.25, z: 2.95, parent: S, cast: false });
  for (const x of [-10.2, -9.1]) {
    M.box(0.6, 0.1, 1.3, "#FFFFFF", { x, y: 0.3, z: 4.6, parent: S, r: 0.04 });
    M.box(0.6, 0.06, 0.5, PAL.coral, { x, y: 0.48, z: 4.15, rx: -0.6, parent: S, r: 0.03 });
  }
  // palms, trees, lamps, benches, parasols
  W_.palms = [];
  const palmAt = (x, z, seed, s = 1, live = false) => {
    const p = M.palm(seed, s);
    p.group.position.set(x, 0, z);
    if (live) {
      scene.add(p.group);
      W_.palms.push(p);
    } else S.add(p.group);
  };
  palmAt(12.4, -11.5, 1, 1.05);
  palmAt(12.4, -5.6, 2, 0.95, true);
  palmAt(12.4, 1.8, 3, 1.1, true);
  palmAt(12.4, 7.0, 4, 1.0, true);
  palmAt(-11.6, 12.4, 5, 1.0);
  palmAt(-5.0, 12.4, 6, 1.05);
  palmAt(7.6, 12.4, 7, 1.0, true);
  palmAt(12.5, 12.5, 8, 1.15, true);
  palmAt(-12.2, -3.2, 9, 1.0);
  palmAt(-12.2, -7.8, 10, 1.1);
  palmAt(-7.0, 1.9, 11, 0.9);
  palmAt(-2.2, -12.4, 13, 1.0);
  for (const [x, z, sd, s] of [
    [-11.5, -11.5, 1, 1.0],
    [-8.5, -11.8, 2, 0.9],
    [-5.0, -11.6, 3, 1.1],
    [-12.0, 7.5, 4, 0.9],
    [6.5, -12.6, 5, 0.9],
    [-12.4, 2.4, 6, 0.8],
  ]) {
    const tr = M.tree(sd, s);
    tr.position.set(x, 0, z);
    S.add(tr);
  }
  for (const [x, z] of [
    [12.3, -9],
    [12.3, -2],
    [12.3, 7.6],
    [-8.5, 12.3],
    [-1.8, 12.3],
    [8.6, 12.3],
  ]) {
    const l = M.lamp();
    l.position.set(x, 0, z);
    l.rotation.y = x > 12 ? Math.PI : -Math.PI / 2;
    S.add(l);
  }
  for (const [x, z, ry] of [
    [12.3, -3.6, Math.PI / 2],
    [2.6, 12.3, 0],
    [-10.4, 12.3, 0],
  ]) {
    const b = M.bench();
    b.position.set(x, 0, z);
    b.rotation.y = ry;
    S.add(b);
  }
  // beach furniture
  const beach = [
    [15.6, -9.5, "parasolB", "towelB"],
    [15.8, -2.0, "parasolC", "towelA"],
    [16.0, 6.5, "parasolA", "towelB"],
    [-8.0, 15.8, "parasolC", "towelB"],
    [-1.5, 15.6, "parasolB", "towelA"],
    [10.5, 16.0, "parasolC", "towelB"],
    [16.0, 15.8, "parasolB", "towelA"],
  ];
  for (const [x, z, pt, tw] of beach) {
    const p = M.parasol(PAL.coral, 1.0, tex[pt]);
    p.position.set(x, -0.12, z);
    S.add(p);
    M.mesh(new THREE.BoxGeometry(1.0, 0.03, 1.9), M.mat("#FFFFFF", { map: tex[tw] }), { x: x + 0.9, y: -0.1, z: z + 0.4, ry: 0.3, parent: S, cast: false });
  }
  // the customer's own parasol + towel on the south beach (hero spot)
  const hp = M.parasol(PAL.coral, 1.1, tex.parasolA);
  hp.position.set(5.0, -0.12, 15.4);
  S.add(hp);
  M.mesh(new THREE.BoxGeometry(1.1, 0.03, 2.0), M.mat("#FFFFFF", { map: tex.towelA }), { x: 6.1, y: -0.1, z: 15.9, ry: -0.25, parent: S, cast: false });
  // sea life: sailboats
  W_.boats = [];
  for (const [x, z, ry, col] of [
    [9.0, 21.5, 0.3, PAL.coral],
    [21.3, 0.0, -1.2, PAL.teal],
    [-9.5, 21.0, 2.6, PAL.sun],
  ]) {
    const b = M.sailboat(col);
    b.position.set(x, -0.45, z);
    b.rotation.y = ry;
    b.scale.setScalar(0.85);
    scene.add(b);
    W_.boats.push({ b, x, z, ry });
  }
  // beach ball
  const ballTex = TX.stripeTexture(PAL.coral, "#FFFFFF", 6, 256, 64, true);
  W_.ball = M.mesh(new THREE.SphereGeometry(0.32, 18, 12), M.mat("#FFFFFF", { map: ballTex }), { x: 7.6, y: 0.2, z: 16.4, parent: scene });
  // clouds
  W_.clouds = [];
  for (const [x, y, z, s, sd] of [
    [-14, 10.5, -17, 1.4, 1],
    [16, 12.5, -15, 1.1, 2],
    [-20, 11.5, 6, 1.2, 3],
    [27, 14.5, 4, 1.3, 4],
    [4, 14.5, -22, 1.0, 5],
  ]) {
    const c = M.cloud(sd, s);
    c.position.set(x, y, z);
    scene.add(c);
    W_.clouds.push({ c, x, y, z });
  }
}

// collect a built group into the static root (keeps its transform)
function staticAdopt(g) {
  g.updateMatrixWorld(true);
  const parent = g.parent;
  if (parent) parent.remove(g);
  staticRoot.add(g);
}

// ---------------------------------------------------------------- the boutique
function buildShop() {
  const SX = -6.5,
    SZ = -6.0;
  const g = M.group(scene, { x: SX, z: SZ });
  const gs = M.group(scene, { x: SX, z: SZ }); // static interior → merged
  W_.shop = { g, x: SX, z: SZ };
  const pink = "#FF8FA3";
  const pinkIn = "#FFD3DC";
  M.box(7.2, 0.16, 6.0, "#EBC9A0", { y: 0.08, parent: gs, r: 0.02, cast: false });
  // plank lines
  for (let i = -3; i <= 3; i++) M.box(0.03, 0.005, 5.9, "#D9B287", { x: i, y: 0.163, parent: gs, r: 0, cast: false });
  // back + left walls (stay)
  M.mesh(new THREE.BoxGeometry(7.2, 3.6, 0.24), [M.mat(pink), M.mat(pink), M.mat("#FFFFFF"), M.mat(pink), M.mat(pinkIn), M.mat(pink)], { y: 1.96, z: -2.88, parent: gs });
  M.mesh(new THREE.BoxGeometry(0.24, 3.6, 6.0), [M.mat(pinkIn), M.mat(pink), M.mat("#FFFFFF"), M.mat(pink), M.mat(pink), M.mat(pink)], { x: -3.48, y: 1.96, parent: gs });
  // front wall (sinks) with door, display windows, awning and sign
  const front = M.group(g, { z: 2.88 });
  M.box(2.6, 3.6, 0.24, pink, { x: -2.3, y: 1.96, parent: front, r: 0.04 });
  M.box(2.6, 3.6, 0.24, pink, { x: 2.3, y: 1.96, parent: front, r: 0.04 });
  M.box(2.0, 1.1, 0.24, pink, { y: 3.21, parent: front, r: 0.04 });
  for (const x of [-2.2, 2.2]) {
    M.box(1.8, 1.7, 0.08, "#FFFFFF", { x, y: 1.55, z: 0.14, parent: front, r: 0.03, cast: false });
    M.box(1.6, 1.5, 0.08, M.smat(PAL.glass, { roughness: 0.2 }), { x, y: 1.55, z: 0.17, parent: front, r: 0.03, cast: false });
  }
  for (const x of [-0.5, 0.5]) M.box(0.94, 2.4, 0.08, M.smat("#9FC8DA", { roughness: 0.2, transparent: true, opacity: 0.8 }), { x, y: 1.36, z: 0.02, parent: front, r: 0.03, cast: false });
  const aw = M.mesh(new THREE.BoxGeometry(7.4, 0.08, 1.5), [M.mat(PAL.coral), M.mat(PAL.coral), M.mat("#FFFFFF", { map: tex.awning }), M.mat("#FFFFFF", { map: tex.awning }), M.mat(PAL.coral), M.mat(PAL.coral)], {
    y: 2.86,
    z: 0.75,
    rx: 0.3,
    parent: front,
  });
  M.mesh(new THREE.PlaneGeometry(3.4, 0.62), M.mat("#FFFFFF", { map: tex.sign, transparent: true }), { y: 3.36, z: 0.13, parent: front, cast: false });
  // right wall (sinks)
  const side = M.group(g, { x: 3.48 });
  M.box(0.24, 3.6, 6.0, pink, { y: 1.96, parent: side, r: 0.04 });
  M.box(0.08, 1.4, 2.4, "#FFFFFF", { x: 0.13, y: 1.9, parent: side, r: 0.03, cast: false });
  M.box(0.08, 1.2, 2.2, M.smat(PAL.glass, { roughness: 0.2 }), { x: 0.16, y: 1.9, parent: side, r: 0.03, cast: false });
  // roof (lifts away) with rooftop sign
  const roof = M.group(g);
  M.box(7.7, 0.32, 6.5, "#FFFFFF", { y: 3.92, parent: roof, r: 0.06 });
  M.box(7.74, 0.12, 6.54, PAL.coral, { y: 3.82, parent: roof, r: 0.04 });
  M.box(5.6, 1.3, 0.14, "#FFFFFF", { y: 4.85, z: 2.6, parent: roof, r: 0.06 });
  M.mesh(new THREE.PlaneGeometry(5.4, 1.35), M.mat("#FFFFFF", { map: tex.sign, transparent: true }), { y: 4.85, z: 2.68, parent: roof, cast: false });
  for (const x of [-2.2, 2.2]) M.box(0.12, 0.5, 0.12, PAL.ink, { x, y: 4.1, z: 2.6, parent: roof, r: 0.02 });
  M.box(1.0, 0.5, 0.8, "#E8E1EC", { x: -2.4, y: 4.3, z: -1.6, parent: roof, r: 0.06 });
  W_.shop.front = front;
  W_.shop.side = side;
  W_.shop.roof = roof;

  // ---- interior
  M.mesh(new THREE.CylinderGeometry(1.5, 1.5, 0.02, 28), M.mat("#FFC2B0"), { x: 0.7, y: 0.17, z: 0.7, parent: gs, cast: false });
  // clothes rack with bikinis on hangers
  for (const x of [-2.9, 1.2]) M.cyl(0.04, 0.04, 2.4, "#C9A26B", { x, y: 1.36, z: -2.25, parent: gs, seg: 8 });
  M.mesh(new THREE.CylinderGeometry(0.035, 0.035, 4.1, 8), M.mat("#C9A26B"), { x: -0.85, y: 2.5, z: -2.25, rz: Math.PI / 2, parent: gs });
  for (const x of [-2.9, 1.2]) M.box(0.5, 0.06, 0.5, "#C9A26B", { x, y: 0.19, z: -2.25, parent: gs, r: 0.02 });
  W_.rack = [];
  const rackPrints = ["leaf", "stripes", "polka", "daisy", "leaf"];
  rackPrints.forEach((pr, i) => {
    const hg = M.group(g, { x: -2.45 + i * 0.85, y: 2.5, z: -2.25 });
    const hgr = M.hanger();
    hgr.position.y = -0.27;
    hg.add(hgr);
    const bk = M.bikini3D(prints[pr]);
    bk.scale.setScalar(0.62);
    bk.position.set(0, -0.82, 0);
    hg.add(bk);
    W_.rack.push({ hg, bk, i, pr });
  });
  // shelves with folded bikinis on the left wall
  for (let k = 0; k < 3; k++) {
    M.box(0.6, 0.06, 2.6, "#FFFFFF", { x: -3.05, y: 0.9 + k * 0.75, z: 0.4, parent: gs, r: 0.02 });
    ["polka", "stripes", "daisy", "leaf"].forEach((pr, j) => {
      M.box(0.42, 0.1, 0.42, M.mat("#FFFFFF", { map: prints[pr] }), { x: -3.0, y: 0.98 + k * 0.75, z: -0.55 + j * 0.62, parent: gs, r: 0.03 });
      if ((j + k) % 2) M.box(0.4, 0.1, 0.4, M.mat("#FFFFFF", { map: prints[pr] }), { x: -3.0, y: 1.08 + k * 0.75, z: -0.55 + j * 0.62, parent: gs, r: 0.03 });
    });
  }
  // mirror
  const mir = M.mesh(new THREE.TorusGeometry(0.62, 0.07, 8, 28), M.mat("#E2B860"), { x: 2.3, y: 1.9, z: -2.72, parent: gs });
  mir.scale.set(1, 1.6, 1);
  const mg = M.mesh(new THREE.CircleGeometry(0.6, 28), M.smat("#CFE8F2", { roughness: 0.1 }), { x: 2.3, y: 1.9, z: -2.74, parent: gs, cast: false });
  mg.scale.set(1, 1.6, 1);
  // monstera plant
  M.cyl(0.32, 0.24, 0.55, "#FFFFFF", { x: 2.9, y: 0.44, z: -2.2, parent: gs, seg: 12 });
  for (let k = 0; k < 6; k++) {
    const a = (k / 6) * TAU;
    M.sph(0.36, k % 2 ? PAL.leaf : PAL.leafDark, { x: 2.9 + Math.cos(a) * 0.3, y: 1.05 + (k % 3) * 0.22, z: -2.2 + Math.sin(a) * 0.3, parent: gs, ico: 1, flat: true });
  }
  // string lights along the back wall
  W_.bulbs = [];
  for (let k = 0; k < 11; k++) {
    const x = -3.2 + k * 0.62;
    const y = 3.35 - Math.sin((k / 10) * Math.PI) * 0.35;
    const b = M.sph(0.075, new THREE.MeshLambertMaterial({ color: "#FFF6D0", emissive: k % 2 ? "#FFC93C" : "#FF8FA3", emissiveIntensity: 0.6 }), { x, y, z: -2.68, parent: g, ws: 8, hs: 6, cast: false });
    W_.bulbs.push(b);
  }
  // packing table + open box + tape roll
  M.box(2.8, 0.12, 1.4, "#FFFFFF", { x: 0.7, y: 1.0, z: 0.9, parent: gs, r: 0.04 });
  for (const [x, z] of [
    [-0.55, 0.3],
    [1.95, 0.3],
    [-0.55, 1.5],
    [1.95, 1.5],
  ])
    M.box(0.1, 0.94, 0.1, "#C9A26B", { x, y: 0.55, z, parent: gs, r: 0.02 });
  M.mesh(new THREE.TorusGeometry(0.13, 0.06, 8, 16), M.mat(PAL.coral), { x: 1.75, y: 1.12, z: 1.35, rx: Math.PI / 2, parent: gs });
  M.cyl(0.11, 0.11, 0.9, "#F5E6D3", { x: -0.2, y: 1.12, z: 1.35, rz: Math.PI / 2, parent: gs, seg: 12 });
  const ob = M.openBox(1);
  ob.group.position.set(0.55, 1.06, 0.85);
  g.add(ob.group);
  W_.packBox = ob;
  // tissue paper halves + thank-you card + sticker for the packing sequence
  const tissueM = M.mat("#FFC2D1", { side: THREE.DoubleSide });
  W_.tissue = [-1, 1].map((sx) => {
    const p = M.group(ob.group, { x: sx * 0.47, y: 0.6 });
    M.mesh(new THREE.PlaneGeometry(0.5, 0.74), tissueM, { x: -sx * 0.25, rx: -Math.PI / 2, parent: p, cast: false });
    p.userData.sx = sx;
    return p;
  });
  const cardTex = (() => {
    const { c, g: cg } = TX.canvas(256, 160);
    cg.fillStyle = "#FFFFFF";
    TX.rr(cg, 0, 0, 256, 160, 18);
    cg.fill();
    cg.fillStyle = PAL.coral;
    TX.heartPath(cg, 128, 70, 70);
    cg.fill();
    cg.fillStyle = PAL.ink;
    cg.font = `800 34px ${TX.FONT_D}`;
    cg.textAlign = "center";
    cg.fillText("Merci", 128, 138);
    return TX.tex(c);
  })();
  W_.card = M.mesh(new THREE.BoxGeometry(0.46, 0.02, 0.3), [M.mat("#FFFFFF"), M.mat("#FFFFFF"), M.mat("#FFFFFF", { map: cardTex }), M.mat("#FFFFFF"), M.mat("#FFFFFF"), M.mat("#FFFFFF")], { parent: ob.group });
  W_.stickerTop = M.mesh(new THREE.PlaneGeometry(0.34, 0.34), M.mat("#FFFFFF", { map: tex.sticker, transparent: true }), { rx: -Math.PI / 2, parent: ob.group, cast: false });
  // the bikini that gets packed (the coral polka set, same as on the phone)
  W_.packBikini = M.bikini3D(prints.polka);
  scene.add(W_.packBikini);
  // pre-packed parcels by the door
  W_.shopParcels = [];
  for (const [x, y, z] of [
    [2.3, 0.16, 1.9],
    [3.0, 0.16, 1.9],
    [2.3, 0.76, 1.9],
    [2.65, 0.16, 1.2],
  ]) {
    W_.shopParcels.push(new THREE.Vector3(SX + x, y, SZ + z));
  }
  // the shop owner behind the table
  const owner = M.person({ style: "curly", top: "#FFFFFF", bottom: PAL.ink, skin: PAL.skinA, hair: PAL.hairDark });
  owner.group.position.set(SX + 0.7, 0.16, SZ - 0.35);
  scene.add(owner.group);
  // coral apron
  M.box(0.5, 0.5, 0.05, PAL.coral, { y: 0.3, z: 0.18, parent: owner.torso, r: 0.03 });
  W_.owner = owner;
  staticAdopt(gs);
}

// ---------------------------------------------------------------- van, route, parcels
function buildVanAndRoute() {
  const v = M.van(tex.vanSide, tex.topper);
  scene.add(v.group);
  W_.van = v;
  const path = buildPath([
    [-4.4, 0],
    [10.6, 0],
    [10.6, 10.6],
    [0, 10.6],
    [0, 0],
    [10.6, 0],
    [10.6, -8.9],
  ]);
  W_.path = path;
  const hs = W_.houses;
  W_.sA = path.nearest(10.05, hs.A.doorW.z - 1.2);
  W_.sB = path.nearest(hs.B.doorW.x + 3.4, 10.05);
  W_.sEnd = path.len;
  W_.sS1 = path.nearest(0.55, hs.S1.doorW.z, W_.sB);
  W_.sN1 = path.nearest(hs.N1.doorW.x, 0.55, W_.sB);

  // route ribbon (drawn ahead of the van)
  const pts = path.pts,
    cum = path.cum;
  const pos = [],
    uv = [],
    idx = [];
  for (let i = 0; i < pts.length; i++) {
    const q = pts[Math.min(i + 1, pts.length - 1)],
      o = pts[Math.max(i - 1, 0)];
    const tg = q.clone().sub(o).normalize();
    const nx = -tg.y * 0.36,
      nz = tg.x * 0.36;
    pos.push(pts[i].x + nx, 0.09, pts[i].y + nz, pts[i].x - nx, 0.09, pts[i].y - nz);
    uv.push(cum[i] / 1.0, 0, cum[i] / 1.0, 1);
    if (i < pts.length - 1) {
      const a = i * 2;
      idx.push(a, a + 1, a + 2, a + 1, a + 3, a + 2);
    }
  }
  const rg = new THREE.BufferGeometry();
  rg.setAttribute("position", new THREE.Float32BufferAttribute(pos, 3));
  rg.setAttribute("uv", new THREE.Float32BufferAttribute(uv, 2));
  rg.setIndex(idx);
  const rm = new THREE.MeshBasicMaterial({ color: "#FFFFFF", map: tex.dash, transparent: true, depthWrite: false, side: THREE.DoubleSide });
  const ribbon = new THREE.Mesh(rg, rm);
  ribbon.renderOrder = 5;
  scene.add(ribbon);
  W_.ribbon = ribbon;
  W_.ribbonIndexAt = (s) => {
    let lo = 0,
      hi = cum.length - 1;
    while (hi - lo > 1) {
      const mid = (lo + hi) >> 1;
      if (cum[mid] <= s) lo = mid;
      else hi = mid;
    }
    return lo;
  };
  // glowing head dot on the route
  W_.routeHead = makeSprite(spr.puff, 34);
  W_.routeHead.material.color.set(PAL.coral);

  // parcels: A, S1, N1, N2 are pre-packed; B is the one packed on screen
  W_.parcels = {};
  for (const name of ["A", "S1", "N1", "N2", "B"]) {
    const p = M.parcel(tex.sticker, 1);
    scene.add(p);
    W_.parcels[name] = p;
  }
  // exhaust puffs and speed lines
  W_.puffs = Array.from({ length: 6 }, () => makeSprite(spr.puff, 70));
  W_.speed = Array.from({ length: 5 }, () => {
    const m = M.mesh(new THREE.PlaneGeometry(1, 0.07), new THREE.MeshBasicMaterial({ color: "#FFFFFF", transparent: true, opacity: 0.0, depthWrite: false }), { parent: scene, cast: false, recv: false });
    m.rotation.x = -Math.PI / 2;
    m.renderOrder = 6;
    return m;
  });
}

// ---------------------------------------------------------------- people
function buildPeople() {
  W_.driver = M.person({ style: "cap", top: PAL.coral, bottom: PAL.navy, skin: PAL.skinA, cap: "#FFFFFF" });
  scene.add(W_.driver.group);
  W_.custA = M.person({ style: "long", dress: true, top: PAL.sun, skin: PAL.skinC, hair: PAL.hairDark });
  scene.add(W_.custA.group);
  W_.custB = M.person({ style: "bun", dress: true, top: "#7FD6CF", skin: PAL.skinB, hair: PAL.hairBrown });
  scene.add(W_.custB.group);
  const polkaBig = prints.polka.clone();
  polkaBig.repeat.set(1.1, 1.1);
  polkaBig.needsUpdate = true;
  W_.beachB = M.person({ style: "bun", skin: PAL.skinB, hair: PAL.hairBrown, bikini: polkaBig, glasses: true });
  scene.add(W_.beachB.group);
  // a couple of townsfolk for life on the beach
  const sun1 = M.person({ style: "long", skin: PAL.skinC, hair: PAL.hairDark, bikini: prints.stripes, glasses: true });
  sun1.group.position.set(16.7, -0.05, 6.9);
  sun1.group.rotation.set(-Math.PI / 2, 0, 0.3);
  scene.add(sun1.group);
  const kid = M.person({ style: "curly", top: PAL.sun, bottom: PAL.teal, skin: PAL.skinA, hair: PAL.hairDark });
  kid.group.scale.setScalar(0.72);
  kid.group.position.set(10.0, -0.12, 17.4);
  kid.group.rotation.y = -2.2;
  scene.add(kid.group);
  W_.kid = kid;
  // the hero bikini that bursts out of the parcel at stop B
  W_.heroBikini = M.bikini3D(prints.polka);
  scene.add(W_.heroBikini);
}

// ---------------------------------------------------------------- phone (hook)
const PH = new THREE.Vector3(70, 3, -55);
function buildPhone() {
  const g = new THREE.Group();
  scene.add(g);
  const body = M.mesh(new RoundedBoxGeometry_(3.02, 6.26, 0.34, 0.42), M.smat("#FF6B85", { roughness: 0.45 }), { parent: g, cast: false, recv: false });
  M.mesh(new RoundedBoxGeometry_(2.88, 6.12, 0.06, 0.36), M.smat("#15111C", { roughness: 0.3 }), { z: 0.15, parent: g, cast: false, recv: false });
  for (const y of [1.6, 0.9]) M.box(0.05, 0.5, 0.12, "#E23A5C", { x: -1.52, y, parent: g, r: 0.02, cast: false, recv: false });
  M.box(0.05, 0.8, 0.12, "#E23A5C", { x: 1.52, y: 1.3, parent: g, r: 0.02, cast: false, recv: false });
  const ui = TX.canvas(TX.UI.W, TX.UI.H);
  const uiTex = TX.tex(ui.c, { mips: false });
  const screen = M.mesh(new THREE.PlaneGeometry(2.75, 5.957), new THREE.MeshBasicMaterial({ map: uiTex, transparent: true }), { z: 0.185, parent: g, cast: false, recv: false });
  // live map: the real island seen from above, rendered into rt
  const k = 2.75 / TX.UI.W;
  const mapW = TX.UI.map.w * k,
    mapH = TX.UI.map.h * k;
  const mapCy = (TX.UI.H / 2 - (TX.UI.map.y + TX.UI.map.h / 2)) * k;
  const map = M.mesh(new THREE.PlaneGeometry(mapW, mapH), new THREE.MeshBasicMaterial({ map: rt.texture, alphaMap: tex.mapMask, transparent: true, opacity: 0 }), {
    y: mapCy,
    z: 0.19,
    parent: g,
    cast: false,
    recv: false,
  });
  // touch hand + its soft shadow + ripple
  const handM = new THREE.MeshBasicMaterial({ map: spr.hand, transparent: true, depthWrite: false });
  const hand = M.mesh(new THREE.PlaneGeometry(1.1, 1.375), handM, { z: 0.7, parent: g, cast: false, recv: false });
  const shadowM = new THREE.MeshBasicMaterial({ map: spr.blob, transparent: true, depthWrite: false, opacity: 0 });
  const hshadow = M.mesh(new THREE.PlaneGeometry(0.9, 0.9), shadowM, { z: 0.2, parent: g, cast: false, recv: false });
  const ripM = new THREE.MeshBasicMaterial({ map: spr.ring, transparent: true, depthWrite: false, opacity: 0, color: "#FFFFFF" });
  const ripple = M.mesh(new THREE.PlaneGeometry(1, 1), ripM, { z: 0.21, parent: g, cast: false, recv: false });
  // explicit draw order on the screen stack (transparent sorting by centre is unreliable when tilted)
  screen.renderOrder = 1;
  map.renderOrder = 2;
  map.material.depthWrite = false;
  ripple.renderOrder = 3;
  hshadow.renderOrder = 4;
  hand.renderOrder = 5;
  W_.phone = { g, ui, uiTex, screen, map, mapW, mapH, mapCy, hand, hshadow, ripple, lastKey: "" };
  // the button centre on screen (canvas 360,1362)
  W_.phone.btn = new THREE.Vector2(0, (TX.UI.H / 2 - 1362) * k);
}
function RoundedBoxGeometry_(w, h, d, r) {
  return new RoundedBoxGeometry(w, h, d, 4, r);
}

// ---------------------------------------------------------------- markers (pins, chips)
function buildMarkers() {
  W_.pins = {};
  for (const name of ["B", "N1", "N2", "A", "S1"]) {
    const h = W_.houses[name];
    const pin = makeSprite(spr.pin, 150, { aspect: 160 / 200, center: [0.5, 0.02] });
    const plus = makeSprite(spr.plus1, 100, { aspect: 220 / 120 });
    const done = makeSprite(spr.delivered, 78, { aspect: 300 / 120, center: [0.5, 0.0] });
    const tick = makeSprite(spr.tick, 74, { center: [0.5, 0.0] });
    W_.pins[name] = { h, pin, plus, done, tick };
  }
  W_.bell = makeSprite(spr.bell, 92);
  W_.hearts = Array.from({ length: 7 }, () => makeSprite(spr.heart, 54));
  W_.beachHearts = Array.from({ length: 6 }, () => makeSprite(spr.heart, 58));
  W_.sparkles = Array.from({ length: 10 }, () => makeSprite(spr.sparkle, 60));
}

// merge every static mesh that shares a material into one draw call
function mergeStatic() {
  staticRoot.updateMatrixWorld(true);
  const buckets = new Map();
  const leftovers = [];
  staticRoot.traverse((o) => {
    if (!o.isMesh) return;
    if (Array.isArray(o.material)) {
      leftovers.push(o);
      return;
    }
    let geo = o.geometry.clone().applyMatrix4(o.matrixWorld);
    if (geo.index) geo = geo.toNonIndexed();
    for (const k of Object.keys(geo.attributes)) if (!["position", "normal", "uv"].includes(k)) geo.deleteAttribute(k);
    if (!geo.attributes.uv) geo.setAttribute("uv", new THREE.Float32BufferAttribute(new Float32Array((geo.attributes.position.count * 2) | 0), 2));
    const key = o.material.uuid + (o.castShadow ? "c" : "n");
    if (!buckets.has(key)) buckets.set(key, { m: o.material, cast: o.castShadow, geos: [] });
    buckets.get(key).geos.push(geo);
  });
  const merged = new THREE.Group();
  for (const { m, cast, geos } of buckets.values()) {
    const mg = mergeGeometries(geos, false);
    const me = new THREE.Mesh(mg, m);
    me.castShadow = cast;
    me.receiveShadow = true;
    merged.add(me);
  }
  for (const o of leftovers) {
    o.updateMatrixWorld(true);
    const c = o.clone();
    c.matrixAutoUpdate = false;
    c.matrix.copy(o.matrixWorld);
    merged.add(c);
  }
  scene.remove(staticRoot);
  scene.add(merged);
  merged.traverse((o) => {
    if (o.isMesh && o.matrixAutoUpdate) o.updateMatrix();
  });
}

// ================================================================= ANIMATION
// ---------------------------------------------------------------- van kinematics
const vanLegs = () => [
  [T.DEPART, T.ARRIVE_A, 0, W_.sA, E.inOut2],
  [T.LEAVE_A, T.ARRIVE_B, W_.sA, W_.sB, E.inOut2],
  [T.LEAVE_B, T.END_RUN, W_.sB, W_.sEnd, E.inOut2],
];
function vanS(t) {
  const legs = vanLegs();
  if (t <= legs[0][0]) return 0;
  for (let i = 0; i < legs.length; i++) {
    const [a, b, s0, s1, ease] = legs[i];
    if (t < a) return legs[i - 1] ? legs[i - 1][3] : 0;
    if (t <= b) return lerp(s0, s1, ease(inv(a, b, t)));
  }
  return W_.sEnd;
}
function vanPose(t) {
  const s = vanS(t);
  const p = W_.path.at(Math.max(s, 0.01));
  const dt = 1 / 30;
  const v0 = (vanS(t) - vanS(t - dt)) / dt;
  const v1 = (vanS(t + dt) - vanS(t)) / dt;
  return { s, x: p.x, z: p.z, yaw: Math.atan2(-p.tz, p.tx), tx: p.tx, tz: p.tz, speed: (v0 + v1) / 2, accel: (v1 - v0) / dt };
}
// point beside the van (right-hand side door) in world space
function vanSide(vp, out = 0.95, fwd = 0) {
  const rx = -vp.tz,
    rz = vp.tx;
  return new THREE.Vector3(vp.x + rx * out + vp.tx * fwd, 0, vp.z + rz * out + vp.tz * fwd);
}

function updateVan(t) {
  const v = W_.van;
  const vp = vanPose(t);
  v.group.position.set(vp.x, 0, vp.z);
  v.group.rotation.y = vp.yaw;
  // engine idle shimmy, braking/accel pitch, bounce on the move
  const idle = env(t, 17.95, 31.9, 0.2, 0.3) * 0.012 * Math.sin(t * 55);
  const pitch = clamp(-vp.accel * 0.006, -0.07, 0.07);
  const hopA = 0.035 * Math.abs(Math.sin(vp.s * 2.1)) * clamp(Math.abs(vp.speed) / 6);
  v.body.position.y = idle + hopA;
  v.body.rotation.z = pitch;
  // happy squash on the horn beeps
  const beep = Math.max(env(t, 18.38, 18.55, 0.05, 0.12), env(t, 18.58, 18.75, 0.05, 0.12));
  v.body.scale.set(1 + beep * 0.03, 1 - beep * 0.05, 1 + beep * 0.03);
  for (const w of v.wheels) w.rotation.z = -vp.s / 0.36;
  // rear doors: open for loading, slam shut
  const open = seg(t, 16.05, 16.4, E.out3) * (1 - seg(t, 17.72, 17.92, E.in2));
  for (const d of v.doors) d.hinge.rotation.y = d.side * open * 1.75;
  // topper wobble
  v.topper.rotation.y = Math.sin(t * 2.0) * 0.6;
  // exhaust puffs on start-up and each departure
  const starts = [17.98, 18.6, T.LEAVE_A, T.LEAVE_B];
  W_.puffs.forEach((pf, i) => {
    const st = starts[i % starts.length] + Math.floor(i / starts.length) * 0.12;
    const u = inv(st, st + 0.9, t);
    const live = t > st && t < st + 0.9;
    const tail = new THREE.Vector3(-1.9, 0.45, -0.45).applyAxisAngle(new THREE.Vector3(0, 1, 0), vp.yaw);
    pf.position.set(vp.x + tail.x - vp.tx * u * 1.2, 0.45 + u * 0.9, vp.z + tail.z - vp.tz * u * 1.2);
    pf.userData.k = live ? 0.5 + u * 1.1 : 0;
    pf.material.opacity = live ? 0.85 * (1 - u) : 0;
  });
  // speed lines during the fast montage
  const fast = clamp((Math.abs(vp.speed) - 7) / 6);
  W_.speed.forEach((m, i) => {
    const side = (i - 2) * 0.45;
    const L = 1.4 + ((i * 37) % 5) * 0.35;
    const back = 2.2 + ((i * 53) % 3) * 0.5 + 0.4 * Math.sin(t * 20 + i);
    m.position.set(vp.x - vp.tx * back - vp.tz * side, 0.5 + (i % 3) * 0.45, vp.z - vp.tz * back + vp.tx * side);
    m.rotation.set(-Math.PI / 2, 0, vp.yaw);
    m.scale.set(L, 1, 1);
    m.material.opacity = fast * 0.85;
    m.visible = fast > 0.01;
  });
  return vp;
}

function updateRoute(t, vp) {
  // the full tour draws itself on departure, then the travelled part disappears
  const draw = seg(t, 18.5, 19.7, E.inOut3) * W_.path.len;
  const s0 = vp.s;
  const i0 = W_.ribbonIndexAt(s0);
  const i1 = W_.ribbonIndexAt(Math.max(draw, s0));
  const g = W_.ribbon.geometry;
  g.setDrawRange(i0 * 6, Math.max(0, i1 - i0) * 6);
  W_.ribbon.visible = draw > 0.05 && t < 32.2;
  W_.ribbon.material.opacity = 1 - seg(t, 31.4, 32.2);
  tex.dash.offset.x = -t * 1.6;
  const hp = W_.path.at(draw);
  W_.routeHead.position.set(hp.x, 0.25, hp.z);
  W_.routeHead.userData.k = env(t, 18.5, 19.95, 0.15, 0.3) * 1.0;
  W_.routeHead.material.opacity = 1;
}

// ---------------------------------------------------------------- parcels
function parcelState(name, t, vp) {
  const p = W_.parcels[name];
  const shopIdx = { A: 0, S1: 1, N1: 2, N2: 3 }[name];
  const vanIn = (tt) => {
    const v = W_.van.group;
    return new THREE.Vector3(-1.2, 0.95, 0).applyAxisAngle(new THREE.Vector3(0, 1, 0), v.rotation.y).add(v.position);
  };
  p.visible = true;
  p.rotation.set(0, 0, 0);
  p.scale.setScalar(1);
  // loading hop timings
  const hopStart = { A: 16.45, S1: 16.6, N1: 16.75, N2: 16.9, B: 17.15 }[name];
  const hopEnd = hopStart + 0.55;
  let start;
  if (name === "B") {
    // appears when the packing box closes (swap), then hops off the table
    if (t < 15.55) {
      p.visible = false;
      return;
    }
    const tbl = new THREE.Vector3(W_.shop.x + 0.55, 1.06, W_.shop.z + 0.85);
    const floor = new THREE.Vector3(W_.shop.x + 1.6, 0.16, W_.shop.z + 2.2);
    if (t < 16.3) {
      const u = seg(t, 15.75, 16.3, E.inOut2);
      const q = hop(tbl.toArray(), floor.toArray(), 0.7, u);
      p.position.set(...q);
      p.rotation.y = u * Math.PI;
      return;
    }
    start = floor;
  } else {
    start = W_.shopParcels[shopIdx].clone();
    if (t < 9.0) {
      p.position.copy(start);
      return;
    }
  }
  if (t < hopStart) {
    p.position.copy(start);
    if (name === "B") p.rotation.y = Math.PI;
    return;
  }
  if (t < hopEnd) {
    const u = seg(t, hopStart, hopEnd, E.linear);
    const q = hop(start.toArray(), vanIn().toArray(), 1.4, u);
    p.position.set(...q);
    p.rotation.set(u * 1.2, u * 2.4, 0);
    const sq = 1 - 0.2 * Math.sin(u * Math.PI);
    p.scale.set(1, sq, 1);
    return;
  }
  // inside the van until delivery
  const deliver = {
    A: () => carryDeliver(t, "A"),
    B: () => carryDeliver(t, "B"),
    S1: () => tossDeliver(t, "S1", W_.sS1),
    N1: () => tossDeliver(t, "N1", W_.sN1),
    N2: () => tossDeliver(t, "N2", W_.sEnd - 0.4),
  }[name];
  const r = deliver();
  if (!r) {
    p.visible = false;
    return;
  }
  p.position.copy(r.pos);
  if (r.rot) p.rotation.set(...r.rot);
  if (r.scale !== undefined) p.scale.setScalar(r.scale);
  p.visible = r.visible !== false;
}

// time when the van passes arc-length s during the montage leg
function timeAtS(s, a, b, s0, s1) {
  let lo = a,
    hi = b;
  for (let k = 0; k < 30; k++) {
    const m = (lo + hi) / 2;
    if (lerp(s0, s1, E.inOut2(inv(a, b, m))) < s) lo = m;
    else hi = m;
  }
  return (lo + hi) / 2;
}
function tossTime(name, s) {
  if (name === "N2") return T.END_RUN - 0.05;
  return timeAtS(s, T.LEAVE_B, T.END_RUN, W_.sB, W_.sEnd);
}
function tossDeliver(t, name, s) {
  const t0 = tossTime(name, s);
  const t1 = t0 + 0.55;
  if (t < t0) return null;
  const h = W_.houses[name];
  const target = h.doorW.clone();
  if (t < t1) {
    const vp = vanPose(t0);
    const from = [vp.x, 2.2, vp.z];
    const u = seg(t, t0, t1, E.linear);
    const q = hop(from, [target.x, 0.1, target.z], 2.6, u);
    return { pos: new THREE.Vector3(...q), rot: [u * 5, u * 3, 0] };
  }
  const land = seg(t, t1, t1 + 0.25, back(3));
  return { pos: new THREE.Vector3(target.x, 0.1, target.z), rot: [0, 0.4, 0], scale: 0.85 + 0.15 * land };
}

// ---------------------------------------------------------------- delivery choreography
// Stop timings (A gets the full story; B is quicker and ends with the bikini reveal)
const STOP = {
  A: { arrive: T.ARRIVE_A, out: 21.3, walk0: 21.55, walk1: 22.35, bell: 22.45, open: 22.8, step: 22.95, give: 23.3, joy: 23.5, back0: 23.75, back1: 24.3 },
  B: { arrive: T.ARRIVE_B, out: 26.33, walk0: 26.45, walk1: 27.05, bell: 99, open: 26.4, step: 26.5, give: 27.1, joy: 27.4, back0: 28.05, back1: 28.65 },
};
function stopVan(name) {
  return vanPose(STOP[name].arrive + 0.05);
}
function carryDeliver(t, name) {
  const st = STOP[name];
  if (t < st.out) return null;
  const d = W_.driver;
  const hold = new THREE.Vector3(0, 1.08, 0.42).applyAxisAngle(new THREE.Vector3(0, 1, 0), d.group.rotation.y).add(d.group.position);
  if (t < st.give) return { pos: hold, rot: [0, d.group.rotation.y, 0] };
  const c = name === "A" ? W_.custA : W_.custB;
  const cHold = new THREE.Vector3(0, 1.08, 0.42).applyAxisAngle(new THREE.Vector3(0, 1, 0), c.group.rotation.y).add(c.group.position);
  if (t < st.give + 0.28) {
    const u = seg(t, st.give, st.give + 0.28, E.inOut2);
    const q = hop(hold.toArray(), cHold.toArray(), 0.25, u);
    return { pos: new THREE.Vector3(...q), rot: [0, lerp(d.group.rotation.y, c.group.rotation.y, u), 0] };
  }
  if (name === "B" && t > 27.55) {
    // she pops it open — the box shrinks away as the bikini bursts out
    const k = 1 - seg(t, 27.55, 27.85, E.in2);
    return { pos: cHold, rot: [0, c.group.rotation.y, 0], scale: Math.max(0.001, k), visible: k > 0.01 };
  }
  return { pos: cHold, rot: [0, c.group.rotation.y, 0], visible: !(name === "A" && t > 24.9) };
}

function updateDriver(t) {
  const d = W_.driver;
  const g = d.group;
  g.visible = false;
  let name = null;
  if (t >= STOP.A.out && t < STOP.A.back1) name = "A";
  if (t >= STOP.B.out && t < STOP.B.back1) name = "B";
  if (!name) return;
  g.visible = true;
  const st = STOP[name];
  const vp = stopVan(name);
  const exitP = vanSide(vp, 1.0, 0.3);
  const h = W_.houses[name];
  const door = h.doorW.clone();
  // stand a little in front of the doorstep, facing the door
  const toDoor = door.clone().sub(exitP).normalize();
  const meet = name === "B" ? exitP.clone().lerp(door, 0.45) : door.clone().addScaledVector(toDoor, -0.35);
  const faceDoor = Math.atan2(toDoor.x, toDoor.z);
  M.poseIdle(d, t);
  if (t < st.walk0) {
    // hop out of the van
    const u = seg(t, st.out, st.walk0, E.out2);
    const inside = vanSide(vp, 0.2, 0.3);
    g.position.set(lerp(inside.x, exitP.x, u), Math.sin(u * Math.PI) * 0.35, lerp(inside.z, exitP.z, u));
    g.rotation.y = faceDoor;
    M.poseCarry(d, 1);
  } else if (t < st.walk1) {
    const u = seg(t, st.walk0, st.walk1, E.inOut2);
    g.position.set(lerp(exitP.x, meet.x, u), 0, lerp(exitP.z, meet.z, u));
    g.rotation.y = faceDoor;
    const dist = exitP.distanceTo(meet) * u;
    M.poseWalk(d, dist * 5.2, 0.6);
    M.poseCarry(d, 1);
  } else if (t < st.back0) {
    g.position.set(meet.x, 0, meet.z);
    g.rotation.y = faceDoor;
    if (t < st.give + 0.15) M.poseCarry(d, 1);
    // ring the bell
    if (name === "A" && t > st.bell - 0.1 && t < st.bell + 0.35) d.arms[1].rotation.set(-1.9, 0, -0.3);
    if (t > st.give + 0.2) {
      // a little thumbs-up wave
      M.poseWave(d, t, env(t, st.give + 0.2, st.back0, 0.15, 0.1), 0);
    }
  } else {
    const u = seg(t, st.back0, st.back1, E.inOut2);
    g.position.set(lerp(meet.x, exitP.x, u), u > 0.85 ? Math.sin(inv(0.85, 1, u) * Math.PI) * 0.3 : 0, lerp(meet.z, exitP.z, u));
    g.rotation.y = faceDoor + Math.PI;
    M.poseWalk(d, meet.distanceTo(exitP) * u * 5.2, 0.6);
  }
}

function updateCustomer(t, name) {
  const c = name === "A" ? W_.custA : W_.custB;
  const st = STOP[name];
  const h = W_.houses[name];
  const g = c.group;
  // door: open, then close behind her (A) after she goes back in
  const openK = seg(t, st.open, st.open + 0.3, E.out3) * (name === "A" ? 1 - seg(t, 24.95, 25.25, E.inOut2) : 1 - seg(t, 31.0, 31.3));
  h.hinge.rotation.y = -1.55 * openK * h.hingeSign;
  g.visible = t > st.step - 0.05 && (name === "B" ? t < 30.5 : t < 25.0);
  if (!g.visible) return;
  const yaw = h.hingeParent.rotation.y;
  const side = 0.3 * h.hingeSign;
  const inside = h.doorstep.clone().add(new THREE.Vector3(side, 0, -1.1));
  const outside = h.doorstep.clone().add(new THREE.Vector3(side, 0, name === "B" ? 0.15 : -0.15));
  const m = h.hingeParent.matrixWorld;
  const pi = inside.applyMatrix4(m),
    po = outside.applyMatrix4(m);
  let pos;
  if (name === "B") {
    // she rushes out to meet the driver halfway
    const vp = stopVan("B");
    const meetD = vanSide(vp, 1.0, 0.3).lerp(h.doorW, 0.45);
    const meetC = meetD.clone().lerp(h.doorW, 0.62);
    const u1 = seg(t, st.step, st.step + 0.25, E.out2);
    const u2 = seg(t, st.step + 0.25, st.give - 0.05, E.inOut2);
    pos = pi.clone().lerp(po, u1).lerp(meetC, u2);
    M.poseIdle(c, t);
    if (u2 > 0 && u2 < 1) M.poseWalk(c, u2 * 9, 0.55);
  } else {
    const u = seg(t, st.step, st.step + 0.35, E.out2);
    const back = seg(t, 24.55, 24.95, E.inOut2);
    pos = pi.clone().lerp(po, u - back);
    M.poseIdle(c, t);
    if ((u > 0 && u < 1) || (back > 0 && back < 1)) M.poseWalk(c, (u + back) * 6, 0.5);
  }
  g.position.copy(pos);
  g.rotation.y = yaw + (name === "B" && t > 26.9 ? 0.0 : 0);
  if (name === "A" && t > 24.55) g.rotation.y = yaw + Math.PI;
  if (t > st.give + 0.1) {
    M.poseCarry(c, 1);
    // little jump of joy
    const j = env(t, st.joy, st.joy + 0.45, 0.2, 0.25);
    c.root.position.y = j * 0.28;
  }
  if (name === "B" && t > 27.55) {
    // arms up in delight as the bikini appears
    const k = seg(t, 27.55, 27.8, E.out3);
    c.arms[0].rotation.set(0, 0, -2.6 * k);
    c.arms[1].rotation.set(0, 0, 2.6 * k);
    c.root.position.y = env(t, 27.6, 28.3, 0.15, 0.3) * 0.22 + Math.abs(Math.sin(t * 9)) * 0.05 * env(t, 27.6, 28.6);
  }
}

// ---------------------------------------------------------------- shop sequence
function updateShop(t) {
  const sh = W_.shop;
  // dollhouse cutaway: roof flies off, near walls sink
  const lift = seg(t, 10.45, 11.35, E.inOut3) * (1 - seg(t, 18.0, 18.75, E.outBack));
  sh.roof.position.y = lift * 12;
  sh.roof.rotation.set(-lift * 0.25, 0, lift * 0.35);
  sh.roof.visible = lift < 0.995;
  const sink = seg(t, 10.55, 11.2, E.in3) * (1 - seg(t, 17.85, 18.4, E.out3));
  sh.front.position.y = -sink * 3.95;
  sh.side.position.y = -sink * 3.95;
  sh.front.visible = sh.side.visible = sink < 0.999;
  // string lights twinkle
  W_.bulbs.forEach((b, i) => {
    b.material.emissiveIntensity = 0.35 + 0.45 * (0.5 + 0.5 * Math.sin(t * 5 + i * 1.3));
  });
  // rack bikinis sway; the polka one (index 2) is plucked
  W_.rack.forEach((r) => {
    r.hg.rotation.z = Math.sin(t * 1.8 + r.i) * 0.05;
    r.bk.visible = !(r.i === 2 && t > 11.9);
  });
  // packed bikini flight: rack → box
  const pb = W_.packBikini;
  const rack = W_.rack[2];
  rack.hg.updateMatrixWorld(true);
  const from = new THREE.Vector3().setFromMatrixPosition(rack.bk.matrixWorld);
  const boxTop = new THREE.Vector3(sh.x + 0.55, 1.55, sh.z + 0.85);
  pb.visible = t > 11.9 && t < 15.6;
  if (pb.visible) {
    const u = seg(t, 11.95, 12.75, E.inOut3);
    const q = hop(from.toArray(), boxTop.toArray(), 2.2, u);
    const land = seg(t, 12.75, 13.05, E.in2);
    pb.position.set(q[0], q[1] - land * 0.45, q[2]);
    pb.rotation.set(-u * 1.35, u * TAU, 0);
    const s = lerp(0.62, 1.15, Math.sin(u * Math.PI)) * (1 - land * 0.35);
    pb.scale.set(s, s * (1 - 0.35 * land), s);
  }
  // box: flaps open → tissue folds → card → flaps close → tape → sticker → hop
  const ob = W_.packBox;
  ob.group.visible = t < 15.7;
  const closeT = [13.7, 13.85, 14.05, 14.2];
  ob.flaps.forEach((f, i) => {
    const c = seg(t, closeT[i], closeT[i] + 0.28, back(1.6));
    M.setFlap(f, 1 - c);
  });
  W_.tissue.forEach((p) => {
    const sx = p.userData.sx;
    const u = seg(t, 13.05 + (sx > 0 ? 0.12 : 0), 13.4 + (sx > 0 ? 0.12 : 0), E.out3);
    p.rotation.z = sx * (1 - u) * 1.45;
    p.visible = t > 12.95;
  });
  W_.card.visible = t > 13.25;
  if (W_.card.visible) {
    const u = seg(t, 13.25, 13.6, E.out3);
    W_.card.position.set(0.1 * (1 - u), 0.62 + (1 - u) * 1.2, 0.05);
    W_.card.rotation.set((1 - u) * 3.0, 0.3, (1 - u) * 1.2);
  }
  ob.tape.scale.x = Math.max(0.001, seg(t, 14.45, 14.85, E.inOut3));
  ob.tape.position.x = (1 - seg(t, 14.45, 14.85, E.inOut3)) * -0.5;
  const sp = pop(t, 14.95, 0.35, 3);
  W_.stickerTop.visible = t > 14.95;
  W_.stickerTop.position.set(0.2, ob.h + 0.09 + (1 - seg(t, 14.95, 15.1)) * 0.4, 0.16);
  W_.stickerTop.scale.setScalar(Math.max(0.001, sp));
  const hopK = env(t, 15.2, 15.6, 0.18, 0.22, E.out2, E.in2);
  ob.group.position.y = 1.06 + hopK * 0.35;
  ob.group.scale.set(1 + 0.08 * Math.sin(hopK * Math.PI), 1 - 0.1 * Math.sin(hopK * Math.PI), 1);
  // the owner: magic gesture at the rack, packing hands, waving goodbye
  const o = W_.owner;
  M.poseIdle(o, t);
  o.group.rotation.y = 0;
  if (t > 11.6 && t < 12.6) {
    const k = env(t, 11.6, 12.6, 0.2, 0.3);
    o.arms[1].rotation.set(-2.4 * k, 0, -0.3 * k);
    o.group.rotation.y = -2.6 * k;
  }
  if (t > 12.7 && t < 15.3) {
    const k = env(t, 12.7, 15.3, 0.2, 0.2);
    o.arms[0].rotation.set(-1.2 * k + Math.sin(t * 9) * 0.15 * k, 0, 0.1);
    o.arms[1].rotation.set(-1.2 * k - Math.sin(t * 9) * 0.15 * k, 0, -0.1);
  }
  if (t > 15.4 && t < 15.9) o.root.position.y = env(t, 15.4, 15.9, 0.15, 0.2) * 0.18;
  if (t > 17.2 && t < 18.6) M.poseWave(o, t, env(t, 17.2, 18.6, 0.2, 0.3), 1);
  o.group.visible = t < 18.6 || t > 40;
}

// ---------------------------------------------------------------- hero bikini burst (stop B)
function updateHero(t) {
  const hb = W_.heroBikini;
  hb.visible = t > 27.55 && t < 28.95;
  if (!hb.visible) return;
  const c = W_.custB.group;
  const base = c.position.clone().add(new THREE.Vector3(0, 1.1, 0));
  const u = seg(t, 27.55, 27.95, E.out3);
  const back_ = seg(t, 28.55, 28.95, E.in3);
  hb.position.set(base.x, base.y + u * 2.05 - back_ * 2.35 + Math.sin(t * 4) * 0.06, base.z);
  hb.rotation.set(0.12, 0.25 + (1 - u) * TAU + Math.sin((t - 27.55) * 3.2) * 0.45, Math.sin(t * 2.6) * 0.08);
  const s = 1.6 * u * (1 - back_);
  hb.scale.setScalar(Math.max(0.001, s));
  // sparkles around it
  W_.sparkles.forEach((sp, i) => {
    const a = (i / W_.sparkles.length) * TAU + t * 1.6;
    const r = 0.95 + 0.25 * Math.sin(t * 3 + i);
    sp.position.set(hb.position.x + Math.cos(a) * r, hb.position.y + Math.sin(a * 1.3) * 0.6, hb.position.z + Math.sin(a) * r);
    const tw = 0.5 + 0.5 * Math.sin(t * 9 + i * 2.1);
    sp.userData.k = u * (1 - back_) * (0.5 + 0.6 * tw);
    sp.material.opacity = 1;
    sp.material.rotation = t * 2 + i;
  });
}

// ---------------------------------------------------------------- pins, bell, hearts
const PIN_POP = { B: -1, N1: 7.15, N2: 7.45, A: 7.75, S1: 8.05 };
function deliveredAt(name) {
  if (name === "A") return 23.5;
  if (name === "B") return 27.45;
  return tossTime(name, name === "S1" ? W_.sS1 : name === "N1" ? W_.sN1 : W_.sEnd - 0.4) + 0.55;
}
function updatePins(t) {
  for (const [name, P] of Object.entries(W_.pins)) {
    const h = P.h;
    const top = h.topW;
    const bob = Math.sin(t * 3.2 + name.length) * 0.15;
    const dAt = deliveredAt(name);
    let k;
    if (name === "B") k = pop(t, 0.2, 0.5, 2.5);
    else k = pop(t, PIN_POP[name], 0.45, 2.6);
    const flip = seg(t, dAt - 0.12, dAt + 0.05, E.in2);
    // the pin that started it all pulses on the phone map
    const pulse = name === "B" ? 1 + 0.12 * Math.max(0, Math.sin(t * 6)) * (t < 7 ? 1 : 0) : 1;
    P.pin.userData.k = k * (1 - flip) * pulse;
    P.pin.position.set(top.x, top.y + 0.4 + bob, top.z);
    P.pin.material.opacity = 1;
    // +1 bubbles rise beside the new pins
    const pp = PIN_POP[name] + 0.12;
    const pu = inv(pp, pp + 1.1, t);
    P.plus.userData.k = name === "B" ? 0 : pop(t, pp, 0.35, 2.4) * (1 - seg(t, pp + 0.8, pp + 1.1));
    P.plus.position.set(top.x, top.y + 2.4 + pu * 1.0, top.z);
    P.plus.material.opacity = 1;
    // delivered chip replaces the pin
    const dk = pop(t, dAt, 0.42, 2.6);
    const wide = clamp((CUR_VH - 24) / 10);
    P.done.userData.k = dk;
    P.done.position.set(top.x, top.y + 0.35 + bob * 0.5, top.z);
    P.done.material.opacity = 1 - wide;
    P.tick.userData.k = dk;
    P.tick.position.copy(P.done.position);
    P.tick.material.opacity = wide;
  }
  // doorbell at A
  const bk = pop(t, STOP.A.bell, 0.25, 3) * (1 - seg(t, STOP.A.bell + 0.6, STOP.A.bell + 0.85));
  const hA = W_.houses.A;
  W_.bell.position.copy(hA.bellW).add(new THREE.Vector3(0, 0.6, 0));
  W_.bell.userData.k = bk;
  W_.bell.material.opacity = 1;
  W_.bell.material.rotation = Math.sin(t * 30) * 0.35 * bk;
  // hearts float up from customer A, then from B at the reveal
  W_.hearts.forEach((ht, i) => {
    const isB = i >= 4;
    const c = isB ? W_.custB.group : W_.custA.group;
    const t0 = (isB ? 27.65 : STOP.A.joy) + (i % 4) * 0.12;
    const u = inv(t0, t0 + 1.3, t);
    const live = t > t0 && t < t0 + 1.3 && c.visible;
    ht.position.set(c.position.x + Math.sin(u * 6 + i) * 0.3 + (i % 2 ? 0.35 : -0.35), 1.9 + u * 2.2, c.position.z + (i % 3) * 0.15);
    ht.userData.k = live ? E.outBack(clamp(u * 4), 2) * (1 - u * 0.3) : 0;
    ht.material.opacity = live ? 1 - E.in2(u) : 0;
  });
}

// ---------------------------------------------------------------- phone UI + hand
function updatePhone(t) {
  const P = W_.phone;
  const g = P.g;
  g.visible = t < T.SW;
  if (!g.visible) return;
  // stay square to the iso camera, with an entrance spin and a resting tilt that
  // flattens out as the camera dives into the screen
  const B = camBasis(45, ISO_EL);
  const q0 = new THREE.Quaternion().setFromRotationMatrix(new THREE.Matrix4().makeBasis(B.right, B.up, B.d));
  const enter = seg(t, 0.0, 1.0, E.out4);
  const flat = seg(t, 3.5, T.SW - 0.08, E.inOut3);
  const yaw = lerp(-2.2, -0.32, E.outBack(clamp(t / 1.05), 1.3)) * (1 - flat);
  const pitch = lerp(0.5, 0.1, enter) * (1 - flat);
  const roll = lerp(-0.25, 0.04, enter) * (1 - flat) + Math.sin(t * 1.4) * 0.015 * (1 - flat);
  const qt = new THREE.Quaternion().setFromEuler(new THREE.Euler(pitch, yaw, roll, "YXZ"));
  g.quaternion.copy(q0).multiply(qt);
  const rise = lerp(-9, 0, enter);
  g.position.copy(PH).addScaledVector(B.up, rise + Math.sin(t * 1.3) * 0.05 * (1 - flat));
  // UI state
  const s = {
    hover: env(t, 1.75, 2.15, 0.15, 0.05),
    press: seg(t, 2.1, 2.18, E.out2) * (1 - seg(t, 2.18, 2.36, E.out3)),
    done: seg(t, 2.3, 2.62, E.inOut2),
    sheet: seg(t, 2.55, 2.98, E.out4),
    check: seg(t, 2.85, 3.35, E.out2),
  };
  const key = Object.values(s)
    .map((v) => v.toFixed(3))
    .join(",");
  if (key !== P.lastKey) {
    TX.drawPhoneUI(P.ui.g, s);
    P.uiTex.needsUpdate = true;
    P.lastKey = key;
  }
  // the map card slides up with the sheet, then the live island fades in
  const k = 2.75 / TX.UI.W;
  const top = lerp(TX.UI.H + 20, 300, s.sheet);
  P.map.position.y = P.mapCy - (top - 300) * k;
  P.map.material.opacity = seg(t, 3.0, 3.4, E.inOut2);
  // hand: glide in, tap, leave
  const btn = P.btn;
  const tipOff = new THREE.Vector2(0.099, -0.606);
  const inU = seg(t, 1.05, 1.85, E.out4);
  const outU = seg(t, 2.42, 2.95, E.in3);
  const press = seg(t, 2.06, 2.12, E.in2) * (1 - seg(t, 2.16, 2.32, E.out2));
  const hx = btn.x + tipOff.x + lerp(2.3, 0, inU) + outU * 2.6;
  const hy = btn.y + tipOff.y + lerp(-3.6, 0, inU) - outU * 3.2;
  P.hand.position.set(hx, hy, 0.75 - press * 0.45);
  P.hand.scale.setScalar(1 - press * 0.1);
  P.hand.visible = t > 1.0 && t < 3.0;
  P.hshadow.position.set(hx - 0.05, hy + 0.48, 0.2);
  P.hshadow.material.opacity = (0.25 + 0.35 * press) * inU * (1 - outU);
  // tap ripple
  const ru = inv(2.12, 2.7, t);
  P.ripple.position.set(btn.x, btn.y, 0.21);
  P.ripple.scale.setScalar(0.4 + ru * 2.6);
  P.ripple.material.opacity = t > 2.12 && t < 2.7 ? 0.9 * (1 - ru) : 0;
  P.ripple.material.color.set(PAL.coral);
}

// world position of the phone map's centre (used to aim the dive)
function mapCenterWorld() {
  const P = W_.phone;
  P.g.updateMatrixWorld(true);
  return P.map.getWorldPosition(new THREE.Vector3());
}

// ---------------------------------------------------------------- ambient life
function updateAmbient(t) {
  for (const f of tickers) f(t);
  W_.palms.forEach((p, i) => {
    p.fronds.forEach((f) => {
      f.tilt.rotation.x = f.base + Math.sin(t * 1.6 + f.ph + i) * 0.06;
    });
  });
  W_.boats.forEach(({ b, x, z, ry }, i) => {
    b.position.set(x + Math.sin(t * 0.2 + i) * 0.6, -0.45 + Math.sin(t * 1.8 + i) * 0.08, z);
    b.rotation.set(Math.sin(t * 1.5 + i) * 0.06, ry, Math.sin(t * 1.2 + i * 2) * 0.05);
  });
  W_.clouds.forEach(({ c, x, y, z }, i) => {
    c.position.set(x + t * 0.22, y + Math.sin(t * 0.5 + i) * 0.15, z);
  });
  // beach ball bounce + kid
  const bt = (t * 1.25) % 1;
  W_.ball.position.set(9.0 + Math.sin(t * 0.9) * 0.4, -0.12 + 0.32 + 4 * 1.1 * bt * (1 - bt), 17.0 + Math.cos(t * 0.9) * 0.25);
  W_.ball.rotation.set(t * 2, t * 3, 0);
  M.poseIdle(W_.kid, t);
  W_.kid.arms[0].rotation.set(-2.8 + Math.sin(t * 7.85) * 0.3, 0, 0);
  W_.kid.arms[1].rotation.set(-2.8 + Math.sin(t * 7.85) * 0.3, 0, 0);
  // the customer at the beach (she wears her new bikini)
  const bb = W_.beachB;
  bb.group.visible = t > 31.5;
  bb.group.position.set(5.9, -0.12, 15.0);
  bb.group.rotation.y = 0.75;
  M.poseIdle(bb, t);
  bb.group.rotation.y = 0.75 + Math.sin(t * 1.3) * 0.18;
  M.poseWave(bb, t, env(t, 33.0, 40, 0.3, 0.3), 1);
  W_.beachHearts.forEach((ht, i) => {
    const t0 = 33.25 + i * 0.36;
    const u = inv(t0, t0 + 1.6, t);
    const live = t > t0 && t < t0 + 1.6;
    ht.position.set(5.9 + Math.sin(u * 5 + i * 1.7) * 0.45 + (i % 2 ? 0.4 : -0.4), 2.2 + u * 2.6, 15.0);
    ht.userData.k = live ? E.outBack(clamp(u * 4), 2) * (1 - u * 0.3) : 0;
    ht.material.opacity = live ? 1 - E.in2(u) : 0;
  });
}

// ================================================================= CAMERA
function hookCam(t) {
  // 0 → SW: phone shots, then the dive into the live map
  const phoneShot = (vh) => () => shot(PH.x, PH.y, PH.z, vh, 45, ISO_EL, 0.58);
  const mapShot = () => {
    const c = mapCenterWorld();
    return shot(c.x, c.y, c.z, W_.phone.mapH * 0.92, 45, ISO_EL, 0.5);
  };
  return camTrack([
    [0.0, phoneShot(16)],
    [1.0, phoneShot(11.8), E.out4],
    [3.5, phoneShot(10.6), E.inOut2],
    [T.SW, mapShot, (u) => u * u * u],
  ])(t);
}
const ISLAND = new THREE.Vector3(1.5, 0, 1.5);
const RT_VH = 66;
function islandTop() {
  return shot(ISLAND.x, 0, ISLAND.z, RT_VH, 45, 89.9, 0.5);
}

let worldTrack;
function buildWorldTrack() {
  const hs = W_.houses;
  const shopC = () => shot(W_.shop.x + 0.0, 1.4, W_.shop.z - 0.4, 10.6, 38, 44, 0.56);
  const boxC = () => shot(W_.shop.x + 0.55, 1.3, W_.shop.z + 0.85, 7.4, 44, 46, 0.6);
  const vanFollow = (vh, az, el = ISO_EL, lead = 2.2, fy = 0.6) => (t) => {
    const vp = vanPose(t);
    return shot(vp.x + vp.tx * lead, 0.8, vp.z + vp.tz * lead, vh, az, el, fy);
  };
  const stopA = () => {
    const d = hs.A.doorW;
    return shot(d.x + 0.5, 1.0, d.z + 0.1, 8.6, 58, 33, 0.6);
  };
  const stopB = () => {
    const d = hs.B.doorW;
    return shot(d.x + 1.0, 1.1, d.z + 0.5, 8.8, 78, 33, 0.6);
  };
  const heroB = () => {
    const d = hs.B.doorW;
    return shot(d.x + 0.8, 1.9, d.z + 0.4, 6.4, 76, 29, 0.58);
  };
  const beach = () => shot(6.2, 1.1, 15.4, 8.6, 50, 30, 0.6);
  worldTrack = camTrack([
    [T.SW, (() => {
      const s = islandTop();
      s.vh = RT_VH * 0.92;
      return s;
    })()],
    [6.9, shot(ISLAND.x, 0, ISLAND.z, 44, 52, ISO_EL, 0.56), E.out3],
    [9.6, shot(ISLAND.x, 0, ISLAND.z, 40.5, 57, ISO_EL, 0.56), E.inOutSine],
    [10.9, shopC(), E.inOut4],
    [13.2, shot(W_.shop.x + 0.35, 1.3, W_.shop.z + 0.3, 9.8, 44, 44, 0.58), E.inOutSine],
    [14.15, boxC(), E.inOut3],
    [15.4, boxC(), E.linear],
    [16.35, shot(W_.shop.x + 1.6, 0.9, W_.shop.z + 3.6, 12.5, 40, 40, 0.6), E.inOut3],
    [17.9, shot(W_.shop.x + 2.1, 0.9, W_.shop.z + 4.6, 13.5, 46, 38, 0.6), E.inOutSine],
    [19.0, shot(2.4, 0, 3.0, 36, 48, 42, 0.58), E.inOut3],
    [19.75, shot(2.4, 0, 3.0, 35, 46, 42, 0.58), E.linear],
    [20.6, vanFollow(17, 34, 38, 3.0), E.inOut3],
    [21.55, stopA(), E.out4],
    [24.2, () => {
      const s = stopA();
      s.vh = 8.4;
      return s;
    }, E.inOutSine],
    [25.3, vanFollow(17, 50, 38, 2.5), E.inOut3],
    [26.6, stopB(), E.out4],
    [27.45, stopB(), E.linear],
    [27.9, heroB(), E.out4],
    [28.6, heroB(), E.linear],
    [29.4, vanFollow(24, 60, 40, 3.5), E.inOut3],
    [30.9, vanFollow(22, 48, 40, 3.5), E.linear],
    [31.85, shot(ISLAND.x, 0, ISLAND.z, 46, 45, 38, 0.56), E.inOut3],
    [32.25, shot(ISLAND.x, 0, ISLAND.z, 45, 45, 38, 0.56), E.linear],
    [33.2, beach(), E.out4],
    [35.3, () => {
      const s = beach();
      s.vh = 7.8;
      s.az = 34;
      return s;
    }, E.inOutSine],
    [36.75, shot(ISLAND.x + 0.5, 0, ISLAND.z + 0.5, 62, 52, 33, 0.68), E.inOut3],
    [40.0, shot(ISLAND.x + 0.5, 0, ISLAND.z + 0.5, 58, 64, 33, 0.68), E.linear],
  ]);
}

function camAt(t) {
  if (t < T.SW) return hookCam(t);
  return worldTrack(t);
}

// ================================================================= RENDER
function setShadowFrame(cx, cz, half) {
  sun.target.position.set(cx, 0, cz);
  sun.position.set(cx + SUN_DIR.x * 60, SUN_DIR.y * 60, cz + SUN_DIR.z * 60);
  const c = sun.shadow.camera;
  c.left = -half;
  c.right = half;
  c.top = half;
  c.bottom = -half;
  c.near = 1;
  c.far = 160;
  c.updateProjectionMatrix();
  sun.target.updateMatrixWorld();
}

function renderAt(t) {
  updateAmbient(t);
  updateShop(t);
  const vp = updateVan(t);
  updateRoute(t, vp);
  updateCustomer(t, "A");
  updateCustomer(t, "B");
  updateDriver(t);
  for (const n of ["A", "S1", "N1", "N2", "B"]) parcelState(n, t, vp);
  updateHero(t);
  updatePhone(t);
  scene.updateMatrixWorld(true);

  // live map on the phone: the island from straight above
  if (t > 2.9 && t < T.SW + 0.02) {
    const s = islandTop();
    CUR_VH = s.vh;
    updatePins(t);
    applyCam(rtCam, s);
    setShadowFrame(ISLAND.x, ISLAND.z, 26);
    updateSprites(s.vh);
    W_.phone.g.visible = false;
    scene.background = tex.pageBg;
    renderer.setRenderTarget(rt);
    renderer.clear();
    renderer.render(scene, rtCam);
    renderer.setRenderTarget(null);
    scene.background = null;
    W_.phone.g.visible = true;
  }
  const s = camAt(t);
  CUR_VH = s.vh;
  updatePins(t);
  applyCam(cam, s);
  if (t < T.SW) setShadowFrame(ISLAND.x, ISLAND.z, 26);
  else setShadowFrame(s.tx, s.tz, clamp(s.vh * 0.62, 7, 30));
  updateSprites(s.vh);
  renderer.render(scene, cam);
}

// ================================================================= WIRING
let ready = false;
let lastT = 0;
window.addEventListener("hf-seek", (e) => {
  lastT = e.detail.time;
  if (ready) renderAt(lastT);
});
build()
  .then(() => {
    buildWorldTrack();
    ready = true;
    renderAt(window.__hfThreeTime || lastT || 0);
    if (window.__worldReady) window.__worldReady();
  })
  .catch((err) => {
    console.error("world build failed", err);
    if (window.__worldReady) window.__worldReady();
  });
