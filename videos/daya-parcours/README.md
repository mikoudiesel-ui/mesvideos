# Pub BIKINI SHOP (@daya_na990) : du TikTok à ta porte

Pub verticale (1080×1920, 30 i/s, 26,5 s, en boucle) faite avec [HyperFrames](https://hyperframes.heygen.com) (HTML + GSAP).
Elle reprend la mise en scène de la pub 4.roues analysée (15 scènes, caméra 3D, flou de mouvement,
vue éclatée, maquette isométrique) avec le contenu de la boutique **BIKINI SHOP**, compte TikTok **@daya_na990** :
recherche TikTok → profil → vidéo → DM → préparation → commande → avis → livraison → signature.

C'est un **squelette prêt à recevoir les vrais médias** : toutes les photos et vidéos sont des
placeholders (marqués « PLACEHOLDER ») à remplacer.

## Structure

| Fichier | Rôle |
| --- | --- |
| `index.html` | Les 15 scènes (une `<section class="clip">` par scène, ou par groupe de scènes enchaînées), le style, le logo |
| `assets/js/timeline.js` | La timeline GSAP unique : toutes les animations, avec les heures de l'analyse |
| `assets/photos/` | Les placeholders (SVG) à remplacer par les vrais médias |
| `tools/make_placeholders.py` | Régénère les placeholders |
| `BRIEF.md`, `STORYBOARD.md` | Le brief et le découpage scène par scène |

## Musique

La musique est celle de la vidéo de référence (TikTok 4.roues) : piste extraite telle quelle et calée à 0 s,
donc elle tombe sur les mêmes transitions que dans l'original. Elle est dans `.media/audio/bgm/bgm_001.m4a`,
montée à -14 LUFS (le niveau habituel des réseaux sociaux), et branchée dans `index.html` (`<audio id="music">`).

- **Changer de musique** : remplace le `src` de `<audio id="music">` par un fichier d'environ 26,5 s.
- **Qualité** : la piste vient d'un TikTok téléchargé (AAC 32 kb/s). Avec le fichier original du son, remplace-le pour un rendu plus propre.
- **Droits** : si c'est un son commercial, TikTok peut couper le son d'une vidéo publiée par un compte professionnel ou en pub.
  Dans ce cas, publie la vidéo et ajoute le même son depuis la bibliothèque TikTok au moment de publier.

## Médias à fournir

Dépose ton fichier dans `assets/photos/`, puis remplace le nom du placeholder dans `index.html`.

| Placeholder | Scène | À remplacer par |
| --- | --- | --- |
| `grid-01.svg` … `grid-06.svg` | 4-5 · grille du profil | Miniatures de tes vidéos TikTok (format 3:4) |
| `grid-05.svg` | 5 · tuile qui se détache | La miniature de la vidéo mise en avant |
| `tiktok-bikini.svg` | 6 · vidéo TikTok | Ta vidéo (9:16). Pour une vidéo : `<video class="ph" src="assets/video/….mp4" muted playsinline></video>` |
| `dm-bikini.svg` | 7 · photo dans le DM | Photo du bikini (carrée) |
| `bikini-3d.svg` | 8 · vue éclatée | Photo du bikini **détourée** (PNG transparent) |
| `cinema-plage.svg` | 9 · plan cinéma | Vidéo plein écran 9:16 (plage, coucher de soleil). Le code pour la vidéo est en commentaire dans `index.html` |
| `livraison-colis.svg` | 13 · livraison | Photo d'une cliente qui reçoit son colis |
| `main-colis.svg` | 14 · conclusion | Photo **détourée** d'une main qui tend le colis |

Le **logo BIKINI SHOP** est un wordmark recréé en SVG (`<template id="logo-tpl">` en bas de `index.html`).
Il est cloné automatiquement dans tous les emplacements `data-logo` : avatar, logo néon, plaque, signature.
Si la boutique a un vrai logo, remplace le contenu du template.

## Valeurs provisoires à remplacer

- **Compteurs du profil** (scène 4) : attributs `data-from` / `data-to` des `<b class="cnt">` dans `index.html`.
- **Vues de la vidéo** (scène 6) : `count($("#s6-count"), 13, 96, …)` et `count(…, 96, 248, …)` dans `timeline.js`.
- **Vues des tuiles** : les `<div class="views">` de la grille.
- **Avis client** (scène 12) : nom, texte et article dans `#s12-card`. Mets un vrai avis de cliente.

## Modifier

- **Textes** : directement dans `index.html` (chaque scène est commentée avec ses heures).
- **Minutage** : `timeline.js`. Chaque bloc `S1` … `S15` donne les heures en secondes. Si tu décales une scène, décale aussi `data-start` / `data-duration` de sa `<section>`.
- **Couleurs** : variables `--red` (corail), `--black` (nuit prune) en haut de `index.html`.

## Commandes

```bash
npx hyperframes lint      # vérification rapide
npx hyperframes check     # vérification complète (lint, rendu, mise en page, contraste)
npx hyperframes snapshot --at 1.7,4.6,7.3,11.2,16.6,19.5,23.3,25.3   # images fixes
npx hyperframes render --output renders/bikini-shop-parcours.mp4
```

Les avertissements `nested_structure_needs_subcomposition` du lint sont attendus. Toutes les scènes sont
dans un seul fichier parce que plusieurs transitions passent d'une scène à l'autre (la tuile devient la vidéo,
le DM devient la vue éclatée).
