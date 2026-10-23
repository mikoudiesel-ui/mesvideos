# Mathématiques Financières : couverture du livre

Couverture complète du manuel *Mathématiques Financières, cours complet et exercices corrigés* (Professeur Raoul,
Édition Moderna, 2026) : 1re de couverture, dos et 4e de couverture, prête pour l'imprimeur. La mise en page reprend
la maquette fournie (`reference/banniere-maquette.avif`), en **émeraude et or**, la palette choisie à la place du bleu
marine, qu'un autre ouvrage utilise déjà.

![Le livre en volume](planches/couverture-maquette.png)

## Fichiers

| Fichier | Usage |
| --- | --- |
| `couverture/Mathematiques-Financieres_couverture_imprimeur.pdf` | Couverture à plat pour l'imprimeur : CMJN, texte vectorisé, fond perdu 3 mm |
| `couverture/Mathematiques-Financieres_couverture_traits-de-coupe.pdf` | La même avec traits de coupe et repères de pliure du dos |
| `couverture/Mathematiques-Financieres_face-avant.png` / `.jpg` | 1re de couverture, 300 dpi / 1200 px, pour le web et les réseaux |
| `couverture/Mathematiques-Financieres_4e-de-couverture.png` | 4e de couverture, 300 dpi |
| `couverture/LISEZ-MOI.txt` | Mode d'emploi pour l'imprimeur et pour la diffusion |
| `Mathematiques-Financieres_couverture.zip` | Tout le dossier à envoyer, avec la maquette et la planche de contrôle |
| `planches/couverture-controle.png` | Couverture à plat avec coupe, fond perdu, zone de sécurité et plis du dos |
| `planches/couverture-palettes.png` | Les quatre palettes proposées (émeraude, bordeaux, anthracite, ivoire) |

## Caractéristiques d'impression

- Format fini : 170 × 240 mm par face ; fond perdu : 3 mm ; fichier à plat : 359,4 × 246 mm (TrimBox et BleedBox
  renseignées dans le PDF).
- Dos : 13,4 mm, **estimé** pour 240 pages à 0,056 mm par page. L'imprimeur donne l'épaisseur réelle selon le nombre
  de pages et le papier.
- Couleurs CMJN uniquement : fond en dégradé de C90 M30 J75 N35 à C95 M40 J80 N56, or C5 M20 J72 N0 ; encrage
  maximal de 271 %.
- Texte vectorisé, mis en forme avec HarfBuzz (crénage) : le PDF ne contient aucune police.
- Polices : Noto Serif et Noto Sans, licence SIL OFL 1.1 (usage commercial autorisé), instances figées dans `fonts/`
  par `tools/prep_fonts.py`.

Trois fautes de la maquette d'origine sont corrigées : « Sciences Écommiques » (Économiques), « professionnels de lia
finance » (la finance) et, sur le dos, « Mathématiques Firamières » (Financières).

## À compléter avant l'impression

Dans `tools/make_couverture.py` :

- `PAGES` et `EPAISSEUR_PAGE` : nombre de pages et épaisseur du papier, qui donnent la largeur du dos ;
- `FORMAT` si le livre n'est pas en 17 × 24 cm ;
- `A_COMPLETER` : présentation de l'auteur (`bio`), ISBN à 13 chiffres (`isbn`, le code-barres est alors dessiné) et
  prix (`prix`). Tant qu'une valeur manque, un texte d'attente pâle est imprimé à sa place.

## Régénérer

```bash
python3 -I livres/mathematiques-financieres/tools/make_couverture.py                     # palette émeraude
python3 -I livres/mathematiques-financieres/tools/make_couverture.py --palette bordeaux  # autre palette
```

Il faut Python avec `reportlab`, `uharfbuzz`, `pyphen`, `fontTools` et `Pillow`, l'outil `pdftoppm` (Poppler) pour
les aperçus, et le Chromium de Playwright pour la maquette en volume.
