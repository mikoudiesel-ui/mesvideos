// Pure helpers shared by the world: math, easing, seeded randomness, time windows.
// Everything here is deterministic — the frame at time t is a pure function of t.

export const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
export const lerp = (a, b, t) => a + (b - a) * t;
export const inv = (a, b, x) => clamp((x - a) / (b - a));
export const smooth = (x) => x * x * (3 - 2 * x);
export const TAU = Math.PI * 2;
export const DEG = Math.PI / 180;

// GSAP-equivalent ease family (power1 = quad … power4 = quint).
export const E = {
  linear: (t) => t,
  in2: (t) => t * t,
  out2: (t) => 1 - (1 - t) * (1 - t),
  inOut2: (t) => (t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2),
  in3: (t) => t * t * t,
  out3: (t) => 1 - Math.pow(1 - t, 3),
  inOut3: (t) => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2),
  out4: (t) => 1 - Math.pow(1 - t, 4),
  inOut4: (t) => (t < 0.5 ? 8 * t * t * t * t : 1 - Math.pow(-2 * t + 2, 4) / 2),
  out5: (t) => 1 - Math.pow(1 - t, 5),
  inOut5: (t) => (t < 0.5 ? 16 * Math.pow(t, 5) : 1 - Math.pow(-2 * t + 2, 5) / 2),
  inOutSine: (t) => -(Math.cos(Math.PI * t) - 1) / 2,
  outSine: (t) => Math.sin((t * Math.PI) / 2),
  outBack: (t, s = 1.70158) => 1 + (s + 1) * Math.pow(t - 1, 3) + s * Math.pow(t - 1, 2),
  inBack: (t, s = 1.70158) => (s + 1) * t * t * t - s * t * t,
  outElastic: (t) => {
    if (t === 0 || t === 1) return t;
    return Math.pow(2, -10 * t) * Math.sin((t * 10 - 0.75) * ((2 * Math.PI) / 3)) + 1;
  },
};
export const back = (s) => (t) => E.outBack(t, s);

// Progress of t through [a,b] with an ease.
export const seg = (t, a, b, ease = E.linear) => ease(inv(a, b, t));

// Attack / hold / release envelope: 0 before a, ramps to 1 by a+ain, holds, falls to 0 at b.
export const env = (t, a, b, ain = 0.2, aout = 0.2, easeIn = E.out3, easeOut = E.in2) => {
  if (t <= a || t >= b) return 0;
  if (t < a + ain) return easeIn(inv(a, a + ain, t));
  if (t > b - aout) return 1 - easeOut(inv(b - aout, b, t));
  return 1;
};

// Spring-pop scale: 0 → 1 with overshoot, starting at a, lasting d.
export const pop = (t, a, d = 0.45, s = 2.2) => (t <= a ? 0 : t >= a + d ? 1 : E.outBack(inv(a, a + d, t), s));

// Deterministic PRNG (mulberry32).
export function rng(seed) {
  let a = seed >>> 0;
  return () => {
    a |= 0;
    a = (a + 0x6d2b79f5) | 0;
    let r = Math.imul(a ^ (a >>> 15), 1 | a);
    r = (r + Math.imul(r ^ (r >>> 7), 61 | r)) ^ r;
    return ((r ^ (r >>> 14)) >>> 0) / 4294967296;
  };
}

// Piecewise keyframe track: keys = [[t, value], ...]; value may be a number or array.
// Each key may carry an ease used for the segment that ARRIVES at it.
export function track(keys) {
  return (t) => {
    if (t <= keys[0][0]) return keys[0][1];
    for (let i = 1; i < keys.length; i++) {
      const [t1, v1, ease = E.inOut3] = keys[i];
      if (t <= t1) {
        const [t0, v0] = keys[i - 1];
        const p = ease(inv(t0, t1, t));
        if (Array.isArray(v0)) return v0.map((x, j) => lerp(x, v1[j], p));
        return lerp(v0, v1, p);
      }
    }
    return keys[keys.length - 1][1];
  };
}

// Parabolic hop between two points (arrays [x,y,z]) with an apex height.
export function hop(p0, p1, h, p) {
  const x = lerp(p0[0], p1[0], p);
  const z = lerp(p0[2], p1[2], p);
  const y = lerp(p0[1], p1[1], p) + 4 * h * p * (1 - p);
  return [x, y, z];
}
