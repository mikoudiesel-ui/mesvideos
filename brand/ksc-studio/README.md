# KSC STUDIO : propositions de logo sur les initiales K S C

Six pistes de logo pour le studio photo KSC STUDIO, toutes construites sur les initiales **K S C**. Elles
partent des couleurs du logo actuel : orange `#FF741F` et noir `#111518`. La piste Couture passe à
l'or champagne `#C9A45C`.

**À envoyer : `KSC_STUDIO_propositions_logo.pdf`**, un seul fichier de 7 pages (0,8 Mo) qui s'ouvre sur
téléphone comme sur ordinateur. Les logos y restent vectoriels, donc nets même en zoomant.

Le PDF reprend les planches de `planches/` : d'abord la vue d'ensemble (`ksc-planche-00-ensemble.png`),
puis une planche par piste avec la version principale, le fond sombre, les avatars, les cartes de visite
et le filigrane sur photo.

| Piste | Idée | Idéal pour |
| --- | --- | --- |
| 1 · Objectif | Le logo actuel, plus fort et plus net : le C devient un objectif photo dessiné | Tous publics, enseigne, réseaux sociaux |
| 2 · Viseur | Initiales fines cadrées par les repères du viseur, point de mise au point orange | Portraits, entreprises, mode |
| 3 · Couture | Monogramme de maison de luxe, capitales Didot italiques, or champagne | Mariages, grossesse, portraits premium |
| 4 · Signature | Signature calligraphiée soulignée d'un trait orange, idéale en filigrane | Mariages, familles, artistes |
| 5 · Planche contact | K, S, C et l'objectif rangés en planche contact 2 × 2 : un carré iconique | Instagram, TikTok, événementiel |
| 6 · Cachet | Tampon rond avec diaphragme orange | Tirages, packaging, stickers, textile |
| 7 · Fusion | Ajoutée après le choix des pistes 1 et 2 : initiales fines du Viseur, C en objectif, cadre de mise au point | Tous usages |

## Finalistes

Les pistes 1 (Objectif) et 2 (Viseur) ont été retenues ; la piste 7 (Fusion) les réunit. Le document
**`KSC_STUDIO_finalistes.pdf`** (5 pages, à faire voter : A, B ou C) les compare dans les mêmes
situations : logos, profil réseaux sociaux, façade, cartes de visite, filigrane sur photo. Les pages
sont aussi dans `planches/finalistes/`. Les photos des maquettes sont générées (`tools/photos.py`),
ce ne sont pas des photos réelles.

## Logo retenu : A · Objectif — le kit

**`KSC_STUDIO_kit_logo.zip`** (le même contenu que `kit-objectif/`) contient tout ce qu'il faut pour
utiliser le logo, avec un `LISEZ-MOI.txt` :

- `1_logo/` : versions verticale, horizontale, initiales et symbole ; chacune en couleur, négatif,
  noir et blanc (une seule couleur) ; en SVG et PDF vectoriels et en PNG transparent ;
- `2_reseaux-sociaux/` : photo de profil, couverture Facebook, bannière YouTube, modèle de story,
  post d'annonce du nouveau logo ;
- `3_filigrane/` : logo à poser sur les photos ;
- `4_carte-de-visite/` : PDF recto verso 85 × 55 mm avec 3 mm de fond perdu, pour l'imprimeur
  (coordonnées d'exemple tant que `CONTACT` n'est pas rempli dans `tools/make_kit.py`) ;
- `5_site-web/` : favicon.ico et icônes d'application ;
- `KSC_STUDIO_charte-graphique.pdf` : versions, couleurs, police, tailles minimales, règles
  (aperçus dans `planches/kit/`).

## Fichiers

Chaque piste a trois versions, en SVG (vectoriel) et en PNG transparent :

- `clair` : sur fond clair (site, documents, cartes) ;
- `sombre` : sur fond sombre ou sur photo (filigrane) ;
- `icone` : carré 1000 × 1000 pour photo de profil, appli, favicon.

Les SVG sont 100 % vectoriels : le texte est converti en tracés, aucune police à installer. Ils
s'ouvrent dans Illustrator, Inkscape, Affinity, Canva ou chez un imprimeur, et s'agrandissent sans
perte (enseigne, bâche, textile). Les PNG servent au web et aux réseaux.

## Polices

Polices libres sous licence SIL Open Font License 1.1, utilisables commercialement, y compris dans un
logo : Montserrat, Jost, Bodoni Moda, Corinthia. Les fichiers et les licences sont dans `fonts/`.

## Régénérer

```bash
python3 -I brand/ksc-studio/tools/make_logos.py --planches   # logos, planches PNG et PDF des 6 pistes
python3 -I brand/ksc-studio/tools/make_finalistes.py          # document des finalistes A, B, C
python3 -I brand/ksc-studio/tools/make_kit.py                 # kit du logo retenu (dossier + ZIP)
```

Il faut Python avec `fontTools` et le Chromium de Playwright (rendu des PNG). Les couleurs, tailles et
espacements sont en tête de chaque piste dans `tools/make_logos.py`.
