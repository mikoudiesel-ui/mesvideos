"""Prépare les images produit de la maquette à partir des scènes du dossier.

Toutes les sources sont des illustrations générées (reference/sequences/*.png) :
ce sont des visuels de maquette, à remplacer par les vraies photos HD.

    python3 -I tools/prep_assets.py --project videos/daya-motion-social

Étapes : découpe + agrandissement (Lanczos + accentuation légère), détourage
local avec `hyperframes remove-background` pour le mannequin bleu et le doigt,
puis nettoyage du masque (feuille de palmier résiduelle, zones hors peau).
"""

import argparse
import subprocess
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageFilter

CLI = ["npx", "--yes", "hyperframes@0.8.143", "remove-background"]

# (fichier source, boîte de découpe x0 y0 x1 y1 en pixels de la scène, facteur)
PHOTOS = {
    "rose-photo.jpg": ("S03.png", (141, 490, 256, 715), 4),
    "vert-photo.jpg": ("S03.png", (264, 490, 379, 715), 4),
    "detail-fleur.jpg": ("S07.png", (247, 179, 376, 335), 3),
    "detail-motif.jpg": ("S07.png", (277, 439, 381, 591), 3),
    "detail-liens.jpg": ("S07.png", (10, 525, 126, 683), 3),
    "detail-fleur-anneau.jpg": ("S11.png", (287, 213, 386, 414), 3),
    "detail-liens-cordon.jpg": ("S11.png", (287, 440, 386, 665), 3),
}
HERO = ("S13.png", (96, 262, 386, 818), 3)
FINGER = ("S12.png", (170, 400, 389, 802), 3)


def upscale(seq_dir, src, box, k):
    im = Image.open(seq_dir / src).convert("RGB").crop(box)
    im = im.resize((im.width * k, im.height * k), Image.LANCZOS)
    return im.filter(ImageFilter.UnsharpMask(radius=2, percent=60, threshold=2))


def matte(src_png, out_png, cwd):
    subprocess.run(CLI + [str(src_png), "-o", str(out_png)], check=True, cwd=cwd,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return np.array(Image.open(out_png).convert("RGBA"))


def clean_hero(rgba):
    """Retire la feuille de palmier sombre restée au-dessus de l'épaule droite."""
    a = rgba[..., 3].astype(np.float32)
    v = cv2.cvtColor(rgba[..., :3], cv2.COLOR_RGB2HSV)[..., 2].astype(np.float32)
    h, w = a.shape
    yy, xx = np.mgrid[0:h, 0:w]
    region = (xx >= 560) & (yy <= 390)
    a[region] *= np.clip((v - 70) / 60.0, 0, 1)[region]
    a[region & (a < 110)] = 0
    # fondu bas : le socle se perd dans le sol de la scène
    fade = np.clip((h - 1 - yy) / 90.0, 0, 1)
    rgba[..., 3] = (a * fade).astype(np.uint8)
    return rgba


def clean_finger(rgba):
    """Garde la plus grande zone couleur peau (le doigt) et retire le téléphone."""
    hsv = cv2.cvtColor(rgba[..., :3], cv2.COLOR_RGB2HSV)
    hh, ss, vv = (hsv[..., i].astype(int) for i in range(3))
    skin = (((hh <= 22) | (hh >= 170)) & (ss >= 25) & (ss <= 170) & (vv >= 90)).astype(np.uint8)
    skin = cv2.morphologyEx(skin, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    skin = cv2.morphologyEx(skin, cv2.MORPH_CLOSE, np.ones((15, 15), np.uint8))
    n, lab, stats, _ = cv2.connectedComponentsWithStats(skin, 8)
    keep = (lab == 1 + np.argmax(stats[1:, cv2.CC_STAT_AREA])).astype(np.uint8)
    inv = 1 - keep
    n2, lab2, st2, _ = cv2.connectedComponentsWithStats(inv, 4)
    for i in range(1, n2):
        x, y, w, h, _ = st2[i]
        if x > 0 and y > 0 and x + w < keep.shape[1] and y + h < keep.shape[0]:
            keep[lab2 == i] = 1
    keep[590:672, :318] = 0  # éclat d'icône du téléphone collé au bord du doigt
    # second doigt (en bas à gauche) : tout ce qui est à gauche de la diagonale (480, 930) → (575, 1206)
    h, w = keep.shape
    yy, xx = np.mgrid[0:h, 0:w]
    keep[(yy >= 930) & (xx < 480 + (yy - 930) * (95 / 276))] = 0
    # bord gauche découpé par l'écran du téléphone : lissage du contour
    keep = cv2.morphologyEx(keep, cv2.MORPH_OPEN, np.ones((9, 9), np.uint8))
    n, lab, stats, _ = cv2.connectedComponentsWithStats(keep, 8)
    keep = (lab == 1 + np.argmax(stats[1:, cv2.CC_STAT_AREA])).astype(np.uint8)
    rgba[..., 3] = (cv2.GaussianBlur(keep.astype(np.float32), (9, 9), 0) * 255).astype(np.uint8)
    return rgba


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", required=True)
    args = ap.parse_args()
    project = Path(args.project).resolve()
    seq = project / "reference" / "sequences"
    out = project / "assets" / "img"
    work = project / ".hyperframes" / "prep"
    out.mkdir(parents=True, exist_ok=True)
    work.mkdir(parents=True, exist_ok=True)

    for name, (src, box, k) in PHOTOS.items():
        upscale(seq, src, box, k).save(out / name, quality=92)
        print("photo", name)

    hero_in = work / "bleu_x3.png"
    upscale(seq, *HERO).save(hero_in)
    hero = clean_hero(matte(hero_in, work / "bleu_cut.png", project))
    Image.fromarray(hero).save(out / "bleu-detoure.png", optimize=True)
    print("détouré bleu-detoure.png", hero.shape[1], hero.shape[0])

    finger_in = work / "doigt_x3.png"
    upscale(seq, *FINGER).save(finger_in)
    finger = clean_finger(matte(finger_in, work / "doigt_cut.png", project))
    Image.fromarray(finger).save(out / "main-doigt.png", optimize=True)
    print("détouré main-doigt.png", finger.shape[1], finger.shape[0])


if __name__ == "__main__":
    main()
