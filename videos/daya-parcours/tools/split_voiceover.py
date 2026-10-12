"""Découpe la voix off (une seule prise Gemini) en une phrase par fichier, et calcule où la placer.

La voix est générée d'un seul tenant (ton homogène, une seule requête) dans assets/voice/vo-full.wav,
avec une pause d'environ une seconde entre les phrases. Ce script :
  1. repère les silences (ffmpeg silencedetect) ;
  2. choisit les 11 coupures qui séparent le mieux les 12 phrases de assets/voice/lines.json
     (silences longs + durées cohérentes avec la longueur de chaque phrase) ;
  3. écrit assets/voice/vo-01.wav … vo-12.wav, rognés au début et à la fin ;
  4. affiche le planning : chaque phrase démarre à l'ancre de sa scène, ou juste après la phrase précédente.

Usage : python3 tools/split_voiceover.py
"""
import json
import re
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "assets" / "voice" / "vo-full.wav"
SRC = ROOT / ".hyperframes" / "vo-full.limited.wav"  # prise limitée à -2 dBFS (la sortie TTS crête au-dessus de 0)
LINES = json.loads((ROOT / "assets" / "voice" / "lines.json").read_text(encoding="utf-8"))

# Ancre (en secondes) de chaque phrase : le moment de la scène où elle doit tomber.
ANCHORS = [0.95, 2.05, 3.70, 6.15, 8.05, 9.70, 11.55, 14.55, 18.35, 20.85, 22.75, 24.15]
GAP = 0.12  # écart minimal entre deux phrases qui se suivent
assert len(ANCHORS) == len(LINES)


def read_wav(path):
    with wave.open(str(path)) as w:
        sr, ch, sw = w.getframerate(), w.getnchannels(), w.getsampwidth()
        raw = w.readframes(w.getnframes())
    assert sw == 2, "PCM 16 bits attendu"
    x = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768
    if ch > 1:
        x = x.reshape(-1, ch).mean(axis=1)
    return x, sr


def write_wav(path, x, sr):
    y = np.clip(x * 32767, -32768, 32767).astype(np.int16)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(y.tobytes())


def silences(path, noise_db=-38, min_d=0.18):
    out = subprocess.run(
        ["ffmpeg", "-hide_banner", "-i", str(path), "-af", f"silencedetect=noise={noise_db}dB:d={min_d}", "-f", "null", "-"],
        capture_output=True, text=True,
    ).stderr
    starts = [float(v) for v in re.findall(r"silence_start: ([0-9.]+)", out)]
    ends = [float(v) for v in re.findall(r"silence_end: ([0-9.]+)", out)]
    return list(zip(starts, ends))


def limit_take():
    SRC.parent.mkdir(exist_ok=True)
    # limiteur suréchantillonné ×4 : crêtes vraies sous -1,5 dBTP, sans toucher au niveau moyen
    subprocess.run(
        ["ffmpeg", "-v", "error", "-y", "-i", str(RAW), "-af",
         "aresample=96000,alimiter=limit=0.79:attack=3:release=50:level=disabled,aresample=24000",
         "-c:a", "pcm_s16le", str(SRC)],
        check=True,
    )


def main():
    limit_take()
    x, sr = read_wav(SRC)
    total = len(x) / sr
    sil = silences(SRC)
    # silences internes uniquement (ni le début ni la fin du fichier)
    cand = [(a, b) for a, b in sil if a > 0.05 and b < total - 0.05]
    n = len(LINES)
    need = n - 1
    if len(cand) < need:
        sys.exit(f"seulement {len(cand)} silences pour {need} coupures : relance avec un seuil plus doux")

    # durée attendue de chaque phrase, proportionnelle à son nombre de caractères
    chars = np.array([len(t) for t in LINES], dtype=float)
    speech_total = total - sum(b - a for a, b in cand)
    expected = speech_total * chars / chars.sum()

    # programmation dynamique : choisir `need` silences parmi les candidats (dans l'ordre)
    # en maximisant la longueur des pauses retenues et la cohérence des durées.
    m = len(cand)
    mids = [(a + b) / 2 for a, b in cand]
    NEG = -1e9
    best = np.full((m, need), NEG)
    back = np.full((m, need), -1, dtype=int)

    def seg_cost(t0, t1, k):
        d = max(t1 - t0, 0.05)
        return abs(np.log(d / expected[k]))

    for j in range(m):
        best[j, 0] = (cand[j][1] - cand[j][0]) * 3 - seg_cost(0, mids[j], 0)
    for c in range(1, need):
        for j in range(c, m):
            for i in range(c - 1, j):
                if best[i, c - 1] == NEG:
                    continue
                v = best[i, c - 1] + (cand[j][1] - cand[j][0]) * 3 - seg_cost(mids[i], mids[j], c)
                if v > best[j, c]:
                    best[j, c], back[j, c] = v, i
    # dernière phrase : du dernier silence choisi à la fin
    final = [best[j, need - 1] - seg_cost(mids[j], total, n - 1) for j in range(m)]
    j = int(np.argmax(final))
    picks = []
    for c in range(need - 1, -1, -1):
        picks.append(j)
        j = back[j, c]
    picks = sorted(picks)
    cuts = [0.0] + [mids[p] for p in picks] + [total]

    out_dir = RAW.parent
    plan = []
    prev_end = 0.0
    for k in range(n):
        a, b = int(cuts[k] * sr), int(cuts[k + 1] * sr)
        seg = x[a:b]
        # rognage : on garde la parole (> -45 dBFS) avec 40 ms avant et 90 ms après
        env = np.abs(seg)
        thr = 10 ** (-45 / 20)
        idx = np.where(env > thr)[0]
        s0 = max(int(idx[0]) - int(0.04 * sr), 0) if len(idx) else 0
        s1 = min(int(idx[-1]) + int(0.09 * sr), len(seg)) if len(idx) else len(seg)
        seg = seg[s0:s1].copy()
        fi, fo = int(0.005 * sr), int(0.03 * sr)
        seg[:fi] *= np.linspace(0, 1, fi)
        seg[-fo:] *= np.linspace(1, 0, fo)
        path = out_dir / f"vo-{k + 1:02d}.wav"
        write_wav(path, seg, sr)
        dur = len(seg) / sr
        start = max(ANCHORS[k], prev_end + GAP)
        prev_end = start + dur
        plan.append({"id": f"vo-{k + 1:02d}", "start": round(start, 2), "duration": round(dur, 2),
                     "end": round(prev_end, 2), "anchor": ANCHORS[k], "text": LINES[k]})

    (ROOT / "assets" / "voice" / "plan.json").write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"prise complète : {total:.2f} s, {len(sil)} silences, coupures à "
          + ", ".join(f"{c:.2f}" for c in cuts[1:-1]))
    for p in plan:
        late = p["start"] - p["anchor"]
        flag = f"  (+{late:.2f} s)" if late > 0.01 else ""
        print(f"{p['id']}  {p['start']:6.2f} → {p['end']:6.2f}  ({p['duration']:.2f} s){flag}  {p['text']}")


if __name__ == "__main__":
    main()
