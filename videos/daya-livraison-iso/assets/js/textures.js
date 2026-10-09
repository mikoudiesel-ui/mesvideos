// Canvas-drawn textures: bikini prints, signage, the phone's shop UI, and sprite icons.
// Drawn once at build time (the phone UI redraws only when its state key changes).
import * as THREE from "../vendor/three.module.min.js";
import { PAL } from "./palette.js";
import { clamp, lerp, E, TAU } from "./util.js";

export const FONT_D = "Unbounded"; // display sans
export const FONT_S = "Fraunces"; // italic serif accent

export function canvas(w, h) {
  const c = document.createElement("canvas");
  c.width = w;
  c.height = h;
  return { c, g: c.getContext("2d") };
}

export function rr(g, x, y, w, h, r) {
  const k = Math.min(r, w / 2, h / 2);
  g.beginPath();
  g.moveTo(x + k, y);
  g.arcTo(x + w, y, x + w, y + h, k);
  g.arcTo(x + w, y + h, x, y + h, k);
  g.arcTo(x, y + h, x, y, k);
  g.arcTo(x, y, x + w, y, k);
  g.closePath();
}

export function tex(c, { repeat = null, srgb = true, mips = true } = {}) {
  const t = new THREE.CanvasTexture(c);
  if (srgb) t.colorSpace = THREE.SRGBColorSpace;
  t.anisotropy = 4;
  if (!mips) {
    t.generateMipmaps = false;
    t.minFilter = THREE.LinearFilter;
  }
  if (repeat) {
    t.wrapS = t.wrapT = THREE.RepeatWrapping;
    t.repeat.set(repeat[0], repeat[1]);
  }
  return t;
}

// ---------- small vector icons ----------
export function heartPath(g, cx, cy, s) {
  g.beginPath();
  g.moveTo(cx, cy + s * 0.32);
  g.bezierCurveTo(cx - s * 0.62, cy - s * 0.12, cx - s * 0.36, cy - s * 0.62, cx, cy - s * 0.3);
  g.bezierCurveTo(cx + s * 0.36, cy - s * 0.62, cx + s * 0.62, cy - s * 0.12, cx, cy + s * 0.32);
  g.closePath();
}

function checkPath(g, cx, cy, s, p = 1) {
  // A two-stroke check mark drawn to progress p.
  const a = [cx - s * 0.42, cy + s * 0.02];
  const b = [cx - s * 0.12, cy + s * 0.3];
  const c = [cx + s * 0.44, cy - s * 0.3];
  const l1 = Math.hypot(b[0] - a[0], b[1] - a[1]);
  const l2 = Math.hypot(c[0] - b[0], c[1] - b[1]);
  const d = p * (l1 + l2);
  g.beginPath();
  g.moveTo(a[0], a[1]);
  if (d <= l1) {
    g.lineTo(lerp(a[0], b[0], d / l1), lerp(a[1], b[1], d / l1));
  } else {
    g.lineTo(b[0], b[1]);
    const q = (d - l1) / l2;
    g.lineTo(lerp(b[0], c[0], q), lerp(b[1], c[1], q));
  }
}

// 2D bikini illustration (top + bottom), centred at cx,cy, width ~ s.
export function drawBikini2D(g, cx, cy, s, base = PAL.coral, dot = "#FFFFFF") {
  g.save();
  const cup = (dx, flip) => {
    g.save();
    g.translate(cx + dx * s, cy - s * 0.32);
    g.rotate(flip * 0.18);
    g.beginPath();
    g.moveTo(0, -s * 0.2);
    g.quadraticCurveTo(s * 0.2, s * 0.02, s * 0.2, s * 0.12);
    g.quadraticCurveTo(0, s * 0.19, -s * 0.2, s * 0.12);
    g.quadraticCurveTo(-s * 0.2, s * 0.02, 0, -s * 0.2);
    g.closePath();
    g.fillStyle = base;
    g.fill();
    g.clip();
    g.fillStyle = dot;
    for (let i = -3; i <= 3; i++)
      for (let j = -3; j <= 3; j++) {
        g.beginPath();
        g.arc(i * s * 0.075 + (j % 2) * s * 0.037, j * s * 0.065, s * 0.016, 0, TAU);
        g.fill();
      }
    g.restore();
  };
  // straps
  g.strokeStyle = PAL.coralDeep;
  g.lineWidth = s * 0.018;
  g.lineCap = "round";
  g.beginPath();
  g.moveTo(cx - s * 0.33, cy - s * 0.5);
  g.quadraticCurveTo(cx, cy - s * 0.78, cx + s * 0.33, cy - s * 0.5);
  g.moveTo(cx - s * 0.06, cy - s * 0.26);
  g.lineTo(cx + s * 0.06, cy - s * 0.26);
  g.moveTo(cx - s * 0.42, cy - s * 0.2);
  g.quadraticCurveTo(cx - s * 0.56, cy - s * 0.18, cx - s * 0.62, cy - s * 0.1);
  g.moveTo(cx + s * 0.42, cy - s * 0.2);
  g.quadraticCurveTo(cx + s * 0.56, cy - s * 0.18, cx + s * 0.62, cy - s * 0.1);
  g.stroke();
  cup(-0.22, -1);
  cup(0.22, 1);
  // bottom
  g.save();
  g.translate(cx, cy + s * 0.22);
  g.beginPath();
  g.moveTo(-s * 0.36, -s * 0.12);
  g.quadraticCurveTo(0, -s * 0.06, s * 0.36, -s * 0.12);
  g.quadraticCurveTo(s * 0.3, s * 0.06, s * 0.08, s * 0.2);
  g.quadraticCurveTo(0, s * 0.24, -s * 0.08, s * 0.2);
  g.quadraticCurveTo(-s * 0.3, s * 0.06, -s * 0.36, -s * 0.12);
  g.closePath();
  g.fillStyle = base;
  g.fill();
  g.save();
  g.clip();
  g.fillStyle = dot;
  for (let i = -5; i <= 5; i++)
    for (let j = -2; j <= 3; j++) {
      g.beginPath();
      g.arc(i * s * 0.075 + (j % 2) * s * 0.037, j * s * 0.065, s * 0.016, 0, TAU);
      g.fill();
    }
  g.restore();
  // side bows
  g.strokeStyle = PAL.coralDeep;
  g.lineWidth = s * 0.016;
  for (const sx of [-1, 1]) {
    g.beginPath();
    g.moveTo(sx * s * 0.36, -s * 0.12);
    g.quadraticCurveTo(sx * s * 0.46, -s * 0.06, sx * s * 0.42, s * 0.05);
    g.moveTo(sx * s * 0.36, -s * 0.12);
    g.quadraticCurveTo(sx * s * 0.5, -s * 0.16, sx * s * 0.52, -s * 0.05);
    g.stroke();
  }
  g.restore();
  g.restore();
}

// ---------- prints for the 3D bikinis ----------
export function printTextures() {
  const out = {};
  {
    const { c, g } = canvas(256, 256);
    g.fillStyle = PAL.coral;
    g.fillRect(0, 0, 256, 256);
    g.fillStyle = "#FFFFFF";
    for (let i = 0; i < 4; i++)
      for (let j = 0; j < 4; j++) {
        g.beginPath();
        g.arc(32 + i * 64 + (j % 2) * 32, 32 + j * 64, 10, 0, TAU);
        g.fill();
      }
    out.polka = tex(c, { repeat: [3, 3] });
  }
  {
    const { c, g } = canvas(512, 512);
    g.fillStyle = "#FF6B85";
    g.fillRect(0, 0, 512, 512);
    const leafAt = (x, y, r, rot, col) => {
      g.save();
      g.translate(x, y);
      g.rotate(rot);
      g.fillStyle = col;
      g.beginPath();
      g.moveTo(0, -r);
      g.bezierCurveTo(r * 0.8, -r * 0.6, r * 0.7, r * 0.6, 0, r);
      g.bezierCurveTo(-r * 0.7, r * 0.6, -r * 0.8, -r * 0.6, 0, -r);
      g.fill();
      g.strokeStyle = "rgba(255,255,255,0.55)";
      g.lineWidth = r * 0.06;
      g.beginPath();
      g.moveTo(0, -r * 0.9);
      g.lineTo(0, r * 0.9);
      for (let k = -3; k <= 3; k++) {
        g.moveTo(0, k * r * 0.22);
        g.lineTo(r * 0.45, k * r * 0.22 - r * 0.18);
        g.moveTo(0, k * r * 0.22);
        g.lineTo(-r * 0.45, k * r * 0.22 - r * 0.18);
      }
      g.stroke();
      g.restore();
    };
    const spots = [
      [80, 90, 70, 0.6, PAL.leaf],
      [300, 60, 60, -0.5, PAL.leafDark],
      [420, 220, 75, 1.1, PAL.leaf],
      [180, 300, 80, -1.0, PAL.leafDark],
      [400, 430, 65, 0.3, PAL.leaf],
      [60, 450, 60, 2.2, PAL.leaf],
      [250, 480, 40, 1.6, PAL.leafDark],
    ];
    for (const s of spots) leafAt(...s);
    g.fillStyle = PAL.sun;
    for (const [x, y] of [
      [200, 150],
      [470, 330],
      [110, 230],
      [330, 330],
      [480, 70],
      [160, 410],
    ]) {
      for (let k = 0; k < 5; k++) {
        g.beginPath();
        g.arc(x + Math.cos((k * TAU) / 5) * 10, y + Math.sin((k * TAU) / 5) * 10, 7, 0, TAU);
        g.fill();
      }
      g.fillStyle = "#FFFFFF";
      g.beginPath();
      g.arc(x, y, 5, 0, TAU);
      g.fill();
      g.fillStyle = PAL.sun;
    }
    out.leaf = tex(c, { repeat: [1.6, 1.6] });
  }
  {
    const { c, g } = canvas(256, 256);
    for (let i = 0; i < 8; i++) {
      g.fillStyle = i % 2 ? "#FFFFFF" : "#22B8C4";
      g.fillRect(0, i * 32, 256, 32);
    }
    out.stripes = tex(c, { repeat: [2, 2] });
  }
  {
    const { c, g } = canvas(256, 256);
    g.fillStyle = PAL.sun;
    g.fillRect(0, 0, 256, 256);
    g.fillStyle = "#FFFFFF";
    for (let i = 0; i < 3; i++)
      for (let j = 0; j < 3; j++) {
        const x = 42 + i * 86 + (j % 2) * 43;
        const y = 42 + j * 86;
        for (let k = 0; k < 5; k++) {
          g.beginPath();
          g.arc(x + Math.cos((k * TAU) / 5) * 11, y + Math.sin((k * TAU) / 5) * 11, 8, 0, TAU);
          g.fill();
        }
      }
    g.fillStyle = PAL.coral;
    for (let i = 0; i < 3; i++)
      for (let j = 0; j < 3; j++) {
        g.beginPath();
        g.arc(42 + i * 86 + (j % 2) * 43, 42 + j * 86, 6, 0, TAU);
        g.fill();
      }
    out.daisy = tex(c, { repeat: [3, 3] });
  }
  return out;
}

// ---------- signage ----------
export function signTexture(text, { w = 1024, h = 256, bg = "#FFFFFF", fg = PAL.coral, size = 120, heart = true, sub = null } = {}) {
  const { c, g } = canvas(w, h);
  if (bg) {
    g.fillStyle = bg;
    rr(g, 8, 8, w - 16, h - 16, h * 0.3);
    g.fill();
  }
  g.fillStyle = fg;
  g.textAlign = "center";
  g.textBaseline = "middle";
  g.font = `900 ${size}px ${FONT_D}`;
  const tw = g.measureText(text).width;
  const hx = heart ? size * 0.55 : 0;
  g.fillText(text, w / 2 + hx / 2, sub ? h * 0.4 : h / 2 + size * 0.04);
  if (heart) {
    heartPath(g, w / 2 - tw / 2 - hx * 0.35, sub ? h * 0.4 : h / 2, size * 0.62);
    g.fill();
  }
  if (sub) {
    g.font = `700 ${size * 0.36}px ${FONT_D}`;
    g.fillStyle = PAL.ink;
    g.fillText(sub, w / 2, h * 0.76);
  }
  return tex(c);
}

export function stripeTexture(a, b, n = 8, w = 256, h = 64, vertical = true) {
  const { c, g } = canvas(w, h);
  for (let i = 0; i < n; i++) {
    g.fillStyle = i % 2 ? b : a;
    if (vertical) g.fillRect((i * w) / n, 0, w / n + 1, h);
    else g.fillRect(0, (i * h) / n, w, h / n + 1);
  }
  return tex(c);
}

export function stickerTexture() {
  const { c, g } = canvas(256, 256);
  g.fillStyle = "#FFFFFF";
  g.beginPath();
  g.arc(128, 128, 118, 0, TAU);
  g.fill();
  g.fillStyle = PAL.coral;
  heartPath(g, 128, 118, 150);
  g.fill();
  return tex(c);
}

export function roundMask(w, h, r) {
  const { c, g } = canvas(w, h);
  g.fillStyle = "#000";
  g.fillRect(0, 0, w, h);
  g.fillStyle = "#FFF";
  rr(g, 0, 0, w, h, r);
  g.fill();
  return tex(c, { srgb: false });
}

export function dashTexture() {
  // navigation route: solid coral band with a soft edge and white centre dashes
  const { c, g } = canvas(128, 64);
  g.clearRect(0, 0, 128, 64);
  g.fillStyle = "rgba(255,79,112,0.35)";
  g.fillRect(0, 2, 128, 60);
  g.fillStyle = "#FF4F70";
  g.fillRect(0, 10, 128, 44);
  g.fillStyle = "#FFFFFF";
  rr(g, 22, 26, 60, 12, 6);
  g.fill();
  const t = tex(c);
  t.wrapS = THREE.RepeatWrapping;
  return t;
}

// ---------- sprites ----------
export function spriteTextures() {
  const out = {};
  {
    const { c, g } = canvas(160, 200);
    g.fillStyle = "rgba(42,27,61,0.18)";
    g.beginPath();
    g.ellipse(80, 188, 26, 8, 0, 0, TAU);
    g.fill();
    g.fillStyle = PAL.coral;
    g.beginPath();
    g.moveTo(80, 182);
    g.bezierCurveTo(40, 130, 14, 104, 14, 72);
    g.arc(80, 72, 66, Math.PI, 0);
    g.bezierCurveTo(146, 104, 120, 130, 80, 182);
    g.fill();
    g.fillStyle = "#FFFFFF";
    g.beginPath();
    g.arc(80, 72, 42, 0, TAU);
    g.fill();
    g.fillStyle = PAL.coral;
    heartPath(g, 80, 70, 52);
    g.fill();
    out.pin = tex(c);
  }
  {
    const { c, g } = canvas(220, 120);
    g.fillStyle = "rgba(42,27,61,0.16)";
    rr(g, 14, 20, 196, 92, 46);
    g.fill();
    g.fillStyle = "#FFFFFF";
    rr(g, 8, 8, 196, 92, 46);
    g.fill();
    g.fillStyle = PAL.coral;
    g.font = `900 56px ${FONT_D}`;
    g.textAlign = "center";
    g.textBaseline = "middle";
    g.fillText("+1", 106, 58);
    out.plus1 = tex(c);
  }
  {
    const { c, g } = canvas(300, 120);
    g.fillStyle = "rgba(42,27,61,0.16)";
    rr(g, 12, 18, 280, 96, 48);
    g.fill();
    g.fillStyle = PAL.teal;
    rr(g, 6, 6, 280, 96, 48);
    g.fill();
    g.fillStyle = "#FFFFFF";
    g.beginPath();
    g.arc(56, 54, 32, 0, TAU);
    g.fill();
    g.strokeStyle = PAL.teal;
    g.lineWidth = 9;
    g.lineCap = "round";
    g.lineJoin = "round";
    checkPath(g, 56, 54, 40, 1);
    g.stroke();
    g.fillStyle = "#FFFFFF";
    g.font = `800 46px ${FONT_D}`;
    g.textAlign = "left";
    g.textBaseline = "middle";
    g.fillText("Livré", 102, 57);
    out.delivered = tex(c);
  }
  {
    // compact delivered tick for wide shots
    const { c, g } = canvas(128, 128);
    g.fillStyle = "rgba(42,27,61,0.18)";
    g.beginPath();
    g.arc(68, 70, 54, 0, TAU);
    g.fill();
    g.fillStyle = PAL.teal;
    g.beginPath();
    g.arc(64, 64, 54, 0, TAU);
    g.fill();
    g.strokeStyle = "#FFFFFF";
    g.lineWidth = 13;
    g.lineCap = "round";
    g.lineJoin = "round";
    checkPath(g, 64, 66, 64, 1);
    g.stroke();
    out.tick = tex(c);
  }
  {
    const { c, g } = canvas(128, 128);
    g.fillStyle = PAL.coral;
    heartPath(g, 64, 66, 118);
    g.fill();
    g.fillStyle = "rgba(255,255,255,0.65)";
    g.beginPath();
    g.ellipse(42, 44, 10, 6, -0.6, 0, TAU);
    g.fill();
    out.heart = tex(c);
  }
  {
    const { c, g } = canvas(128, 128);
    const star = (col, r1, r2) => {
      g.fillStyle = col;
      g.beginPath();
      for (let i = 0; i < 8; i++) {
        const a = (i * Math.PI) / 4 - Math.PI / 2;
        const r = i % 2 ? r2 : r1;
        g.lineTo(64 + Math.cos(a) * r, 64 + Math.sin(a) * r);
      }
      g.closePath();
      g.fill();
    };
    star(PAL.sun, 62, 14);
    star("#FFFFFF", 30, 8);
    out.sparkle = tex(c);
  }
  {
    const { c, g } = canvas(160, 160);
    g.strokeStyle = PAL.ink;
    g.lineWidth = 6;
    g.lineCap = "round";
    g.fillStyle = PAL.sun;
    g.beginPath();
    g.moveTo(80, 28);
    g.bezierCurveTo(46, 30, 44, 70, 42, 96);
    g.lineTo(32, 112);
    g.lineTo(128, 112);
    g.lineTo(118, 96);
    g.bezierCurveTo(116, 70, 114, 30, 80, 28);
    g.closePath();
    g.fill();
    g.stroke();
    g.fillStyle = PAL.ink;
    g.beginPath();
    g.arc(80, 124, 11, 0, TAU);
    g.fill();
    g.beginPath();
    g.moveTo(16, 50);
    g.lineTo(28, 60);
    g.moveTo(10, 80);
    g.lineTo(26, 82);
    g.moveTo(144, 50);
    g.lineTo(132, 60);
    g.moveTo(150, 80);
    g.lineTo(134, 82);
    g.stroke();
    out.bell = tex(c);
  }
  {
    const { c, g } = canvas(128, 128);
    const gr = g.createRadialGradient(64, 64, 4, 64, 64, 62);
    gr.addColorStop(0, "rgba(255,255,255,1)");
    gr.addColorStop(0.55, "rgba(255,255,255,0.85)");
    gr.addColorStop(1, "rgba(255,255,255,0)");
    g.fillStyle = gr;
    g.beginPath();
    g.arc(64, 64, 62, 0, TAU);
    g.fill();
    out.puff = tex(c);
  }
  {
    const { c, g } = canvas(256, 256);
    g.strokeStyle = "#FFFFFF";
    g.lineWidth = 14;
    g.beginPath();
    g.arc(128, 128, 110, 0, TAU);
    g.stroke();
    out.ring = tex(c);
  }
  {
    const { c, g } = canvas(256, 256);
    const gr = g.createRadialGradient(128, 128, 0, 128, 128, 128);
    gr.addColorStop(0, "rgba(42,27,61,0.55)");
    gr.addColorStop(1, "rgba(42,27,61,0)");
    g.fillStyle = gr;
    g.fillRect(0, 0, 256, 256);
    out.blob = tex(c);
  }
  {
    // pointing hand (touch) icon
    const { c, g } = canvas(256, 320);
    g.save();
    g.translate(128, 150);
    g.rotate(-0.18);
    g.lineJoin = "round";
    g.lineCap = "round";
    const hand = () => {
      g.beginPath();
      g.moveTo(-18, -110);
      g.bezierCurveTo(-18, -136, 20, -136, 20, -110);
      g.lineTo(20, -30);
      g.bezierCurveTo(22, -46, 56, -46, 56, -24);
      g.bezierCurveTo(58, -38, 90, -36, 88, -12);
      g.bezierCurveTo(92, -22, 118, -18, 116, 6);
      g.lineTo(112, 64);
      g.bezierCurveTo(108, 110, 80, 130, 40, 130);
      g.lineTo(0, 130);
      g.bezierCurveTo(-30, 130, -46, 112, -58, 88);
      g.lineTo(-92, 26);
      g.bezierCurveTo(-104, 2, -76, -14, -58, 6);
      g.lineTo(-18, 40);
      g.closePath();
    };
    g.fillStyle = "rgba(42,27,61,0.25)";
    g.translate(10, 12);
    hand();
    g.fill();
    g.translate(-10, -12);
    g.fillStyle = "#FFFFFF";
    hand();
    g.fill();
    g.strokeStyle = PAL.ink;
    g.lineWidth = 9;
    hand();
    g.stroke();
    g.restore();
    out.hand = tex(c);
  }
  return out;
}

// ---------- the phone's shop UI ----------
// state: { press 0..1, done 0..1 (button → ordered), sheet 0..1, check 0..1, hover 0..1 }
export const UI = { W: 720, H: 1560, map: { x: 60, y: 480, w: 600, h: 1067 } };

export function drawPhoneUI(g, s) {
  const { W, H } = UI;
  g.clearRect(0, 0, W, H);
  g.fillStyle = "#FFF7F0";
  rr(g, 0, 0, W, H, 86);
  g.fill();
  g.save();
  rr(g, 0, 0, W, H, 86);
  g.clip();

  // status bar + island
  g.fillStyle = PAL.ink;
  g.font = `700 28px ${FONT_D}`;
  g.textBaseline = "middle";
  g.textAlign = "left";
  g.fillText("9:41", 70, 52);
  g.fillStyle = "#14101C";
  rr(g, 262, 24, 196, 54, 27);
  g.fill();
  g.strokeStyle = PAL.ink;
  g.lineWidth = 3;
  rr(g, 590, 40, 56, 26, 8);
  g.stroke();
  g.fillStyle = PAL.ink;
  rr(g, 595, 45, 40, 16, 4);
  g.fill();

  // header
  const av = g.createLinearGradient(40, 110, 130, 200);
  av.addColorStop(0, "#FF7A93");
  av.addColorStop(1, PAL.coralDeep);
  g.fillStyle = av;
  g.beginPath();
  g.arc(92, 156, 46, 0, TAU);
  g.fill();
  drawBikini2D(g, 92, 158, 62, "#FFFFFF", "#FFFFFF");
  g.fillStyle = PAL.ink;
  g.font = `800 34px ${FONT_D}`;
  g.fillText("@daya_na990", 156, 140);
  g.fillStyle = "#8A7F95";
  g.font = `500 22px ${FONT_D}`;
  g.fillText("Boutique · Bikinis", 158, 182);

  // product card
  const cx = 40,
    cy = 232,
    cw = 640,
    ch = 760;
  const pg = g.createLinearGradient(0, cy, 0, cy + ch);
  pg.addColorStop(0, "#5FDCD6");
  pg.addColorStop(1, "#18A9B4");
  g.fillStyle = pg;
  rr(g, cx, cy, cw, ch, 52);
  g.fill();
  g.save();
  rr(g, cx, cy, cw, ch, 52);
  g.clip();
  g.fillStyle = PAL.sun;
  g.beginPath();
  g.arc(cx + cw - 120, cy + 130, 78, 0, TAU);
  g.fill();
  g.strokeStyle = "rgba(255,255,255,0.45)";
  g.lineWidth = 10;
  for (let k = 0; k < 3; k++) {
    g.beginPath();
    for (let x = 0; x <= cw; x += 10) {
      const y = cy + ch - 150 + k * 46 + Math.sin(x / 48 + k) * 10;
      x === 0 ? g.moveTo(cx + x, y) : g.lineTo(cx + x, y);
    }
    g.stroke();
  }
  g.restore();
  drawBikini2D(g, cx + cw / 2, cy + ch / 2 + 10, 470);

  // title + options
  g.fillStyle = PAL.ink;
  g.font = `900 64px ${FONT_D}`;
  g.fillText("Bikini", 46, 1062);
  g.fillStyle = "#8A7F95";
  g.font = `500 26px ${FONT_D}`;
  g.fillText("Collection été", 48, 1116);
  g.fillStyle = PAL.coral;
  heartPath(g, 640, 1060, 64);
  g.fill();
  const sw = [PAL.coral, "#22B8C4", PAL.sun];
  sw.forEach((col, i) => {
    g.fillStyle = col;
    g.beginPath();
    g.arc(78 + i * 74, 1192, 26, 0, TAU);
    g.fill();
  });
  g.strokeStyle = PAL.ink;
  g.lineWidth = 4;
  g.beginPath();
  g.arc(78, 1192, 35, 0, TAU);
  g.stroke();
  ["S", "M", "L"].forEach((sz, i) => {
    const x = 390 + i * 100;
    g.fillStyle = sz === "M" ? PAL.ink : "#FFFFFF";
    rr(g, x, 1162, 82, 60, 30);
    g.fill();
    g.strokeStyle = PAL.ink;
    g.lineWidth = 3;
    rr(g, x, 1162, 82, 60, 30);
    g.stroke();
    g.fillStyle = sz === "M" ? "#FFFFFF" : PAL.ink;
    g.font = `800 28px ${FONT_D}`;
    g.textAlign = "center";
    g.fillText(sz, x + 41, 1194);
    g.textAlign = "left";
  });

  // CTA button: press squash, then morph to "Commandé"
  {
    const sc = 1 - 0.06 * s.press;
    const bw = 620 * sc,
      bh = 124 * sc;
    const bx = W / 2 - bw / 2,
      by = 1300 + (124 - bh) / 2;
    g.fillStyle = `rgba(226,58,92,${0.35 * (1 - s.press)})`;
    rr(g, bx, by + 14, bw, bh, bh / 2);
    g.fill();
    const col = s.done > 0.5 ? PAL.teal : s.press > 0.01 ? PAL.coralDeep : PAL.coral;
    g.fillStyle = col;
    rr(g, bx, by, bw, bh, bh / 2);
    g.fill();
    if (s.hover > 0) {
      g.strokeStyle = `rgba(255,79,112,${0.5 * s.hover})`;
      g.lineWidth = 8;
      rr(g, bx - 10, by - 10, bw + 20, bh + 20, bh / 2 + 10);
      g.stroke();
    }
    g.fillStyle = "#FFFFFF";
    g.textAlign = "center";
    g.font = `800 ${46 * sc}px ${FONT_D}`;
    if (s.done < 0.5) {
      g.globalAlpha = 1 - s.done * 2;
      g.fillText("Commander", W / 2, by + bh / 2 + 3);
    } else {
      g.globalAlpha = (s.done - 0.5) * 2;
      g.fillText("Commandé", W / 2 + 26, by + bh / 2 + 3);
      g.strokeStyle = "#FFFFFF";
      g.lineWidth = 9;
      g.lineCap = "round";
      g.lineJoin = "round";
      checkPath(g, W / 2 - 150, by + bh / 2, 46, (s.done - 0.5) * 2);
      g.stroke();
    }
    g.globalAlpha = 1;
    g.textAlign = "left";
  }

  // confirmation sheet slides up over the page
  if (s.sheet > 0) {
    const top = lerp(H + 20, 300, s.sheet);
    g.fillStyle = `rgba(42,27,61,${0.28 * s.sheet})`;
    g.fillRect(0, 0, W, H);
    g.fillStyle = "#FFFFFF";
    rr(g, 0, top, W, H - top + 120, 56);
    g.fill();
    g.fillStyle = "#E6DCE8";
    rr(g, W / 2 - 50, top + 18, 100, 10, 5);
    g.fill();
    const oy = top - 300;
    g.fillStyle = PAL.teal;
    g.beginPath();
    g.arc(110, 392 + oy, 50 * E.outBack(clamp(s.check * 1.6), 2.2), 0, TAU);
    g.fill();
    g.strokeStyle = "#FFFFFF";
    g.lineWidth = 10;
    g.lineCap = "round";
    g.lineJoin = "round";
    if (s.check > 0.35) {
      checkPath(g, 110, 392 + oy, 54, clamp((s.check - 0.35) / 0.65));
      g.stroke();
    }
    g.fillStyle = PAL.ink;
    g.font = `800 36px ${FONT_D}`;
    g.textBaseline = "middle";
    g.fillText("Commande confirmée !", 182, 376 + oy);
    g.fillStyle = "#8A7F95";
    g.font = `500 24px ${FONT_D}`;
    g.fillText("Suivi de ta livraison", 184, 420 + oy);
    const m = UI.map;
    g.fillStyle = "#BFEDEA";
    rr(g, m.x, m.y + oy, m.w, m.h, 26);
    g.fill();
  }
  g.restore();
}
