#!/usr/bin/env python3
"""Musique originale « afro-house tropical » pour BIKINIS SHOP / @daya_na990.

Composée et synthétisée localement (libre de droits), 120 BPM en la mineur, calée sur les 794 images
de la vidéo. Les mesures commencent à 1,8 s + 2 s·n : les coupes 1,8 / 3,8 / 7,8 / 11,8 / 17,8 s tombent
sur un premier temps. Les deux drops (produit héros 9,6 s, signature 23,0 s) sont préparés par une coupure
et une montée, l'impact tombe sur la coupe, le groove repart sur le premier temps suivant (9,8 et 23,8 s).
Chaque détail visuel a sa note : vignettes S03, inserts S07, widgets S08, cœur S10, inserts S11,
bouton Message S12, signature S13. Les queues de réverbération de la fin sont repliées sur le début,
ce qui rend la boucle TikTok continue.

    python3 -I tools/make_music.py --project videos/daya-motion-social
    → assets/audio/musique_daya_afrohouse_120bpm.wav (+ pistes séparées dans .hyperframes/stems/)
"""

import argparse
import math
import wave
from pathlib import Path

import numpy as np
from scipy.signal import butter, fftconvolve, istft, sosfilt, stft

SR = 48000
TOTAL = 794 / 30
NLOOP = int(round(TOTAL * SR))  # 1 270 400 échantillons
TAIL = 4.0
N = NLOOP + int(TAIL * SR)
BEAT = 0.5
STEP = BEAT / 4  # double-croche
BAR0 = 1.8  # premier temps de la première mesure de groove
RNG = np.random.default_rng(20261011)


# ------------------------------------------------------------------ outils
def midi(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def tt(n):
    return np.arange(n) / SR


def noise(n):
    return RNG.standard_normal(n)


def filt(x, kind, f, order=2):
    sos = butter(order, f, btype=kind, fs=SR, output="sos")
    return sosfilt(sos, x, axis=-1)


def bar(n, step=0.0):
    """Instant de la mesure n (n = 0 → 1,8 s), décalé de `step` double-croches."""
    return BAR0 + 2.0 * n + STEP * step


def stereo(sig, pan=0.0):
    a = (pan + 1) * math.pi / 4
    return np.stack([sig * math.cos(a), sig * math.sin(a)]) * math.sqrt(2)


class Bus:
    def __init__(self):
        self.x = np.zeros((2, N))

    def add(self, sig, at, gain=1.0, pan=0.0):
        if sig.ndim == 1:
            sig = stereo(sig, pan)
        i0 = int(round(at * SR))
        s0 = 0
        if i0 < 0:
            s0, i0 = -i0, 0
        n = min(sig.shape[1] - s0, N - i0)
        if n > 0:
            self.x[:, i0:i0 + n] += sig[:, s0:s0 + n] * gain


def make_ir(rt60=1.6, predelay=0.022, damp=5200, width=1.0):
    n = int(rt60 * 1.1 * SR)
    t = tt(n)
    ir = RNG.standard_normal((2, n)) * np.exp(-6.9 * t / rt60)
    ir[1] = width * ir[1] + (1 - width) * ir[0]
    dark = filt(ir, "low", damp)
    mix = np.clip(t / (rt60 * 0.5), 0, 1)
    ir = ir * (1 - mix) + dark * mix
    ir = np.concatenate([np.zeros((2, int(predelay * SR))), ir], axis=1)
    return ir / np.sqrt(np.sum(ir ** 2) / 2)


def reverb(x, ir, wet):
    mono = x.mean(axis=0)
    y = np.stack([fftconvolve(mono, ir[0])[: x.shape[1]], fftconvolve(mono, ir[1])[: x.shape[1]]])
    return y * wet


def pingpong(x, delay=0.375, fb=0.38, wet=0.32, lp=3800):
    d = int(delay * SR)
    mono = filt(x.mean(axis=0), "low", lp)
    out = np.zeros_like(x)
    g = wet
    for k in range(1, 7):
        ch = (k + 1) % 2
        if k * d >= x.shape[1]:
            break
        out[ch, k * d:] += mono[: x.shape[1] - k * d] * g
        g *= fb
    return out


def tv_lowpass(x, keys, order=2.0):
    """Passe-bas dont la coupure suit des points (temps, Hz) interpolés en log (STFT)."""
    f, t, Z = stft(x, fs=SR, nperseg=2048, noverlap=1536, axis=-1)
    kt = np.array([k[0] for k in keys])
    kf = np.log(np.array([k[1] for k in keys]))
    fc = np.exp(np.interp(t, kt, kf))
    gain = 1 / np.sqrt(1 + (f[:, None] / fc[None, :]) ** (2 * order))
    _, y = istft(Z * gain[None, :, :], fs=SR, nperseg=2048, noverlap=1536)
    y = y[:, : x.shape[1]]
    if y.shape[1] < x.shape[1]:
        y = np.pad(y, ((0, 0), (0, x.shape[1] - y.shape[1])))
    return y


def sidechain(kicks, depth, release=0.13):
    t = tt(N)
    sc = np.zeros(N)
    for tk in kicks:
        i0 = int(tk * SR)
        n = min(int(0.5 * SR), N - i0)
        if n <= 0:
            continue
        tau = t[:n]
        sc[i0:i0 + n] = np.maximum(sc[i0:i0 + n], (1 - np.exp(-tau / 0.004)) * np.exp(-tau / release))
    return 1 - depth * sc


# ------------------------------------------------------------------ instruments
def kick(vel=1.0):
    n = int(0.45 * SR)
    t = tt(n)
    f = 51 + 110 * np.exp(-t / 0.026) + 45 * np.exp(-t / 0.004)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.22)
    knock = np.sin(2 * np.pi * np.cumsum(2.02 * f) / SR) * np.exp(-t / 0.045) * 0.35
    click = filt(noise(n), "band", [1500, 7000]) * np.exp(-t / 0.003) * 0.55
    return np.tanh(1.7 * (body + knock + click)) * vel


def clap(vel=1.0):
    n = int(0.42 * SR)
    t = tt(n)
    env = np.zeros(n)
    for d in (0.0, 0.009, 0.018):
        i = int(d * SR)
        env[i:] += np.exp(-t[: n - i] / 0.007)
    i = int(0.026 * SR)
    env[i:] += 0.6 * np.exp(-t[: n - i] / 0.12)
    s = filt(noise(n), "band", [900, 4800]) * env
    return s / (np.abs(s).max() + 1e-9) * vel


def hat(open_=False, vel=1.0):
    n = int((0.22 if open_ else 0.06) * SR)
    t = tt(n)
    s = filt(noise(n), "high", 7500, order=4) * (1 - np.exp(-t / 0.0015)) * np.exp(-t / (0.10 if open_ else 0.013))
    return s / (np.abs(s).max() + 1e-9) * vel


def shaker(vel=1.0):
    n = int(0.09 * SR)
    t = tt(n)
    s = filt(noise(n), "band", [4200, 11000]) * (1 - np.exp(-t / 0.005)) * np.exp(-t / 0.032)
    return s / (np.abs(s).max() + 1e-9) * vel


def conga(f0, vel=1.0, dec=0.2):
    n = int(0.45 * SR)
    t = tt(n)
    f = f0 * (1 + 0.22 * np.exp(-t / 0.012))
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / dec)
    s += 0.45 * np.sin(2 * np.pi * np.cumsum(f * 1.5) / SR) * np.exp(-t / (dec * 0.35))
    s += filt(noise(n), "band", [1200, 5200]) * np.exp(-t / 0.006) * 0.35
    return s / (np.abs(s).max() + 1e-9) * vel


def rim(vel=1.0):
    n = int(0.08 * SR)
    t = tt(n)
    s = (np.sin(2 * np.pi * 1760 * t) + 0.6 * np.sin(2 * np.pi * 2440 * t)) * np.exp(-t / 0.011)
    s += filt(noise(n), "band", [2000, 8000]) * np.exp(-t / 0.002) * 0.5
    return s / (np.abs(s).max() + 1e-9) * vel


def tom(f0, vel=1.0):
    n = int(0.5 * SR)
    t = tt(n)
    f = f0 * (1 + 0.5 * np.exp(-t / 0.03))
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.22) + filt(noise(n), "band", [300, 3000]) * np.exp(-t / 0.01) * 0.3
    return np.tanh(1.3 * s) * vel


def crash(vel=1.0):
    n = int(2.2 * SR)
    t = tt(n)
    s = filt(noise(n), "high", 4200, order=3) * (1 - np.exp(-t / 0.002)) * np.exp(-t / 0.75)
    s += 0.3 * filt(noise(n), "band", [3000, 9000]) * np.exp(-t / 0.05)
    return s / (np.abs(s).max() + 1e-9) * vel


def bass_note(m, dur, vel=1.0):
    n = int((dur + 0.06) * SR)
    t = tt(n)
    f = midi(m)
    sub = np.sin(2 * np.pi * f * t)
    harm = 0.42 * np.sin(2 * np.pi * 2 * f * t) + 0.18 * np.sin(2 * np.pi * 3 * f * t)
    saw = filt(2 * ((f * t) % 1.0) - 1, "low", 420)
    env = (1 - np.exp(-t / 0.005)) * (0.78 + 0.22 * np.exp(-t / 0.12)) * np.where(t < dur, 1.0, np.clip(1 - (t - dur) / 0.05, 0, 1))
    return np.tanh(1.5 * (sub + harm + 0.3 * saw)) * env * vel


def ep_note(m, dur, vel=1.0):
    """Piano électrique FM (lame + caisse), sons courts et ronds."""
    n = int((dur + 0.7) * SR)
    t = tt(n)
    f = midi(m)
    idx = 1.6 * np.exp(-t / 0.3) + 0.35
    mod = np.sin(2 * np.pi * f * t)
    car = np.sin(2 * np.pi * f * t + idx * mod)
    tine = 0.22 * np.sin(2 * np.pi * f * 14.0 * t) * np.exp(-t / 0.025)
    env = (1 - np.exp(-t / 0.003)) * np.exp(-t / 1.1) * np.where(t < dur, 1.0, np.exp(-(t - dur) / 0.1))
    return (car + tine) * env * vel


def ep_chord(notes, dur, vel=1.0, strum=0.006):
    out = None
    for k, m in enumerate(notes):
        s = np.concatenate([np.zeros(int(k * strum * SR)), ep_note(m, dur, vel)])
        out = s if out is None else (np.pad(out, (0, max(0, len(s) - len(out)))) + np.pad(s, (0, max(0, len(out) - len(s)))))
    return out / len(notes) ** 0.6


def pad_chord(notes, dur, attack=0.25, release=0.7):
    n = int((dur + release + 0.05) * SR)
    t = tt(n)
    out = np.zeros((2, n))
    for m in notes:
        for det, p in ((-0.09, -0.75), (0.0, 0.0), (0.09, 0.75)):
            f = midi(m) * 2 ** (det / 12)
            ph = RNG.random()
            saw = 2 * ((f * t + ph) % 1.0) - 1
            out += stereo(saw, p)
    env = np.minimum(1, t / attack) * np.where(t < dur, 1.0, np.clip(1 - (t - dur) / release, 0, 1))
    return out * env / len(notes)


def marimba(m, vel=1.0):
    n = int(1.0 * SR)
    t = tt(n)
    f = midi(m)
    s = np.sin(2 * np.pi * f * t) * np.exp(-t / 0.42)
    s += 0.32 * np.sin(2 * np.pi * 3.93 * f * t) * np.exp(-t / 0.06)
    s += 0.1 * np.sin(2 * np.pi * 9.7 * f * t) * np.exp(-t / 0.018)
    return s * (1 - np.exp(-t / 0.0015)) * vel


def kalimba(m, vel=1.0):
    n = int(1.4 * SR)
    t = tt(n)
    f = midi(m)
    s = np.sin(2 * np.pi * f * t) * np.exp(-t / 0.75)
    s += 0.28 * np.sin(2 * np.pi * 5.4 * f * t) * np.exp(-t / 0.07)
    s += 0.1 * np.sin(2 * np.pi * 11.1 * f * t) * np.exp(-t / 0.025)
    return s * (1 - np.exp(-t / 0.001)) * vel


def bell(m, vel=1.0, dur=2.2):
    n = int(dur * SR)
    t = tt(n)
    f0 = midi(m)
    s = np.zeros(n)
    for ratio, amp, dec in ((1, 1, 1.2), (2.0, 0.45, 0.6), (2.76, 0.35, 0.4), (5.4, 0.16, 0.2), (8.93, 0.07, 0.1)):
        s += amp * np.sin(2 * np.pi * f0 * ratio * t) * np.exp(-t / dec)
    return s * (1 - np.exp(-t / 0.002)) * vel / 2.0


def riser(dur, f0=350, f1=7000, vel=1.0):
    n = int(dur * SR)
    t = tt(n)
    blk = int(0.01 * SR)
    src = noise(n)
    out = np.zeros(n)
    nb = n // blk + 1
    for b in range(nb):
        fc = f0 * (f1 / f0) ** (b / max(1, nb - 1))
        i0 = max(0, b * blk - blk)
        seg = src[i0:i0 + 3 * blk]
        if len(seg) < 16:
            continue
        lo, hi = max(40, fc / 1.6), min(20000, fc * 1.6)
        y = filt(seg, "band", [lo, hi]) * np.hanning(len(seg))
        out[i0:i0 + len(seg)] += y
    env = (t / dur) ** 2.2
    tone_f = 180 * (1200 / 180) ** (t / dur)
    tone = (2 * ((np.cumsum(tone_f) / SR) % 1.0) - 1) * 0.12
    s = out / (np.abs(out).max() + 1e-9) + filt(tone, "low", 3000)
    return s * env * vel


def downlifter(dur, vel=1.0):
    return riser(dur, 6000, 300, vel)[::-1] * np.linspace(1, 0.2, int(dur * SR)) ** 0.5


def impact(vel=1.0, big=True):
    n = int((2.4 if big else 1.2) * SR)
    t = tt(n)
    f = 32 + 48 * np.exp(-t / 0.18)
    sub = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / (0.9 if big else 0.45))
    burst = filt(noise(n), "low", 2600) * np.exp(-t / 0.09) * 0.55
    s = np.tanh(1.4 * (sub + burst))
    return s * vel


def rev_cymbal(dur, vel=1.0):
    n = int(dur * SR)
    t = tt(n)
    s = filt(noise(n), "high", 3500, order=3) * (t / dur) ** 3
    return s / (np.abs(s).max() + 1e-9) * vel


# ------------------------------------------------------------------ harmonie (la mineur)
AM9 = [57, 60, 64, 67, 71]
FMAJ9 = [53, 57, 60, 64, 67]
CMAJ9 = [52, 55, 59, 62]
G69 = [55, 59, 62, 64, 69]
DM9 = [53, 57, 60, 64]
E7SUS = [52, 57, 59, 62]
E7 = [52, 56, 59, 62]
ROOT = {"Am": 33, "F": 29, "C": 36, "G": 31, "Dm": 38, "E": 40}
CHORD = {"Am": AM9, "F": FMAJ9, "C": CMAJ9, "G": G69, "Dm": DM9, "Esus": E7SUS, "E": E7}

# (début, fin, accord) — intro et fin en la mineur 9 pour une boucle continue
HARMONY = [
    (0.0, 1.8, "Am"),
    (1.8, 3.8, "Am"), (3.8, 5.8, "F"), (5.8, 7.8, "C"), (7.8, 9.8, "G"),
    (9.8, 11.8, "Am"), (11.8, 13.8, "F"), (13.8, 15.8, "C"), (15.8, 17.8, "G"),
    (17.8, 19.8, "Am"), (19.8, 21.8, "F"),
    (21.8, 22.8, "Dm"), (22.8, 23.3, "Esus"), (23.3, 23.8, "E"),
    (23.8, 24.8, "Am"), (24.8, 25.5, "F"), (25.5, TOTAL, "Am"),
]

# sections de groove : mesure n → rôle
GROOVE = {0: "ui", 1: "ui", 2: "full", 3: "lite", 4: "drop", 5: "drop", 6: "full", 7: "full", 8: "drop", 9: "break", 10: "build", 11: "drop"}

BASS_PAT = [(0, 0, 2), (3, 0, 1), (6, 12, 2), (8, 0, 2), (10, 7, 1), (11, 0, 1), (13, 12, 1), (14, 7, 2)]
MOTIF_A = [(0, 76), (3, 79), (6, 81), (8, 79), (10, 76), (11, 74), (14, 72)]
MOTIF_A2 = [(0, 72), (3, 74), (6, 76), (8, 79), (10, 76), (12, 74), (14, 72)]
MOTIF_B = [(0, 81), (2, 79), (3, 76), (6, 79), (8, 81), (11, 84), (14, 81)]


def chord_at(t):
    for a, b, c in HARMONY:
        if a <= t < b:
            return c
    return "Am"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", required=True)
    args = ap.parse_args()
    project = Path(args.project).resolve()

    drums, perc, bass, keys, pad, lead, fx = (Bus() for _ in range(7))
    kicks = []

    # ---------------- batterie et percussions
    for n, role in GROOVE.items():
        for s in range(16):
            t = bar(n, s)
            swing = STEP * 0.12 if s % 2 else 0.0
            beat = s % 4 == 0
            # grosse caisse
            kick_on = beat and role in ("ui", "full", "lite", "drop", "build")
            if role == "lite" and t >= 9.3:  # coupure avant le produit héros
                kick_on = False
            if role == "build" and t >= 22.8:  # coupure avant la signature
                kick_on = False
            if n == 11 and t >= 25.5:
                kick_on = False
            if kick_on:
                v = 0.62 if role == "ui" else 1.0
                drums.add(kick(v), t, 0.62)
                kicks.append(t)
            # clap sur 2 et 4
            if s in (4, 12) and role in ("full", "drop") and not (n == 11 and t >= 25.5):
                drums.add(clap(0.9), t, 0.55)
            # charleston fermé (double-croches légères) et ouvert sur les contretemps
            stop = (role == "lite" and t >= 9.3) or (role == "build" and t >= 22.8) or (n == 11 and t >= 25.5)
            if role != "break" and not stop:
                v = 0.55 if s % 4 == 2 else 0.22
                perc.add(hat(False, v), t + swing, 0.62, pan=0.25)
                if s % 4 == 2 and role in ("full", "drop"):
                    perc.add(hat(True, 0.6), t, 0.42, pan=-0.2)
                # shaker
                v = 0.8 if s % 4 == 2 else 0.45
                perc.add(shaker(v), t + swing, 0.38 if role != "ui" else 0.26, pan=-0.35)
            # congas / bongos (motif afro)
            if role in ("ui", "full", "drop") and not stop and (role != "ui" or n == 1):
                if s in (3, 10):
                    perc.add(conga(185, 0.9), t, 0.6, pan=-0.3)
                if s in (6, 7, 14):
                    perc.add(conga(285, 0.75 if s == 7 else 0.9), t + swing, 0.55, pan=0.3)
                if s in (11, 15) and role == "drop":
                    perc.add(conga(410, 0.7, 0.12), t + swing, 0.45, pan=0.45)
            # rim (tresillo)
            if role in ("ui", "lite", "break") and s in (0, 3, 6, 10, 12) and not stop:
                perc.add(rim(0.8), t, 0.34, pan=0.15)
        # roulements de caisse claire dans les montées
        if n == 7:
            for k in range(8):
                drums.add(clap(0.35 + 0.08 * k), bar(7, 12 + k * 0.5), 0.3)
        if n == 10:  # 21,8 → 22,8 s : triples croches en crescendo
            for k in range(16):
                drums.add(clap(0.2 + 0.05 * k), bar(10, k * 0.5), 0.26)
    # relance avant le drop final : toms descendants sur le 4e temps (23,3 s)
    for k, f0 in enumerate((240, 200, 165, 135)):
        drums.add(tom(f0, 0.8), 23.3 + k * STEP, 0.5, pan=0.3 - 0.2 * k)
    # cymbales
    for tc, v in ((5.3, 0.7), (9.8, 1.0), (17.8, 1.0), (23.8, 1.0)):
        fx.add(crash(v), tc, 0.34)

    # ---------------- basse
    for n, role in GROOVE.items():
        if role == "break":
            # nappe de basse tenue (la sous-basse respire sous la pause)
            c = chord_at(bar(n, 0))
            bass.add(bass_note(ROOT[c], 1.9, 0.6), bar(n, 0), 0.5)
            continue
        for s, iv, ln in BASS_PAT:
            t = bar(n, s)
            if (role == "lite" and t >= 9.3) or (role == "build" and t >= 22.8) or (n == 11 and t >= 25.5):
                continue
            if role == "ui" and s not in (0, 6, 8, 14):
                continue
            c = chord_at(t + 0.001)
            root = ROOT["E"] if c in ("Esus", "E") else ROOT[c]
            bass.add(bass_note(root + iv, ln * STEP * 0.92, 0.95), t, 0.5)

    # ---------------- accords : piano électrique en contretemps, nappes continues
    for n, role in GROOVE.items():
        for s in (2, 6, 10, 14):
            t = bar(n, s)
            if role in ("full", "drop") and not (n == 11 and t >= 25.5):
                keys.add(ep_chord(CHORD[chord_at(t)], STEP * 1.1, 0.8), t, 0.5, pan=-0.15 if s % 8 == 2 else 0.15)
        if role == "break":
            keys.add(ep_chord(CHORD["F"], 1.7, 0.7), bar(n, 0), 0.5)
            keys.add(ep_chord(CHORD["F"], 1.0, 0.5), bar(n, 8), 0.4)
            for s, m in MOTIF_A2:  # écho de marimba dans la pause
                lead.add(marimba(m + 12, 0.45), bar(n, s), 0.3, pan=-0.2)
    for a, b, c in HARMONY:
        pad.add(pad_chord(CHORD[c], b - a), a, 1.0)

    # ---------------- mélodie : marimba (crochet) et notes de détail
    for n, motif in ((4, MOTIF_A), (5, MOTIF_A2), (8, MOTIF_A), (11, MOTIF_B)):
        for s, m in motif:
            t = bar(n, s)
            if t >= 25.5:
                continue
            lead.add(marimba(m, 0.85), t, 0.55, pan=0.1)
    # détails : chaque apparition visuelle a sa note
    details = [
        (0.267, 81, "k"), (0.367, 88, "k"),  # S01 nom et handle
        (2.733, 84, "k"), (2.8, 88, "k"),  # S02 résultat révélé
        (3.933, 81, "k"), (4.0, 84, "k"), (4.067, 88, "k"),  # S03 trois vignettes
        (7.3, 79, "k"),  # S04 sélection douce
        (10.067, 88, "b"),  # S06 cœur
        (11.8, 76, "k"), (11.9, 81, "k"), (12.0, 84, "k"),  # S07 trois inserts
        (12.1, 88, "b"), (12.167, 91, "b"), (12.233, 93, "b"),  # S07 traits et repères
        (14.5, 84, "m"), (14.7, 88, "m"), (14.9, 91, "m"),  # S08 Modèle, Couleur, Disponibilité
        (15.9, 93, "b"),  # S08 pulsation de la sélection
        (19.6, 93, "b"), (19.6, 100, "b"),  # S10 cœur
        (20.767, 81, "k"), (20.833, 88, "k"),  # S11 inserts
        (24.0, 93, "b"),  # S13 halo du bouton
    ]
    for t, m, kind in details:
        if kind == "k":
            lead.add(kalimba(m, 0.8), t, 0.45, pan=0.25)
        elif kind == "m":
            lead.add(marimba(m, 0.9), t, 0.52, pan=0.3)
        else:
            lead.add(bell(m, 0.7), t, 0.38, pan=-0.2)
    # S12 : appui sur Message, accord bref
    keys.add(ep_chord([65, 69, 72, 76], 0.18, 0.9), 22.4, 0.36)
    # S13 : signature sonore (cloches la – do – mi – la)
    for k, m in enumerate((81, 84, 88, 93)):
        lead.add(bell(m, 0.85, 2.6), 23.0 + 0.09 * k, 0.36, pan=-0.3 + 0.2 * k)
    # S09 : accord de révélation du showroom
    keys.add(ep_chord(AM9 + [76], 1.4, 0.9, strum=0.015), 17.8, 0.34)

    # ---------------- effets : montées, impacts, cymbales inversées, descente
    for t0, t1, v in ((8.8, 9.6, 0.75), (17.0, 17.8, 0.7), (21.9, 22.8, 0.8)):
        fx.add(riser(t1 - t0, vel=v), t0, 0.32)
    for t, v, big in ((0.167, 0.55, False), (9.6, 1.0, True), (17.8, 0.9, True), (23.0, 0.95, True)):
        fx.add(impact(v, big), t, 0.6)
    for t1, d, v in ((5.3, 0.5, 0.7), (13.9, 0.4, 0.5), (20.7, 0.35, 0.45), (TOTAL, 0.55, 0.6)):
        fx.add(rev_cymbal(d, v), t1 - d, 0.22)
    fx.add(downlifter(0.8, 0.8), 25.5, 0.28)

    # ---------------- traitements : sidechain, filtres de section, espace
    sc_pad = sidechain(kicks, 0.62)
    sc_bass = sidechain(kicks, 0.38, 0.09)
    sc_keys = sidechain(kicks, 0.3)
    pad.x *= sc_pad
    bass.x *= sc_bass
    keys.x *= sc_keys

    E = TOTAL + TAIL
    tonal_keys = [(0, 900), (1.8, 1300), (5.25, 4200), (5.3, 16000), (19.8, 16000), (20.1, 2600), (21.8, 2600), (22.8, 15000), (25.5, 16000), (TOTAL, 900), (E, 900)]
    pad.x = tv_lowpass(pad.x * 0.32, tonal_keys, order=1.5)
    keys.x = tv_lowpass(keys.x, tonal_keys, order=1.0)
    bass.x = tv_lowpass(filt(bass.x, "high", 32), [(0, 400), (1.8, 600), (5.25, 1600), (5.3, 6000), (E, 6000)], order=1.5)
    drum_keys = [(0, 2400), (1.8, 2400), (5.25, 5200), (5.3, 18000), (E, 18000)]
    drums.x = tv_lowpass(drums.x, drum_keys, order=1.0)
    perc.x = tv_lowpass(perc.x, drum_keys, order=1.0)

    ir_room = make_ir(1.1, 0.012, 6000)
    ir_hall = make_ir(2.4, 0.03, 4200)
    lead_wet = pingpong(lead.x, 0.375, 0.4, 0.34) + reverb(lead.x, ir_hall, 0.28)
    keys_wet = reverb(keys.x, ir_hall, 0.22)
    perc_wet = reverb(perc.x, ir_room, 0.12)
    clap_wet = reverb(drums.x, ir_room, 0.08)
    fx_wet = reverb(fx.x, ir_hall, 0.35)

    stems = {
        "batterie": drums.x + clap_wet,
        "percussions": perc.x + perc_wet,
        "basse": bass.x,
        "accords": keys.x + keys_wet + pad.x,
        "melodie": lead.x + lead_wet,
        "effets": fx.x + fx_wet,
    }
    gains = {"batterie": 1.0, "percussions": 1.3, "basse": 0.85, "accords": 0.9, "melodie": 0.9, "effets": 0.7}
    mix = sum(stems[k] * gains[k] for k in stems)
    # égalisation de bus : moins de sous-grave (inaudible au téléphone), plus d'air
    mix = mix - (1 - 10 ** (-4 / 20)) * filt(mix, "low", 70) + (10 ** (3 / 20) - 1) * filt(mix, "high", 5000)
    # colle de bus : légère saturation
    mix = np.tanh(mix * 0.9) / 0.9

    # boucle : la queue au-delà de la dernière image revient au début
    def fold(x):
        y = x[:, :NLOOP].copy()
        y[:, : x.shape[1] - NLOOP] += x[:, NLOOP:]
        return y

    out = fold(mix)
    out /= np.abs(out).max() + 1e-9
    out *= 0.89

    dst = project / "assets" / "audio" / "musique_daya_afrohouse_120bpm.wav"
    write_wav(dst, out)
    stem_dir = project / ".hyperframes" / "stems"
    stem_dir.mkdir(parents=True, exist_ok=True)
    scale = 0.89 / (np.abs(fold(mix)).max() + 1e-9)
    for k, v in stems.items():
        write_wav(stem_dir / f"{k}.wav", fold(v * gains[k]) * scale)
    print("écrit", dst, f"{NLOOP / SR:.4f} s")


def write_wav(path, x):
    y = np.clip(x, -1, 1)
    pcm = (y.T * 32767).round().astype(np.int16)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())


if __name__ == "__main__":
    main()
