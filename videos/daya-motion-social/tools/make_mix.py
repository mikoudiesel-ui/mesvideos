#!/usr/bin/env python3
"""Mix audio de la maquette BIKINIS SHOP / @daya_na990 (26,4667 s, 48 kHz stéréo).

Base : assets/audio/musique_daya_afrohouse_120bpm.wav, la musique originale composée pour la vidéo
(tools/make_music.py ; le son témoin du dossier reste dans reference/audio/). On y ajoute les bruitages
d'interface synthétisés localement sur les cues de reference/TIMELINE_14_SCENES.json, recalés sur les
animations réelles (saisie du handle, clics, widgets) ; les impacts et cloches déjà joués par la musique
ne sont pas doublés. Puis gain vers −16 LUFS intégrés et limiteur true-peak (plafond −1,5 dBTP)
pour garder ≤ −1 dBTP après AAC.

    python3 -I tools/make_mix.py --project videos/daya-motion-social
"""

import argparse
import json
import math
import re
import subprocess
import wave
from pathlib import Path

import numpy as np
from scipy.signal import resample_poly

SR = 48000
FPS = 30
RNG = np.random.default_rng(20261011)


def tt(n):
    return np.arange(n) / SR


def noise(n):
    return RNG.standard_normal(n)


def band(x, lo=None, hi=None, order=4):
    n = x.shape[-1]
    spec = np.fft.rfft(x, axis=-1)
    f = np.fft.rfftfreq(n, 1 / SR)
    g = np.ones_like(f)
    if hi:
        g *= 1 / np.sqrt(1 + (f / hi) ** (2 * order))
    if lo:
        g *= 1 / np.sqrt(1 + (lo / np.maximum(f, 1e-3)) ** (2 * order))
    return np.fft.irfft(spec * g, n=n, axis=-1)


def sweep_band(x, f0, f1, q=1.2):
    """Band-pass dont la fréquence centrale glisse de f0 à f1 (blocs de 10 ms)."""
    out = np.zeros_like(x)
    blk = int(0.01 * SR)
    nb = int(math.ceil(len(x) / blk))
    win = np.hanning(2 * blk)
    for b in range(nb):
        fc = f0 * (f1 / f0) ** (b / max(1, nb - 1))
        i0 = max(0, b * blk - blk // 2)
        seg = x[i0:i0 + 2 * blk]
        if len(seg) < 8:
            continue
        y = band(seg, lo=fc / q, hi=fc * q, order=2) * win[:len(seg)]
        out[i0:i0 + len(seg)] += y
    return out


# ---------------------------------------------------------------- bruitages
def impact_doux():
    n = int(0.55 * SR)
    t = tt(n)
    f = 44 + 70 * np.exp(-t / 0.05)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.22)
    tex = band(noise(n), lo=200, hi=1800) * np.exp(-t / 0.03) * 0.25
    return np.tanh(1.4 * (body + tex)) * 0.9


def souffle(dur=0.35, f0=600, f1=2400, gain=0.5, reverse=False):
    n = int(dur * SR)
    t = tt(n)
    env = np.sin(np.pi * np.clip(t / dur, 0, 1)) ** 1.6
    s = sweep_band(noise(n), f0, f1) * env
    s = s / (np.abs(s).max() + 1e-9) * gain
    if reverse:
        s = s[::-1] * (np.linspace(0.3, 1, n) ** 2)
    return s


def clic(freq=2600, gain=0.45, dur=0.05):
    n = int(dur * SR)
    t = tt(n)
    tick = band(noise(n), lo=2500, hi=9000) * np.exp(-t / 0.0025)
    tone = np.sin(2 * np.pi * freq * t) * np.exp(-t / 0.012) * 0.6
    body = np.sin(2 * np.pi * 180 * t) * np.exp(-t / 0.02) * 0.5
    s = tick + tone + body
    return s / (np.abs(s).max() + 1e-9) * gain


def touche(gain=0.35):
    n = int(0.03 * SR)
    t = tt(n)
    s = band(noise(n), lo=1800, hi=7000) * np.exp(-t / 0.004)
    s += np.sin(2 * np.pi * 1400 * t) * np.exp(-t / 0.006) * 0.3
    return s / (np.abs(s).max() + 1e-9) * gain


def pop(freq=880, gain=0.4):
    n = int(0.16 * SR)
    t = tt(n)
    f = freq * (1 + 0.6 * np.exp(-t / 0.012))
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.05)
    s += 0.25 * np.sin(4 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.02)
    return s * (1 - np.exp(-t / 0.002)) * gain


def carillon(notes, step=0.07, gain=0.32, dur=1.4):
    """Petite signature : arpège de cloches douces."""
    n = int((dur + step * len(notes)) * SR)
    out = np.zeros(n)
    for k, m in enumerate(notes):
        f0 = 440 * 2 ** ((m - 69) / 12)
        nn = int(dur * SR)
        t = tt(nn)
        s = np.zeros(nn)
        for ratio, amp, dec in ((1, 1, 0.9), (2.0, 0.4, 0.45), (3.0, 0.18, 0.25), (4.2, 0.08, 0.12)):
            s += amp * np.sin(2 * np.pi * f0 * ratio * t) * np.exp(-t / dec)
        s *= 1 - np.exp(-t / 0.003)
        i0 = int(k * step * SR)
        out[i0:i0 + nn] += s
    return out / (np.abs(out).max() + 1e-9) * gain


def coeur(gain=0.42):
    a = pop(1046, 0.8)
    b = pop(1568, 0.6)
    out = np.zeros(len(a) + int(0.06 * SR))
    out[:len(a)] += a
    out[int(0.06 * SR):] += b
    return out / (np.abs(out).max() + 1e-9) * gain


# ---------------------------------------------------------------- utilitaires
def read_wav(path):
    with wave.open(str(path), "rb") as w:
        assert w.getframerate() == SR and w.getnchannels() == 2 and w.getsampwidth() == 2
        x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float64) / 32768
    return x.reshape(-1, 2).T.copy()


def write_wav(path, x):
    y = np.clip(x, -1, 1)
    pcm = (y.T * 32767).round().astype(np.int16)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())


def measure(path):
    out = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-af",
                          "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
    summary = out[out.rfind("Summary:"):]
    i = float(re.search(r"I:\s+(-?[\d.]+) LUFS", summary).group(1))
    tp = float(re.search(r"Peak:\s+(-?[\d.]+) dBFS", summary).group(1))
    return i, tp


def true_peak_limit(x, ceiling_db=-1.5, attack=0.0015, release=0.08):
    ceiling = 10 ** (ceiling_db / 20)
    over = np.abs(resample_poly(x, 4, 1, axis=1)).max(axis=0)
    peak = over.reshape(-1, 4).max(axis=1)[: x.shape[1]]
    need = np.minimum(1.0, ceiling / np.maximum(peak, 1e-9))
    la = int(attack * SR)
    # anticipation : le gain descend avant le pic (minimum glissant vers l'avant)
    padded = np.concatenate([need, np.ones(la)])
    ahead = np.min(np.lib.stride_tricks.sliding_window_view(padded, la + 1), axis=1)[: len(need)]
    g = np.empty_like(ahead)
    acc = 1.0
    rel = math.exp(-1 / (release * SR))
    for i, v in enumerate(ahead):
        acc = v if v < acc else v + (acc - v) * rel
        g[i] = acc
    k = np.hanning(2 * la + 1)
    g = np.convolve(np.concatenate([np.full(la, g[0]), g, np.full(la, g[-1])]), k / k.sum(), "valid")
    return x * np.minimum(g, ahead)


def place(bus, sig, at, gain=1.0, pan=0.0):
    if sig.ndim == 1:
        a = (pan + 1) * math.pi / 4
        sig = np.stack([sig * math.cos(a), sig * math.sin(a)]) * math.sqrt(2)
    i0 = int(round(at * SR))
    n = min(sig.shape[1], bus.shape[1] - i0)
    if n > 0:
        bus[:, i0:i0 + n] += sig[:, :n] * gain


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", required=True)
    ap.add_argument("--sfx-gain", type=float, default=1.3)
    ap.add_argument("--bed", default="assets/audio/musique_daya_afrohouse_120bpm.wav")
    ap.add_argument("--stems", action="store_true", help="écrit aussi les pistes séparées dans .hyperframes/")
    args = ap.parse_args()
    project = Path(args.project).resolve()
    timeline = json.loads((project / "reference" / "TIMELINE_14_SCENES.json").read_text())
    bed = read_wav(project / args.bed)
    total = timeline["total_frames"] / timeline["fps"]
    assert abs(bed.shape[1] / SR - total) < 1e-3
    sfx = np.zeros_like(bed)

    f = lambda frame: frame / FPS  # noqa: E731 — instants en images du master
    # S01 — ouverture (l'impact est joué par la musique)
    place(sfx, souffle(0.32, 700, 2600, 0.45), f(46) - 0.12, 0.6, 0.2)
    # S02 — recherche : clic de champ, saisie du handle (11 caractères, images 64→82), sélection
    place(sfx, clic(2400, 0.5), f(66), 1.0, -0.1)
    handle = "@daya_na990"
    for k in range(len(handle)):
        place(sfx, touche(0.32 + 0.05 * (k % 3)), f(64) + k * (f(82) - f(64)) / len(handle), 1.0, 0.15 * ((k % 2) * 2 - 1))
    place(sfx, clic(1900, 0.55), f(104), 1.0)
    # S03 — profil
    place(sfx, clic(2900, 0.4), f(119), 1.0, 0.1)
    # S04 — galerie
    place(sfx, souffle(0.4, 400, 1800, 0.5), f(171) - 0.15, 1.0, -0.2)
    place(sfx, pop(740, 0.45), f(219), 1.0)
    # S05 — message (exemple) : saisie, bouton d'envoi (sans réponse)
    for k in range(14):
        place(sfx, touche(0.28 + 0.04 * (k % 4)), f(244) + k * 0.058, 1.0, 0.12 * ((k % 2) * 2 - 1))
    place(sfx, clic(2200, 0.5), f(276), 1.0)
    # S06 — produit héros
    place(sfx, souffle(0.7, 160, 900, 0.6), f(296) - 0.25, 0.5)
    # S07 — détails : souffle léger puis un pop par insert (images 360, 363, 366, puis 369)
    place(sfx, souffle(0.3, 900, 3000, 0.35), f(360) - 0.1, 0.6, 0.3)  # les repères sont joués par les cloches de la musique
    # S08 — widgets Modèle / Couleur / Disponibilité
    for fr, fq in ((435, 2300), (441, 2600), (447, 2900)):
        place(sfx, clic(fq, 0.45), f(fr), 1.0, 0.35)
    # S09 — showroom
    place(sfx, souffle(0.5, 300, 2000, 0.55), f(538) - 0.15, 0.6)
    # S10 — favori
    place(sfx, coeur(0.5), f(588), 0.9)
    # S11 — photo du modèle
    place(sfx, souffle(0.3, 800, 2800, 0.4), f(627) - 0.1, 0.7, -0.2)
    # S12 — clic Message, souffle de signature
    place(sfx, clic(2000, 0.6), f(672), 1.0)
    place(sfx, souffle(0.35, 1200, 3600, 0.4), f(684) - 0.1, 0.6)
    # S13 — la signature sonore (cloches) est jouée par la musique
    # S14 — souffle inversé vers la boucle
    place(sfx, souffle(0.55, 2400, 500, 0.4, reverse=True), f(777) - 0.35, 0.5)

    # musique sous les accents : la base baisse d'environ 2,5 dB pendant chaque bruitage
    env = np.abs(sfx).max(axis=0)
    att, rel = math.exp(-1 / (0.005 * SR)), math.exp(-1 / (0.18 * SR))
    follow = np.empty_like(env)
    acc = 0.0
    for i, v in enumerate(env):
        acc = v + (acc - v) * (att if v > acc else rel)
        follow[i] = acc
    duck = 1 - (1 - 10 ** (-2.5 / 20)) * np.clip(follow / (0.5 * env.max()), 0, 1)
    mix = bed * duck + sfx * args.sfx_gain
    tmp = project / ".hyperframes" / "mix_tmp.wav"
    tmp.parent.mkdir(parents=True, exist_ok=True)
    if args.stems:
        write_wav(project / ".hyperframes" / "stem_bed.wav", bed * duck)
        write_wav(project / ".hyperframes" / "stem_sfx.wav", sfx * args.sfx_gain)
    out = project / "assets" / "audio" / "mix_daya_motion_social.wav"
    gain_db = 0.0
    for _ in range(4):
        y = true_peak_limit(mix * 10 ** (gain_db / 20))
        write_wav(tmp, y)
        i, tp = measure(tmp)
        print(f"gain {gain_db:+.2f} dB → {i:.2f} LUFS, true peak {tp:.2f} dBTP")
        if abs(i + 16) < 0.2:
            break
        gain_db += -16 - i
    write_wav(out, y)
    tmp.unlink()
    print("écrit", out)


if __name__ == "__main__":
    main()
