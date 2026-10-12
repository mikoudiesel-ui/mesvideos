"""Découpe la voix off (une seule prise Gemini) en une phrase par fichier, et calcule où la placer.

La voix est générée d'un seul tenant (ton homogène, une seule requête) dans assets/voice/vo-full.wav,
avec une pause d'environ une seconde entre les phrases. Ce script :
  1. repère les pauses sur l'énergie RMS (fenêtres de 20 ms, petits clics ignorés) ;
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
ANCHORS = [0.95, 2.05, 3.70, 6.15, 8.05, 9.70, 11.55, 14.55, 18.35, 20.55, 22.75, 24.15]
GAP = 0.12  # écart minimal entre deux phrases qui se suivent
assert len(ANCHORS) == len(LINES)


VOWELS = "aeiouyàâäéèêëîïôöùûüœæ"


def syllables(text):
    """Nombre de syllabes approximatif d'une phrase française (groupes de voyelles, e muet final retiré)."""
    n = 0
    for w in re.findall(r"[a-zàâäéèêëîïôöùûüœæç]+", text.lower()):
        groups = re.findall(f"[{VOWELS}]+", w)
        k = len(groups)
        if k > 1 and re.search(r"(e|es|ent)$", w) and not w.endswith(("ée", "ées")):
            k -= 1
        n += max(k, 1)
    return n


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


def silences(x, sr, thr_db=-38.0, min_d=0.12, max_blip=0.06, hop_s=0.02):
    """Pauses mesurées sur l'énergie RMS (fenêtres de 20 ms).

    Un petit bruit (clic, souffle) de moins de 60 ms au milieu d'une pause ne la coupe pas en deux :
    c'est ce qui avait fait rater la pause entre « Et le meilleur ? » et « On te livre… »."""
    hop = int(hop_s * sr)
    n = len(x) // hop
    rms = np.array([np.sqrt(np.mean(x[i * hop:(i + 1) * hop] ** 2)) for i in range(n)])
    quiet = 20 * np.log10(rms + 1e-9) < thr_db
    # combler les petits blips bruyants entre deux zones calmes
    k = int(round(max_blip / hop_s))
    i = 0
    while i < n:
        if not quiet[i]:
            j = i
            while j < n and not quiet[j]:
                j += 1
            if i > 0 and j < n and (j - i) <= k:
                quiet[i:j] = True
            i = j
        else:
            i += 1
    out, i = [], 0
    while i < n:
        if quiet[i]:
            j = i
            while j < n and quiet[j]:
                j += 1
            if (j - i) * hop_s >= min_d:
                out.append((i * hop_s, j * hop_s))
            i = j
        else:
            i += 1
    return out


TARGET_LUFS = -16.0  # niveau de la voix avant mixage (les voix Gemini sortent entre -16 et -18 LUFS)


def take_lufs(path):
    out = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(path), "-af", "ebur128=framelog=quiet", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    for line in out.splitlines():
        if line.strip().startswith("I:"):
            return float(line.split()[1])
    raise RuntimeError("mesure de loudness impossible")


def limit_take():
    SRC.parent.mkdir(exist_ok=True)
    # gain statique vers TARGET_LUFS, puis limiteur suréchantillonné ×4 : crêtes vraies sous -1,5 dBTP
    gain = TARGET_LUFS - take_lufs(RAW)
    subprocess.run(
        ["ffmpeg", "-v", "error", "-y", "-i", str(RAW), "-af",
         f"volume={gain:.2f}dB,aresample=96000,alimiter=limit=0.79:attack=3:release=50:level=disabled,aresample=24000",
         "-c:a", "pcm_s16le", str(SRC)],
        check=True,
    )
    print(f"prise ramenée à {TARGET_LUFS} LUFS (gain {gain:+.1f} dB)")


def main():
    limit_take()
    x, sr = read_wav(SRC)
    total = len(x) / sr
    sil = silences(x, sr)
    # silences internes uniquement (ni le début ni la fin du fichier)
    cand = [(a, b) for a, b in sil if a > 0.05 and b < total - 0.05]
    n = len(LINES)
    need = n - 1
    if len(cand) < need:
        sys.exit(f"seulement {len(cand)} silences pour {need} coupures : relance avec un seuil plus doux")

    # durée de parole attendue : un minimum par phrase (attaque, emphase) + un débit par syllabe
    syl = np.array([syllables(t) for t in LINES], dtype=float)
    lead = sil[0][1] if sil and sil[0][0] <= 0.05 else 0.0
    tail = sil[-1][0] if sil and sil[-1][1] >= total - 0.05 else total
    speech_total = (tail - lead) - sum(b - a for a, b in cand)
    BASE = 0.25
    rate = (speech_total - BASE * n) / syl.sum()
    expected = BASE + rate * syl

    # programmation dynamique : choisir `need` pauses parmi les candidates (dans l'ordre) en maximisant
    # la longueur des pauses retenues et la cohérence entre parole mesurée et parole attendue.
    m = len(cand)
    NEG = -1e9
    W_PAUSE = 2.0
    best = np.full((m, need), NEG)
    back = np.full((m, need), -1, dtype=int)

    def cost(speech, k):
        return abs(np.log(max(speech, 0.05) / expected[k]))

    # parole entre deux coupures = durée moins les pauses internes (virgules, deux-points…),
    # sinon une phrase avec des virgules paraît plus longue qu'elle ne l'est
    plen = np.array([b - a for a, b in cand])
    csum = np.concatenate([[0.0], np.cumsum(plen)])

    def speech(i, j):  # entre la fin de la pause i (-1 = début) et le début de la pause j (m = fin)
        t0 = lead if i < 0 else cand[i][1]
        t1 = tail if j >= m else cand[j][0]
        inner = csum[j if j < m else m] - csum[i + 1 if i >= 0 else 0]
        return (t1 - t0) - inner

    for j in range(m):
        best[j, 0] = plen[j] * W_PAUSE - cost(speech(-1, j), 0)
    for c in range(1, need):
        for j in range(c, m):
            for i in range(c - 1, j):
                if best[i, c - 1] == NEG:
                    continue
                v = best[i, c - 1] + plen[j] * W_PAUSE - cost(speech(i, j), c)
                if v > best[j, c]:
                    best[j, c], back[j, c] = v, i
    final = [best[j, need - 1] - cost(speech(j, m), n - 1) if best[j, need - 1] > NEG else NEG for j in range(m)]
    j = int(np.argmax(final))
    picks = []
    for c in range(need - 1, -1, -1):
        picks.append(j)
        j = back[j, c]
    picks = sorted(picks)
    mids = [(cand[p][0] + cand[p][1]) / 2 for p in picks]
    cuts = [0.0] + mids + [total]

    # contrôle : débit de chaque phrase (syllabes par seconde de parole)
    edges = [-1] + picks + [m]
    for k in range(n):
        sp = speech(edges[k], edges[k + 1])
        print(f"  phrase {k + 1:2d} : {sp:4.2f} s de parole, {int(syl[k]):2d} syllabes → {syl[k] / max(sp, 0.05):4.1f} syll/s")

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
