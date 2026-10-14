# Y-K Design : publicité de services pour boutiques

Pub horizontale **1920 × 1080, 30 i/s, 623 images (20,7667 s)**, faite avec [HyperFrames](https://hyperframes.heygen.com)
(HTML + GSAP) à partir du dossier « DOSSIER_YK_DESIGN_CLAUDE_LEGER ». Elle reprend la mécanique de la vidéo de
référence (17 plans, coupes franches aux images 152, 368, 524, 555, 573, 584 et 596) avec l'identité Y-K Design :
monogramme YK (option B), Y-K Design, les trois concepts (baskets, parfum, sac) et le contact **+225 07 12 35 46 02**.

Rendu livré : `renders/YK_DESIGN_PUBLICITE_1080P.mp4` (H.264 yuv420p 30 i/s constant, AAC stéréo 48 kHz ~194 kb/s, faststart).

## Fichiers

| Fichier | Rôle |
| --- | --- |
| `index.html` | Les 8 plans (un par coupe franche) avec tous les textes, boutons, champ et numéro en calques éditables |
| `assets/js/timeline.js` | La timeline maîtresse unique, en images (`F(f) = f / 30`) : chaque mouvement est daté à l'image |
| `assets/images/` | Monogramme (original + version rognée à sa silhouette), trois affiches, curseurs et spinner du dossier |
| `assets/fonts/` | Inter 400/700 et EB Garamond 700 (licences OFL incluses) |
| `assets/audio/AUDIO_MASTER.wav` | Le mix fourni, décodé du FLAC sans perte (`ffmpeg -i AUDIO_MASTER.flac -c:a pcm_s24le …`) |
| `dossier/` | Le brief : prompt, BRAND_CONFIG, TIMELINE, CARTES, VERIFICATIONS et les 17 fiches de scène |

Les fenêtres des plans sont bornées à la demi-image, `(f − 0,5) / 30`, pour que l'image f appartienne bien au nouveau plan.
Les gros plans des cartes sont des recadrages des trois affiches (`CARDS` dans `timeline.js`, d'après `CARTES.json`) ;
aucun produit n'a été généré. Les cartes de la couronne gardent une rotation nulle : seuls leurs centres tournent.

## Plan par plan

| Scène | Images | Contenu |
| --- | --- | --- |
| 01 | 0–35 | Monogramme géant qui recule (≈154 px à f6, 71 px à f12, 90 px à f30) |
| 02 | 36–77 | Le monogramme glisse à gauche, Y-K Design se révèle, le bloc monte |
| 03–04 | 78–151 | Galerie quatre colonnes masquées (affiches, gros plans, cartes STYLE / SIGNATURE / ALLURE), EXEMPLES CRÉATIFS, défilement continu jusqu'à la coupe |
| 05 | 152–233 | « Des publicités » + créatives / dynamiques / sur mesure / pour boutiques dans le cartouche |
| 06 | 234–283 | « Je réalise » « vos montages », punch-in à f257, « vos montages » seul au centre |
| 07 | 284–327 | Six cartes en couronne (rayons 430 × 330 px, cartes de 250 px), rotation horaire des positions |
| 08 | 328–343 | Curseur blanc sur le parfum, voile, bouton Créer ma publicité, appui à f340–343 |
| 09 | 344–367 | Punch-in ×2,4 puis translation : le même parfum (600 px) près du centre |
| 10 | 368–437 | Page projet floutée, modal Votre projet publicitaire, frappe de « Votre boutique » (f380–416) |
| 11 | 438–458 | Appui sur Préparer le montage, spinner blanc fini (deux tours, f444–458) |
| 12 | 459–523 | Carte sombre Montages pour boutiques + numéro, zoom vers f483 puis pause |
| 13 | 524–554 | Intéressé ? Écrivez-moi. + numéro |
| 14–16 | 555–595 | AVEC · monogramme · Y-K Design (flashs aux coupes de la référence) |
| 17 | 596–622 | Signature compacte, Montages publicitaires pour boutiques, numéro ; pas de fondu final |

## Vérifications faites

- 623 images vidéo comptées, 1920×1080, 30 i/s, aucune image noire (`blackdetect`).
- Chaque coupe contrôlée image par image dans le MP4 (f151/152, f367/368, f523/524, f554/555, f572/573, f583/584, f595/596).
- Son : corrélé au mix fourni, **décalage 0 échantillon**, même niveau (−14,0 LUFS, crête −1,3 dB), aucun son ajouté.
- `npx hyperframes check` : 0 erreur (les avertissements `nested_structure_needs_subcomposition` sont attendus : un plan contient plusieurs scènes enchaînées).

## Commandes

```bash
npx --yes hyperframes@0.8.143 check
npx --yes hyperframes@0.8.143 snapshot --at 0.2,2.0,3.7,5.3,8.6,10.3,11.7,13.3,16.3,18.0,19.3,20.5
npx --yes hyperframes@0.8.143 render --output renders/YK_DESIGN_PUBLICITE_1080P.mp4
ffprobe -v error -count_frames -show_entries stream=nb_read_frames -of csv=p=0 renders/YK_DESIGN_PUBLICITE_1080P.mp4   # 623
```

## À savoir

- **Bande-son** : le mix fourni vient de la publicité de référence (Pinterest). Il est utilisé tel quel, comme le demande
  le dossier, mais il appartient à son auteur : pour une diffusion publique, une musique libre de droits recalée sur les
  mêmes repères évite un blocage ou un retrait.
- La vidéo de référence, les maquettes et le PDF du dossier ne sont pas dans le dépôt (seulement les fichiers nécessaires au rendu).
- Les textes, couleurs et le numéro sont dans `index.html` ; les minutages dans `timeline.js` (en images).
