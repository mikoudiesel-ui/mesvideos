#!/usr/bin/env python3
"""Planche de revue de l'intro KSC STUDIO : 8 images du MP4 rendu, légendées.

    python3 -I videos/ksc-studio-intro/tools/planche.py

Écrit `captures/ksc-intro-planche.png` à partir de `renders/KSC_STUDIO_intro-logo.mp4`.
"""

import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

PROJECT = Path(__file__).resolve().parent.parent
FONTS = PROJECT.parent.parent / "brand" / "ksc-studio" / "fonts"
MP4 = PROJECT / "renders" / "KSC_STUDIO_intro-logo.mp4"
OUT = PROJECT / "captures" / "ksc-intro-planche.png"
FPS = 30
IMAGES = [  # (numéro d'image, légende)
    (6, "Le C sort du noir, flou"),
    (10, "Mise au point de l'objectif"),
    (21, "Reflet + bip-bip de l'autofocus"),
    (24, "Déclic : flash"),
    (27, "Le logo jaillit du flash"),
    (36, "STUDIO s'élargit"),
    (60, "Étincelle + carillon"),
    (89, "Image finale, tenue"),
]
CW, CH, CAP, PAD, TOP = 360, 640, 70, 24, 120
ORANGE, NOIR, BLANC, GRIS = (255, 116, 31), (17, 21, 24), (255, 255, 255), (150, 156, 162)


def frames(tmp):
    sel = "+".join(f"eq(n\\,{n})" for n, _ in IMAGES)
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-i", str(MP4), "-vf", f"select='{sel}'",
                    "-vsync", "0", str(Path(tmp) / "f%02d.png")], check=True)
    return [Image.open(Path(tmp) / f"f{i + 1:02d}.png").convert("RGB") for i in range(len(IMAGES))]


def main():
    with tempfile.TemporaryDirectory() as tmp:
        shots = frames(tmp)
    cols = 4
    rows = (len(shots) + cols - 1) // cols
    W = PAD + cols * (CW + PAD)
    H = TOP + rows * (CH + CAP + PAD)
    sheet = Image.new("RGB", (W, H), (28, 31, 34))
    d = ImageDraw.Draw(sheet)
    title = ImageFont.truetype(str(FONTS / "montserrat-700.ttf"), 34)
    sub = ImageFont.truetype(str(FONTS / "montserrat-500.ttf"), 20)
    cap = ImageFont.truetype(str(FONTS / "montserrat-600.ttf"), 19)
    tim = ImageFont.truetype(str(FONTS / "montserrat-700.ttf"), 19)
    d.text((PAD, 30), "KSC STUDIO · intro animée du logo", font=title, fill=BLANC)
    d.text((PAD, 76), "3 s · 1080 × 1920 · 30 images/s · avec le son  —  images extraites de la vidéo rendue",
           font=sub, fill=GRIS)
    for i, (img, (n, text)) in enumerate(zip(shots, IMAGES)):
        x = PAD + (i % cols) * (CW + PAD)
        y = TOP + (i // cols) * (CH + CAP + PAD)
        sheet.paste(img.resize((CW, CH), Image.LANCZOS), (x, y))
        d.rectangle((x, y + CH, x + CW, y + CH + CAP), fill=NOIR)
        t = f"{n / FPS:.2f} s".replace(".", ",")
        d.text((x + 14, y + CH + 12), t, font=tim, fill=ORANGE)
        d.text((x + 14, y + CH + 38), text, font=cap, fill=BLANC)
    OUT.parent.mkdir(exist_ok=True)
    sheet.save(OUT)
    print(OUT, sheet.size)


if __name__ == "__main__":
    main()
