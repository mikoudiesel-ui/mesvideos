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
| `assets/audio/musique_daya_nudisco_120bpm.wav` | Musique originale composée pour la vidéo, nu-disco / French touch (`tools/make_music_nudisco.py`) |
| `assets/audio/musique_daya_afrohouse_120bpm.wav` | Première version de la musique, afro-house (`tools/make_music_afrohouse.py`), gardée en alternative |
| `assets/audio/mix_daya_motion_social.wav` | Mix final : musique + bruitages d'interface (`tools/make_mix.py`) |
| `renders/DAYA_MOTION_SOCIAL_MAQUETTE.mp4` | Vidéo rendue (H.264, AAC 48 kHz) |
| `captures/` | 14 captures de milieu de scène et planches de revue (`tools/review_sheets.py`) |
| `BRIEF.md`, `STORYBOARD.md` | Brief et découpage, avec la géométrie partagée entre les scènes |

## Modifier

- **Textes** : chaque titre est un `<h1 class="scene-title">` dans sa scène ; le handle et le CTA sont en clair dans `s13-signature.html`.
- **Vraies photos** : remplacer `assets/img/bleu-detoure.png` (mannequin détouré, 870×1668), `rose-photo.jpg`, `vert-photo.jpg` et les `detail-*.jpg` en gardant les mêmes noms et proportions ; les raccords reposent sur ces dimensions.
- **Musique** : `python3 -I videos/daya-motion-social/tools/make_music_nudisco.py --project videos/daya-motion-social` (tempo, accords, motifs et détails en tête du fichier), puis `python3 -I videos/daya-motion-social/tools/make_mix.py --project videos/daya-motion-social` (musique + bruitages, −16 LUFS). Pour revenir à l'afro-house : ajouter `--bed assets/audio/musique_daya_afrohouse_120bpm.wav` au mix, puis relancer le rendu.
- **Vérifier un rendu** : `python3 -I videos/daya-motion-social/tools/verify_render.py --project videos/daya-motion-social --mp4 videos/daya-motion-social/renders/DAYA_MOTION_SOCIAL_MAQUETTE.mp4`.
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
- Une musique sous licence, si l'on préfère un titre existant à la composition originale.
