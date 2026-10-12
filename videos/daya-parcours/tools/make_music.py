#!/usr/bin/env python3
"""Musique originale de la pub BIKINI SHOP : dance-pop / afro-house d'été, 120 BPM, 26,5 s.

Synthétisée ici (aucun échantillon externe, donc libre de droits) et calée sur le montage :
à 120 BPM un temps dure 0,5 s, et toutes les transitions de la vidéo tombent sur ce quadrillage
(1,0 · 2,0 · 3,5 · 5,0 · 6,0 · 8,0 · 9,5 · 11,5 · 14,0 · 15,0 · 18,0 · 21,0 · 22,5 · 23,5 · 24,0 · 25,5 s).

Structure (une mesure = 2 s, mesure 0 à t = 0) :
  0,0–1,0   montée (riser) → IMPACT sur le logo à 1,0
  2,0–8,0   groove principal : grosse caisse 4/4 qui « pompe », clap, charleston à contretemps,
            shaker, conga, basse syncopée, accords plaqués, mélodie (hook) cuivrée/steel-drum
  8,0–11,5  groove sans hook (DM, vue éclatée), petits « ping » sur la checklist
  11,5–14,0 pause plage : plus de grosse caisse, nappe + hook filtré, montée vers le drop
  14,0–15,0 roulement de caisse claire (téléphone)
  15,0      DROP (« Ta commande, en 1 clic ») : énergie maximale
  17,0–18,0 whoosh + coupure d'un temps avant la boutique 3D
  18,0–22,5 groove (avis client, livraison), étoiles en notes
  22,5–23,5 retombée filtrée → IMPACT à 23,5 (explosion corail)
  24,0–25,5 final plein pot sur la signature
  25,5–26,5 accord final qui s'éteint (la vidéo boucle sur la montée du début)

Usage : python3 tools/make_music.py   →  assets/audio/music.wav (48 kHz, stéréo, -14 LUFS)
"""
import math
import os
import subprocess
import wave

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "assets", "audio", "music.wav")
SR = 48000
DUR = 26.5
N = int(SR * DUR)
BEAT = 0.5
BAR = 2.0
RNG = np.random.default_rng(20261012)
SWING = 0.012  # léger swing des doubles-croches (groove afro-house)


def midi(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def tt(n):
    return np.arange(n) / SR


def noise(n):
    return RNG.standard_normal(n)


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
            self.x[:, i0:i0 + n] += sig[:, s0:s0 + n] * gain


# ------------------------------------------------------------------ instruments
def kick():
    n = int(0.45 * SR)
    t = tt(n)
    f = 52 + 150 * np.exp(-t / 0.025)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.20)
    click = fft_band(noise(n), lo=2000, hi=8000) * np.exp(-t / 0.003) * 0.5
    return np.tanh(2.4 * (body + click)) * 0.95


def clap():
    n = int(0.4 * SR)
    t = tt(n)
    env = np.zeros(n)
    for d in (0.0, 0.009, 0.019, 0.028):
        i = int(d * SR)
        env[i:] += np.exp(-(t[:n - i]) / 0.007)
    env += 0.6 * np.exp(-t / 0.13) * (t > 0.03)
    snap = fft_band(noise(n), lo=1000, hi=5500) * env
    tone = np.sin(2 * np.pi * 190 * t) * np.exp(-t / 0.05) * 0.4
    return (snap + tone) * 0.6


def snare_hit(gain=0.5):
    n = int(0.22 * SR)
    t = tt(n)
    s = fft_band(noise(n), lo=1500, hi=9000) * np.exp(-t / 0.06)
    s += np.sin(2 * np.pi * 210 * t) * np.exp(-t / 0.04) * 0.6
    return s * gain


def hat(open_=False):
    n = int((0.22 if open_ else 0.05) * SR)
    t = tt(n)
    return fft_band(noise(n), lo=7500) * np.exp(-t / (0.08 if open_ else 0.012)) * (0.32 if open_ else 0.22)


def shaker():
    n = int(0.08 * SR)
    t = tt(n)
    env = (1 - np.exp(-t / 0.005)) * np.exp(-t / 0.025)
    return fft_band(noise(n), lo=5000, hi=13000) * env * 0.3


def conga(f=210, gain=0.35):
    n = int(0.25 * SR)
    t = tt(n)
    fr = f * (1 + 0.25 * np.exp(-t / 0.015))
    s = np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t / 0.09)
    s += fft_band(noise(n), lo=800, hi=4000) * np.exp(-t / 0.008) * 0.3
    return np.tanh(1.4 * s) * gain


def bassnote(m, dur):
    n = int(dur * SR)
    t = tt(n)
    f = midi(m)
    env = (1 - np.exp(-t / 0.003)) * np.clip((dur - t) / 0.03, 0, 1) * (0.7 + 0.3 * np.exp(-t / 0.07))
    sub = np.sin(2 * np.pi * f * t) * 0.75
    saw = 2 * ((f * t) % 1.0) - 1
    mid = fft_band(saw, lo=90, hi=1400) * 0.85
    return np.tanh(1.8 * (sub + mid)) * env * 0.42


def supersaw(notes, dur, bright=3200.0):
    n = int(dur * SR)
    t = tt(n)
    out = np.zeros((2, n))
    for m in notes:
        for det, pan in ((-0.11, -0.8), (-0.04, -0.3), (0.0, 0.0), (0.04, 0.3), (0.11, 0.8)):
            f = midi(m) * 2 ** (det / 12)
            saw = 2 * ((f * t + RNG.random()) % 1.0) - 1
            a = (pan + 1) * math.pi / 4
            out[0] += saw * math.cos(a)
            out[1] += saw * math.sin(a)
    out = fft_band(out, hi=bright, order=2)
    return out


def stab(notes, dur=0.22, bright=3800.0):
    s = supersaw(notes, dur, bright)
    t = tt(s.shape[1])
    env = (1 - np.exp(-t / 0.002)) * np.exp(-t / 0.11)
    return s * env * 0.12


def pad(notes, dur, bright=1400.0):
    s = supersaw(notes, dur, bright)
    t = tt(s.shape[1])
    env = np.minimum(1, t / 0.4) * np.clip((dur - t) / 0.5, 0, 1)
    return s * env * 0.055


def steelpan(m, dur=0.5, gain=0.3):
    n = int(dur * SR)
    t = tt(n)
    f = midi(m) * (1 + 0.003 * np.sin(2 * np.pi * 5.5 * t))
    ph = 2 * np.pi * np.cumsum(f) / SR
    s = np.sin(ph) * np.exp(-t / 0.45) + 0.6 * np.sin(2 * ph) * np.exp(-t / 0.22) + 0.3 * np.sin(3 * ph + 0.4) * np.exp(-t / 0.1)
    return s * (1 - np.exp(-t / 0.002)) * gain


def pluck(m, dur=0.35, gain=0.28, bright=1.0):
    n = int(dur * SR)
    t = tt(n)
    f = midi(m)
    saw = 2 * ((f * t) % 1.0) - 1
    sq = np.sign(np.sin(2 * np.pi * f * t))
    s = fft_band(0.7 * saw + 0.3 * sq, hi=2500 * bright, order=2)
    s += 0.25 * np.sin(2 * np.pi * 2 * f * t)
    return s * (1 - np.exp(-t / 0.0015)) * np.exp(-t / 0.13) * gain


def bell(m, dur=1.2, gain=0.22):
    n = int(dur * SR)
    t = tt(n)
    f0 = midi(m)
    s = np.zeros(n)
    for ratio, amp, dec in ((1, 1, 0.8), (2.0, 0.45, 0.45), (2.76, 0.3, 0.3), (5.4, 0.18, 0.12)):
        s += amp * np.sin(2 * np.pi * f0 * ratio * t) * np.exp(-t / dec)
    return s * (1 - np.exp(-t / 0.002)) * gain


def riser(dur, gain=0.5, f0=180, f1=2400):
    n = int(dur * SR)
    t = tt(n)
    p = t / dur
    nz = noise(n)
    # bruit qui s'ouvre (filtrage par blocs) + sinus qui monte
    out = np.zeros(n)
    blocks = 24
    for b in range(blocks):
        a, z = b * n // blocks, (b + 1) * n // blocks
        fc = 400 + 11000 * ((b + 0.5) / blocks) ** 2
        out[a:z] = fft_band(nz[a:z], hi=fc, order=2)
    sweep = np.sin(2 * np.pi * np.cumsum(f0 * (f1 / f0) ** p) / SR) * 0.3
    return (out * 0.8 + sweep) * p ** 2.4 * gain


def reverse_cymbal(dur=1.0, gain=0.35):
    n = int(dur * SR)
    t = tt(n)
    s = np.stack([fft_band(noise(n), lo=4000), fft_band(noise(n), lo=4000)])
    return s * (t / dur) ** 3 * gain


def crash(dur=2.4, gain=0.3):
    n = int(dur * SR)
    t = tt(n)
    s = np.stack([fft_band(noise(n), lo=3200), fft_band(noise(n), lo=3200)])
    return s * np.exp(-t / 0.8) * (1 - np.exp(-t / 0.002)) * gain


def impact(gain=0.9):
    """Gros coup : sous-grave qui descend + souffle + crash."""
    n = int(1.6 * SR)
    t = tt(n)
    f = 45 + 110 * np.exp(-t / 0.07)
    boom = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.35) * 0.8
    air = fft_band(noise(n), lo=150, hi=3000) * np.exp(-t / 0.18) * 0.5
    mono = np.tanh(2.0 * (boom + air)) * gain
    out = np.stack([mono, mono])
    out[:, :len(t)] += crash(1.6, 0.25)[:, :len(t)]
    return out


def whoosh(dur=0.6, gain=0.4):
    n = int(dur * SR)
    t = tt(n)
    p = t / dur
    env = np.sin(np.pi * p) ** 2
    out = np.zeros(n)
    nz = noise(n)
    blocks = 16
    for b in range(blocks):
        a, z = b * n // blocks, (b + 1) * n // blocks
        x = (b + 0.5) / blocks
        fc = 600 + 6000 * math.sin(math.pi * x)
        out[a:z] = fft_band(nz[a:z], lo=fc * 0.4, hi=fc, order=2)
    return out * env * gain


def downlifter(dur=1.0, gain=0.35):
    n = int(dur * SR)
    t = tt(n)
    p = t / dur
    f = 1600 * (60 / 1600) ** p
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * (1 - p) ** 2
    return s * gain


def reverb(x, seconds=1.6, mix=1.0):
    """Réverbe par convolution avec une réponse synthétique (bruit à décroissance exponentielle)."""
    n_ir = int(seconds * SR)
    t = tt(n_ir)
    ir = np.stack([noise(n_ir), noise(n_ir)]) * np.exp(-t / (seconds / 5))
    ir = fft_band(ir, lo=200, hi=7000, order=1)
    ir /= np.sqrt((ir ** 2).sum(axis=1, keepdims=True))
    L = x.shape[1] + n_ir
    nfft = 1 << (L - 1).bit_length()
    y = np.fft.irfft(np.fft.rfft(x, nfft) * np.fft.rfft(ir, nfft), nfft)[:, :x.shape[1]]
    return y * mix


def delay(x, time, fb=0.35, mix=0.35, pingpong=True):
    y = np.zeros_like(x)
    d = int(time * SR)
    g = mix
    for k in range(1, 6):
        src = x[:, :-d * k] if d * k < x.shape[1] else None
        if src is None:
            break
        if pingpong:
            ch = (k % 2)
            y[ch, d * k:] += src[(ch + 1) % 2] * g
        else:
            y[:, d * k:] += src * g
        g *= fb
    return y


# ------------------------------------------------------------------ composition
def main():
    drums, bass, music, lead, fx, send = (Bus() for _ in range(6))

    # La majeur, progression vi–IV–I–V (F#m – D – A – E), une mesure (2 s) par accord
    Fsm = ([66, 69, 73], 42)
    D = ([66, 69, 74], 38)
    A = ([64, 69, 73], 45)
    E = ([64, 68, 71], 40)
    PROG = [Fsm, D, A, E]
    # hook (pentatonique de La) : (temps dans la mesure, note, durée)
    HOOK = [
        [(0.0, 76, 0.4), (0.75, 78, 0.3), (1.5, 81, 0.5), (2.5, 78, 0.3), (3.0, 76, 0.4), (3.5, 73, 0.4)],
        [(0.0, 74, 0.4), (0.75, 76, 0.3), (1.5, 78, 0.5), (2.5, 76, 0.3), (3.0, 74, 0.4), (3.5, 71, 0.4)],
        [(0.0, 73, 0.4), (0.75, 76, 0.3), (1.5, 81, 0.5), (2.5, 80, 0.3), (3.0, 78, 0.4), (3.5, 76, 0.4)],
        [(0.0, 76, 0.6), (1.0, 73, 0.3), (1.5, 71, 0.4), (2.0, 68, 0.6), (3.0, 71, 0.4), (3.5, 73, 0.4)],
    ]
    # basse house syncopée : (temps, décalage d'octave, durée)
    BASS = [(0.5, 0, 0.32), (1.0, 0, 0.18), (1.5, 0, 0.32), (2.5, 0, 0.32), (3.0, 12, 0.18), (3.5, 0, 0.32)]
    STABS = [0.5, 1.5, 2.25, 3.0]

    k_s, c_s = kick(), clap()
    kicks = []

    def sec(t):
        if t < 1.0:
            return "intro"
        if t < 2.0:
            return "logo"
        if t < 8.0:
            return "main"
        if t < 11.5:
            return "groove"
        if t < 14.0:
            return "beach"
        if t < 15.0:
            return "build"
        if t < 17.75:
            return "drop"
        if t < 18.0:
            return "stop"
        if t < 22.5:
            return "groove2"
        if t < 24.0:
            return "fall"
        if t < 25.5:
            return "final"
        return "outro"

    FULL = ("main", "drop", "groove", "groove2", "final")

    # ---- batterie, temps par temps
    for b in range(int(DUR / BEAT)):
        t = b * BEAT
        s = sec(t)
        beat_in_bar = b % 4
        if s in FULL:
            drums.add(k_s, t, 1.0)
            kicks.append(t)
            if beat_in_bar in (1, 3):
                drums.add(c_s, t, 0.85)
                send.add(c_s, t, 0.25)
            # charleston ouvert à contretemps
            drums.add(hat(True), t + BEAT / 2, 0.9, pan=0.25)
            # shaker en doubles-croches, swingué
            for k in range(4):
                off = k * BEAT / 4 + (SWING if k % 2 else 0)
                drums.add(shaker(), t + off, 0.55 if k % 2 else 0.35, pan=-0.35)
            # congas (motif afro)
            if beat_in_bar in (0, 2):
                drums.add(conga(230), t + 0.375, 0.7, pan=0.45)
            if beat_in_bar == 3:
                drums.add(conga(320), t + 0.125, 0.55, pan=0.55)
                drums.add(conga(260), t + 0.25 + SWING, 0.5, pan=0.5)
        elif s == "logo" and t >= 1.0:
            if t == 1.0:
                drums.add(k_s, t, 1.0)
                kicks.append(t)
            drums.add(hat(), t + 0.25, 0.6)
        elif s == "beach":
            drums.add(shaker(), t + 0.25, 0.55, pan=-0.3)
            drums.add(hat(True), t + BEAT / 2, 0.45, pan=0.25)
            if beat_in_bar in (1, 3):
                drums.add(c_s, t, 0.35)
                send.add(c_s, t, 0.4)
        elif s == "fall":
            if beat_in_bar in (1, 3):
                drums.add(c_s, t, 0.5)
                send.add(c_s, t, 0.3)

    # roulement de caisse claire avant le drop (14,0 → 15,0) : croches puis doubles puis triples
    t = 14.0
    while t < 15.0 - 1e-6:
        u = (t - 14.0) / 1.0
        step = 0.125 if u < 0.5 else (0.0625 if u < 0.85 else 0.03125)
        drums.add(snare_hit(0.25 + 0.5 * u), t, 1.0, pan=0.1)
        t += step
    # roulement plus court avant la retombée finale (23,0 → 23,5)
    t = 23.0
    while t < 23.5 - 1e-6:
        u = (t - 23.0) / 0.5
        drums.add(snare_hit(0.2 + 0.45 * u), t, 1.0, pan=-0.1)
        t += 0.0625 if u < 0.6 else 0.03125

    # ---- basse, accords, hook (mesure par mesure)
    for bar in range(int(math.ceil(DUR / BAR))):
        t0 = bar * BAR
        notes, root = PROG[bar % 4]
        s = sec(t0 + 0.01)
        if s in FULL or s in ("logo", "fall"):
            for (beat, octv, dur) in BASS:
                tb = t0 + beat * BEAT
                sb = sec(tb)
                if sb in FULL:
                    bass.add(bassnote(root + octv, dur), tb, 1.0)
            for beat in STABS:
                tb = t0 + beat * BEAT
                if sec(tb) in FULL:
                    st = stab([m - 12 for m in notes] + [notes[0]])
                    music.add(st, tb, 1.0)
                    send.add(st, tb, 0.2)
        if s in ("beach", "intro", "logo", "fall", "outro", "build"):
            pd = pad([m - 12 for m in notes], BAR + 0.3)
            music.add(pd, t0, 1.0 if s != "build" else 0.8)
            send.add(pd, t0, 0.3)
        # hook : section principale, drop, livraison, final ; filtré sur la plage
        hook_on = s in ("main", "drop", "final") or (s == "groove2" and t0 >= 20.0)
        for (beat, m, dur) in HOOK[bar % 4]:
            tb = t0 + beat * BEAT
            sb = sec(tb)
            if hook_on and sb in ("main", "drop", "final", "groove2"):
                p = steelpan(m, 0.5, 0.3)
                lead.add(p, tb, 1.0, pan=0.15)
                lead.add(pluck(m - 12, 0.3, 0.16), tb, 1.0, pan=-0.2)
                if sb == "drop":
                    lead.add(steelpan(m + 12, 0.4, 0.14), tb, 1.0, pan=-0.3)
            elif sb == "beach":
                lead.add(pluck(m, 0.45, 0.4, bright=0.6), tb, 1.0, pan=0.2)
                lead.add(steelpan(m, 0.5, 0.14), tb, 1.0, pan=-0.2)

    # ---- effets calés sur l'image
    fx.add(riser(1.0, 0.45), 0.0)                         # montée vers le logo
    fx.add(impact(0.85), 1.0)                              # flash du logo
    fx.add(reverse_cymbal(0.9, 0.3), 1.1)                  # aspiration vers la recherche
    fx.add(crash(1.8, 0.22), 2.0)
    fx.add(whoosh(0.5, 0.35), 3.25, pan=-0.3)             # zoom recherche → profil
    fx.add(whoosh(0.7, 0.35), 4.85, pan=0.3)              # scroll de la grille
    fx.add(crash(1.6, 0.2), 6.0)                           # la vidéo s'ouvre
    fx.add(whoosh(0.5, 0.3), 7.75, pan=-0.2)              # vidéo → DM
    for i, tc in enumerate((10.55, 10.85, 11.15)):         # coches de la checklist
        fx.add(bell(81 + (0, 4, 7)[i], 0.9, 0.16), tc + 0.28, pan=(-0.3, 0.0, 0.3)[i])
    fx.add(downlifter(0.9, 0.3), 11.4)                     # coupe vers la plage
    fx.add(riser(1.5, 0.55), 13.5)                         # montée vers le drop
    fx.add(impact(1.0), 15.0)                              # DROP « Ta commande, en 1 clic »
    for i, tc in enumerate((15.85, 16.25, 16.65)):         # statuts validés
        fx.add(bell(76 + (0, 4, 9)[i], 0.7, 0.14), tc + 0.22, pan=(-0.25, 0.25, 0.0)[i])
    fx.add(whoosh(0.7, 0.5), 16.9)                         # zoom qui traverse
    fx.add(reverse_cymbal(0.6, 0.3), 17.4)                 # bulles → boutique
    fx.add(crash(2.0, 0.25), 18.0)
    for i in range(5):                                     # étoiles qui se remplissent
        fx.add(bell(81 + (0, 2, 4, 7, 9)[i], 0.6, 0.11), 18.95 + i * 0.13, pan=-0.4 + 0.2 * i)
    fx.add(whoosh(0.5, 0.3), 20.85, pan=0.25)              # boutique → livraison
    fx.add(crash(1.6, 0.2), 21.0)
    fx.add(downlifter(0.8, 0.28), 22.3)                    # retombée « Ton été commence ici »
    fx.add(riser(1.0, 0.45), 22.5)
    fx.add(impact(0.95), 23.5)                             # explosion corail
    fx.add(crash(1.5, 0.2), 24.0)
    fx.add(reverse_cymbal(0.5, 0.2), 25.0)
    # accord final qui sonne et s'éteint
    for j, m in enumerate(A[0] + [A[0][0] + 12]):
        lead.add(steelpan(m, 1.0, 0.22), 25.5, pan=(j - 1.5) * 0.3)
    music.add(pad([m - 12 for m in A[0]], 1.0, 1800), 25.5, 1.4)

    # ---- sidechain : basse et accords « pompent » sur la grosse caisse
    duck = np.ones(N)
    rel = int(0.22 * SR)
    shape = 1 - 0.85 * np.exp(-np.arange(rel) / (0.06 * SR))
    for tk in kicks:
        i = int(tk * SR)
        n = min(rel, N - i)
        duck[i:i + n] = np.minimum(duck[i:i + n], shape[:n])
    bass.x *= duck
    music.x *= duck ** 0.8
    lead.x *= duck ** 0.35

    # ---- effets d'espace
    lead_dly = delay(lead.x, 0.375, fb=0.35, mix=0.28)
    space = reverb(send.x + 0.35 * lead.x, 1.8, 0.55)

    mix = drums.x * 0.9 + bass.x * 0.8 + music.x * 1.5 + lead.x * 1.6 + lead_dly * 1.2 + fx.x * 0.8 + space * 1.2
    mix = fft_band(mix, lo=38, order=2)          # nettoie l'infra-grave (inaudible sur téléphone)
    mix = tilt_eq(mix)                           # un peu moins de sub, plus de mordant (2-8 kHz) pour le téléphone
    # niveau avant saturation : seules les crêtes rares (0,05 %) touchent la courbe
    mix /= np.percentile(np.abs(mix), 99.95) / 0.8
    mix = np.tanh(1.1 * mix) / np.tanh(1.1)      # saturation douce (colle le mix)
    # fondu de fin (la vidéo boucle sur la montée du début)
    t = tt(N)
    mix *= np.clip((DUR - t) / 0.6, 0, 1) ** 1.5

    tmp = OUT + ".raw.wav"
    write_wav(tmp, mix / max(1e-9, np.abs(mix).max()) * 0.9)
    # niveau final : gain statique + limiteur suréchantillonné → -14 LUFS, crête < -1 dBTP
    loud = measure_lufs(tmp)
    gain = -14.0 - loud
    subprocess.run(
        ["ffmpeg", "-v", "error", "-y", "-i", tmp, "-af",
         f"volume={gain:.2f}dB,aresample=192000,alimiter=limit=0.84:attack=2:release=40:level=disabled,aresample=48000",
         "-c:a", "pcm_s16le", OUT],
        check=True,
    )
    os.remove(tmp)
    print(f"→ {os.path.relpath(OUT, ROOT)} : {DUR} s, gain {gain:+.1f} dB, {measure_lufs(OUT):.1f} LUFS")


def tilt_eq(x, low_db=-2.0, low_f=70.0, high_db=4.5, high_f=2200.0):
    """Égaliseur de mastering en plateaux (shelves), appliqué dans le domaine fréquentiel."""
    X = np.fft.rfft(x, axis=-1)
    f = np.fft.rfftfreq(x.shape[-1], 1 / SR)
    lo = 10 ** (low_db / 20) + (1 - 10 ** (low_db / 20)) / (1 + (low_f / np.maximum(f, 1e-3)) ** 2)
    hi = 1 + (10 ** (high_db / 20) - 1) / (1 + (high_f / np.maximum(f, 1e-3)) ** 2)
    return np.fft.irfft(X * lo * hi, n=x.shape[-1], axis=-1)


def write_wav(path, x):
    y = np.clip(x.T * 32767, -32768, 32767).astype(np.int16)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with wave.open(path, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(y.tobytes())


def measure_lufs(path):
    out = subprocess.run(["ffmpeg", "-hide_banner", "-i", path, "-af", "ebur128=framelog=quiet", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    for line in out.splitlines():
        line = line.strip()
        if line.startswith("I:"):
            return float(line.split()[1])
    raise RuntimeError("mesure de loudness impossible")


if __name__ == "__main__":
    main()
