#!/usr/bin/env python3
"""Soundtrack for the daya_na990 isometric delivery ad.

Synthesises a 120 BPM tropical-house bed whose bar lines land on the film's cuts
(bars start at 0.6 s + 2 s·k), then mixes sound effects on the exact animation
times used in assets/js/world.js and index.html. Bundled HyperFrames SFX (resolved
into .media/ with provenance) are layered with locally synthesised foley.

Usage:  python3 tools/make_soundtrack.py   →  assets/audio/soundtrack.wav
"""
import math
import os
import subprocess
import wave

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SR = 48000
DUR = 40.0
N = int(SR * DUR)
RNG = np.random.default_rng(20261009)

BAR0, BEAT = 0.6, 0.5


def bar(b, k=0.0):
    return BAR0 + 2.0 * b + BEAT * k


def midi(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def tt(n):
    return np.arange(n) / SR


# ------------------------------------------------------------------ buses
class Bus:
    def __init__(self):
        self.x = np.zeros((2, N))

    def add(self, sig, at, gain=1.0, pan=0.0):
        if sig.ndim == 1:
            a = (pan + 1) * math.pi / 4
            sig = np.stack([sig * math.cos(a), sig * math.sin(a)]) * math.sqrt(2)
        i0 = int(round(at * SR))
        s0 = 0
        if i0 < 0:
            s0, i0 = -i0, 0
        n = min(sig.shape[1] - s0, N - i0)
        if n > 0:
            self.x[:, i0 : i0 + n] += sig[:, s0 : s0 + n] * gain


def fft_band(x, lo=None, hi=None, order=4):
    n = x.shape[-1]
    X = np.fft.rfft(x, axis=-1)
    f = np.fft.rfftfreq(n, 1 / SR)
    g = np.ones_like(f)
    if hi:
        g *= 1 / np.sqrt(1 + (f / hi) ** (2 * order))
    if lo:
        g *= 1 / np.sqrt(1 + (lo / np.maximum(f, 1e-3)) ** (2 * order))
    return np.fft.irfft(X * g, n=n, axis=-1)


def onepole_var(x, fc):
    """Time-varying one-pole low-pass (short signals only)."""
    y = np.zeros_like(x)
    acc = 0.0
    k = 1 - np.exp(-2 * np.pi * np.asarray(fc) / SR)
    for i in range(len(x)):
        acc += k[i] * (x[i] - acc)
        y[i] = acc
    return y


def noise(n):
    return RNG.standard_normal(n)


def resample(x, ratio):
    """Speed/pitch change by ratio (>1 = higher & shorter)."""
    if x.ndim == 1:
        x = x[None, :]
    n = x.shape[1]
    m = int(n / ratio)
    src = np.arange(m) * ratio
    return np.stack([np.interp(src, np.arange(n), ch) for ch in x])


def load(path):
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", path, "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"],
        check=True,
        capture_output=True,
    ).stdout
    return np.frombuffer(raw, dtype=np.float32).reshape(-1, 2).T.astype(np.float64)


def peak_time(x, win=0.05):
    m = np.abs(x).mean(axis=0)
    w = int(win * SR)
    env = np.convolve(m, np.ones(w) / w, mode="same")
    return int(np.argmax(env)) / SR


# ------------------------------------------------------------------ instruments
def kick():
    n = int(0.42 * SR)
    t = tt(n)
    f = 46 + 110 * np.exp(-t / 0.032)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.26)
    click = fft_band(noise(n), lo=1500, hi=6000) * np.exp(-t / 0.004) * 0.35
    return np.tanh(1.8 * (s + click)) * 0.95


def clap():
    n = int(0.35 * SR)
    t = tt(n)
    env = np.zeros(n)
    for d in (0.0, 0.011, 0.022):
        i = int(d * SR)
        env[i:] += np.exp(-(t[: n - i]) / 0.008)
    env += 0.55 * np.exp(-t / 0.11) * (t > 0.03)
    return fft_band(noise(n), lo=900, hi=4200) * env * 0.55


def hat(open_=False):
    n = int((0.18 if open_ else 0.05) * SR)
    t = tt(n)
    return fft_band(noise(n), lo=7000) * np.exp(-t / (0.07 if open_ else 0.014)) * 0.3


def shaker():
    n = int(0.09 * SR)
    t = tt(n)
    env = (1 - np.exp(-t / 0.006)) * np.exp(-t / 0.03)
    return fft_band(noise(n), lo=4500, hi=12000) * env * 0.35


def pluck(m, dur=0.45, bright=1.0):
    n = int(dur * SR)
    t = tt(n)
    f = midi(m)
    a = 1 - np.exp(-t / 0.0015)
    s = np.sin(2 * np.pi * f * t) * np.exp(-t / 0.32)
    s += 0.32 * bright * np.sin(2 * np.pi * 4 * f * t) * np.exp(-t / 0.045)
    s += 0.18 * np.sin(2 * np.pi * 2 * f * t) * np.exp(-t / 0.12)
    return s * a * 0.32


def steelpan(m, dur=0.6):
    n = int(dur * SR)
    t = tt(n)
    f = midi(m) * (1 + 0.003 * np.sin(2 * np.pi * 5.5 * t))
    ph = 2 * np.pi * np.cumsum(f) / SR
    s = np.sin(ph) * np.exp(-t / 0.55) + 0.55 * np.sin(2 * ph) * np.exp(-t / 0.28) + 0.3 * np.sin(3 * ph + 0.4) * np.exp(-t / 0.12)
    return s * (1 - np.exp(-t / 0.003)) * 0.26


def bassnote(m, dur):
    n = int(dur * SR)
    t = tt(n)
    f = midi(m)
    env = (1 - np.exp(-t / 0.004)) * np.minimum(1, (dur - t) / 0.04).clip(0, 1) * (0.75 + 0.25 * np.exp(-t / 0.08))
    s = np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * 2 * f * t) + 0.12 * np.sin(2 * np.pi * 3 * f * t)
    return np.tanh(1.3 * s) * env * 0.42


def pad(notes, dur):
    n = int(dur * SR)
    t = tt(n)
    out = np.zeros((2, n))
    for m in notes:
        for det, pan in ((-0.07, -0.6), (0.0, 0.0), (0.07, 0.6)):
            f = midi(m) * 2 ** (det / 12)
            saw = 2 * ((f * t + RNG.random()) % 1.0) - 1
            a = (pan + 1) * math.pi / 4
            out[0] += saw * math.cos(a)
            out[1] += saw * math.sin(a)
    env = np.minimum(1, t / 0.35) * np.minimum(1, (dur - t) / 0.4).clip(0, 1)
    return out * env * 0.035


def bell(f0, dur=1.6, gain=0.3):
    n = int(dur * SR)
    t = tt(n)
    s = np.zeros(n)
    for ratio, amp, dec in ((1, 1, 0.9), (2.0, 0.45, 0.5), (2.76, 0.35, 0.35), (5.4, 0.2, 0.15), (8.9, 0.08, 0.08)):
        s += amp * np.sin(2 * np.pi * f0 * ratio * t) * np.exp(-t / dec)
    return s * (1 - np.exp(-t / 0.002)) * gain


def riser(dur, f0=200, f1=1800, gain=0.5):
    n = int(dur * SR)
    t = tt(n)
    p = t / dur
    nz = onepole_var(noise(n), 300 + 9000 * p ** 2)
    sweep = np.sin(2 * np.pi * np.cumsum(f0 * (f1 / f0) ** p) / SR) * 0.25
    return (nz * 0.9 + sweep) * p ** 2.2 * gain


def thud(f=170, dur=0.16, gain=0.6, nz=0.5):
    n = int(dur * SR)
    t = tt(n)
    f_ = f * (1 + 0.6 * np.exp(-t / 0.01))
    s = np.sin(2 * np.pi * np.cumsum(f_) / SR) * np.exp(-t / (dur / 4))
    s += fft_band(noise(n), lo=120, hi=900) * np.exp(-t / 0.02) * nz
    return np.tanh(1.5 * s) * gain


def rustle(dur=0.25, gain=0.25):
    n = int(dur * SR)
    t = tt(n)
    am = (np.abs(noise(n)) > 1.2).astype(float)
    am = np.convolve(am, np.ones(240) / 240, mode="same")
    return fft_band(noise(n), lo=2500, hi=9000) * (0.35 + am) * np.sin(np.pi * t / dur) * gain


def tape_rip(dur=0.42, gain=0.45):
    n = int(dur * SR)
    t = tt(n)
    crackle = (np.sin(2 * np.pi * np.cumsum(90 + 160 * t / dur) / SR) > 0.2).astype(float)
    crackle = np.convolve(crackle, np.ones(60) / 60, mode="same")
    nz = onepole_var(noise(n), 1500 + 5000 * t / dur)
    nz = nz - onepole_var(nz, np.full(n, 600.0))
    return nz * (0.3 + 0.7 * crackle) * np.sin(np.pi * np.minimum(1, t / dur * 1.15)).clip(0) * gain * 3


def boing(f0=240, f1=520, dur=0.28, gain=0.3):
    n = int(dur * SR)
    t = tt(n)
    f = f0 + (f1 - f0) * (1 - np.exp(-t / 0.05))
    f = f * (1 + 0.04 * np.sin(2 * np.pi * 22 * t))
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.09) * gain


def horn(f=415, dur=0.16, gain=0.32):
    n = int(dur * SR)
    t = tt(n)
    s = sum(np.sin(2 * np.pi * f * k * t) / k for k in (1, 3, 5, 7))
    s += 0.6 * sum(np.sin(2 * np.pi * f * 1.26 * k * t) / k for k in (1, 3, 5))
    env = np.minimum(1, t / 0.01) * np.minimum(1, (dur - t) / 0.03).clip(0, 1)
    return fft_band(np.tanh(s), hi=2600) * env * gain


def engine(dur=0.9, rev=1.0, gain=0.35):
    n = int(dur * SR)
    t = tt(n)
    f = 52 + 70 * rev * np.minimum(1, t / (dur * 0.7))
    ph = 2 * np.pi * np.cumsum(f) / SR
    putter = 0.6 + 0.4 * np.sign(np.sin(2 * np.pi * 16 * t))
    s = (np.sin(ph) + 0.5 * np.sin(2 * ph) + 0.3 * fft_band(noise(n), hi=400)) * putter
    env = np.minimum(1, t / 0.05) * np.minimum(1, (dur - t) / 0.3).clip(0, 1)
    return fft_band(np.tanh(1.4 * s), hi=900) * env * gain


def squeak(dur=0.2, gain=0.08):
    n = int(dur * SR)
    t = tt(n)
    f = 2300 - 500 * t / dur + 60 * np.sin(2 * np.pi * 30 * t)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * t / dur) * gain


def step(gain=0.12):
    n = int(0.05 * SR)
    t = tt(n)
    return fft_band(noise(n), lo=150, hi=1400) * np.exp(-t / 0.012) * gain


def waves(dur, gain=0.18):
    n = int(dur * SR)
    t = tt(n)
    swell = 0.55 + 0.45 * np.sin(2 * np.pi * t / 3.2 - 1.2) ** 2
    s = np.stack([fft_band(noise(n), lo=120, hi=1600), fft_band(noise(n), lo=120, hi=1600)])
    fade = np.minimum(1, t / 1.0) * np.minimum(1, (dur - t) / 1.0).clip(0, 1)
    return s * swell * fade * gain


def crash(dur=2.2, gain=0.22):
    n = int(dur * SR)
    t = tt(n)
    s = np.stack([fft_band(noise(n), lo=3500), fft_band(noise(n), lo=3500)])
    return s * np.exp(-t / 0.7) * (1 - np.exp(-t / 0.002)) * gain


# ------------------------------------------------------------------ van path (mirrors world.js)
def van_toss_times():
    corners = [(-4.4, 0), (10.6, 0), (10.6, 10.6), (0, 10.6), (0, 0), (10.6, 0), (10.6, -8.9)]
    R, lane = 1.5, 0.55
    P = [np.array(c, float) for c in corners]
    raw = [P[0]]
    for i in range(1, len(P) - 1):
        a = (P[i] - P[i - 1]) / np.linalg.norm(P[i] - P[i - 1])
        b = (P[i + 1] - P[i]) / np.linalg.norm(P[i + 1] - P[i])
        s0, s1 = P[i] - a * R, P[i] + b * R
        raw.append(s0)
        for k in range(1, 12):
            u = k / 12
            raw.append((1 - u) ** 2 * s0 + 2 * (1 - u) * u * P[i] + u * u * s1)
        raw.append(s1)
    raw.append(P[-1])
    dense = []
    for i in range(len(raw) - 1):
        a, b = raw[i], raw[i + 1]
        n = max(1, math.ceil(np.linalg.norm(b - a) / 0.5))
        for k in range(n):
            dense.append(a + (b - a) * k / n)
    dense.append(raw[-1])
    pts = []
    for i, p in enumerate(dense):
        q = dense[min(i + 1, len(dense) - 1)]
        o = dense[max(i - 1, 0)]
        tg = (q - o) / np.linalg.norm(q - o)
        pts.append(np.array([p[0] - tg[1] * lane, p[1] + tg[0] * lane]))
    cum = [0.0]
    for i in range(1, len(pts)):
        cum.append(cum[-1] + float(np.linalg.norm(pts[i] - pts[i - 1])))

    def nearest(x, z, min_s=-1.0):
        d = [((p[0] - x) ** 2 + (p[1] - z) ** 2) if cum[i] >= min_s else 1e9 for i, p in enumerate(pts)]
        return cum[int(np.argmin(d))]

    sB = nearest(2.14 + 3.4, 10.05)
    sEnd = cum[-1]
    sS1 = nearest(0.55, 5.504, sB)
    sN1 = nearest(3.552, 0.55, sB)

    def inout2(u):
        return 2 * u * u if u < 0.5 else 1 - (-2 * u + 2) ** 2 / 2

    def time_at(s, a=28.7, b=31.4):
        lo, hi = a, b
        for _ in range(40):
            m = (lo + hi) / 2
            if sB + (sEnd - sB) * inout2((m - a) / (b - a)) < s:
                lo = m
            else:
                hi = m
        return (lo + hi) / 2

    return {"S1": time_at(sS1), "N1": time_at(sN1), "N2": 31.35}


# ------------------------------------------------------------------ compose
def main():
    music, drums, bass, chords, lead, sfx, send = (Bus() for _ in range(7))
    med = os.path.join(ROOT, ".media", "audio", "sfx")
    S = {k: load(os.path.join(med, f"{k}.mp3")) for k in ("sfx_001", "sfx_002", "sfx_003", "sfx_004", "sfx_005", "sfx_006", "sfx_007", "sfx_008", "sfx_009", "sfx_010", "sfx_011")}
    WHOOSH_CINE, POP, SPARKLE, CHIME, IMPACT, RISER, CLICK, WHOOSH, NOTIF, PING, WHOOSH2 = (S[k] for k in sorted(S))

    A = ([57, 61, 64], 45)
    Emaj = ([56, 59, 64], 40)
    Fm = ([57, 61, 66], 42)
    D = ([57, 62, 66], 38)
    PROG = [A, Emaj, Fm, D]
    MEL = [
        [(0, 76, 0.5), (0.75, 73, 0.5), (1.5, 76, 0.5), (2.0, 78, 0.75), (3.0, 76, 0.5), (3.5, 73, 0.5)],
        [(0, 71, 0.75), (1.0, 73, 0.5), (1.5, 71, 0.5), (2.0, 68, 1.0), (3.5, 71, 0.5)],
        [(0, 73, 0.5), (0.75, 69, 0.5), (1.5, 73, 0.5), (2.0, 76, 0.75), (3.0, 78, 0.5), (3.5, 76, 0.5)],
        [(0, 78, 0.75), (1.0, 76, 0.5), (1.5, 74, 0.5), (2.0, 73, 1.0), (3.0, 71, 0.5), (3.5, 73, 0.5)],
    ]
    PLUCK_RHYTHM = [0, 0.75, 1.5, 2.5, 3.0]

    kick_s, clap_s = kick(), clap()
    kicks = []

    def section(b):
        if b < 2:
            return "intro"
        if b < 5:
            return "dropA"
        if b < 8:
            return "verse"
        if b == 8:
            return "build"
        if b < 16:
            return "dropB"
        if b < 18:
            return "beach"
        if b == 18:
            return "final"
        return "end"

    # pickup chord before the first downbeat (phone flies in)
    for m in Emaj[0]:
        chords.add(pluck(m + 12, 0.6, 0.6), 0.1, 0.5)
    for b in range(-1, 20):
        sec = section(max(b, 0)) if b >= 0 else "pre"
        notes, root = PROG[b % 4]
        t0 = bar(b)
        if sec == "pre":
            continue
        # pad underneath everything except the final tail
        pd = pad(notes, 2.25 if sec != "end" else 1.45)
        chords.add(pd, t0, 1.0 if sec in ("beach", "intro") else 0.75)
        send.add(pd, t0, 0.25)
        # plucks
        if sec != "end":
            br = 0.5 if sec in ("intro", "beach") else 1.0
            for k in PLUCK_RHYTHM:
                if sec == "beach" and k not in (0, 1.5, 3.0):
                    continue
                for j, m in enumerate(notes):
                    p = pluck(m + 12, 0.5, br)
                    chords.add(p, t0 + k * BEAT, 0.8 if sec != "intro" else 0.6, pan=(j - 1) * 0.35)
                    send.add(p, t0 + k * BEAT, 0.22)
        else:
            for j, m in enumerate(notes + [notes[0] + 12]):
                p = pluck(m + 12, 1.4, 1.0)
                chords.add(p, t0, 0.9, pan=(j - 1.5) * 0.3)
                send.add(p, t0, 0.35)
        # drums
        if sec in ("dropA", "verse", "dropB", "final", "build"):
            for k in range(4):
                if sec == "build" and k == 3:
                    continue
                drums.add(kick_s, t0 + k * BEAT, 0.95)
                kicks.append(t0 + k * BEAT)
            if sec != "build":
                for k in (1, 3):
                    drums.add(clap_s, t0 + k * BEAT, 0.7)
                    send.add(clap_s, t0 + k * BEAT, 0.25)
            for k in range(8):
                drums.add(hat(open_=(k % 2 == 1 and sec in ("dropB", "final"))), t0 + k * BEAT / 2, 0.55 if k % 2 else 0.3, pan=0.3)
            for k in range(16):
                drums.add(shaker(), t0 + k * BEAT / 4, 0.5 if k % 4 == 2 else 0.25, pan=-0.35)
        if sec in ("intro", "beach"):
            for k in range(8):
                drums.add(shaker(), t0 + k * BEAT / 2, 0.35 if k % 2 else 0.18, pan=-0.3)
        if sec == "build":
            # clap roll, 8ths then 16ths, then a breath for the horn
            for k in range(4):
                drums.add(clap_s, t0 + k * BEAT / 2, 0.35 + 0.05 * k)
        # bass: house off-beat eighths with a pickup
        if sec in ("dropA", "verse", "dropB", "final"):
            for k in range(4):
                bass.add(bassnote(root, 0.22), t0 + k * BEAT + BEAT / 2, 1.0)
            bass.add(bassnote(root + 12, 0.12), t0 + 3.75 * BEAT, 0.7)
        # lead melody
        if sec in ("dropB", "final") or (sec == "verse" and b >= 6):
            g = 0.9 if sec != "verse" else 0.45
            for (k, m, d) in MEL[b % 4]:
                s_ = steelpan(m, max(0.35, d * BEAT * 2.2))
                lead.add(s_, t0 + k * BEAT, g, pan=0.15)
                send.add(s_, t0 + k * BEAT, 0.3)
                # dotted-eighth echo
                lead.add(s_ * 0.35, t0 + k * BEAT + 0.375, g, pan=-0.5)
                lead.add(s_ * 0.15, t0 + k * BEAT + 0.75, g, pan=0.5)

    # build-up snare roll (16ths) into the horn gap, plus a riser
    for k in range(4):
        drums.add(clap_s, bar(8, 2) + k * BEAT / 4, 0.35 + 0.08 * k)
    drums.add(riser(1.4, 200, 2600, 0.3), 16.7, 1.0)
    # sidechain pump from every kick
    duck = np.ones(N)
    L = int(0.32 * SR)
    shape = 1 - 0.55 * np.exp(-tt(L) / 0.09) * (1 - np.exp(-tt(L) / 0.003))
    for k in kicks:
        i = int(k * SR)
        n = min(L, N - i)
        duck[i : i + n] = np.minimum(duck[i : i + n], shape[:n])
    chords.x *= duck
    bass.x *= duck

    # final fade
    fade = np.ones(N)
    i0 = int(39.2 * SR)
    fade[i0:] = np.linspace(1, 0, N - i0) ** 1.5
    music.x = (drums.x * 0.78 + fft_band(bass.x, hi=900) * 0.72 + fft_band(chords.x, hi=5200) * 0.7 + lead.x * 0.9)

    # ------------------------------------------------ SFX on picture
    def put(sig, at, gain, pan=0.0, rev=0.0):
        sfx.add(sig, at, gain, pan)
        if rev:
            send.add(sig, at, gain * rev, pan)

    put(WHOOSH, 0.0, 0.55)
    for a in (0.32, 0.48, 7.07, 7.23, 11.17, 11.33, 14.22, 14.38, 18.27, 18.43, 20.87, 21.03, 27.57, 27.73, 32.87, 33.03):
        put(resample(POP, 1.2), a, 0.22, pan=-0.2)
    put(resample(WHOOSH2, 1.2), 1.05, 0.25, pan=0.3)
    put(CLICK, 2.09, 0.9)
    put(thud(140, 0.12, 0.25, 0.2), 2.1, 1.0)
    put(NOTIF, 2.3, 0.65, rev=0.2)
    put(resample(WHOOSH2, 1.1), 2.52, 0.3)
    put(resample(POP, 1.3), 2.88, 0.45)
    put(SPARKLE, 2.95, 0.3, rev=0.3)
    # dive into the phone: riser + cinematic whoosh cresting on the match cut
    put(riser(1.05, 300, 2400, 0.5), 3.55, 1.0)
    pk = peak_time(WHOOSH_CINE)
    put(WHOOSH_CINE, 4.6 - pk, 0.75)
    put(IMPACT, 4.6, 0.85, rev=0.2)
    put(crash(1.6, 0.12), 4.6, 1.0)
    # orders pop up over the houses
    for i, a in enumerate((7.15, 7.45, 7.75, 8.05)):
        put(resample(POP, 1.0 + 0.12 * i), a, 0.55, pan=(-0.4 + 0.27 * i))
        put(pluck(81 + [0, 4, 7, 12][i], 0.6, 1.0), a, 0.9, rev=0.4)
        put(resample(PING, 1.6), a + 0.12, 0.1)
    # into the shop
    put(WHOOSH, 10.42, 0.5)
    put(boing(500, 900, 0.5, 0.12), 10.48, 1.0)
    put(resample(WHOOSH_CINE, 1.5), 10.55, 0.3)
    put(thud(70, 0.4, 0.3, 0.8), 11.1, 1.0)
    put(SPARKLE, 11.85, 0.65, rev=0.4)
    put(resample(WHOOSH2, 0.9), 12.0, 0.45)
    put(thud(120, 0.18, 0.35, 0.9), 12.85, 1.0)
    put(rustle(0.22), 13.05, 1.0, pan=-0.2)
    put(rustle(0.22), 13.17, 1.0, pan=0.2)
    put(resample(CLICK, 1.4), 13.27, 0.45)
    for i, a in enumerate((13.75, 13.9, 14.1, 14.25)):
        put(thud(150 + 25 * i, 0.12, 0.42, 0.6), a, 1.0, pan=(-0.3 + 0.2 * i))
    put(tape_rip(0.42), 14.45, 1.0)
    put(thud(110, 0.15, 0.45, 0.4), 14.98, 1.0)
    put(resample(POP, 0.8), 14.98, 0.4)
    put(boing(260, 560, 0.3, 0.22), 15.2, 1.0)
    put(boing(300, 620, 0.25, 0.16), 15.75, 1.0)
    # loading the van
    put(resample(CLICK, 0.7), 16.05, 0.6)
    for i, a in enumerate((16.45, 16.6, 16.75, 16.9, 17.15)):
        put(resample(WHOOSH2, 1.3 + 0.08 * i), a, 0.22, pan=-0.3)
        put(thud(95, 0.12, 0.3, 0.7), a + 0.55, 1.0, pan=-0.4)
    put(thud(85, 0.22, 0.6, 0.9), 17.85, 1.0, pan=-0.3)
    put(resample(WHOOSH, 0.85), 17.88, 0.3)
    put(engine(0.7, 0.3, 0.3), 17.98, 1.0)
    put(thud(75, 0.3, 0.4, 0.8), 18.48, 1.0)
    put(horn(415, 0.14), 18.38, 1.0)
    put(horn(470, 0.18), 18.58, 1.0)
    put(engine(1.1, 1.0, 0.32), 18.62, 1.0)
    put(resample(WHOOSH, 0.9), 18.7, 0.35)
    # route draws itself: a rising arpeggio
    for i, m in enumerate([69, 73, 76, 81, 85, 88]):
        put(pluck(m + 12, 0.4, 1.0), 18.55 + i * 0.19, 0.45, pan=(-0.5 + 0.2 * i), rev=0.4)
    # stop A
    put(squeak(), 21.1, 1.0)
    put(thud(130, 0.1, 0.25, 0.5), 21.52, 1.0)
    for a in (21.68, 21.9, 22.12, 22.3):
        put(step(), a, 1.0)
    put(bell(659.25, 1.4, 0.3), 22.45, 1.0, rev=0.3)
    put(bell(523.25, 1.6, 0.3), 22.78, 1.0, rev=0.3)
    put(resample(CLICK, 0.8), 22.82, 0.5)
    put(resample(POP, 1.1), 23.3, 0.4)
    put(CHIME, 23.5, 0.8, rev=0.3)
    for i in range(3):
        put(resample(POP, 1.5 + 0.2 * i), 23.55 + 0.13 * i, 0.22, pan=0.3)
    for a in (23.85, 24.05, 24.25):
        put(step(0.1), a, 1.0)
    put(engine(0.9, 0.8, 0.28), 24.42, 1.0)
    put(resample(WHOOSH, 1.05), 24.5, 0.3)
    put(thud(120, 0.12, 0.25, 0.5), 25.2, 1.0)
    # stop B
    put(squeak(), 26.22, 1.0)
    put(resample(CLICK, 0.8), 26.42, 0.45)
    for a in (26.55, 26.72, 26.88, 27.0):
        put(step(0.1), a, 1.0)
    put(resample(POP, 1.1), 27.1, 0.4)
    put(resample(CHIME, 1.12), 27.45, 0.75, rev=0.3)
    put(SPARKLE, 27.55, 0.9, rev=0.5)
    put(resample(WHOOSH2, 1.2), 27.55, 0.4)
    for i, m in enumerate([81, 85, 88, 93]):
        put(pluck(m, 0.6, 1.0), 27.58 + i * 0.07, 0.55, rev=0.5)
    put(resample(WHOOSH2, 0.9), 28.55, 0.25)
    put(engine(1.0, 1.0, 0.3), 28.66, 1.0)
    put(WHOOSH, 28.72, 0.45)
    # montage: parcels tossed to the doors
    toss = van_toss_times()
    for i, name in enumerate(("S1", "N1", "N2")):
        a = toss[name]
        put(resample(WHOOSH2, 1.25), a, 0.3, pan=0.2)
        put(resample(POP, 0.9), a + 0.55, 0.45)
        put(resample(PING, 1.0 + 0.12 * i), a + 0.57, 0.28, rev=0.3)
        put(pluck(88 + [0, 4, 7][i], 0.5, 1.0), a + 0.57, 0.6, rev=0.4)
    put(squeak(0.18, 0.06), 31.3, 1.0)
    # to the beach
    put(WHOOSH, 32.3, 0.4)
    put(waves(5.2, 0.16), 31.9, 1.0)
    for i in range(6):
        put(resample(POP, 1.6 + 0.08 * i), 33.25 + 0.36 * i, 0.16, pan=(-0.3 + 0.12 * i))
    # pull back to the end card
    put(riser(1.3, 250, 2000, 0.4), 35.3, 1.0)
    pk2 = peak_time(WHOOSH_CINE)
    put(WHOOSH_CINE, 36.6 - pk2, 0.55)
    put(IMPACT, 36.6, 0.9, rev=0.25)
    put(crash(2.4, 0.16), 36.6, 1.0)
    put(resample(POP, 0.75), 36.75, 0.55)
    put(SPARKLE, 36.8, 0.6, rev=0.4)
    put(resample(POP, 1.2), 37.2, 0.35)
    put(resample(POP, 1.0), 37.6, 0.5)
    put(resample(PING, 1.2), 37.62, 0.25, rev=0.3)
    put(SPARKLE, 38.6, 0.4, rev=0.5)

    # ------------------------------------------------ reverb (synthetic stereo hall), mix, master
    ir_len = int(1.9 * SR)
    t = tt(ir_len)
    ir = np.stack([noise(ir_len), noise(ir_len)]) * np.exp(-t / 0.42)
    ir = fft_band(ir, lo=250, hi=7000)
    ir[:, : int(0.012 * SR)] = 0
    ir /= np.sqrt((ir**2).sum(axis=1, keepdims=True))
    nfft = 1 << int(np.ceil(np.log2(N + ir_len)))
    wet = np.stack([np.fft.irfft(np.fft.rfft(send.x[c], nfft) * np.fft.rfft(ir[c], nfft), nfft)[:N] for c in range(2)])
    mix = music.x * 0.62 + sfx.x * 0.95 + wet * 0.55
    mix *= fade
    # gentle high-pass on the master, then loudness to ~-14 LUFS-ish (RMS proxy) and a soft limiter
    mix = fft_band(mix, lo=28, order=2)
    rms = np.sqrt((mix**2).mean())
    mix *= 10 ** (-15.5 / 20) / max(rms, 1e-9)
    ceiling = 10 ** (-1.2 / 20)
    mix = np.tanh(mix / ceiling) * ceiling
    out = os.path.join(ROOT, "assets", "audio", "soundtrack.wav")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    pcm = (np.clip(mix, -1, 1).T * 32767).astype("<i2")
    with wave.open(out, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    print("wrote", out, "toss times", {k: round(v, 3) for k, v in toss.items()})


if __name__ == "__main__":
    main()
