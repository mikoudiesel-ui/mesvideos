# KSC STUDIO : propositions de logo sur les initiales K S C

Six pistes de logo pour le studio photo KSC STUDIO, toutes construites sur les initiales **K S C**. Elles
partent des couleurs du logo actuel : orange `#FF741F` et noir `#111518`. La piste Couture passe à
l'or champagne `#C9A45C`.

Commencer par `planches/ksc-planche-00-ensemble.png` (vue d'ensemble), puis une planche par piste :
version principale, fond sombre, avatars, cartes de visite, filigrane sur photo.

| Piste | Idée | Idéal pour |
| --- | --- | --- |
| 1 · Objectif | Le logo actuel, plus fort et plus net : le C devient un objectif photo dessiné | Tous publics, enseigne, réseaux sociaux |
| 2 · Viseur | Initiales fines cadrées par les repères du viseur, point de mise au point orange | Portraits, entreprises, mode |
| 3 · Couture | Monogramme de maison de luxe, capitales Didot italiques, or champagne | Mariages, grossesse, portraits premium |
| 4 · Signature | Signature calligraphiée soulignée d'un trait orange, idéale en filigrane | Mariages, familles, artistes |
| 5 · Planche contact | K, S, C et l'objectif rangés en planche contact 2 × 2 : un carré iconique | Instagram, TikTok, événementiel |
| 6 · Cachet | Tampon rond avec diaphragme orange | Tirages, packaging, stickers, textile |

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
python3 -I brand/ksc-studio/tools/make_logos.py --planches
```

Il faut Python avec `fontTools` et le Chromium de Playwright (rendu des PNG). Les couleurs, tailles et
espacements sont en tête de chaque piste dans `tools/make_logos.py`.
