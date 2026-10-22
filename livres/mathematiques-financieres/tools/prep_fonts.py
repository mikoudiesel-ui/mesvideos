#!/usr/bin/env python3
"""Polices de la couverture : instances fixes de Noto Serif et Noto Sans (licence SIL OFL 1.1).

Les fichiers variables viennent des paquets npm @fontsource-variable/noto-serif et noto-sans (5.3.0,
sous-ensemble latin : français complet, œ et € compris). Chaque instance fige une graisse et une largeur.

    npm install @fontsource-variable/noto-serif @fontsource-variable/noto-sans    # dans un dossier de travail
    python3 -I livres/mathematiques-financieres/tools/prep_fonts.py <dossier>/node_modules/@fontsource-variable
"""

import sys
from pathlib import Path

from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

FONTS = Path(__file__).resolve().parent.parent / "fonts"
INSTANCES = {  # fichier : (famille, style, graisse, largeur en %)
    "noto-serif-cond-700": ("noto-serif", "normal", 700, 80),  # titre, comme sur la maquette
    "noto-serif-semicond-400": ("noto-serif", "normal", 400, 87.5),  # texte de la 4e de couverture
    "noto-serif-semicond-700": ("noto-serif", "normal", 700, 87.5),
    "noto-serif-semicond-400i": ("noto-serif", "italic", 400, 87.5),  # sous-titre
    "noto-sans-600": ("noto-sans", "normal", 600, 100),  # petites capitales espacées
    "noto-sans-semicond-400": ("noto-sans", "normal", 400, 87.5),
    "noto-sans-semicond-500": ("noto-sans", "normal", 500, 87.5),  # sommaire
    "noto-sans-semicond-700": ("noto-sans", "normal", 700, 87.5),  # numéros de chapitre
}


def main(src):
    FONTS.mkdir(exist_ok=True)
    for name, (fam, style, wght, wdth) in INSTANCES.items():
        tt = TTFont(src / fam / "files" / f"{fam}-latin-standard-{style}.woff2")
        tt.flavor = None
        instancer.instantiateVariableFont(tt, {"wght": wght, "wdth": wdth}, inplace=True)
        tt.save(FONTS / f"{name}.ttf")
    for fam in ("noto-serif", "noto-sans"):
        (FONTS / f"OFL-{fam}.txt").write_text((src / fam / "LICENSE").read_text())
    print(f"{len(INSTANCES)} polices dans {FONTS}")


if __name__ == "__main__":
    main(Path(sys.argv[1]))
