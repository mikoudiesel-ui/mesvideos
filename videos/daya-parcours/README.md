# Pub BIKINI SHOP (@daya_na990) : du TikTok à ta porte

Pub verticale (1080×1920, 30 i/s, 26,5 s, en boucle) faite avec [HyperFrames](https://hyperframes.heygen.com) (HTML + GSAP).
Elle reprend la mise en scène de la pub 4.roues analysée (15 scènes, caméra 3D, flou de mouvement,
vue éclatée, maquette isométrique) avec le contenu de la boutique **BIKINI SHOP**, compte TikTok **@daya_na990** :
recherche TikTok → profil → vidéo → DM → préparation → commande → avis → livraison → signature.

Les photos sont les **vraies vignettes du profil TikTok de la boutique** (bikinis sur mannequin), avec les vrais
chiffres du compte (2368 suivis, 2863 followers, 14.5K j'aime) et la vraie photo de profil.

## Structure

| Fichier | Rôle |
| --- | --- |
| `index.html` | Les 15 scènes (une `<section class="clip">` par scène, ou par groupe de scènes enchaînées), le style, le logo |
| `assets/js/timeline.js` | La timeline GSAP unique : toutes les animations, avec les heures de l'analyse |
| `assets/photos/` | Les vraies photos de la boutique, extraites des captures du profil TikTok (`tiles.json` : fichiers et vues) |
| `tools/extract_tiktok_tiles.py` | Extrait les vignettes « bikini » des captures, efface les compteurs incrustés, agrandit ×4 (EDSR) |
| `tools/make_music.py` | Musique originale 120 BPM |
| `tools/make_voiceover.sh`, `tools/split_voiceover.py` | Voix off Gemini : génération, découpe et placement |
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

## Photos

Les 15 vignettes de la grille du profil sont les vraies vignettes TikTok de la boutique, dans cet ordre :
`bikini-bleu-fleuri.jpg` (309 vues), `bikini-rose-crochet.jpg` (166 vues), `bikini-marron-leopard.jpg` (1343 vues), `bikini-orange.jpg` (484 vues), `bikini-vert.jpg` (775 vues), `maillot-beige.jpg` (1655 vues), `bikini-papillons.jpg` (510 vues), `bikini-marron-paillettes.jpg` (2320 vues), `bikini-bleu-pareo.jpg` (1560 vues), `bikini-marron-chaine.jpg` (630 vues), `bikini-rouge.jpg` (2562 vues), `top-turquoise.jpg` (841 vues), `bikini-rouge-2.jpg` (1111 vues), `bikini-peche.jpg` (304 vues), `bikini-rose-blanc.jpg` (— vues). Chaque vignette garde son vrai nombre de vues (redessiné net par-dessus).

| Scène | Photo |
| --- | --- |
| 3, 4, 6, 7 · avatar (recherche, profil, vidéo, DM) | `avatar.jpg` (vraie photo de profil) |
| 5 · la vignette qui se détache | `bikini-rouge-hero.jpg` (2562 vues, la vidéo produit la plus vue) |
| 6 · vidéo TikTok, 7 · photo du DM, 8 · produit préparé | `bikini-rouge-hero.jpg` |
| 9 · mur de photos derrière le logo | 12 autres vignettes, dont les 4 coupées en haut sur la capture |
| 13 · livraison | `bikini-rouge-2-hero.jpg` |
| 14 · « Ton été commence ici » | éventail `bikini-bleu-fleuri`, `bikini-rouge-hero`, `bikini-vert-hero` |

Les fichiers `*-hero.jpg` sont les mêmes photos sans leur haut, où la vidéo TikTok incruste son texte : illisible une fois
agrandi, et sur le bikini rouge c'est un bout de numéro de téléphone (liste `HEROES` dans le script d'extraction).
Dans la grille et le mur de photos, les vignettes restent entières, comme sur TikTok : leurs textes y sont trop petits pour être lus.

**Netteté** : les vignettes font 135 × 179 pixels sur la capture. Elles sont agrandies ×4 par super-résolution (EDSR),
ce qui suffit pour la grille et les cartes, mais les **photos ou vidéos originales** (depuis le téléphone, ou des
vidéos TikTok téléchargées) donneraient une image bien plus nette : il suffit de remplacer les fichiers du même nom.

**Refaire l'extraction** avec de nouvelles captures (navigateur, page profil, grille de 6 colonnes) :
`python3 tools/extract_tiktok_tiles.py capture1.webp capture2.webp --model EDSR_x4.pb` ; le modèle EDSR se télécharge sur
`raw.githubusercontent.com/Saafke/EDSR_Tensorflow/master/models/EDSR_x4.pb`. La liste des vignettes gardées est dans `GRID` et `EXTRA`.
Les captures elles-mêmes ne sont pas versionnées (numéro de téléphone de la bio, vignettes avec des personnes).

Le **logo BIKINI SHOP** est un wordmark recréé en SVG (`<template id="logo-tpl">` en bas de `index.html`).
Il est cloné automatiquement dans les emplacements `data-logo` : logo néon, plaque, signature (les avatars de
l'interface TikTok utilisent la vraie photo de profil).
Si la boutique a un vrai logo, remplace le contenu du template.

## Valeur provisoire à remplacer

- **Avis client** (scène 12) : nom, texte et article dans `#s12-card` sont inventés. Mets un vrai avis de cliente.
- Les compteurs du profil (`data-from` / `data-to` des `<b class="cnt">`), les vues de la vidéo (`count($("#s6-count"), …)`
  dans `timeline.js`) et les vues des vignettes sont les vrais chiffres relevés sur le profil TikTok.

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
