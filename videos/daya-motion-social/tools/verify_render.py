#!/usr/bin/env python3
"""Vérifie le MP4 rendu : images, format, audio, décodage complet, sonie après encodage,
lisibilité du bouton final (23,3 → 25,3 s) et planche de contrôle extraite du MP4 lui-même.

    python3 -I tools/verify_render.py --project videos/daya-motion-social --mp4 <fichier.mp4>
"""

import argparse
import json
import re
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

EXPECT = {"width": 1080, "height": 1920, "fps": 30, "frames": 794, "sample_rate": 48000, "channels": 2}
MIDS = [27, 84, 136, 196, 261, 321, 385, 475, 552, 595, 639, 673, 727, 779]


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def probe(mp4):
    out = run(["ffprobe", "-v", "error", "-count_frames", "-show_streams", "-show_format", "-of", "json", str(mp4)]).stdout
    return json.loads(out)


def frame_at(mp4, n):
    data = subprocess.run(["ffmpeg", "-v", "error", "-i", str(mp4), "-vf", f"select=eq(n\\,{n})", "-vframes", "1",
                           "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    return np.frombuffer(data, np.uint8).reshape(1920, 1080, 3)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", required=True)
    ap.add_argument("--mp4", required=True)
    args = ap.parse_args()
    project = Path(args.project)
    mp4 = Path(args.mp4)
    report = {}
    info = probe(mp4)
    v = next(s for s in info["streams"] if s["codec_type"] == "video")
    a = next((s for s in info["streams"] if s["codec_type"] == "audio"), None)
    num, den = (int(x) for x in v["r_frame_rate"].split("/"))
    report["video"] = {
        "codec": v["codec_name"], "pix_fmt": v.get("pix_fmt"), "width": v["width"], "height": v["height"],
        "fps": num / den, "frames": int(v.get("nb_read_frames", v.get("nb_frames", 0))), "duration_s": float(v.get("duration", 0)),
    }
    report["audio"] = None if a is None else {
        "codec": a["codec_name"], "sample_rate": int(a["sample_rate"]), "channels": a["channels"], "duration_s": float(a.get("duration", 0)),
    }
    report["size_mb"] = round(mp4.stat().st_size / 1e6, 2)
    dec = run(["ffmpeg", "-v", "error", "-i", str(mp4), "-f", "null", "-"])
    report["decode_errors"] = dec.stderr.strip()[:500]
    ebu = run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(mp4), "-map", "0:a:0", "-af", "ebur128=peak=true", "-f", "null", "-"]).stderr
    s = ebu[ebu.rfind("Summary:"):]
    report["loudness_lufs"] = float(re.search(r"I:\s+(-?[\d.]+) LUFS", s).group(1))
    report["true_peak_dbtp"] = float(re.search(r"Peak:\s+(-?[\d.]+) dBFS", s).group(1))

    # bouton final : la zone du CTA doit rester corail et nette de 23,3 à 25,3 s (images 699 → 759)
    cta = []
    for n in (699, 714, 729, 744, 759):
        img = frame_at(mp4, n)
        region = img[1520:1600, 140:880].reshape(-1, 3).astype(float)
        coral = np.mean((region[:, 0] > 200) & (region[:, 1] < 140) & (region[:, 2] > 60))
        cta.append((n, round(float(coral), 3)))
    report["cta_coral_ratio"] = cta

    checks = {
        "1080x1920": report["video"]["width"] == EXPECT["width"] and report["video"]["height"] == EXPECT["height"],
        "30 i/s": abs(report["video"]["fps"] - EXPECT["fps"]) < 1e-6,
        "794 images": report["video"]["frames"] == EXPECT["frames"],
        "audio AAC 48 kHz stéréo": report["audio"] is not None and report["audio"]["codec"] == "aac" and report["audio"]["sample_rate"] == EXPECT["sample_rate"] and report["audio"]["channels"] == EXPECT["channels"],
        "décodage complet sans erreur": report["decode_errors"] == "",
        "≈ −16 LUFS": abs(report["loudness_lufs"] + 16) <= 1.0,
        "crête vraie ≤ −1 dBTP": report["true_peak_dbtp"] <= -1.0,
        "CTA lisible 23,3–25,3 s": all(r > 0.25 for _, r in cta),
    }
    report["checks"] = checks

    # planche de contrôle extraite du MP4 (milieux de scène + images 0 et 793)
    fonts = project / "assets" / "fonts"
    font = ImageFont.truetype(str(fonts / "DejaVuSans-Bold.ttf"), 15)
    frames = [0] + MIDS + [793]
    w, h = 216, 384
    cols = 8
    rows = (len(frames) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * (w + 8) + 8, rows * (h + 34) + 8), (14, 12, 18))
    d = ImageDraw.Draw(sheet)
    for i, n in enumerate(frames):
        im = Image.fromarray(frame_at(mp4, n)).resize((w, h), Image.LANCZOS)
        x = 8 + (i % cols) * (w + 8)
        y = 8 + (i // cols) * (h + 34)
        sheet.paste(im, (x, y + 28))
        d.text((x + 2, y + 6), f"img {n} · {n / 30:.2f} s", font=font, fill=(255, 220, 140))
    out = project / "captures" / "PLANCHE_D_controle_mp4.jpg"
    sheet.save(out, quality=88)
    report["contact_sheet"] = str(out)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
