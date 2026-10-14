"""Planches de revue (images) à partir des captures `hyperframes snapshot`.

    npx hyperframes snapshot videos/daya-motion-social --at <temps> --no-end -o <dossier>
    python3 -I tools/review_sheets.py --project videos/daya-motion-social --snaps <dossier> --out videos/daya-motion-social/captures

Produit : 14 captures de milieu de scène (JPG pleine résolution), la planche des 14 scènes,
les planches de raccords (image avant / première image / image suivante, boucle 793 → 0)
et les planches de détail (6 temps clés par scène).
"""

import argparse
import glob
import json
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

MID = [27, 84, 136, 196, 261, 321, 385, 475, 552, 595, 639, 673, 727, 779]
DETAIL = [
    [0, 6, 12, 27, 47, 53], [54, 64, 74, 90, 108, 113], [114, 122, 132, 144, 153, 158],
    [159, 168, 177, 199, 227, 233], [234, 244, 256, 272, 282, 287], [288, 297, 306, 324, 347, 353],
    [354, 360, 369, 387, 410, 416], [417, 429, 447, 477, 523, 533], [534, 540, 546, 554, 565, 569],
    [570, 578, 588, 600, 615, 620], [621, 626, 631, 639, 652, 656], [657, 665, 672, 678, 685, 689],
    [690, 694, 699, 730, 761, 764], [765, 770, 775, 780, 789, 793],
]
BG = (14, 12, 18)
INK = (255, 236, 214)
CORAL = (255, 66, 105)
MUTED = (170, 160, 175)


def load_frames(snap_dir):
    frames = {}
    for f in glob.glob(str(Path(snap_dir) / "frame-*.png")):
        m = re.search(r"at-([\d.]+)s", f)
        frames[round(float(m.group(1)) * 30)] = f
    return frames


def fit(text, font, width):
    """Coupe le libellé avec une ellipse pour qu'il tienne dans la colonne."""
    if font.getlength(text) <= width:
        return text
    while text and font.getlength(text + "…") > width:
        text = text[:-1]
    return text.rstrip() + "…"


def wrap(text, font, width):
    """Retour à la ligne au mot, mesuré en pixels."""
    lines, cur = [], ""
    for word in text.split(" "):
        test = (cur + " " + word).strip()
        if font.getlength(test) <= width or not cur:
            cur = test
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def thumb(path, w):
    im = Image.open(path).convert("RGB")
    return im.resize((w, round(w * im.height / im.width)), Image.LANCZOS)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", required=True)
    ap.add_argument("--snaps", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    project = Path(args.project)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    tl = json.loads((project / "reference" / "TIMELINE_14_SCENES.json").read_text())
    scenes = tl["scenes"]
    frames = load_frames(args.snaps)
    fonts = project / "assets" / "fonts"
    f_big = ImageFont.truetype(str(fonts / "DejaVuSans-Bold.ttf"), 30)
    f_mid = ImageFont.truetype(str(fonts / "DejaVuSans-Bold.ttf"), 22)
    f_small = ImageFont.truetype(str(fonts / "DejaVuSans.ttf"), 19)

    def scene_of(fr):
        for s in scenes:
            if s["start_frame"] <= fr < s["end_frame_exclusive"]:
                return s
        return scenes[-1]

    def label(fr):
        s = scene_of(fr)
        return f"{s['id']} · image {fr} · {fr / 30:.3f} s · locale {fr - s['start_frame']}"

    # ---- 14 captures pleine résolution
    for i, fr in enumerate(MID):
        s = scenes[i]
        Image.open(frames[fr]).convert("RGB").save(out / f"{s['id']}_milieu_image{fr:03d}.jpg", quality=90)

    # ---- planche des 14 scènes
    w, cols = 340, 7
    h = round(w * 1920 / 1080)
    head, cap = 90, 74
    sheet = Image.new("RGB", (cols * (w + 12) + 12, head + 2 * (h + cap + 12) + 12), BG)
    d = ImageDraw.Draw(sheet)
    d.text((16, 18), "BIKINIS SHOP / @daya_na990 — MAQUETTE · les 14 scènes (milieu de chaque scène)", font=f_big, fill=INK)
    d.text((16, 56), "1080×1920 · 30 i/s · 794 images (26,467 s) · visuels illustratifs, pas une publicité catalogue finale", font=f_small, fill=MUTED)
    for i, fr in enumerate(MID):
        s = scenes[i]
        x = 12 + (i % cols) * (w + 12)
        y = head + (i // cols) * (h + cap + 12)
        sheet.paste(thumb(frames[fr], w), (x, y))
        d.text((x + 4, y + h + 6), fit(f"{s['id']} — {s['title']}", f_mid, w - 8), font=f_mid, fill=CORAL)
        d.text((x + 4, y + h + 36), f"{s['start_s']:.2f}–{s['end_s']:.2f} s · image {fr}", font=f_small, fill=INK)
    sheet.save(out / "PLANCHE_A_14_scenes.jpg", quality=88)

    # ---- planches de raccords : image avant | première image | image suivante
    pairs = [(s["end_frame_exclusive"], f"{s['id']} → {scenes[i + 1]['id']}") for i, s in enumerate(scenes[:-1])]
    pairs.append((794, "S14 → S01 (boucle 793 → 0)"))
    w = 230
    h = round(w * 1920 / 1080)
    tw = 3 * (w + 6)
    per = 8
    for part in range(0, len(pairs), per):
        chunk = pairs[part:part + per]
        rows = (len(chunk) + 1) // 2
        sheet = Image.new("RGB", (2 * (tw + 30) + 20, 90 + rows * (h + 86) + 10), BG)
        d = ImageDraw.Draw(sheet)
        d.text((16, 18), f"Raccords {part // per + 1}/2 — image avant la coupe · première image · image suivante", font=f_big, fill=INK)
        d.text((16, 56), "Les éléments partagés doivent rester au même endroit d'une image à l'autre.", font=f_small, fill=MUTED)
        for j, (b, name) in enumerate(chunk):
            x0 = 20 + (j % 2) * (tw + 30)
            y0 = 90 + (j // 2) * (h + 86)
            d.text((x0, y0), name, font=f_mid, fill=CORAL)
            trio = [b - 1, b, b + 1] if b < 794 else [792, 793, 0]
            for k, fr in enumerate(trio):
                x = x0 + k * (w + 6)
                sheet.paste(thumb(frames[fr], w), (x, y0 + 32))
                d.text((x + 2, y0 + 32 + h + 6), f"image {fr}", font=f_small, fill=INK if k != 1 else CORAL)
        sheet.save(out / f"PLANCHE_B_raccords_{part // per + 1}.jpg", quality=88)

    # ---- planches de détail : 6 temps par scène
    w = 200
    h = round(w * 1920 / 1080)
    lw = 250
    groups = [range(0, 5), range(5, 10), range(10, 14)]
    for g, idx in enumerate(groups):
        idx = list(idx)
        sheet = Image.new("RGB", (lw + 6 * (w + 8) + 16, 80 + len(idx) * (h + 48) + 10), BG)
        d = ImageDraw.Draw(sheet)
        d.text((16, 18), f"Détail des scènes {g + 1}/3 — entrée · pose · sortie (6 temps par scène)", font=f_big, fill=INK)
        for r, i in enumerate(idx):
            s = scenes[i]
            y = 80 + r * (h + 48)
            d.text((16, y + 8), s["id"], font=f_big, fill=CORAL)
            ty = y + 48
            for line in wrap(s["title"], f_mid, lw - 24)[:2]:
                d.text((16, ty), line, font=f_mid, fill=INK)
                ty += 28
            d.text((16, ty + 6), f"{s['start_s']:.2f}–{s['end_s']:.2f} s", font=f_small, fill=MUTED)
            d.text((16, ty + 30), f"images {s['start_frame']}–{s['end_frame_exclusive'] - 1}", font=f_small, fill=MUTED)
            head = s["heading"].replace("\n", " / ") or "(sans texte)"
            for k, line in enumerate(wrap(head, f_small, lw - 24)[:4]):
                d.text((16, ty + 66 + 24 * k), line, font=f_small, fill=INK)
            for k, fr in enumerate(DETAIL[i]):
                x = lw + k * (w + 8)
                sheet.paste(thumb(frames[fr], w), (x, y))
                d.text((x + 2, y + h + 4), f"{fr} · loc {fr - s['start_frame']}", font=f_small, fill=MUTED)
        sheet.save(out / f"PLANCHE_C_detail_{g + 1}.jpg", quality=88)
    print("planches écrites dans", out)


if __name__ == "__main__":
    main()
