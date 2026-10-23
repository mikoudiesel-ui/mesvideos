#!/usr/bin/env python3
"""Intro animée KSC STUDIO (logo A · Objectif) : 3 s, 1080×1920, 30 i/s.

Écrit `index.html` (hôte), `compositions/ksc-logo.html` (logo vectorisé découpé en pièces animables :
K, S, objectif, lettres de STUDIO, recalculées à l'identique par brand/ksc-studio/tools/make_logos.py) et le son
`assets/audio/ksc-intro-son.wav` (bruitages et nappe synthétisés, −16 LUFS, crête ≤ −1 dBTP).

    python3 -I videos/ksc-studio-intro/tools/build_intro.py

Déroulé : l'objectif se dessine en grand et fait sa mise au point (bip-bip de l'autofocus), déclic
(flash, obturateur), l'objectif rejoint sa place dans le logo pendant que K et S arrivent, STUDIO se
resserre, étincelle et carillon à 1,9 s, puis le logo tient jusqu'à la fin.
"""

import importlib.util
import json
import math
import re
import subprocess
import wave
from pathlib import Path

import numpy as np
from scipy.signal import butter, fftconvolve, resample_poly, sosfilt

PROJECT = Path(__file__).resolve().parent.parent
REPO = PROJECT.parent.parent
spec = importlib.util.spec_from_file_location("make_logos", REPO / "brand/ksc-studio/tools/make_logos.py")
ml = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ml)

W, H, DUR = 1080, 1920, 3.0
LOGO_W = 780  # largeur finale du logo à l'écran (72 % du cadre)
HERO = (540, 880, 300)  # objectif en grand plan : centre x, y et rayon en px


# ------------------------------------------------------------------ logo découpé en pièces
def logo_parts():
    """Mêmes paramètres que make_logos.objectif_mark (version négatif), pièce par pièce."""
    f = ml.font("montserrat-800")
    F = 400.0
    word = ml.Line(f, "KSC", F, kern={"KS": -0.01, "SC": 0.035})
    word.place(left=0, baseline=0)
    cb = word.gbox(2)
    Ro = (cb[3] - cb[1]) / 2
    cx, cy = cb[0] + Ro, (cb[1] + cb[3]) / 2
    t = 0.19 * F
    lens, _ = ml.lens_c(0, 0, Ro, t, 78, ml.BLANC, ml.ORANGE, ml.NOIR, ml.BLANC)
    top = ml.union(word.gbox(0), word.gbox(1), (cx - Ro, cy - Ro, cx + Ro, cy + Ro))
    g = ml.font("montserrat-700")
    size = 0.36 * F
    st = ml.Line(g, "STUDIO", size, tracking=ml.fit(g, "STUDIO", size, top[2] - top[0]))
    st.place(left=top[0], top=top[3] + 0.17 * f.cap * F)
    box = ml.union(top, st.box)
    elems = re.findall(r"<[^>]+/>", lens)
    assert len(elems) == 5, elems  # anneau, verre, pupille, arc du reflet, point du reflet
    Ri = Ro - t
    Rl = Ri - 0.21 * t
    Rp = 0.46 * Rl
    rg = (Rl + Rp) / 2
    return {
        "k": word.path(only={0}), "s": word.path(only={1}), "kbox": word.gbox(0), "sbox": word.gbox(1),
        "studio": [(st.path(only={i}), st.gbox(i)) for i in range(6)],
        "lens": elems, "Ro": Ro, "t": t, "cx": cx, "cy": cy, "box": box,
        "ring_r": Ro - t / 2, "rg": rg, "glint_len": rg * math.radians(244 - 196),
    }


def build_html(parts):
    box = parts["box"]
    k = LOGO_W / (box[2] - box[0])
    tx = W / 2 - k * (box[0] + box[2]) / 2
    ty = H / 2 - k * (box[1] + box[3]) / 2
    Ro = parts["Ro"]
    Cx, Cy, rf = tx + k * parts["cx"], ty + k * parts["cy"], k * Ro
    half = 1.32 * Ro  # marge autour de l'objectif pour le flou et le reflet
    D = 2 * half * k
    ring, iris, pupil, glint, dot = parts["lens"]
    ring = ring.replace("<path ", '<path id="ring" mask="url(#ring-mask)" ', 1)
    iris = iris.replace("<circle ", '<circle id="iris" ', 1)
    pupil = pupil.replace("<circle ", '<circle id="pupil" ', 1)
    gl = parts["glint_len"]
    glint = glint.replace("<path ", f'<path id="glint" stroke-dasharray="{ml.n(gl)}" stroke-dashoffset="{ml.n(gl)}" opacity="0" ', 1)
    dot = dot.replace("<circle ", '<circle id="glint-dot" opacity="0" ', 1)
    rr = parts["ring_r"]
    ring_len = 2 * math.pi * rr
    studio_cx = (box[0] + box[2]) / 2
    letters = "".join(
        f'<path class="st" data-dx="{ml.n((gb[0] + gb[2]) / 2 - studio_cx)}" d="{d}" fill="{ml.ORANGE}"/>'
        for d, gb in parts["studio"])
    # K et S jaillissent du point du flash (x = HERO[0]) : départ à 60 % du trajet, en unités du logo
    kb, sb = parts["kbox"], parts["sbox"]
    k_from = 0.6 * (HERO[0] - (tx + k * (kb[0] + kb[2]) / 2)) / k
    s_from = 0.6 * (HERO[0] - (tx + k * (sb[0] + sb[2]) / 2)) / k
    params = {
        "heroX": round(HERO[0] - Cx, 2), "heroY": round(HERO[1] - Cy, 2), "heroScale": round(HERO[2] / rf, 4),
        "ringLen": round(ring_len, 2), "glintLen": round(gl, 2), "kFrom": round(k_from, 2), "sFrom": round(s_from, 2),
    }
    # l'étincelle brille dans le vide en haut à droite du C : sur le fond sombre, sans toucher le logo
    a, r = math.radians(-45), 1.5 * rf
    sparkle = (Cx + r * math.cos(a), Cy + r * math.sin(a))
    html = LOGO
    for key, val in {
        "__LOCKUP__": f"matrix({ml.n(k)} 0 0 {ml.n(k)} {ml.n(tx)} {ml.n(ty)})",
        "__K__": parts["k"], "__S__": parts["s"], "__STUDIO__": letters,
        "__LENS_LEFT__": ml.n(Cx - D / 2), "__LENS_TOP__": ml.n(Cy - D / 2), "__LENS_SIZE__": ml.n(D),
        "__LENS_VB__": f"{ml.n(-half)} {ml.n(-half)} {ml.n(2 * half)} {ml.n(2 * half)}",
        "__RING_R__": ml.n(rr), "__RING_W__": ml.n(parts["t"] * 1.3), "__RING_LEN__": ml.n(ring_len),
        "__RING__": ring, "__IRIS__": iris, "__PUPIL__": pupil, "__GLINT__": glint, "__DOT__": dot,
        "__HERO_X__": str(HERO[0]), "__HERO_Y__": str(HERO[1]),
        "__SPARK_X__": ml.n(sparkle[0]), "__SPARK_Y__": ml.n(sparkle[1]),
        "__PARAMS__": json.dumps(params),
    }.items():
        html = html.replace(key, val)
    assert "__" not in re.sub(r"__timelines|__hyperframes", "", html), "jeton non remplacé"
    (PROJECT / "compositions" / "ksc-logo.html").write_text(html)
    (PROJECT / "index.html").write_text(INDEX)
    return params


INDEX = """<!doctype html>
<html lang="fr">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
      * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
      }
      html,
      body {
        width: 1080px;
        height: 1920px;
        overflow: hidden;
        background: #111518;
      }
      #stage {
        position: relative;
        width: 1080px;
        height: 1920px;
        overflow: hidden;
        background: #111518;
      }
      #stage > div[data-composition-src] {
        position: absolute;
        inset: 0;
        pointer-events: none;
      }
    </style>
  </head>
  <body>
    <!-- KSC STUDIO, intro du logo A · Objectif : généré par tools/build_intro.py (1080×1920, 3 s, 30 i/s). -->
    <div id="stage" data-composition-id="main" data-start="0" data-duration="3" data-fps="30" data-width="1080" data-height="1920">
      <div id="el-logo" data-composition-id="ksc-logo" data-composition-src="compositions/ksc-logo.html"
        data-start="0" data-duration="3" data-track-index="1" data-width="1080" data-height="1920"></div>
      <div id="el-flash" data-composition-id="editorial-flash-overlay" data-composition-src="compositions/editorial-flash-overlay.html"
        data-start="0.17" data-duration="1" data-track-index="2" data-width="1080" data-height="1920"></div>
      <audio id="son" src="assets/audio/ksc-intro-son.wav" data-start="0" data-duration="3" data-track-index="10" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {};
      const tl = gsap.timeline({ paused: true });
      tl.to({}, { duration: 3 }, 0); // l'animation du logo vit dans compositions/ksc-logo.html
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""

LOGO = """<!doctype html>
<html lang="fr">
  <head>
    <meta charset="UTF-8" />
    <!-- HyperFrames ne monte que le contenu de <template> ; GSAP est chargé par index.html. -->
  </head>
  <body>
    <template>
      <style>
        #ksc-logo {
          position: absolute;
          inset: 0;
          width: 1080px;
          height: 1920px;
          overflow: hidden;
          background: #111518;
        }
        #cam {
          position: absolute;
          inset: 0;
          transform-origin: 540px 960px;
        }
        #glow {
          position: absolute;
          left: -160px;
          top: 260px;
          width: 1400px;
          height: 1400px;
          border-radius: 50%;
          background: radial-gradient(closest-side, rgba(255, 116, 31, 0.5), rgba(255, 116, 31, 0.12) 55%, rgba(255, 116, 31, 0));
          opacity: 0;
        }
        #vignette {
          position: absolute;
          inset: 0;
          background: radial-gradient(ellipse 75% 60% at 50% 48%, rgba(17, 21, 24, 0) 55%, rgba(5, 6, 8, 0.75) 100%);
        }
        #rings,
        #impact {
          position: absolute;
          left: 0;
          top: 0;
          width: 1080px;
          height: 1920px;
          opacity: 0;
          transform-origin: __HERO_X__px __HERO_Y__px;
        }
        #logo {
          position: absolute;
          left: 0;
          top: 0;
          width: 1080px;
          height: 1920px;
        }
        #lens-wrap {
          position: absolute;
          left: __LENS_LEFT__px;
          top: __LENS_TOP__px;
          width: __LENS_SIZE__px;
          height: __LENS_SIZE__px;
        }
        #lens-wrap svg {
          display: block;
          width: 100%;
          height: 100%;
          overflow: visible;
        }
        #sparkle {
          position: absolute;
          left: __SPARK_X__px;
          top: __SPARK_Y__px;
          width: 116px;
          height: 116px;
          margin: -58px 0 0 -58px;
          opacity: 0;
        }
      </style>
      <div id="ksc-logo" data-composition-id="ksc-logo" data-start="0" data-duration="3" data-width="1080" data-height="1920">
        <div id="cam">
          <div id="glow"></div>
          <svg id="rings" viewBox="0 0 1080 1920" aria-hidden="true">
            <circle cx="__HERO_X__" cy="__HERO_Y__" r="372" fill="none" stroke="#ffffff" stroke-opacity="0.1" stroke-width="2" />
            <circle cx="__HERO_X__" cy="__HERO_Y__" r="452" fill="none" stroke="#ffffff" stroke-opacity="0.06" stroke-width="2" />
            <circle cx="__HERO_X__" cy="__HERO_Y__" r="540" fill="none" stroke="#ffffff" stroke-opacity="0.035" stroke-width="2" />
          </svg>
          <svg id="impact" viewBox="0 0 1080 1920" aria-hidden="true">
            <circle cx="__HERO_X__" cy="__HERO_Y__" r="330" fill="none" stroke="#ff741f" stroke-width="10" />
          </svg>
          <svg id="logo" viewBox="0 0 1080 1920" aria-label="KSC STUDIO">
            <g id="lockup" transform="__LOCKUP__">
              <path id="k" d="__K__" fill="#ffffff" />
              <path id="s" d="__S__" fill="#ffffff" />
              <g id="studio">__STUDIO__</g>
            </g>
          </svg>
          <div id="lens-wrap">
            <svg viewBox="__LENS_VB__" aria-hidden="true">
              <defs>
                <mask id="ring-mask" maskUnits="userSpaceOnUse" x="-400" y="-400" width="800" height="800">
                  <circle id="ring-sweep" cx="0" cy="0" r="__RING_R__" fill="none" stroke="#ffffff" stroke-width="__RING_W__"
                    stroke-dasharray="__RING_LEN__" stroke-dashoffset="__RING_LEN__" transform="rotate(39)" />
                </mask>
              </defs>
              __RING__
              __IRIS__
              __PUPIL__
              __GLINT__
              __DOT__
            </svg>
          </div>
          <svg id="sparkle" viewBox="-60 -60 120 120" aria-hidden="true">
            <defs>
              <radialGradient id="spark-glow">
                <stop offset="0" stop-color="#ffffff" stop-opacity="0.6" />
                <stop offset="1" stop-color="#ffffff" stop-opacity="0" />
              </radialGradient>
            </defs>
            <circle r="40" fill="url(#spark-glow)" />
            <path d="M0,-58 C3.5,-13 13,-3.5 58,0 C13,3.5 3.5,13 0,58 C-3.5,13 -13,3.5 -58,0 C-13,-3.5 -3.5,-13 0,-58 Z" fill="#ffffff" />
          </svg>
          <div id="vignette"></div>
        </div>
      </div>
      <script>
        window.__timelines = window.__timelines || {};
        const P = __PARAMS__;
        const tl = gsap.timeline({ paused: true });
        const letters = gsap.utils.toArray("#studio .st");

        // 1. Lumière et anneaux de fond, puis l'anneau de l'objectif se dessine depuis l'ouverture du C.
        tl.fromTo("#glow", { opacity: 0, scale: 0.82 }, { opacity: 0.38, scale: 1, duration: 0.62, ease: "sine.out" }, 0.04);
        tl.fromTo("#rings", { opacity: 0, scale: 0.92 }, { opacity: 1, scale: 1, duration: 0.56, ease: "power1.out" }, 0.12);
        tl.fromTo("#ring-sweep", { attr: { "stroke-dashoffset": P.ringLen } }, { attr: { "stroke-dashoffset": 0 }, duration: 0.46, ease: "power2.inOut" }, 0.05);

        // 2. Mise au point : l'objectif sort du flou, l'iris s'ouvre, la pupille se règle.
        tl.fromTo("#lens-wrap", { filter: "blur(14px)" }, { filter: "blur(0px)", duration: 0.58, ease: "power3.out" }, 0.06);
        tl.fromTo("#iris", { scale: 0.35, opacity: 0, transformOrigin: "50% 50%" }, { scale: 1, opacity: 1, duration: 0.36, ease: "back.out(1.6)" }, 0.26);
        tl.fromTo("#pupil", { scale: 0.2, opacity: 0, transformOrigin: "50% 50%" }, { scale: 1, opacity: 1, duration: 0.3, ease: "circ.out" }, 0.34);

        // 3. Le reflet s'allume (bip-bip de l'autofocus dans le son).
        tl.fromTo("#glint", { attr: { "stroke-dashoffset": P.glintLen }, opacity: 0 }, { attr: { "stroke-dashoffset": 0 }, opacity: 1, duration: 0.14, ease: "power1.out" }, 0.6);
        tl.fromTo("#glint-dot", { scale: 0, opacity: 0, transformOrigin: "50% 50%" }, { scale: 1, opacity: 1, duration: 0.12, ease: "back.out(3)" }, 0.68);

        // 4. Déclic : le flash (compositions/editorial-flash-overlay.html) monte de 0,75 à 0,79 s ; sous le blanc,
        //    à 0,78 s, tout part de son centre : l'objectif file à sa place, l'onde de choc s'ouvre.
        tl.fromTo("#lens-wrap", { x: P.heroX, y: P.heroY, scale: P.heroScale }, { x: 0, y: 0, scale: 1, duration: 0.5, ease: "expo.out" }, 0.78);
        tl.to("#rings", { opacity: 0, scale: 1.18, duration: 0.24, ease: "power2.in" }, 0.78);
        tl.fromTo("#impact", { opacity: 0, scale: 0.62 }, { opacity: 0.9, scale: 0.62, duration: 0.02, ease: "none" }, 0.78);
        tl.to("#impact", { opacity: 0, scale: 1.75, duration: 0.5, ease: "expo.out" }, 0.8);
        tl.to("#glow", { opacity: 0.78, duration: 0.12, ease: "power4.out" }, 0.78);
        tl.to("#glow", { opacity: 0.46, duration: 0.7, ease: "sine.inOut" }, 0.93);

        // 5. K et S jaillissent du même point (K vers la gauche, S grandit), STUDIO s'élargit d'un souffle.
        tl.fromTo("#k", { x: P.kFrom, opacity: 0 }, { x: 0, opacity: 1, duration: 0.52, ease: "power4.out" }, 0.78);
        tl.fromTo("#s", { x: P.sFrom, scale: 0.72, opacity: 0, transformOrigin: "50% 50%" }, { x: 0, scale: 1, opacity: 1, duration: 0.46, ease: "power3.out" }, 0.8);
        letters.forEach(function (el) {
          const dx = parseFloat(el.getAttribute("data-dx"));
          tl.fromTo(el, { x: -0.3 * dx, opacity: 0 }, { x: 0, opacity: 1, duration: 0.6, ease: "power3.out" }, 1.0);
        });

        // 6. Respiration : lente poussée de caméra, étincelle au-dessus du C à 1,9 s, puis tenue.
        tl.fromTo("#cam", { scale: 1 }, { scale: 1.035, duration: 2.0, ease: "power1.inOut" }, 1.0);
        tl.fromTo("#sparkle", { scale: 0, rotation: -30, opacity: 0 }, { scale: 1, rotation: 0, opacity: 1, duration: 0.18, ease: "back.out(2)" }, 1.9);
        tl.to("#sparkle", { scale: 0, rotation: 30, opacity: 0, duration: 0.32, ease: "power2.in" }, 2.1);

        tl.to({}, { duration: 3 }, 0);
        window.__timelines["ksc-logo"] = tl;
        tl.seek(0);
      </script>
    </template>
  </body>
</html>
"""


# ------------------------------------------------------------------ son
SR = 48000
N = int(DUR * SR)
RNG = np.random.default_rng(20261021)


def tt(n):
    return np.arange(n) / SR


def filt(x, kind, f, order=2):
    return sosfilt(butter(order, f, btype=kind, fs=SR, output="sos"), x, axis=-1)


def add(bus, sig, at, gain=1.0, pan=0.0):
    a = (pan + 1) * math.pi / 4
    st = np.stack([sig * math.cos(a), sig * math.sin(a)]) * math.sqrt(2) if sig.ndim == 1 else sig
    i0 = int(round(at * SR))
    n = min(st.shape[1], bus.shape[1] - i0)
    if n > 0:
        bus[:, i0:i0 + n] += st[:, :n] * gain


def beep(f=2700, dur=0.045):
    n = int((dur + 0.01) * SR)
    t = tt(n)
    env = np.clip(t / 0.003, 0, 1) * np.clip((dur - t) / 0.004, 0, 1)
    return (np.sin(2 * np.pi * f * t) + 0.25 * np.sin(2 * np.pi * 2 * f * t)) * env


def click(vel=1.0):
    n = int(0.12 * SR)
    t = tt(n)
    snap = filt(RNG.standard_normal(n), "band", [1800, 7000]) * np.exp(-t / 0.006)
    body = np.sin(2 * np.pi * 880 * t) * np.exp(-t / 0.018) * 0.5
    thump = np.sin(2 * np.pi * np.cumsum(140 * (1 + np.exp(-t / 0.01))) / SR) * np.exp(-t / 0.035) * 0.7
    return (snap / (np.abs(snap).max() + 1e-9) + body + thump) * vel


def whir(dur=0.28):
    n = int(dur * SR)
    t = tt(n)
    f = 900 + 500 * t / dur
    buzz = np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * 0.25
    hiss = filt(RNG.standard_normal(n), "band", [3000, 9000]) * 0.4
    env = np.sin(np.pi * np.clip(t / dur, 0, 1)) ** 0.8
    return filt(buzz, "low", 4000) * env + hiss * env


def whoosh(dur, f0, f1):
    n = int(dur * SR)
    t = tt(n)
    src = RNG.standard_normal(n)
    out = np.zeros(n)
    blk = int(0.01 * SR)
    for b in range(n // blk + 1):
        fc = f0 * (f1 / f0) ** (b / max(1, n // blk))
        seg = src[b * blk:(b + 2) * blk]
        if len(seg) < 32:
            continue
        out[b * blk:b * blk + len(seg)] += filt(seg, "band", [fc / 1.5, min(fc * 1.5, 20000)]) * np.hanning(len(seg))
    env = np.sin(np.pi * np.clip(t / dur, 0, 1)) ** 1.5
    return out / (np.abs(out).max() + 1e-9) * env


def boom():
    n = int(0.9 * SR)
    t = tt(n)
    f = 46 + 50 * np.exp(-t / 0.08)
    return np.tanh(1.5 * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.32))


def midi(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def pad(notes, start, end, release):
    n = int((end - start + release) * SR)
    t = tt(n)
    out = np.zeros((2, n))
    for m in notes:
        for d, pan in ((-0.08, -0.7), (0.0, 0.0), (0.08, 0.7)):
            f = midi(m) * 2 ** (d / 12)
            ph = RNG.random()
            out[0] += (2 * ((f * t + ph) % 1.0) - 1) * math.cos((pan + 1) * math.pi / 4)
            out[1] += (2 * ((f * t + ph) % 1.0) - 1) * math.sin((pan + 1) * math.pi / 4)
    out = filt(out, "low", 1700)
    env = np.minimum(1, t / 0.35) ** 1.6 * np.clip(1 - (t - (end - start)) / release, 0, 1)
    return out * env / len(notes)


def celesta(m, dur=1.4):
    n = int(dur * SR)
    t = tt(n)
    f = midi(m)
    s = np.sin(2 * np.pi * f * t) * np.exp(-t / 0.7) + 0.32 * np.sin(2 * np.pi * 2 * f * t) * np.exp(-t / 0.3)
    s += 0.1 * np.sin(2 * np.pi * 3 * f * t) * np.exp(-t / 0.15)
    return s * (1 - np.exp(-t / 0.001))


def build_audio():
    bus = np.zeros((2, N))
    add(bus, whoosh(0.68, 400, 5000) * np.linspace(0.2, 1, int(0.68 * SR)), 0.06, 0.16)  # montée vers le déclic
    add(bus, whir(0.26), 0.3, 0.1, 0.2)  # moteur d'autofocus
    for at in (0.62, 0.7):
        add(bus, beep(), at, 0.12, -0.15)  # bip-bip de confirmation
    add(bus, click(1.0), 0.75, 0.7)  # miroir
    add(bus, click(0.75), 0.785, 0.6, 0.1)  # obturateur
    add(bus, whoosh(0.34, 3200, 500), 0.77, 0.3)  # l'objectif rejoint le logo
    add(bus, boom(), 0.785, 0.55)
    add(bus, pad([53, 57, 60, 64, 67], 0.82, 2.55, 0.4), 0.82, 0.55)  # Fa majeur 9, chaud
    for k, m in enumerate((89, 93, 96)):  # carillon sur l'étincelle (fa, la, do)
        add(bus, celesta(m), 1.88 + 0.05 * k, 0.16, -0.3 + 0.3 * k)
    ir_n = int(0.9 * SR)
    ir = RNG.standard_normal((2, ir_n)) * np.exp(-6.9 * tt(ir_n) / 0.8)
    ir = filt(ir, "low", 6000) / np.sqrt(np.sum(ir ** 2) / 2)
    wet = np.stack([fftconvolve(bus.mean(axis=0), ir[c])[:N] for c in range(2)]) * 0.12
    mix = bus + wet
    fade = np.clip((DUR - 0.03 - tt(N)) / 0.3, 0, 1) ** 1.5  # silence propre sur la dernière image
    mix *= fade
    return mix


def true_peak_limit(x, ceiling_db=-1.5):
    ceiling = 10 ** (ceiling_db / 20)
    over = np.abs(resample_poly(x, 4, 1, axis=1)).max(axis=0).reshape(-1, 4).max(axis=1)[: x.shape[1]]
    need = np.minimum(1.0, ceiling / np.maximum(over, 1e-9))
    k = int(0.003 * SR)
    smooth = -np.convolve(np.pad(-need, (k, k), mode="edge"), np.ones(2 * k + 1) / (2 * k + 1), "valid")
    g = np.minimum(need, np.minimum.reduce([np.roll(need, s) for s in range(-k, k + 1)]))
    return x * np.minimum(g, smooth)


def loudness(path):
    out = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-af", "ebur128=peak=true", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    s = out[out.rfind("Summary:"):]
    return float(re.search(r"I:\s+(-?[\d.]+) LUFS", s).group(1)), float(re.search(r"Peak:\s+(-?[\d.]+) dBFS", s).group(1))


def write_wav(path, x):
    pcm = (np.clip(x, -1, 1).T * 32767).round().astype(np.int16)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())


def main():
    params = build_html(logo_parts())
    mix = build_audio()
    out = PROJECT / "assets" / "audio" / "ksc-intro-son.wav"
    out.parent.mkdir(parents=True, exist_ok=True)
    gain = 0.5 / (np.abs(mix).max() + 1e-9)
    for _ in range(5):
        y = true_peak_limit(mix * gain)
        write_wav(out, y)
        i, tp = loudness(out)
        if abs(i + 16) < 0.3:
            break
        gain *= 10 ** ((-16 - i) / 20)
    print("index.html et compositions/ksc-logo.html écrits", params)
    print(f"son : {out.name} {i:.1f} LUFS, crête vraie {tp:.1f} dBTP")


if __name__ == "__main__":
    main()
