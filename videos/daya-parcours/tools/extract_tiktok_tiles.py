#!/usr/bin/env python3
"""Extrait les vraies photos de la boutique depuis deux captures d'écran du profil TikTok @daya_na990.

Les captures (navigateur, grille de vignettes 6 colonnes) ne sont pas versionnées : elles contiennent
le numéro de téléphone de la bio et des vignettes avec des personnes. Seules les vignettes « bikini sur
mannequin » sont extraites. Pour chacune :
  1. découpe dans la grille (colonnes/lignes détectées sur le fond noir de la page) ;
  2. effacement du compteur de vues incrusté (« ▷ 166 ») par inpainting — la vidéo le redessine net ;
  3. agrandissement ×4 par super-résolution (EDSR, OpenCV dnn_superres), sinon Lanczos.
La photo de profil (avatar) est extraite de la même façon.

Usage :
  python3 tools/extract_tiktok_tiles.py CAPTURE1 CAPTURE2 [--model EDSR_x4.pb]
Sorties : assets/photos/<nom>.jpg, assets/photos/avatar.jpg, assets/photos/tiles.json
"""
import argparse
import json
from pathlib import Path

import cv2
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "photos"

# grille de la page profil TikTok (navigateur, capture d'environ 1360 px de large)
COLS = [(329, 464), (474, 609), (620, 755), (766, 901), (912, 1047), (1057, 1193)]
ROWS = {0: [(198, 377), (393, 572)], 1: [(55, 197), (213, 392), (409, 588)]}

# (capture, ligne, colonne) → nom de fichier, vues affichées sur TikTok (None : masquées par le texte de la vidéo)
GRID = [  # ordre de la grille du profil dans la vidéo (5 lignes × 3 colonnes)
    ((0, 0, 1), "bikini-bleu-fleuri", 309),
    ((0, 0, 0), "bikini-rose-crochet", 166),
    ((0, 1, 3), "bikini-marron-leopard", 1343),
    ((0, 1, 1), "bikini-orange", 484),
    ((1, 2, 5), "bikini-vert", 775),
    ((1, 1, 3), "maillot-beige", 1655),
    ((0, 1, 2), "bikini-papillons", 510),
    ((1, 1, 0), "bikini-marron-paillettes", 2320),
    ((1, 2, 4), "bikini-bleu-pareo", 1560),
    ((0, 1, 4), "bikini-marron-chaine", 630),
    ((1, 1, 1), "bikini-rouge", 2562),          # la vignette qui se détache → vidéo, DM, préparation
    ((1, 2, 1), "top-turquoise", 841),
    ((1, 2, 3), "bikini-rouge-2", 1111),
    ((0, 0, 4), "bikini-peche", 304),
    ((1, 1, 2), "bikini-rose-blanc", None),
]
EXTRA = [  # vignettes coupées en haut sur la capture : utilisées seulement dans le mur de photos
    ((1, 0, 0), "bikini-rose-noir", 1234),
    ((1, 0, 1), "bikini-marine", 1274),
    ((1, 0, 3), "bikini-fleuri-clair", 860),
    ((1, 0, 5), "bikini-violet", 851),
]
AVATAR_BOX = (340, 36, 434, 130)  # disque de la photo de profil (sans l'anneau sombre) sur la capture 1
# versions recadrées pour les photos montrées en grand : le haut des vignettes porte le texte incrusté
# de la vidéo TikTok, illisible une fois agrandi (et, sur le bikini rouge, un bout de numéro de téléphone)
HEROES = [  # (source, sortie, part du haut retirée)
    ("bikini-rouge", "bikini-rouge-hero", 0.075),
    ("bikini-rouge-2", "bikini-rouge-2-hero", 0.14),
    ("bikini-vert", "bikini-vert-hero", 0.18),
]


def load(path):
    img = cv2.imread(str(path), cv2.IMREAD_COLOR)
    if img is None:
        raise SystemExit(f"impossible de lire {path}")
    return img


def erase_count(tile):
    """Efface le compteur « ▷ 1234 » blanc en bas à gauche (inpainting sur les seuls pixels du texte)."""
    h, w = tile.shape[:2]
    y0, y1, x0, x1 = h - 28, h - 3, 1, min(60, w)
    zone = tile[y0:y1, x0:x1]
    gray = cv2.cvtColor(zone, cv2.COLOR_BGR2GRAY)
    _, txt = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    # le texte TikTok (chiffres + triangle « lecture » gris clair) a une ombre : masque élargi
    txt = cv2.dilate(txt, np.ones((3, 3), np.uint8), iterations=2)
    mask = np.zeros((h, w), np.uint8)
    mask[y0:y1, x0:x1] = txt
    return cv2.inpaint(tile, mask, 3, cv2.INPAINT_TELEA)


def upscale(img, sr):
    if sr is not None:
        return sr.upsample(img)
    return cv2.resize(img, None, fx=4, fy=4, interpolation=cv2.INTER_LANCZOS4)


def finish(img):
    # léger renfort de netteté après agrandissement
    blur = cv2.GaussianBlur(img, (0, 0), 1.2)
    return cv2.addWeighted(img, 1.35, blur, -0.35, 0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("shots", nargs=2)
    ap.add_argument("--model", default=None, help="EDSR_x4.pb (OpenCV dnn_superres)")
    args = ap.parse_args()
    shots = [load(p) for p in args.shots]

    sr = None
    if args.model and Path(args.model).exists():
        sr = cv2.dnn_superres.DnnSuperResImpl_create()
        sr.readModel(args.model)
        sr.setModel("edsr", 4)
    OUT.mkdir(parents=True, exist_ok=True)

    meta = {"grid": [], "extra": [], "upscaler": "EDSR x4" if sr else "Lanczos x4"}
    for group, key in ((GRID, "grid"), (EXTRA, "extra")):
        for (s, r, c), name, views in group:
            y0, y1 = ROWS[s][r]
            x0, x1 = COLS[c]
            tile = shots[s][y0:y1, x0:x1].copy()
            tile = erase_count(tile)
            big = finish(upscale(tile, sr))
            cv2.imwrite(str(OUT / f"{name}.jpg"), big, [cv2.IMWRITE_JPEG_QUALITY, 92])
            meta[key].append({"file": f"{name}.jpg", "views": views, "size": [big.shape[1], big.shape[0]]})
            print(f"{name:26s} {big.shape[1]}×{big.shape[0]}  vues {views}")

    meta["heroes"] = []
    for src, dst, cut in HEROES:
        hero = cv2.imread(str(OUT / f"{src}.jpg"))
        hero = hero[int(hero.shape[0] * cut):, :]
        cv2.imwrite(str(OUT / f"{dst}.jpg"), hero, [cv2.IMWRITE_JPEG_QUALITY, 92])
        meta["heroes"].append({"file": f"{dst}.jpg", "from": f"{src}.jpg", "size": [hero.shape[1], hero.shape[0]]})

    x0, y0, x1, y1 = AVATAR_BOX
    av = finish(upscale(shots[0][y0:y1, x0:x1].copy(), sr))
    cv2.imwrite(str(OUT / "avatar.jpg"), av, [cv2.IMWRITE_JPEG_QUALITY, 92])
    meta["avatar"] = "avatar.jpg"
    (OUT / "tiles.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    print("avatar.jpg", av.shape[1], "×", av.shape[0], "|", meta["upscaler"])


if __name__ == "__main__":
    main()
