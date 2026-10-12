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

Création **originale** (`tools/make_music.py`) : dance-pop / afro-house d'été à **120 BPM**, 26,5 s, synthétisée
note par note (aucun échantillon externe, donc **libre de droits** : TikTok ne la coupera pas).
À 120 BPM un temps dure 0,5 s, et toutes les transitions de la vidéo tombent sur un temps. Les temps forts sont
calés sur l'image : montée puis impact sur le logo (1,0 s), groove sur la partie TikTok, pause sur la plage (11,5 s),
roulement puis **drop** sur « Ta commande, en 1 clic » (15,0 s), retombée puis impact sur l'explosion corail (23,5 s),
accord final sur la signature. Mixée pour le téléphone (moins de sub, plus de mordant), à -14 LUFS.

- **Régénérer / modifier** : `python3 tools/make_music.py` (tempo, accords, mélodie, effets et leurs heures sont en haut
  du fichier et dans `main()`), puis relance le carve (voir « Voix off »).
- L'ancienne piste (musique de la vidéo de référence) reste dans `.media/audio/bgm/bgm_001.m4a` mais n'est plus utilisée.

## Voix off

Voix **Gemini TTS** (modèle `gemini-3.8-flash-tts`, voix « Laomedeia » : jeune femme, **très énergique**, ton de pub TikTok).
Le texte est généré **en une seule prise** (ton homogène, une seule requête), ramené à -16 LUFS, puis
`tools/split_voiceover.py` le découpe aux pauses en 12 phrases (`assets/voice/vo-01.wav` … `vo-12.wav`) et place
chacune sur sa scène :

| Départ | Phrase |
| --- | --- |
| 0.95 s | « BIKINI SHOP. » |
| 2.14 s | « Ton bikini de l'été ? Tu le trouves sur TikTok. » |
| 4.93 s | « Sur notre compte, tous nos modèles en vidéo. » |
| 7.23 s | « Un coup de cœur ? » |
| 8.05 s | « Écris-nous en message, on te répond. » |
| 9.88 s | « On prépare ton bikini avec soin. » |
| 12.06 s | « Direction la plage ! » |
| 14.55 s | « Ta commande en un clic : confirmée, préparée, en route. » |
| 18.35 s | « Et le meilleur ? » |
| 20.55 s | « On te livre directement à ta porte. » |
| 22.96 s | « Ton été commence ici. » |
| 24.43 s | « BIKINI SHOP, sur TikTok. » |

La musique est « creusée » sous la voix (voiceover carve de HyperFrames, attribut `data-fx-carve` sur `<audio id="music">`) :
elle laisse la place à la voix dans ses fréquences et baisse pendant qu'elle parle, sans s'éteindre.

- **Changer le texte, la voix ou le ton** : modifie `assets/voice/request.json` (texte complet, `voice`, `style`) et
  `assets/voice/lines.json` (les mêmes phrases, une par ligne), puis lance `tools/make_voiceover.sh`. Reporte ensuite les
  départs et durées de `assets/voice/plan.json` dans les `<audio id="vo-NN">` d'`index.html` et relance le carve.
- **Moment de chaque phrase** : liste `ANCHORS` dans `tools/split_voiceover.py`.
- **Clé Gemini** : stockée dans l'environnement cloud (« Network secrets », hôte `generativelanguage.googleapis.com`,
  en-tête `x-goog-api-key`). L'offre gratuite limite à 3 requêtes par minute.

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
