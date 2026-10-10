#!/usr/bin/env python3
"""Soundtrack for the Bikini Shop presentation film.

Synthesises a 104 BPM afro-pop groove (log-drum bass, shaker, rim, plucks, steelpan), lays
sound effects on the exact animation times of index.html + compositions/*.html, and ducks the
music under the voice-over lines (assets/audio/vo/*.wav, placed at the same starts as index.html).
The voice itself stays on its own <audio> clips.

Usage:  python3 tools/make_soundtrack.py   ->  assets/audio/soundtrack.wav
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

BEAT = 60 / 104
BAR = 4 * BEAT
RNG = np.random.default_rng(20261010)


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



def logdrum(m, dur=0.42, gain=0.5):
    n = int(dur * SR)
    t = tt(n)
    f = midi(m) * (1 + 0.5 * np.exp(-t / 0.025))
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.25 * np.sin(4 * np.pi * np.cumsum(f) / SR)
    env = (1 - np.exp(-t / 0.003)) * np.exp(-t / 0.16)
    return np.tanh(2.2 * s) * env * gain


def rim():
    n = int(0.12 * SR)
    t = tt(n)
    s = np.sin(2 * np.pi * 1700 * t) * np.exp(-t / 0.012) + fft_band(noise(n), lo=2000, hi=8000) * np.exp(-t / 0.01) * 0.6
    return s * 0.35


VO = [("l1", 0.55), ("l2", 4.25), ("l3", 10.55), ("l4", 16.45), ("l5", 22.1), ("l6", 24.15), ("l7", 29.35), ("l8", 32.25)]
CUTS = [4.2, 10.4, 16.4, 22.0, 32.0]


def main():
    drums, bass, chords, lead, sfx, send = (Bus() for _ in range(6))
    med = os.path.join(ROOT, ".media", "audio", "sfx")
    S = {k: load(os.path.join(med, f"{k}.mp3")) for k in ("sfx_001", "sfx_002", "sfx_003", "sfx_004", "sfx_005", "sfx_006", "sfx_007", "sfx_008", "sfx_009", "sfx_010", "sfx_011")}
    WHOOSH_CINE, POP, SPARKLE, CHIME, IMPACT, RISER, CLICK, WHOOSH, NOTIF, PING, WHOOSH2 = (S[k] for k in sorted(S))

    # Dm9 - G13 - Cmaj9 - Am9   (i ii V vibe, bright)
    PROG = [([62, 65, 69, 72], 38), ([59, 64, 67, 71], 43), ([60, 64, 67, 71], 36), ([60, 64, 69, 72], 33)]
    MEL = [[(0, 74), (1.5, 72), (2.5, 69), (3.0, 72)], [(0, 71), (1.0, 74), (2.0, 76), (3.5, 74)],
           [(0, 76), (1.5, 74), (2.0, 72), (3.0, 71)], [(0, 72), (0.75, 74), (1.5, 76), (2.5, 79)]]
    kick_s, clap_s, rim_s = kick(), clap(), rim()
    kicks = []
    nbars = int(DUR / BAR) + 1
    for b in range(nbars):
        t0 = b * BAR
        notes, root = PROG[b % 4]
        intro = t0 + BAR <= CUTS[0] - 0.1
        final = t0 >= 32.0 - 0.2
        if t0 > 39.3:
            break
        pd = pad(notes, BAR + 0.15)
        chords.add(pd, t0, 0.9)
        send.add(pd, t0, 0.2)
        # off-beat plucks (afro "skank")
        for k in (0.5, 1.5, 2.25, 3.5):
            for j, m in enumerate(notes[1:]):
                p = pluck(m + 12, 0.35, 0.8)
                chords.add(p, t0 + k * BEAT, 0.55 if not intro else 0.4, pan=(j - 1) * 0.4)
                send.add(p, t0 + k * BEAT, 0.15)
        for k in range(16):
            acc = 0.5 if k % 4 == 2 else (0.32 if k % 2 else 0.2)
            drums.add(shaker(), t0 + k * BEAT / 4, acc * (0.7 if intro else 1.0), pan=-0.3)
        if intro:
            continue
        for k in (0, 1.5, 2.5):
            drums.add(kick_s, t0 + k * BEAT, 0.85)
            kicks.append(t0 + k * BEAT)
        for k in (1, 3):
            drums.add(clap_s, t0 + k * BEAT, 0.55)
            send.add(clap_s, t0 + k * BEAT, 0.2)
        for k in (0.75, 1.75, 2.75, 3.25):
            drums.add(rim_s, t0 + k * BEAT, 0.6, pan=0.35)
        for k in range(8):
            drums.add(hat(open_=(k % 4 == 3)), t0 + k * BEAT / 2, 0.35 if k % 2 else 0.18, pan=0.25)
        # amapiano-style log drum
        for k, o in ((0, 0), (0.75, 0), (1.5, 12), (2.5, 7), (3.25, 0)):
            bass.add(logdrum(root + o, 0.4, 0.55), t0 + k * BEAT, 1.0)
        if final or (12 <= t0 < 16) or (24 <= t0 < 30):
            for (k, m) in MEL[b % 4]:
                s_ = steelpan(m, 0.7)
                lead.add(s_, t0 + k * BEAT, 0.7 if final else 0.45, pan=0.15)
                lead.add(s_ * 0.3, t0 + k * BEAT + 0.75 * BEAT, 0.7, pan=-0.45)
                send.add(s_, t0 + k * BEAT, 0.3)

    # light sidechain from kicks
    duck = np.ones(N)
    L = int(0.25 * SR)
    shape = 1 - 0.4 * np.exp(-tt(L) / 0.08)
    for k in kicks:
        i = int(k * SR)
        n = min(L, N - i)
        if n <= 0:
            continue
        duck[i : i + n] = np.minimum(duck[i : i + n], shape[:n])
    music = drums.x * 0.8 + fft_band(bass.x, hi=700) * 0.8 * duck + fft_band(chords.x * duck, hi=5000) * 0.7 + lead.x * 0.85

    # ------------------------------------------------ SFX on picture (global times)
    def put(sig, at, gain, pan=0.0, rev=0.0):
        sfx.add(sig, at, gain, pan)
        if rev:
            send.add(sig, at, gain * rev, pan)

    # S1 hook
    for i in range(5):
        put(resample(POP, 1.0 + 0.1 * i), 0.08 + i * 0.07, 0.25, pan=-0.4 + 0.2 * i)
    put(SPARKLE, 0.5, 0.35, rev=0.3)
    put(thud(110, 0.18, 0.5, 0.6), 0.55, 1.0)
    put(resample(WHOOSH2, 1.2), 1.1, 0.35)
    put(boing(320, 640, 0.3, 0.2), 1.45, 1.0)
    put(thud(130, 0.15, 0.45, 0.5), 1.97, 1.0)
    put(resample(WHOOSH, 1.4), 2.28, 0.25)
    # wipes on every cut
    for c in CUTS:
        put(resample(WHOOSH, 1.1), c - 0.38, 0.4)
        put(thud(80, 0.3, 0.5, 0.7), c, 1.0)
    put(crash(1.6, 0.1), CUTS[0], 1.0)
    # S2 shop profile
    put(resample(WHOOSH2, 0.9), 4.55, 0.35)
    put(resample(POP, 0.9), 4.95, 0.4)
    put(SPARKLE, 5.45, 0.45, rev=0.3)
    for i in range(10):
        put(resample(CLICK, 1.6), 5.6 + i * 0.11, 0.12)
    put(resample(POP, 1.2), 6.2, 0.35)
    put(resample(WHOOSH2, 1.2), 6.55, 0.3)
    for i in range(5):
        put(resample(POP, 1.1 + 0.08 * i), 6.95 + i * 0.09, 0.22, pan=-0.4 + 0.2 * i)
    put(CLICK, 8.4, 0.6)
    put(resample(PING, 1.2), 8.5, 0.2)
    # S3 catalogue — a pop per look, stamp hit
    for i, a in enumerate((10.55, 11.15, 12.2, 12.8, 13.15, 13.5, 13.85, 14.2, 14.55, 14.9)):
        put(resample(POP, 0.95 + 0.05 * (i % 5)), a, 0.3, pan=-0.3)
    for a in (10.6, 11.2, 12.25, 12.85):
        put(resample(WHOOSH2, 1.4), a, 0.18, pan=0.4)
    put(IMPACT, 13.15, 0.5, rev=0.2)
    # S4 audience
    put(SPARKLE, 17.45, 0.45, rev=0.3)
    put(thud(140, 0.15, 0.35, 0.4), 17.4, 1.0)
    for i, a in enumerate((17.75, 18.73, 19.6)):
        put(resample(WHOOSH2, 1.1), a, 0.3, pan=-0.3 + 0.3 * i)
        put(pluck(81 + [0, 4, 7][i], 0.5, 1.0), a + 0.35, 0.5, rev=0.4)
    # S5 value
    put(IMPACT, 22.2, 0.45)
    put(resample(PING, 1.0), 22.85, 0.3, rev=0.3)
    put(CHIME, 23.5, 0.35, rev=0.3)
    put(resample(WHOOSH, 0.95), 24.05, 0.4)
    put(NOTIF, 24.75, 0.4)
    for i in range(9):
        put(resample(POP, 1.4 + 0.06 * i), 25.0 + i * 0.22, 0.12, pan=0.4)
    put(resample(WHOOSH2, 1.0), 26.95, 0.35)
    put(NOTIF, 27.4, 0.45, rev=0.2)
    put(resample(POP, 1.0), 27.75, 0.3)
    put(resample(NOTIF, 1.15), 28.35, 0.4, rev=0.2)
    put(resample(WHOOSH, 1.0), 28.85, 0.35)
    put(resample(POP, 1.0), 29.2, 0.3)
    put(resample(POP, 1.2), 29.35, 0.3)
    put(riser(1.3, 300, 1600, 0.25), 29.6, 1.0)
    put(thud(150, 0.15, 0.45, 0.6), 30.9, 1.0)
    put(CHIME, 30.95, 0.45, rev=0.3)
    # S6 CTA
    put(resample(POP, 0.85), 32.05, 0.4)
    put(resample(POP, 1.1), 32.3, 0.35)
    put(CLICK, 32.85, 0.8)
    put(SPARKLE, 32.92, 0.6, rev=0.4)
    put(crash(1.8, 0.1), 32.92, 1.0)
    put(resample(WHOOSH2, 1.0), 33.4, 0.3)
    for i, a in enumerate((34.3, 35.26, 35.95, 36.6, 37.35)):
        put(resample(PING, 1.0 + 0.08 * i), a, 0.12)
    put(CHIME, 38.1, 0.5, rev=0.4)

    # ------------------------------------------------ duck the music under the voice
    env = np.zeros(N)
    for name, at in VO:
        v = load(os.path.join(ROOT, "assets", "audio", "vo", name + ".wav")).mean(axis=0)
        i0 = int(at * SR)
        n = min(len(v), N - i0)
        env[i0 : i0 + n] = np.maximum(env[i0 : i0 + n], np.abs(v[:n]))
    w = int(0.25 * SR)
    active = np.convolve((env > 0.01).astype(float), np.ones(w) / w, mode="same")
    active = np.convolve(np.minimum(1, active * 3), np.ones(w) / w, mode="same")
    vo_duck = 1 - 0.6 * np.clip(active, 0, 1)  # ~ -8 dB under speech

    # ------------------------------------------------ reverb, mix, master
    ir_len = int(1.6 * SR)
    t = tt(ir_len)
    ir = np.stack([noise(ir_len), noise(ir_len)]) * np.exp(-t / 0.38)
    ir = fft_band(ir, lo=250, hi=7000)
    ir[:, : int(0.012 * SR)] = 0
    ir /= np.sqrt((ir**2).sum(axis=1, keepdims=True))
    nfft = 1 << int(np.ceil(np.log2(N + ir_len)))
    wet = np.stack([np.fft.irfft(np.fft.rfft(send.x[c], nfft) * np.fft.rfft(ir[c], nfft), nfft)[:N] for c in range(2)])
    fade = np.ones(N)
    fade[: int(0.05 * SR)] = np.linspace(0, 1, int(0.05 * SR))
    i0 = int(38.6 * SR)
    fade[i0:] = np.linspace(1, 0, N - i0) ** 1.5
    mix = (music * 0.55 + wet * 0.4) * vo_duck + sfx.x * 0.8
    mix *= fade
    mix = fft_band(mix, lo=30, order=2)
    rms = np.sqrt((mix**2).mean())
    mix *= 10 ** (-20 / 20) / max(rms, 1e-9)  # bed sits ~6 dB under the voice
    ceiling = 10 ** (-3 / 20)
    mix = np.tanh(mix / ceiling) * ceiling
    out = os.path.join(ROOT, "assets", "audio", "soundtrack.wav")
    pcm = (np.clip(mix, -1, 1).T * 32767).astype("<i2")
    with wave.open(out, "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        wf.writeframes(pcm.tobytes())
    print("wrote", out)


if __name__ == "__main__":
    main()
