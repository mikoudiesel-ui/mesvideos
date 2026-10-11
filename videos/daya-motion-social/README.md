# BIKINIS SHOP / @daya_na990 : motion social en 14 scènes (MAQUETTE)

Vidéo verticale 1080×1920, 30 i/s, 794 images (26,467 s), faite avec [HyperFrames](https://hyperframes.heygen.com)
à partir du dossier « DAYA 14 SCÈNES » (`reference/`). Les visuels produit sont des illustrations du dossier :
c'est une **maquette**, pas une publicité catalogue finale.

## Structure

| Fichier | Rôle |
| --- | --- |
| `index.html` | Composition principale : décor, 14 scènes, marquage maquette, mix audio |
| `compositions/decor.html` | Décor de boutique continu (arches, palmiers) ; lumière et flou par scène |
| `compositions/s01-ouverture.html` … `s14-boucle.html` | Une sous-composition par scène, limites exactes du JSON |
| `compositions/maquette.html` | Mention « MAQUETTE · VISUELS ILLUSTRATIFS » |
| `assets/css/daya.css` | Couleurs, téléphone, cartes, néons, boutons communs |
| `assets/img/` | Découpes produit tirées des maquettes (`tools/prep_assets.py`) |
| `assets/audio/mix_daya_motion_social.wav` | Mix : son témoin + bruitages (`tools/make_mix.py`) |
| `captures/` | 14 captures de milieu de scène et planches de revue (`tools/review_sheets.py`) |
| `BRIEF.md`, `STORYBOARD.md` | Brief et découpage, avec la géométrie partagée entre les scènes |

## Modifier

- **Textes** : chaque titre est un `<h1 class="scene-title">` dans sa scène ; le handle et le CTA sont en clair dans `s13-signature.html`.
- **Vraies photos** : remplacer `assets/img/bleu-detoure.png` (mannequin détouré, 870×1668), `rose-photo.jpg`, `vert-photo.jpg` et les `detail-*.jpg` en gardant les mêmes noms et proportions ; les raccords reposent sur ces dimensions.
- **Son** : `python3 -I tools/make_mix.py --project videos/daya-motion-social` (base témoin + bruitages, −16 LUFS).
- **Planches de revue** : captures avec `npx hyperframes snapshot`, puis `python3 -I tools/review_sheets.py`.

## Commandes

```bash
npx hyperframes@0.8.143 check videos/daya-motion-social
npx hyperframes@0.8.143 snapshot videos/daya-motion-social --at 0.9,2.8,4.53
npx hyperframes@0.8.143 render videos/daya-motion-social --output renders/DAYA_MOTION_SOCIAL_MAQUETTE.mp4
```

## Assets à fournir pour un final catalogue

- Photos HD du modèle bleu fleuri (idéalement détouré), du rose et du vert.
- Un gros plan du bleu (fleur, motif, liens).
- L'avatar / le logo de la boutique, si disponible.
- Une musique autorisée si le son témoin doit être remplacé.
