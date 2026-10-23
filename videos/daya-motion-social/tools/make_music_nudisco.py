#!/usr/bin/env python3
"""Musique originale « nu-disco / French touch » pour BIKINIS SHOP / @daya_na990.

Composée et synthétisée localement (libre de droits), 120 BPM en fa majeur, calée sur les 794 images de
la vidéo. Même grille que la vidéo : les mesures commencent à 1,8 s + 2 s·n, les coupes 1,8 / 3,8 / 7,8 /
11,8 / 17,8 s tombent sur un premier temps. Boucle d'accords disco I – vi – ii – V (Fmaj9 – Dm9 – Gm9 –
C9sus4), pause en IV – iii (Bbmaj9 – Am7), signature sur le I.

Instrumentation : grosse caisse sur chaque temps, caisse claire et tambourin sur 2 et 4, charleston ouvert
sur les contretemps, basse disco en octaves, guitare rythmique en double-croches étouffées, cordes
pompées par la grosse caisse, accords « stabs » en clave sur les drops, montées de cordes vers les coupes,
syndrums, chœur dans la pause. Les détails visuels sont joués au vibraphone, au célesta, à la harpe et
en pizzicato. Intro et UI (S02–S03) filtrées façon French touch, le filtre s'ouvre sur la coupe de S04.
Les queues de la fin sont repliées sur le début : la boucle TikTok est continue.

    python3 -I tools/make_music_nudisco.py --project videos/daya-motion-social
    → assets/audio/musique_daya_nudisco_120bpm.wav (+ pistes séparées dans .hyperframes/stems/)
"""

import argparse
import math
import wave
from pathlib import Path

import numpy as np
from scipy.signal import butter, fftconvolve, istft, lfilter, sosfilt, sosfiltfilt, stft

SR = 48000
TOTAL = 794 / 30
NLOOP = int(round(TOTAL * SR))  # 1 270 400 échantillons
TAIL = 4.0
N = NLOOP + int(TAIL * SR)
BEAT = 0.5
STEP = BEAT / 4  # double-croche
BAR0 = 1.8  # premier temps de la première mesure de groove
EPS = 1e-6
RNG = np.random.default_rng(20261012)


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


def filt0(x, kind, f, order=2):
    """Même filtre, à phase nulle (fondus entre versions filtrées sans effet de peigne)."""
    sos = butter(order, f, btype=kind, fs=SR, output="sos")
    return sosfiltfilt(sos, x, axis=-1)


def gate(t, dur, rel):
    return np.where(t < dur, 1.0, np.clip(1 - (t - dur) / rel, 0, 1))


def norm(x):
    return x / (np.abs(x).max() + 1e-9)


def bar(n, step=0.0):
    """Instant de la mesure n (n = 0 → 1,8 s), décalé de `step` double-croches."""
    return BAR0 + 2.0 * n + STEP * step


def stereo(sig, pan=0.0):
    a = (pan + 1) * math.pi / 4
    return np.stack([sig * math.cos(a), sig * math.sin(a)]) * math.sqrt(2)


def saw(freq, n, phase=0.0):
    """Dent de scie à bande limitée (PolyBLEP) ; `freq` scalaire ou tableau en Hz."""
    dt = np.full(n, freq / SR) if np.ndim(freq) == 0 else np.asarray(freq, float)[:n] / SR
    ph = (phase + np.concatenate([[0.0], np.cumsum(dt[:-1])])) % 1.0
    y = 2 * ph - 1
    a = ph < dt
    x = ph[a] / dt[a]
    y[a] -= x + x - x * x - 1
    b = ph > 1 - dt
    x = (ph[b] - 1) / dt[b]
    y[b] -= x * x + x + x + 1
    return y


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


def tv_lowpass(x, keys, order=2.0, res_db=0.0):
    """Passe-bas dont la coupure suit des points (temps, Hz) interpolés en log (STFT) ;
    `res_db` ajoute une bosse de résonance qui suit la coupure (balayage de filtre French touch)."""
    f, t, Z = stft(x, fs=SR, nperseg=2048, noverlap=1536, axis=-1)
    kt = np.array([k[0] for k in keys])
    kf = np.log(np.array([k[1] for k in keys]))
    fc = np.exp(np.interp(t, kt, kf))
    ratio = np.maximum(f[:, None], 1.0) / fc[None, :]
    gain = 1 / np.sqrt(1 + ratio ** (2 * order))
    if res_db:
        gain = gain * (1 + (10 ** (res_db / 20) - 1) * np.exp(-0.5 * (np.log2(ratio) / 0.3) ** 2))
    _, y = istft(Z * gain[None, :, :], fs=SR, nperseg=2048, noverlap=1536)
    y = y[:, : x.shape[1]]
    if y.shape[1] < x.shape[1]:
        y = np.pad(y, ((0, 0), (0, x.shape[1] - y.shape[1])))
    return y


def curve(keys):
    """Courbe de gain (temps, gain) interpolée linéairement, une valeur par échantillon."""
    return np.interp(tt(N), [k[0] for k in keys], [k[1] for k in keys])


def sidechain(kicks, depth, release=0.13):
    t = tt(N)
    sc = np.zeros(N)
    for tk in kicks:
        i0 = int(round(tk * SR))
        n = min(int(0.5 * SR), N - i0)
        if n <= 0:
            continue
        tau = t[:n]
        sc[i0:i0 + n] = np.maximum(sc[i0:i0 + n], (1 - np.exp(-tau / 0.004)) * np.exp(-tau / release))
    return 1 - depth * sc


# ------------------------------------------------------------------ batterie
def kick(vel=1.0):
    n = int(0.5 * SR)
    t = tt(n)
    f = 50 + 140 * np.exp(-t / 0.02) + 90 * np.exp(-t / 0.0035)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * (0.8 * np.exp(-t / 0.2) + 0.2 * np.exp(-t / 0.05))
    knock = np.sin(2 * np.pi * 190 * t) * np.exp(-t / 0.016) * 0.22  # tient au téléphone
    click = filt(noise(n), "band", [2500, 8000]) * np.exp(-t / 0.002) * 0.45  # après la saturation
    return (np.tanh(1.8 * body) + knock + click) * vel


def snare(vel=1.0):
    n = int(0.4 * SR)
    t = tt(n)
    f1 = 190 * (1 + 0.25 * np.exp(-t / 0.01))
    tone = (np.sin(2 * np.pi * np.cumsum(f1) / SR) + 0.5 * np.sin(2 * np.pi * np.cumsum(1.72 * f1) / SR)) * np.exp(-t / 0.07)
    body = filt(noise(n), "band", [1500, 9500]) * np.exp(-t / 0.13)
    return norm(0.55 * tone + body) * vel


def clap(vel=1.0):
    n = int(0.42 * SR)
    t = tt(n)
    env = np.zeros(n)
    for d in (0.0, 0.009, 0.018):
        i = int(d * SR)
        env[i:] += np.exp(-t[: n - i] / 0.007)
    i = int(0.026 * SR)
    env[i:] += 0.6 * np.exp(-t[: n - i] / 0.12)
    return norm(filt(noise(n), "band", [1000, 5000]) * env) * vel


HAT_F = (205.3, 304.4, 369.6, 522.7, 540.0, 800.0)  # carrés inharmoniques façon boîte à rythmes


def hat(open_=False, vel=1.0):
    n = int((0.32 if open_ else 0.07) * SR)
    t = tt(n)
    metal = sum(np.sign(np.sin(2 * np.pi * f * t + RNG.random() * 6.283)) for f in HAT_F)
    s = 0.7 * filt(metal, "band", [6500, 13000], order=3) + 0.5 * filt(noise(n), "high", 8000, order=3)
    s = s * (1 - np.exp(-t / 0.001)) * np.exp(-t / (0.14 if open_ else 0.018))
    return norm(s) * vel


def tamb(vel=1.0):
    n = int(0.22 * SR)
    t = tt(n)
    env = np.zeros(n)
    for d, a in ((0.0, 1.0), (0.007, 0.7), (0.016, 0.45)):
        i = int(d * SR)
        env[i:] += a * np.exp(-t[: n - i] / 0.035)
    jingles = sum(np.sin(2 * np.pi * f * t + RNG.random() * 6.283) for f in (5150, 6230, 7410, 8770, 10230))
    s = filt(noise(n), "band", [5000, 13000]) * env + 0.25 * jingles * env * np.exp(-t / 0.06)
    return norm(s) * vel


def snap(vel=1.0):
    n = int(0.15 * SR)
    t = tt(n)
    s = filt(noise(n), "band", [1800, 4200]) * np.exp(-t / 0.012) + 0.4 * np.sin(2 * np.pi * 2100 * t) * np.exp(-t / 0.006)
    return norm(s) * vel


def syndrum(f0, vel=1.0):
    """Tom électronique disco : la hauteur tombe d'une octave et demie (« piou »)."""
    n = int(0.55 * SR)
    t = tt(n)
    f = f0 * (0.32 + 0.68 * np.exp(-t / 0.11))
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.28)
    s += filt(noise(n), "band", [1000, 6000]) * np.exp(-t / 0.004) * 0.25
    return np.tanh(1.3 * s) * vel


def crash(vel=1.0):
    n = int(2.2 * SR)
    t = tt(n)
    s = filt(noise(n), "high", 4200, order=3) * (1 - np.exp(-t / 0.002)) * np.exp(-t / 0.75)
    s += 0.3 * filt(noise(n), "band", [3000, 9000]) * np.exp(-t / 0.05)
    return norm(s) * vel


# ------------------------------------------------------------------ instruments
def bass_note(m, dur, vel=1.0):
    """Basse synthé : dent de scie + carré, filtre qui se referme en 70 ms, sous-basse sinusoïdale."""
    n = int((dur + 0.08) * SR)
    t = tt(n)
    f = midi(m)
    raw = 0.6 * saw(f, n) + 0.4 * (saw(f, n) - saw(f, n, 0.5))
    e = np.exp(-t / 0.07)
    tone = filt0(raw, "low", 2600) * e + filt0(raw, "low", 520) * (1 - e)
    env = (1 - np.exp(-t / 0.003)) * (0.8 + 0.2 * np.exp(-t / 0.15)) * gate(t, dur, 0.03)
    return np.tanh(1.4 * (0.75 * np.sin(2 * np.pi * f * t) + 0.55 * tone)) * env * vel


def strings(notes, dur, attack=0.25, release=0.6, bright=4200.0, voices=5, vib=0.0035):
    """Section de cordes synthétiques (ensemble de dents de scie désaccordées, vibrato lent)."""
    n = int((dur + release + 0.05) * SR)
    t = tt(n)
    out = np.zeros((2, n))
    half = (voices - 1) / 2
    for m in notes:
        f0 = midi(m)
        for k in range(voices):
            det = (k - half) / half * 0.12
            f = f0 * 2 ** (det / 12) * (1 + vib * np.sin(2 * np.pi * (5.2 + 0.6 * RNG.random()) * t + RNG.random() * 6.283))
            out += stereo(saw(f, n, RNG.random()), (k - half) / half * 0.8)
    out = filt(filt(out, "low", bright), "high", 260)
    env = np.minimum(1, t / attack) ** 1.5 * gate(t, dur, release)
    return out * env / (len(notes) * voices ** 0.5)


def string_run(seq, step, hold, vel=1.0, bright=6500.0):
    """Montée de cordes legato : une note toutes les `step` s, la dernière tenue `hold` s."""
    dur = step * (len(seq) - 1) + hold
    n = int((dur + 0.5) * SR)
    t = tt(n)
    idx = np.minimum((t / step).astype(int), len(seq) - 1)
    lf = np.log(np.array([midi(m) for m in seq]))[idx]
    k = int(0.012 * SR)
    lf = np.convolve(np.concatenate([np.full(k - 1, lf[0]), lf]), np.ones(k) / k, "valid")
    f = np.exp(lf) * (1 + 0.003 * np.sin(2 * np.pi * 5.5 * t))
    out = np.zeros((2, n))
    for d, pan in ((-0.1, -0.6), (0.0, 0.0), (0.1, 0.6)):
        out += stereo(saw(f * 2 ** (d / 12), n, RNG.random()), pan)
    out = filt(filt(out, "low", bright), "high", 250)
    run = step * (len(seq) - 1)
    since = np.where(t < run + step, t % step, t - run)  # temps depuis le dernier coup d'archet
    bow = 1 + 0.25 * (1 - np.exp(-since / 0.004)) * np.exp(-since / 0.03)
    env = (0.35 + 0.65 * np.clip(t / run, 0, 1) ** 1.5) * np.minimum(1, t / 0.02) * gate(t, dur, 0.35) * bow
    return out * env * vel / 3


def stab(notes, dur, vel=1.0):
    """Accord « cuivres synthé » : le filtre s'ouvre en 12 ms puis se referme à moitié."""
    n = int((dur + 0.15) * SR)
    t = tt(n)
    raw = np.zeros((2, n))
    for m in notes:
        for d, pan in ((-0.07, -0.5), (0.07, 0.5)):
            raw += stereo(saw(midi(m) * 2 ** (d / 12), n, RNG.random()), pan)
    e = (1 - np.exp(-t / 0.012)) * (0.45 + 0.55 * np.exp(-t / 0.09))
    tone = filt0(raw, "low", 5200) * e + filt0(raw, "low", 900) * (1 - e)
    env = (1 - np.exp(-t / 0.004)) * (0.75 + 0.25 * np.exp(-t / 0.1)) * gate(t, dur, 0.06)
    return filt(tone, "high", 200) * env * vel / len(notes)


def ks(m, dur, rho=0.996, tone=4000.0):
    """Corde pincée Karplus-Strong, hauteur exacte par rééchantillonnage."""
    f = midi(m)
    L = max(2, int(SR / f - 0.5))
    f_ks = SR / (L + 0.5)
    n_out = int(dur * SR)
    n_ks = int(n_out * f / f_ks) + 4
    exc = filt(noise(L + 1), "low", tone)
    exc -= exc.mean()
    x = np.zeros(n_ks)
    x[: L + 1] = exc[: n_ks]
    a = np.zeros(L + 2)
    a[0] = 1.0
    a[L] -= rho / 2
    a[L + 1] -= rho / 2
    y = lfilter([1.0], a, x)
    return norm(np.interp(np.arange(n_out) * f / f_ks, np.arange(n_ks), y))


def guitar(notes, dur, up=False, muted=False):
    """Guitare rythmique disco : accord gratté (bas → haut ou haut → bas), ouvert ou étouffé."""
    seq = notes[::-1] if up else notes
    strum = 0.004 if muted else 0.006
    n = int((dur + 0.1 + strum * len(notes)) * SR)
    t = tt(n)
    out = np.zeros(n)
    for k, m in enumerate(seq):
        s = ks(m, dur + 0.1, rho=0.94 if muted else 0.992, tone=3500 if muted else 5200)
        i0 = int(k * strum * SR)
        out[i0:i0 + len(s)] += s[: n - i0]
    out += filt(noise(n), "band", [2000, 7000]) * np.exp(-t / 0.002) * 0.3
    return norm(filt(out, "band", [180, 6500]) * gate(t, dur, 0.02))


def pizz(m, vel=1.0):
    s = ks(m, 0.6, rho=0.985, tone=2800)
    t = tt(len(s))
    return norm((0.6 * s + 0.6 * filt(s, "band", [250, 2500])) * np.exp(-t / 0.25)) * vel


def harp(m, vel=1.0, dec=1.1):
    s = ks(m, 1.8, rho=0.998, tone=7000)
    t = tt(len(s))
    return s * (1 - np.exp(-t / 0.002)) * np.exp(-t / dec) * vel


def vibes(m, vel=1.0, dur=2.2):
    """Vibraphone : partiels 1, 4, 10 et moteur de trémolo."""
    n = int(dur * SR)
    t = tt(n)
    f = midi(m)
    s = np.sin(2 * np.pi * f * t) * np.exp(-t / 1.4) + 0.22 * np.sin(2 * np.pi * 4 * f * t) * np.exp(-t / 0.35)
    s += 0.05 * np.sin(2 * np.pi * 10 * f * t) * np.exp(-t / 0.07)
    trem = 1 - 0.28 * (0.5 - 0.5 * np.cos(2 * np.pi * 5.6 * t))
    mallet = filt(noise(n), "band", [1500, 6000]) * np.exp(-t / 0.0025) * 0.08
    return (s * trem + mallet) * (1 - np.exp(-t / 0.0015)) * vel


def celesta(m, vel=1.0, dur=1.8):
    n = int(dur * SR)
    t = tt(n)
    f = midi(m)
    s = np.sin(2 * np.pi * f * t) * np.exp(-t / 0.9) + 0.35 * np.sin(2 * np.pi * 2 * f * t) * np.exp(-t / 0.35)
    s += 0.12 * np.sin(2 * np.pi * 3 * f * t) * np.exp(-t / 0.18) + 0.06 * np.sin(2 * np.pi * 4.2 * f * t) * np.exp(-t / 0.08)
    return s * (1 - np.exp(-t / 0.001)) * vel


FORMANTS = ((800, 1.0), (1150, 0.5), (2900, 0.25))  # voyelle « a »


def choir(notes, dur, attack=0.35, release=0.8):
    """Chœur « aah » : dents de scie vibrées passées dans trois formants."""
    n = int((dur + release + 0.05) * SR)
    t = tt(n)
    src = np.zeros((2, n))
    for m in notes:
        for k, pan in enumerate((-0.7, 0.0, 0.7)):
            f = midi(m) * 2 ** ((k - 1) * 0.08 / 12) * (1 + 0.004 * np.sin(2 * np.pi * (4.8 + 0.4 * k) * t + RNG.random() * 6.283))
            src += stereo(saw(f, n, RNG.random()), pan)
    out = sum(g * filt(src, "band", [fc / 1.15, fc * 1.15]) for fc, g in FORMANTS)
    out += 0.02 * filt(np.stack([noise(n), noise(n)]), "band", [700, 3000])
    env = np.minimum(1, t / attack) ** 1.5 * gate(t, dur, release)
    return out * env / len(notes)


# ------------------------------------------------------------------ effets
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
        out[i0:i0 + len(seg)] += filt(seg, "band", [max(40, fc / 1.6), min(20000, fc * 1.6)]) * np.hanning(len(seg))
    tone_f = 180 * (1200 / 180) ** (t / dur)
    tone = (2 * ((np.cumsum(tone_f) / SR) % 1.0) - 1) * 0.12
    return (norm(out) + filt(tone, "low", 3000)) * (t / dur) ** 2.2 * vel


def downlifter(dur, vel=1.0):
    return riser(dur, 6000, 300, vel)[::-1] * np.linspace(1, 0.2, int(dur * SR)) ** 0.5


def impact(vel=1.0, big=True):
    n = int((2.4 if big else 1.2) * SR)
    t = tt(n)
    f = 32 + 48 * np.exp(-t / 0.18)
    sub = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / (0.9 if big else 0.45))
    burst = filt(noise(n), "low", 2600) * np.exp(-t / 0.09) * 0.55
    return np.tanh(1.4 * (sub + burst)) * vel


def rev_cymbal(dur, vel=1.0):
    n = int(dur * SR)
    t = tt(n)
    return norm(filt(noise(n), "high", 3500, order=3) * (t / dur) ** 3) * vel


# ------------------------------------------------------------------ harmonie (fa majeur)
ROOT = {"F": 29, "Dm": 38, "Gm": 31, "C9sus": 36, "C9": 36, "Bb": 34, "Am": 33}  # octave basse
STR = {  # nappe de cordes
    "F": [53, 60, 64, 69], "Dm": [50, 57, 60, 65], "Gm": [55, 62, 65, 70], "C9sus": [53, 58, 62, 67],
    "C9": [52, 58, 62, 67], "Bb": [57, 62, 65, 72], "Am": [52, 57, 60, 67],
}
STAB = {  # (position A, position B) des accords cuivres
    "F": ([65, 69, 72, 76], [69, 72, 76, 81]), "Dm": ([65, 69, 72, 74], [69, 72, 74, 77]),
    "Gm": ([65, 70, 74, 77], [70, 74, 77, 81]), "C9sus": ([65, 70, 74, 79], [67, 72, 77, 82]),
    "C9": ([64, 70, 74, 79], [70, 74, 76, 82]), "Bb": ([65, 69, 72, 74], [69, 72, 77, 81]),
    "Am": ([64, 67, 72, 76], [67, 72, 76, 79]),
}
GTR = {
    "F": [60, 65, 69, 72], "Dm": [62, 65, 69, 72], "Gm": [62, 65, 70, 74], "C9sus": [62, 65, 70, 72],
    "C9": [64, 67, 70, 74], "Bb": [62, 65, 69, 72], "Am": [60, 64, 67, 72],
}

# (début, fin, accord) — intro et sortie sur C9sus4 : la boucle retombe sur le fa de 1,8 s
HARMONY = [
    (0.0, 1.8, "C9sus"),
    (1.8, 3.8, "F"), (3.8, 5.8, "Dm"), (5.8, 7.8, "Gm"), (7.8, 8.8, "C9sus"), (8.8, 9.8, "C9"),
    (9.8, 11.8, "F"), (11.8, 13.8, "Dm"), (13.8, 15.8, "Gm"), (15.8, 16.8, "C9sus"), (16.8, 17.8, "C9"),
    (17.8, 19.8, "F"), (19.8, 20.8, "Bb"), (20.8, 21.8, "Am"),
    (21.8, 22.8, "Gm"), (22.8, 23.0, "C9"), (23.0, 23.8, "F"),
    (23.8, 24.8, "Bb"), (24.8, TOTAL + TAIL, "C9sus"),
]
# nappe : silence de 22,8 à 23,0 s (respiration avant la signature)
PAD = [h for h in HARMONY if h[2] != "C9" or h[0] != 22.8]
PAD[-1] = (24.8, TOTAL, "C9sus")  # relâchée sur 0,6 s après la dernière image, repliée sur l'intro

# sections de groove : mesure n → rôle (même découpage que la vidéo)
GROOVE = {0: "ui", 1: "ui", 2: "full", 3: "lite", 4: "drop", 5: "drop", 6: "full", 7: "full", 8: "drop", 9: "break", 10: "build", 11: "drop"}

# (pas, intervalle, durée en pas, vélocité) : octaves disco et notes fantômes
BASS_PAT = [(0, 0, 1.6, 1.0), (2, 12, 1, 0.9), (4, 0, 1, 0.95), (6, 12, 1, 0.9), (7, 12, 0.5, 0.5),
            (8, 0, 1, 0.95), (10, 12, 1, 0.9), (12, 0, 1, 0.95), (14, 12, 1, 0.9), (15, 7, 0.6, 0.7)]
# accroche des drops : accords en clave 3-3-4-2 (pas, durée en pas, position)
HOOK = [(0, 2, 0), (3, 2, 0), (6, 3, 1), (10, 1, 0), (12, 3, 1)]

# détails visuels : (instant, instrument, note) — chaque apparition a sa note, dans l'accord du moment
DETAILS = [
    (0.267, "vib", 84), (0.367, "vib", 91),  # S01 nom et handle
    (2.733, "vib", 81), (2.8, "vib", 88),  # S02 résultat révélé
    (3.933, "pizz", 74), (4.0, "pizz", 77), (4.067, "pizz", 81),  # S03 trois vignettes
    (7.3, "vib", 86),  # S04 sélection douce
    (10.067, "cel", 88), (10.067, "vib", 81),  # S06 cœur
    (11.8, "harp", 81), (11.9, "harp", 84), (12.0, "harp", 86),  # S07 trois inserts
    (12.1, "cel", 89), (12.167, "cel", 93), (12.233, "cel", 96),  # S07 traits et repères
    (14.5, "pizz", 74), (14.7, "pizz", 79), (14.9, "pizz", 82),  # S08 Modèle, Couleur, Disponibilité
    (15.9, "vib", 91),  # S08 pulsation de la sélection
    (19.6, "vib", 93), (19.6, "cel", 96),  # S10 cœur
    (20.767, "harp", 81), (20.833, "harp", 88),  # S11 inserts
    (24.0, "cel", 93),  # S13 halo du bouton
]


def chord_at(t):
    for a, b, c in HARMONY:
        if a <= t < b:
            return c
    return "C9sus"


def role_at(n, t):
    if n == 1 and t >= 5.3 - EPS:  # le groove complet entre sur la coupe de S04 (4e temps)
        return "full"
    return GROOVE[n]


def stopped(n, t):
    """Coupures avant les impacts (9,6 / 17,8 / 23,0 s) et avant la boucle (25,5 s)."""
    cuts = {3: 9.3, 7: 17.3, 10: 22.8, 11: 25.5}
    return n in cuts and t >= cuts[n] - EPS


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", required=True)
    args = ap.parse_args()
    project = Path(args.project).resolve()

    drums, perc, bass, gtr, keys, strs, voix, det, sec, fx = (Bus() for _ in range(10))
    kicks = []

    # ---------------- batterie : quatre temps disco
    for n, role in GROOVE.items():
        for s in range(16):
            t = bar(n, s)
            if stopped(n, t):
                continue
            r = role_at(n, t)
            sw = STEP * 0.08 if s % 2 else 0.0
            if r == "break":  # pause : claquements de doigts et charleston léger
                if s in (4, 12):
                    drums.add(snap(0.8), t, 0.3)
                    perc.add(tamb(0.5), t, 0.16, pan=-0.4)
                if s % 4 == 2:
                    perc.add(hat(False, 0.3), t, 0.3, pan=0.35)
                continue
            if s % 4 == 0:
                drums.add(kick({"ui": 0.8, "lite": 0.9}.get(r, 1.0)), t, 0.72)
                kicks.append(t)
            if s in (4, 12) and r in ("full", "drop", "lite"):
                drums.add(snare(0.9), t, 0.36)
                drums.add(clap(0.85), t, 0.3)
                if r != "lite":
                    perc.add(tamb(0.9), t, 0.26, pan=-0.4)
            if r in ("full", "drop"):
                if s % 4 == 2:
                    perc.add(hat(True, 0.8), t, 0.38, pan=0.25)
                else:
                    perc.add(hat(False, 0.5 if s % 2 == 0 else 0.28), t + sw, 0.36, pan=0.35)
                if r == "drop" and s % 2:
                    perc.add(tamb(0.3), t + sw, 0.14, pan=-0.4)
            elif s % 2 == 0:
                perc.add(hat(False, 0.55 if s % 4 == 2 else 0.32), t, 0.36, pan=0.35)
                if r == "lite" and s % 4 == 2:
                    perc.add(hat(True, 0.5), t, 0.24, pan=0.25)
    # roulements et syndrums vers chaque coupe forte
    for k, f0 in enumerate((300, 240)):  # appel vers l'ouverture de S04 (5,3 s)
        drums.add(syndrum(f0, 0.7), 5.05 + k * STEP, 0.34, pan=0.2 - 0.4 * k)
    for k in range(3):  # S05 : caisse claire 8,8 → 9,05 s (9,2 s reste libre pour le clic d'envoi)
        drums.add(snare(0.5 + 0.15 * k), 8.8 + k * STEP, 0.3)
    for k, f0 in enumerate((210, 270, 350)):  # syndrums en quintolets jusqu'à l'impact de 9,6 s
        drums.add(syndrum(f0, 0.8 + 0.1 * k), 9.3 + 0.1 * k, 0.4, pan=-0.3 + 0.3 * k)
    for k in range(8):  # S08 → S09 : triples croches 17,3 → 17,8 s
        drums.add(snare(0.35 + 0.08 * k), 17.3 + k * STEP / 2, 0.3)
    for k in range(4):  # S12 : montée 21,8 → 22,8 s
        drums.add(snare(0.3 + 0.06 * k), 21.8 + k * STEP, 0.28)
    for k in range(8):
        drums.add(snare(0.5 + 0.06 * k), 22.3 + k * STEP / 2, 0.28)
    for k, f0 in enumerate((420, 340, 270, 210)):  # descente de syndrums vers le drop final (23,8 s)
        drums.add(syndrum(f0, 0.85), 23.3 + k * STEP, 0.4, pan=0.35 - 0.23 * k)
    for tc, v in ((5.3, 0.7), (9.8, 1.0), (17.8, 1.0), (23.8, 1.0)):
        fx.add(crash(v), tc, 0.3)

    # ---------------- basse disco en octaves
    for n, role in GROOVE.items():
        if role == "break":
            continue
        for s, iv, ln, v in BASS_PAT:
            t = bar(n, s)
            if stopped(n, t):
                continue
            c = chord_at(t + 0.001)
            bass.add(bass_note(ROOT[c] + iv, ln * STEP * 0.9, v * (0.8 if role_at(n, t) == "ui" else 1.0)), t, 0.55)
    bass.add(bass_note(ROOT["Bb"], 0.95, 0.7), 19.8, 0.45)  # pause : notes tenues
    bass.add(bass_note(ROOT["Am"], 0.95, 0.7), 20.8, 0.45)
    bass.add(bass_note(ROOT["F"] + 12, 0.7, 0.8), 23.0, 0.5)  # signature
    bass.add(bass_note(ROOT["C9sus"], 1.2, 0.6), 25.5, 0.4)  # sortie

    # ---------------- guitare rythmique : double-croches étouffées, accords ouverts sur les contretemps
    cache = {}
    for n, role in GROOVE.items():
        if role not in ("ui", "full", "drop"):
            continue
        for s in range(16):
            t = bar(n, s)
            if stopped(n, t) or s % 4 == 0:
                continue
            c = chord_at(t + 0.001)
            open_, up = s % 4 == 2, s % 2 == 1
            key = (c, open_, up, s % 3)
            if key not in cache:
                cache[key] = guitar(GTR[c], 0.09 if open_ else 0.05, up=up, muted=not open_)
            v = (0.85 if open_ else 0.38) * (0.8 if role_at(n, t) == "ui" else 1.0)
            gtr.add(cache[key], t + (STEP * 0.08 if s % 2 else 0.0), v, pan=0.35 if up else -0.35)

    # ---------------- accroche des drops : accords cuivres en clave
    for n in (4, 5, 8, 11):
        for s, ln, pos in HOOK:
            t = bar(n, s)
            if stopped(n, t) or (n == 5 and s < 6):  # S07 : les détails passent d'abord
                continue
            keys.add(stab(STAB[chord_at(t + 0.001)][pos], ln * STEP * 0.85), t, 0.5)
    keys.add(stab(STAB["Gm"][1], 0.14, 0.9), 22.4, 0.42)  # S12 : appui sur Message

    # ---------------- cordes : nappe, attaques sur les drops, contre-chant, montées
    for a, b, c in PAD:  # intro : attaque lente, fondu enchaîné avec la queue repliée de la sortie
        attack = 0.6 if a == 0.0 else 0.12 if a in (9.8, 17.8, 23.0) else 0.25
        strs.add(strings(STR[c], b - a, attack=attack, release=0.6 if b == TOTAL else 0.5), a, 1.0)
    for t0 in (9.8, 17.8):
        strs.add(strings([m + 12 for m in STR["F"]], 0.25, attack=0.008, release=0.45, bright=9000), t0, 0.7)
    for t0, d, m in ((5.8, 1.0, 86), (6.8, 1.0, 84), (7.8, 1.0, 82), (8.8, 0.9, 82),
                     (13.8, 2.0, 86), (15.8, 1.0, 84), (16.8, 0.95, 82)):
        strs.add(strings([m - 12, m], d, attack=0.18, release=0.35, bright=7000, voices=4), t0, 0.5)
    for t0, seq, hold in ((1.3, [72, 74, 76, 77, 79, 81], 0.45),  # vers S02 : do → la
                          (4.8, [74, 76, 77, 79, 81, 84, 86], 0.35),  # vers S04 : ré → ré
                          (17.3, [70, 72, 74, 76, 77, 79, 81], 0.4)):  # vers S09 : si♭ → la
        strs.add(string_run(seq, 0.5 / (len(seq) - 1), hold, 0.9), t0, 0.7)
    for a, b, notes, g in ((0.0, 1.8, [62, 65, 67], 0.6), (19.8, 20.8, [62, 65, 69], 1.0),
                           (20.8, 21.8, [60, 64, 67], 1.0), (23.0, 23.8, [60, 65, 69], 0.8)):
        voix.add(choir(notes, b - a), a, g)

    # ---------------- détails : harpe, vibraphone, célesta, pizzicati
    # scènes d'interface (S01–S05, widgets S08) : sans écho, pour laisser lisibles clics et frappes du mix
    def bus_for(t):
        return sec if t < 9.6 or 14.4 <= t < 15.0 else det

    def gliss(notes, t0, dt, vel, gain, p0=-0.6, p1=0.6):
        for k, m in enumerate(notes):
            pan = p0 + (p1 - p0) * k / max(1, len(notes) - 1)
            bus_for(t0).add(harp(m, vel * (0.7 + 0.3 * k / len(notes)), dec=0.55), t0 + k * dt, gain, pan=pan)

    gliss([60, 62, 65, 67, 70, 72, 74, 77, 79, 82], 0.0, 0.026, 0.8, 0.4)  # S01 : ouverture
    gliss([65, 69, 72, 77, 81, 84, 89, 93], 17.8, 0.035, 0.8, 0.36)  # S09 : révélation du showroom
    gliss([91, 89, 86, 84, 82, 79, 77, 74, 72], 25.5, 0.05, 0.7, 0.32, 0.6, -0.6)  # S14 : vers la boucle
    for t, kind, m in DETAILS:
        if kind == "vib":
            bus_for(t).add(vibes(m, 0.85), t, 0.42, pan=-0.25)
        elif kind == "pizz":
            bus_for(t).add(pizz(m, 0.9), t, 0.5, pan=0.3)
        elif kind == "harp":
            bus_for(t).add(harp(m, 0.9), t, 0.45, pan=0.2)
        else:
            bus_for(t).add(celesta(m, 0.8), t, 0.36, pan=-0.15)
    for s, m in ((0, 81), (2, 84), (4, 86), (12, 88), (14, 84)):  # pause : phrase de vibraphone
        det.add(vibes(m, 0.7), bar(9, s), 0.32, pan=-0.3)
    for k, m in enumerate((84, 89, 93, 96)):  # S13 : signature sonore (do – fa – la – do)
        det.add(celesta(m, 0.9, 2.4), 23.0 + 0.09 * k, 0.4, pan=-0.3 + 0.2 * k)
    det.add(vibes(96, 0.6, 2.6), 23.27, 0.3, pan=0.3)

    # ---------------- effets : montées, impacts, cymbales inversées, descente
    for t0, t1, v in ((8.8, 9.6, 0.75), (17.0, 17.8, 0.7), (21.9, 22.8, 0.8)):
        fx.add(riser(t1 - t0, vel=v), t0, 0.3)
    for t, v, big in ((0.167, 0.5, False), (9.6, 1.0, True), (17.8, 0.9, True), (23.0, 0.95, True)):
        fx.add(impact(v, big), t, 0.58)
    for t1, d, v in ((5.3, 0.5, 0.7), (13.9, 0.4, 0.5), (20.7, 0.35, 0.45), (23.0, 0.3, 0.5), (TOTAL, 0.55, 0.6)):
        fx.add(rev_cymbal(d, v), t1 - d, 0.22)
    fx.add(downlifter(0.8, 0.8), 25.5, 0.26)

    # ---------------- traitements : pompage, filtres French touch, espace
    strs.x *= sidechain(kicks, 0.55, 0.17)
    bass.x *= sidechain(kicks, 0.35, 0.09)
    gtr.x *= sidechain(kicks, 0.2, 0.08)
    keys.x *= sidechain(kicks, 0.25, 0.1)

    E = TOTAL + TAIL
    ui = lambda lo, hi, top: [(0, top), (1.8 - 0.01, top), (1.8, lo), (5.25, hi), (5.3, top), (E, top)]  # noqa: E731
    drums.x = tv_lowpass(drums.x, ui(800, 2600, 18000), order=1.2)
    perc.x = tv_lowpass(perc.x, ui(2400, 6000, 18000), order=1.2)
    bass.x = tv_lowpass(filt(bass.x, "high", 30), ui(420, 1400, 6000), order=1.5)
    gtr.x = tv_lowpass(gtr.x, ui(650, 2800, 18000), order=1.5, res_db=3)
    str_gain = curve([(0, 0.9), (1.79, 0.9), (1.8, 0.45), (5.29, 0.45), (5.3, 0.7), (8.8, 0.7), (9.6, 1.0),
                      (9.8, 0.6), (19.79, 0.6), (19.8, 0.95), (21.8, 0.95), (22.8, 1.05), (23.8, 0.8), (25.5, 0.8),
                      (25.7, 0.95), (E, 0.95)])
    str_keys = [(0, 1100), (0.55, 5200), (1.79, 5200), (1.8, 1500), (5.25, 2800), (5.3, 7000), (8.8, 4000), (9.6, 9000),
                (19.79, 9000), (19.8, 4500), (21.8, 3000), (22.8, 9000), (25.5, 9000), (TOTAL, 1100), (E, 1100)]
    strs.x = tv_lowpass(strs.x * str_gain, str_keys, order=1.5, res_db=2)
    voix.x = tv_lowpass(voix.x, str_keys, order=1.5)

    ir_room = make_ir(0.9, 0.008, 6500)
    ir_plate = make_ir(1.8, 0.015, 7000)
    ir_hall = make_ir(2.6, 0.03, 5000)
    stems = {
        "batterie": drums.x + reverb(drums.x, ir_room, 0.1),
        "percussions": perc.x + reverb(perc.x, ir_room, 0.08),
        "basse": bass.x,
        "guitare": gtr.x + reverb(gtr.x, ir_plate, 0.12),
        "cuivres": keys.x + reverb(keys.x, ir_plate, 0.2),
        "cordes": strs.x + reverb(strs.x, ir_plate, 0.25),
        "choeur": voix.x + reverb(voix.x, ir_hall, 0.35),
        "details": (det.x + pingpong(det.x, 0.375, 0.3, 0.24) + reverb(det.x, ir_hall, 0.24)
                    + sec.x + reverb(sec.x, ir_plate, 0.18)),
        "effets": fx.x + reverb(fx.x, ir_hall, 0.35),
    }
    gains = {"batterie": 1.0, "percussions": 2.6, "basse": 1.8, "guitare": 1.1, "cuivres": 1.4, "cordes": 0.65,
             "choeur": 0.5, "details": 0.8, "effets": 0.7}
    mix = sum(stems[k] * gains[k] for k in stems)
    # égalisation de bus : moins de sous-grave (inaudible au téléphone), plus d'air
    mix = mix - (1 - 10 ** (-4 / 20)) * filt(mix, "low", 70) + (10 ** (1.5 / 20) - 1) * filt(mix, "high", 6000)
    mix = np.tanh(mix * 0.9) / 0.9  # colle de bus : légère saturation

    # boucle : la queue au-delà de la dernière image revient au début
    def fold(x):
        y = x[:, :NLOOP].copy()
        y[:, : x.shape[1] - NLOOP] += x[:, NLOOP:]
        return y

    out = fold(mix)
    scale = 0.89 / (np.abs(out).max() + 1e-9)
    dst = project / "assets" / "audio" / "musique_daya_nudisco_120bpm.wav"
    write_wav(dst, out * scale)
    stem_dir = project / ".hyperframes" / "stems"
    stem_dir.mkdir(parents=True, exist_ok=True)
    for old in stem_dir.glob("*.wav"):
        old.unlink()
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
