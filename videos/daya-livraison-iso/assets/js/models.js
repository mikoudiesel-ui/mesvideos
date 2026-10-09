// Low-poly model builders for the isometric seaside town. Every builder returns a Group
// whose origin sits on the ground plane; animated parts are exposed on the returned object.
import * as THREE from "../vendor/three.module.min.js";
import { RoundedBoxGeometry } from "../vendor/RoundedBoxGeometry.js";
import { PAL } from "./palette.js";
import { rng, TAU } from "./util.js";

// ---------- materials & mesh helpers ----------
const mats = new Map();
export function mat(color, opts = {}) {
  const key = color + JSON.stringify(opts, (k, v) => (v && v.isTexture ? v.uuid : v));
  if (!mats.has(key)) mats.set(key, new THREE.MeshLambertMaterial({ color, ...opts }));
  return mats.get(key);
}
const smats = new Map();
export function smat(color, opts = {}) {
  const key = color + JSON.stringify(opts);
  if (!smats.has(key)) smats.set(key, new THREE.MeshStandardMaterial({ color, roughness: 0.55, metalness: 0, ...opts }));
  return smats.get(key);
}

export function mesh(geo, m, o = {}) {
  const me = new THREE.Mesh(geo, m);
  me.position.set(o.x || 0, o.y || 0, o.z || 0);
  me.rotation.set(o.rx || 0, o.ry || 0, o.rz || 0);
  if (o.s) me.scale.setScalar(o.s);
  me.castShadow = o.cast !== false;
  me.receiveShadow = o.recv !== false;
  if (o.parent) o.parent.add(me);
  return me;
}

const geoCache = new Map();
function rbox(w, h, d, r = 0.06, seg = 2) {
  const key = [w, h, d, r, seg].join("|");
  if (!geoCache.has(key)) geoCache.set(key, new RoundedBoxGeometry(w, h, d, seg, Math.min(r, w / 2, h / 2, d / 2)));
  return geoCache.get(key);
}
export function box(w, h, d, color, o = {}) {
  const g = o.r === 0 ? new THREE.BoxGeometry(w, h, d) : rbox(w, h, d, o.r ?? 0.06);
  return mesh(g, typeof color === "string" ? mat(color) : color, o);
}
export function cyl(rt, rb, h, color, o = {}) {
  return mesh(new THREE.CylinderGeometry(rt, rb, h, o.seg || 14), typeof color === "string" ? mat(color) : color, o);
}
export function sph(r, color, o = {}) {
  const g = o.ico ? new THREE.IcosahedronGeometry(r, o.ico) : new THREE.SphereGeometry(r, o.ws || 16, o.hs || 12);
  return mesh(g, typeof color === "string" ? mat(color, o.flat ? { flatShading: true } : {}) : color, o);
}
export function group(parent, o = {}) {
  const g = new THREE.Group();
  g.position.set(o.x || 0, o.y || 0, o.z || 0);
  g.rotation.set(o.rx || 0, o.ry || 0, o.rz || 0);
  if (parent) parent.add(g);
  return g;
}

// ---------- house ----------
// Built with its door on local +z; `yaw` turns it to face the street.
export function house(o) {
  const {
    w = 3.4,
    d = 3.4,
    h = 2.6,
    wall = PAL.white,
    roof = PAL.roofCoral,
    roofType = "gable",
    door = PAL.teal,
    shutter = PAL.teal,
    seed = 1,
    floors = 1,
    awning = null,
    hingeRight = false,
  } = o;
  const R = rng(seed);
  const g = new THREE.Group();
  box(w + 0.5, 0.14, d + 0.5, PAL.pave, { y: 0.07, parent: g, cast: false });
  const H = h * floors;
  box(w, H, d, wall, { y: 0.14 + H / 2, parent: g, r: 0.1 });
  // trim band at the top
  box(w + 0.08, 0.14, d + 0.08, "#FFFFFF", { y: 0.14 + H - 0.05, parent: g, r: 0.04 });
  if (floors > 1) box(w + 0.06, 0.08, d + 0.06, "#FFFFFF", { y: 0.14 + h, parent: g, r: 0.03 });

  // windows on the faces the camera can see (+z, +x, -x)
  const win = (face, u, v) => {
    const wg = group(g);
    const ww = 0.62,
      wh = 0.78;
    box(ww + 0.14, wh + 0.14, 0.06, "#FFFFFF", { parent: wg, r: 0.03, cast: false });
    box(ww, wh, 0.07, smat(PAL.glass, { roughness: 0.25 }), { z: 0.01, parent: wg, r: 0.02, cast: false });
    box(0.05, wh, 0.08, "#FFFFFF", { z: 0.02, parent: wg, r: 0, cast: false });
    box(0.22, wh + 0.04, 0.05, shutter, { x: -(ww / 2 + 0.17), parent: wg, r: 0.02 });
    box(0.22, wh + 0.04, 0.05, shutter, { x: ww / 2 + 0.17, parent: wg, r: 0.02 });
    // flower box
    box(ww + 0.1, 0.14, 0.18, PAL.roofTerra, { y: -(wh / 2 + 0.1), z: 0.08, parent: wg, r: 0.03 });
    for (let i = 0; i < 4; i++)
      sph(0.07, [PAL.coral, "#FFFFFF", PAL.sun, PAL.coral][(i + seed) % 4], {
        x: -0.24 + i * 0.16,
        y: -(wh / 2) + 0.02,
        z: 0.1,
        parent: wg,
        ws: 8,
        hs: 6,
        cast: false,
      });
    const y = 0.14 + v;
    if (face === "+z") wg.position.set(u, y, d / 2 + 0.02);
    if (face === "+x") {
      wg.position.set(w / 2 + 0.02, y, u);
      wg.rotation.y = Math.PI / 2;
    }
    if (face === "-x") {
      wg.position.set(-w / 2 - 0.02, y, u);
      wg.rotation.y = -Math.PI / 2;
    }
  };
  for (let f = 0; f < floors; f++) {
    const vy = f * h + h * 0.58;
    if (f === 0) win("+z", w * 0.24 + 0.1, vy);
    else {
      win("+z", -w * 0.24, vy);
      win("+z", w * 0.24, vy);
    }
    win("+x", -d * 0.2, vy);
    win("-x", d * 0.2, vy);
  }

  // door on +z, hinged on its left edge so it swings outward toward the street
  const doorX = -w * 0.22;
  box(0.98, 1.56, 0.06, "#FFFFFF", { x: doorX, y: 0.14 + 0.78, z: d / 2 + 0.01, parent: g, r: 0.03, cast: false });
  box(0.86, 0.08, 0.5, PAL.pave, { x: doorX, y: 0.18, z: d / 2 + 0.25, parent: g, r: 0.03 });
  const hs = hingeRight ? -1 : 1; // panel extends from the hinge toward +x (left hinge) or −x (right hinge)
  const hinge = group(g, { x: doorX - 0.4 * hs, y: 0.14, z: d / 2 + 0.06 });
  const doorPanel = box(0.8, 1.44, 0.07, door, { x: 0.4 * hs, y: 0.74, parent: hinge, r: 0.03 });
  box(0.5, 0.5, 0.02, mat("#FFFFFF", { transparent: true, opacity: 0.35 }), { x: 0.4 * hs, y: 1.08, z: 0.04, parent: hinge, r: 0.02, cast: false });
  sph(0.05, PAL.sun, { x: 0.68 * hs, y: 0.72, z: 0.07, parent: hinge, cast: false });
  // dark interior behind the door (visible when it opens)
  box(0.78, 1.42, 0.02, "#3A2E4A", { x: doorX, y: 0.14 + 0.72, z: d / 2 - 0.0, parent: g, r: 0, cast: false });
  // wall lamp + house number plate
  sph(0.08, mat("#FFF3C4", { emissive: "#FFE08A", emissiveIntensity: 0.6 }), { x: doorX + 0.66, y: 1.75, z: d / 2 + 0.08, parent: g });

  if (awning) {
    const aw = box(1.3, 0.06, 0.6, awning, { x: doorX, y: 0.14 + 1.72, z: d / 2 + 0.3, rx: 0.32, parent: g, r: 0.02 });
    aw.castShadow = true;
  }

  // roof
  const top = 0.14 + H;
  if (roofType === "gable") {
    const sh = new THREE.Shape();
    const rw = w / 2 + 0.3;
    const rh = 1.1;
    sh.moveTo(-rw, 0);
    sh.lineTo(rw, 0);
    sh.lineTo(0, rh);
    sh.closePath();
    const eg = new THREE.ExtrudeGeometry(sh, { depth: d + 0.5, bevelEnabled: false });
    eg.translate(0, 0, -(d + 0.5) / 2);
    mesh(eg, mat(roof, { flatShading: true }), { y: top, parent: g });
    // gable end walls (fill the triangle with wall colour)
    const gsh = new THREE.Shape();
    gsh.moveTo(-w / 2, 0);
    gsh.lineTo(w / 2, 0);
    gsh.lineTo(0, rh * (w / 2 / rw));
    gsh.closePath();
    const gg = new THREE.ExtrudeGeometry(gsh, { depth: d, bevelEnabled: false });
    gg.translate(0, 0, -d / 2);
    mesh(gg, mat(wall), { y: top, parent: g });
    box(0.36, 0.7, 0.36, PAL.roofTerra, { x: w * 0.22, y: top + 0.8, z: -d * 0.15, parent: g, r: 0.04 });
  } else if (roofType === "hip") {
    const cg = new THREE.ConeGeometry(Math.SQRT1_2 * (Math.max(w, d) + 0.5), 1.25, 4, 1);
    cg.rotateY(Math.PI / 4);
    const m = mesh(cg, mat(roof, { flatShading: true }), { y: top + 0.62, parent: g });
    m.scale.set((w + 0.5) / (Math.max(w, d) + 0.5), 1, (d + 0.5) / (Math.max(w, d) + 0.5));
  } else {
    // flat roof terrace with a parapet, potted plants and a little sun parasol
    box(w + 0.1, 0.32, 0.14, wall, { y: top + 0.16, z: d / 2 - 0.02, parent: g, r: 0.03 });
    box(w + 0.1, 0.32, 0.14, wall, { y: top + 0.16, z: -d / 2 + 0.02, parent: g, r: 0.03 });
    box(0.14, 0.32, d, wall, { x: w / 2 - 0.02, y: top + 0.16, parent: g, r: 0.03 });
    box(0.14, 0.32, d, wall, { x: -w / 2 + 0.02, y: top + 0.16, parent: g, r: 0.03 });
    box(w - 0.3, 0.04, d - 0.3, roof, { y: top + 0.02, parent: g, r: 0.01, cast: false });
    pot(g, w / 2 - 0.45, top, d / 2 - 0.45, R);
    pot(g, -w / 2 + 0.45, top, -d / 2 + 0.45, R);
    const p = parasol(R() > 0.5 ? PAL.coral : PAL.teal, 0.8);
    p.position.set(-w * 0.12, top, d * 0.1);
    g.add(p);
  }

  // garden bits
  pot(g, doorX + 0.85, 0.14, d / 2 + 0.35, R);
  if (R() > 0.4) bush(g, w / 2 + 0.1, 0.14, d / 2 + 0.05, 0.38, R);

  const api = {
    group: g,
    hinge,
    hingeSign: hs,
    doorPanel,
    // doorstep in local coords (door on +z)
    doorstep: new THREE.Vector3(doorX, 0, d / 2 + 0.7),
    bell: new THREE.Vector3(doorX + 0.66, 1.9, d / 2 + 0.2),
    top,
  };
  return api;
}

export function pot(parent, x, y, z, R = Math.random) {
  cyl(0.16, 0.12, 0.28, PAL.roofTerra, { x, y: y + 0.14, z, parent, seg: 10 });
  sph(0.24, R() > 0.5 ? PAL.leaf : PAL.grassDeep, { x, y: y + 0.42, z, parent, ico: 1, flat: true });
}
export function bush(parent, x, y, z, r = 0.4, R = Math.random) {
  sph(r, R() > 0.5 ? PAL.leaf : PAL.grassDeep, { x, y: y + r * 0.7, z, parent, ico: 1, flat: true });
  sph(r * 0.7, PAL.grassDeep, { x: x + r * 0.6, y: y + r * 0.5, z: z + r * 0.2, parent, ico: 1, flat: true });
  if (R() > 0.5) sph(0.07, PAL.coral, { x: x + 0.1, y: y + r * 1.3, z: z + 0.2, parent, ws: 8, hs: 6, cast: false });
}

// ---------- props ----------
export function parasol(color = PAL.coral, s = 1, stripes = null) {
  const g = new THREE.Group();
  cyl(0.035, 0.035, 2.0 * s, "#FFFFFF", { y: 1.0 * s, parent: g, seg: 8 });
  const cone = new THREE.ConeGeometry(1.15 * s, 0.5 * s, 12, 1, true);
  const m = stripes ? mat("#FFFFFF", { map: stripes, side: THREE.DoubleSide }) : mat(color, { side: THREE.DoubleSide, flatShading: true });
  mesh(cone, m, { y: 2.05 * s, parent: g });
  sph(0.07 * s, "#FFFFFF", { y: 2.33 * s, parent: g, ws: 8, hs: 6 });
  g.rotation.z = 0.12;
  return g;
}

export function palm(seed = 1, s = 1) {
  const R = rng(seed * 97 + 3);
  const g = new THREE.Group();
  const lean = (R() - 0.5) * 0.5;
  const segs = 6;
  let y = 0,
    x = 0;
  for (let i = 0; i < segs; i++) {
    const hgt = 0.62 * s;
    const r0 = (0.2 - i * 0.017) * s;
    cyl(r0 * 0.9, r0, hgt, i % 2 ? PAL.trunk : "#B88A5C", { x, y: y + hgt / 2, z: 0, rz: -lean * 0.4, parent: g, seg: 7 });
    y += hgt * 0.97;
    x += lean * 0.12 * s * (i + 1) * 0.35;
  }
  const crown = group(g, { x, y });
  const fronds = [];
  const n = 7;
  for (let i = 0; i < n; i++) {
    const pivot = group(crown, { ry: (i / n) * TAU + R() * 0.4 });
    const tilt = group(pivot, { rx: 0.45 + R() * 0.25 });
    const L = (1.25 + R() * 0.3) * s;
    const sh = new THREE.Shape();
    sh.moveTo(0, 0);
    sh.quadraticCurveTo(0.32 * s, L * 0.45, 0, L);
    sh.quadraticCurveTo(-0.32 * s, L * 0.45, 0, 0);
    const eg = new THREE.ExtrudeGeometry(sh, { depth: 0.04, bevelEnabled: false, curveSegments: 6 });
    eg.rotateX(-Math.PI / 2);
    mesh(eg, mat(i % 2 ? PAL.leaf : "#3BB37A", { flatShading: true, side: THREE.DoubleSide }), { parent: tilt });
    const tip = group(tilt, { z: -L * 0.55, rx: 0.5 });
    const sh2 = new THREE.Shape();
    sh2.moveTo(0, 0);
    sh2.quadraticCurveTo(0.22 * s, L * 0.3, 0, L * 0.62);
    sh2.quadraticCurveTo(-0.22 * s, L * 0.3, 0, 0);
    const eg2 = new THREE.ExtrudeGeometry(sh2, { depth: 0.04, bevelEnabled: false, curveSegments: 6 });
    eg2.rotateX(-Math.PI / 2);
    mesh(eg2, mat(i % 2 ? PAL.leaf : "#3BB37A", { flatShading: true, side: THREE.DoubleSide }), { parent: tip });
    fronds.push({ tilt, base: tilt.rotation.x, ph: R() * TAU });
  }
  for (let i = 0; i < 3; i++) sph(0.11 * s, "#7A4E2D", { x: Math.cos(i * 2.1) * 0.14 * s, y: -0.08, z: Math.sin(i * 2.1) * 0.14 * s, parent: crown, ws: 8, hs: 6 });
  return { group: g, fronds, crown };
}

export function tree(seed = 1, s = 1) {
  const R = rng(seed * 31 + 7);
  const g = new THREE.Group();
  cyl(0.1 * s, 0.14 * s, 0.9 * s, PAL.trunk, { y: 0.45 * s, parent: g, seg: 7 });
  const cols = [PAL.leaf, PAL.grassDeep, "#5DBB63"];
  sph(0.7 * s, cols[Math.floor(R() * 3)], { y: 1.25 * s, parent: g, ico: 1, flat: true });
  sph(0.5 * s, cols[Math.floor(R() * 3)], { x: 0.35 * s, y: 1.05 * s, z: 0.2 * s, parent: g, ico: 1, flat: true });
  sph(0.45 * s, cols[Math.floor(R() * 3)], { x: -0.3 * s, y: 1.55 * s, z: -0.1 * s, parent: g, ico: 1, flat: true });
  return g;
}

export function lamp() {
  const g = new THREE.Group();
  cyl(0.05, 0.07, 2.2, PAL.ink, { y: 1.1, parent: g, seg: 8 });
  box(0.5, 0.05, 0.08, PAL.ink, { x: 0.2, y: 2.2, parent: g, r: 0.02 });
  sph(0.13, mat("#FFF3C4", { emissive: "#FFE08A", emissiveIntensity: 0.5 }), { x: 0.42, y: 2.1, parent: g, ws: 10, hs: 8 });
  return g;
}

export function bench() {
  const g = new THREE.Group();
  for (let i = 0; i < 3; i++) box(1.3, 0.06, 0.12, "#C98F5E", { y: 0.42, z: -0.14 + i * 0.14, parent: g, r: 0.02 });
  box(1.3, 0.3, 0.06, "#C98F5E", { y: 0.66, z: -0.24, rx: -0.15, parent: g, r: 0.02 });
  for (const x of [-0.55, 0.55]) box(0.06, 0.42, 0.4, PAL.ink, { x, y: 0.21, parent: g, r: 0.01 });
  return g;
}

export function cloud(seed = 1, s = 1) {
  const R = rng(seed * 13 + 5);
  const g = new THREE.Group();
  const m = mat("#FFFFFF", { flatShading: true });
  const n = 4 + Math.floor(R() * 3);
  for (let i = 0; i < n; i++) {
    const r = (0.6 + R() * 0.7) * s;
    mesh(new THREE.IcosahedronGeometry(r, 1), m, { x: (i - n / 2) * 0.75 * s, y: R() * 0.4 * s, z: (R() - 0.5) * 0.9 * s, parent: g, recv: false });
  }
  return g;
}

export function sailboat(color = PAL.coral) {
  const g = new THREE.Group();
  const sh = new THREE.Shape();
  sh.moveTo(-1.1, 0.35);
  sh.lineTo(1.2, 0.35);
  sh.quadraticCurveTo(0.9, -0.2, 0.4, -0.25);
  sh.lineTo(-0.8, -0.25);
  sh.quadraticCurveTo(-1.05, -0.1, -1.1, 0.35);
  const eg = new THREE.ExtrudeGeometry(sh, { depth: 0.8, bevelEnabled: true, bevelSize: 0.05, bevelThickness: 0.05, bevelSegments: 1 });
  eg.translate(0, 0, -0.4);
  mesh(eg, mat("#FFFFFF"), { parent: g });
  box(2.3, 0.08, 0.84, color, { y: 0.2, parent: g, r: 0.02 });
  cyl(0.04, 0.04, 2.6, "#FFFFFF", { x: 0.05, y: 1.6, parent: g, seg: 8 });
  const s1 = new THREE.Shape();
  s1.moveTo(0, 0);
  s1.lineTo(1.0, 0);
  s1.lineTo(0, 2.2);
  s1.closePath();
  mesh(new THREE.ExtrudeGeometry(s1, { depth: 0.03, bevelEnabled: false }), mat("#FFFFFF", { side: THREE.DoubleSide }), { x: 0.12, y: 0.5, parent: g });
  const s2 = new THREE.Shape();
  s2.moveTo(0, 0);
  s2.lineTo(-0.85, 0);
  s2.lineTo(0, 1.8);
  s2.closePath();
  mesh(new THREE.ExtrudeGeometry(s2, { depth: 0.03, bevelEnabled: false }), mat(color, { side: THREE.DoubleSide }), { x: -0.02, y: 0.55, parent: g });
  return g;
}

// ---------- parcels ----------
export function parcel(stickerTex, s = 1) {
  const g = new THREE.Group();
  const w = 0.9 * s,
    h = 0.6 * s,
    d = 0.7 * s;
  box(w, h, d, PAL.kraft, { y: h / 2, parent: g, r: 0.05 * s });
  box(w + 0.02, h + 0.02, 0.16 * s, PAL.coral, { y: h / 2, parent: g, r: 0.03 * s, cast: false });
  const st = mesh(new THREE.PlaneGeometry(0.34 * s, 0.34 * s), mat("#FFFFFF", { map: stickerTex, transparent: true }), {
    x: w * 0.22,
    y: h + 0.006,
    z: d * 0.2,
    rx: -Math.PI / 2,
    parent: g,
    cast: false,
  });
  st.receiveShadow = true;
  return g;
}

// Open box with four hinged flaps (flap angle 0 = closed, ~1.9 = wide open).
export function openBox(s = 1) {
  const g = new THREE.Group();
  const w = 1.0 * s,
    h = 0.62 * s,
    d = 0.78 * s,
    t = 0.04 * s;
  const k = mat(PAL.kraft);
  const kd = mat(PAL.kraftDeep);
  box(w, t, d, kd, { y: t / 2, parent: g, r: 0 });
  box(w, h, t, k, { y: h / 2, z: d / 2 - t / 2, parent: g, r: 0 });
  box(w, h, t, k, { y: h / 2, z: -d / 2 + t / 2, parent: g, r: 0 });
  box(t, h, d, k, { x: w / 2 - t / 2, y: h / 2, parent: g, r: 0 });
  box(t, h, d, k, { x: -w / 2 + t / 2, y: h / 2, parent: g, r: 0 });
  box(w - 2 * t, 0.01, d - 2 * t, mat("#A8733F"), { y: t + 0.006, parent: g, r: 0, cast: false });
  const flaps = [];
  const mk = (px, pz, ry, len, wid) => {
    const p = group(g, { x: px, y: h, z: pz, ry });
    box(wid, t * 0.8, len, k, { z: len / 2, parent: p, r: 0 });
    flaps.push(p);
    return p;
  };
  mk(0, d / 2, 0, d / 2, w); // front (+z) flap folds toward -z when closing
  mk(0, -d / 2, Math.PI, d / 2, w);
  mk(w / 2, 0, Math.PI / 2, w / 2, d * 0.98).position.y = h + 0.03;
  mk(-w / 2, 0, -Math.PI / 2, w / 2, d * 0.98).position.y = h + 0.03;
  const tape = box(w + 0.02, 0.02, 0.18 * s, PAL.coral, { y: h + 0.06, parent: g, r: 0, cast: false });
  tape.scale.x = 0.001;
  return { group: g, flaps, tape, h, w, d };
}
// flap rotation: rotate about local x of each pivot (pivot's +z points outward from the edge)
export function setFlap(f, open) {
  // open = 0 → folded flat over the top (−π), 1 → open outward, tipped up (−0.5)
  f.rotation.x = -Math.PI + (Math.PI - 0.5) * open;
}

// ---------- the delivery van ----------
export function van(sideTex, toppperTex) {
  const g = new THREE.Group();
  const body = group(g); // leans / bounces
  const white = mat("#FFFFFF");
  box(2.5, 1.62, 1.66, white, { x: -0.42, y: 1.16, parent: body, r: 0.14 }); // cargo box
  box(1.02, 1.12, 1.6, white, { x: 1.28, y: 0.91, parent: body, r: 0.18 }); // cab
  box(0.08, 0.62, 1.42, smat(PAL.glass, { roughness: 0.2 }), { x: 1.76, y: 1.12, parent: body, r: 0.04, rz: -0.32 }); // windshield
  for (const z of [0.81, -0.81]) {
    box(0.62, 0.46, 0.04, smat(PAL.glass, { roughness: 0.2 }), { x: 1.3, y: 1.18, z, parent: body, r: 0.03 });
    box(0.1, 0.16, 0.14, PAL.ink, { x: 1.62, y: 1.18, z: z * 1.16, parent: body, r: 0.03 });
  }
  box(3.62, 0.2, 1.7, PAL.coral, { x: 0.09, y: 0.66, parent: body, r: 0.06 }); // stripe
  box(0.18, 0.3, 1.5, "#E8E1EC", { x: 1.83, y: 0.52, parent: body, r: 0.06 }); // bumper
  box(0.14, 0.26, 1.68, "#E8E1EC", { x: -1.7, y: 0.52, parent: body, r: 0.06 });
  for (const z of [0.55, -0.55]) {
    sph(0.11, mat("#FFF6D6", { emissive: "#FFE9A8", emissiveIntensity: 0.6 }), { x: 1.79, y: 0.86, z, parent: body, ws: 10, hs: 8 });
    box(0.06, 0.22, 0.16, mat(PAL.coralDeep, { emissive: PAL.coralDeep, emissiveIntensity: 0.3 }), { x: -1.69, y: 1.2, z: z * 1.38, parent: body, r: 0.02 });
  }
  // brand panels on both sides of the cargo box
  for (const side of [1, -1]) {
    const p = mesh(new THREE.PlaneGeometry(2.1, 0.53), mat("#FFFFFF", { map: sideTex, transparent: true }), {
      x: -0.4,
      y: 1.38,
      z: side * 0.836,
      ry: side > 0 ? 0 : Math.PI,
      parent: body,
      cast: false,
    });
    p.renderOrder = 2;
  }
  // roof topper: heart sign
  box(0.9, 0.08, 0.5, PAL.ink, { x: -0.3, y: 2.0, parent: body, r: 0.03 });
  const top = mesh(new THREE.PlaneGeometry(0.62, 0.62), mat("#FFFFFF", { map: toppperTex, transparent: true, side: THREE.DoubleSide }), {
    x: -0.3,
    y: 2.38,
    parent: body,
    cast: false,
  });
  // rear doors, hinged at the outer edges
  const doors = [];
  for (const side of [1, -1]) {
    const hinge = group(body, { x: -1.68, y: 1.16, z: side * 0.82 });
    box(0.06, 1.5, 0.8, white, { z: -side * 0.4, parent: hinge, r: 0.04 });
    box(0.04, 0.4, 0.5, smat(PAL.glass, { roughness: 0.2 }), { x: -0.03, y: 0.35, z: -side * 0.4, parent: hinge, r: 0.03 });
    doors.push({ hinge, side });
  }
  // dark cargo interior visible behind the doors
  box(0.04, 1.44, 1.5, "#4A3B5C", { x: -1.66, y: 1.16, parent: body, r: 0 });
  // wheels
  const wheels = [];
  for (const [x, z] of [
    [1.15, 0.8],
    [1.15, -0.8],
    [-1.05, 0.8],
    [-1.05, -0.8],
  ]) {
    const wg = group(g, { x, y: 0.36, z });
    const tire = cyl(0.36, 0.36, 0.26, "#2A2738", { rx: Math.PI / 2, parent: wg, seg: 16 });
    cyl(0.18, 0.18, 0.27, "#E8E1EC", { rx: Math.PI / 2, parent: wg, seg: 12 });
    wheels.push(wg);
  }
  return { group: g, body, doors, wheels, topper: top };
}

// ---------- people ----------
// A toy-like person, ~1.75 tall, facing +z. Pose with walk(), carry(), wave().
export function person(o) {
  const {
    skin = PAL.skinB,
    top = PAL.coral,
    bottom = PAL.navy,
    hair = PAL.hairDark,
    style = "cap",
    dress = false,
    shoes = "#FFFFFF",
    bikini = null, // texture → swimwear outfit
    glasses = false,
    cap = PAL.coral,
  } = o;
  const g = new THREE.Group();
  const root = group(g); // bob
  const legs = [];
  for (const sx of [-1, 1]) {
    const p = group(root, { x: sx * 0.13, y: 0.82 });
    box(0.2, 0.42, 0.22, bikini ? skin : bottom, { y: -0.2, parent: p, r: 0.07 });
    box(0.17, 0.36, 0.18, skin, { y: -0.56, parent: p, r: 0.07 });
    box(0.2, 0.1, 0.3, bikini ? PAL.sun : shoes, { y: -0.77, z: 0.04, parent: p, r: 0.04 });
    legs.push(p);
  }
  const torso = group(root, { y: 0.82 });
  if (bikini) {
    box(0.5, 0.64, 0.3, skin, { y: 0.34, parent: torso, r: 0.12 });
    const bm = mat("#FFFFFF", { map: bikini });
    box(0.52, 0.16, 0.32, bm, { y: 0.06, parent: torso, r: 0.06 }); // bottoms
    for (const sx of [-1, 1]) box(0.19, 0.15, 0.08, bm, { x: sx * 0.11, y: 0.5, z: 0.15, parent: torso, r: 0.05 });
    box(0.52, 0.04, 0.31, bm, { y: 0.52, parent: torso, r: 0.01 });
  } else {
    box(0.56, 0.66, 0.34, top, { y: 0.34, parent: torso, r: 0.12 });
    if (dress) {
      const sk = new THREE.CylinderGeometry(0.3, 0.46, 0.62, 14);
      mesh(sk, mat(top), { y: -0.14, parent: torso });
    } else box(0.54, 0.16, 0.32, bottom, { y: 0.06, parent: torso, r: 0.06 });
  }
  const arms = [];
  for (const sx of [-1, 1]) {
    const p = group(root, { x: sx * 0.35, y: 1.42 });
    box(0.17, 0.3, 0.19, bikini ? skin : top, { y: -0.13, parent: p, r: 0.07 });
    box(0.14, 0.32, 0.15, skin, { y: -0.42, parent: p, r: 0.06 });
    sph(0.085, skin, { y: -0.62, parent: p, ws: 10, hs: 8 });
    arms.push(p);
  }
  const head = group(root, { y: 1.5 });
  cyl(0.08, 0.09, 0.12, skin, { y: 0.04, parent: head, seg: 8 });
  sph(0.25, skin, { y: 0.3, parent: head, ws: 18, hs: 14 });
  for (const sx of [-1, 1]) {
    sph(0.035, PAL.ink, { x: sx * 0.085, y: 0.32, z: 0.225, parent: head, ws: 8, hs: 6, cast: false });
    sph(0.04, mat("#FF9DAF"), { x: sx * 0.15, y: 0.23, z: 0.19, parent: head, ws: 8, hs: 6, cast: false, s: 1 }).scale.set(1, 0.6, 0.4);
  }
  if (glasses) {
    for (const sx of [-1, 1]) cyl(0.075, 0.075, 0.03, PAL.ink, { x: sx * 0.095, y: 0.33, z: 0.24, rx: Math.PI / 2, parent: head, seg: 12, cast: false });
    box(0.06, 0.025, 0.02, PAL.ink, { y: 0.34, z: 0.25, parent: head, r: 0, cast: false });
  }
  if (style === "cap") {
    const capM = mat(cap);
    mesh(new THREE.SphereGeometry(0.265, 16, 8, 0, TAU, 0, Math.PI / 2), capM, { y: 0.34, parent: head });
    box(0.36, 0.04, 0.26, capM, { y: 0.36, z: 0.24, parent: head, r: 0.02 });
  } else if (style === "long") {
    mesh(new THREE.SphereGeometry(0.275, 16, 10, 0, TAU, 0, Math.PI / 1.9), mat(hair), { y: 0.33, parent: head });
    box(0.52, 0.62, 0.22, hair, { y: 0.06, z: -0.13, parent: head, r: 0.1 });
  } else if (style === "bun") {
    mesh(new THREE.SphereGeometry(0.272, 16, 10, 0, TAU, 0, Math.PI / 1.9), mat(hair), { y: 0.33, parent: head });
    sph(0.15, hair, { y: 0.6, z: -0.06, parent: head, ws: 12, hs: 10 });
  } else if (style === "curly") {
    for (let i = 0; i < 9; i++) {
      const a = (i / 9) * TAU;
      sph(0.12, hair, { x: Math.cos(a) * 0.2, y: 0.45 + Math.sin(i * 1.7) * 0.04, z: Math.sin(a) * 0.2 - 0.04, parent: head, ws: 8, hs: 6 });
    }
  }
  const api = { group: g, root, legs, arms, head, torso };
  return api;
}

// phase-driven poses (pure functions of their arguments)
export function poseWalk(p, phase, amp = 0.55) {
  const s = Math.sin(phase);
  p.legs[0].rotation.x = s * amp;
  p.legs[1].rotation.x = -s * amp;
  p.arms[0].rotation.set(-s * amp * 0.8, 0, 0);
  p.arms[1].rotation.set(s * amp * 0.8, 0, 0);
  p.root.position.y = Math.abs(Math.cos(phase)) * 0.05 * (amp / 0.55);
}
export function poseIdle(p, t) {
  p.legs[0].rotation.x = 0;
  p.legs[1].rotation.x = 0;
  p.arms[0].rotation.set(0, 0, 0.06);
  p.arms[1].rotation.set(0, 0, -0.06);
  p.root.position.y = Math.sin(t * 2.2) * 0.012;
}
export function poseCarry(p, k = 1) {
  p.arms[0].rotation.set(-1.25 * k, 0, 0.12 * k);
  p.arms[1].rotation.set(-1.25 * k, 0, -0.12 * k);
}
export function poseWave(p, t, k = 1, arm = 1) {
  p.arms[arm].rotation.set(0, 0, (arm ? 1 : -1) * k * (2.5 + Math.sin(t * 13) * 0.35));
}

// ---------- 3D bikini (product) ----------
export function bikini3D(print, trim = PAL.coralDeep) {
  const g = new THREE.Group();
  const m = mat("#FFFFFF", { map: print, side: THREE.DoubleSide });
  const tm = mat(trim);
  const ext = { depth: 0.05, bevelEnabled: true, bevelThickness: 0.02, bevelSize: 0.02, bevelSegments: 2, curveSegments: 10 };
  const cupShape = () => {
    const s = new THREE.Shape();
    s.moveTo(0, 0.24);
    s.quadraticCurveTo(0.21, 0.02, 0.21, -0.1);
    s.quadraticCurveTo(0, -0.2, -0.21, -0.1);
    s.quadraticCurveTo(-0.21, 0.02, 0, 0.24);
    return s;
  };
  for (const sx of [-1, 1]) {
    const eg = new THREE.ExtrudeGeometry(cupShape(), ext);
    mesh(eg, m, { x: sx * 0.23, y: 0.42, rz: -sx * 0.16, ry: sx * 0.12, parent: g });
  }
  const curve = (pts, r = 0.016) => {
    const c = new THREE.CatmullRomCurve3(pts.map((p) => new THREE.Vector3(...p)));
    mesh(new THREE.TubeGeometry(c, 24, r, 6, false), tm, { parent: g, cast: false });
  };
  curve([
    [-0.28, 0.62, 0.02],
    [-0.12, 0.86, 0.0],
    [0.0, 0.92, -0.02],
    [0.12, 0.86, 0.0],
    [0.28, 0.62, 0.02],
  ]);
  curve([
    [-0.06, 0.36, 0.05],
    [0, 0.38, 0.06],
    [0.06, 0.36, 0.05],
  ]);
  curve([
    [-0.42, 0.34, 0.03],
    [-0.56, 0.36, 0.0],
    [-0.64, 0.42, -0.02],
  ]);
  curve([
    [0.42, 0.34, 0.03],
    [0.56, 0.36, 0.0],
    [0.64, 0.42, -0.02],
  ]);
  const bs = new THREE.Shape();
  bs.moveTo(-0.38, 0.12);
  bs.quadraticCurveTo(0, 0.17, 0.38, 0.12);
  bs.quadraticCurveTo(0.3, -0.06, 0.08, -0.2);
  bs.quadraticCurveTo(0, -0.24, -0.08, -0.2);
  bs.quadraticCurveTo(-0.3, -0.06, -0.38, 0.12);
  mesh(new THREE.ExtrudeGeometry(bs, ext), m, { y: -0.18, parent: g });
  for (const sx of [-1, 1]) {
    curve([
      [sx * 0.38, -0.06, 0.03],
      [sx * 0.5, -0.02, 0.03],
      [sx * 0.54, -0.12, 0.03],
    ]);
    curve([
      [sx * 0.38, -0.06, 0.03],
      [sx * 0.52, -0.08, 0.03],
      [sx * 0.6, 0.0, 0.03],
    ]);
  }
  return g;
}

export function hanger() {
  const g = new THREE.Group();
  const c = new THREE.CatmullRomCurve3([
    new THREE.Vector3(-0.42, 0, 0),
    new THREE.Vector3(0, 0.2, 0),
    new THREE.Vector3(0.42, 0, 0),
  ]);
  mesh(new THREE.TubeGeometry(c, 12, 0.025, 6, false), mat("#C9A26B"), { parent: g, cast: false });
  mesh(new THREE.TorusGeometry(0.07, 0.015, 6, 12, Math.PI * 1.3), mat("#B9B4C2"), { y: 0.27, parent: g, cast: false });
  return g;
}
