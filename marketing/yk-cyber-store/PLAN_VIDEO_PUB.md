# Vidéo publicitaire : « La Clé des Maths Financières » (YK Cyber Store)

Plan validé avec l'utilisateur, à reprendre dans la session qui aura l'accès HeyGen.

## Demande

- Vidéo publicitaire pensée pour la visibilité (TikTok, Reels, statuts WhatsApp).
- Une présentatrice **avatar réaliste, femme noire africaine**, qui présente l'ebook.
- **Voix off française très naturelle**, proche d'une vraie voix.
- Script de l'utilisateur, à garder mot pour mot :

> Tu es en finance ou en comptabilité et tu prépares un devoir de maths financières ? Tu connais tes formules, mais
> au moment de résoudre l'exercice… tu bloques ?
>
> Regarde cet ebook : “La clé des maths financières”, chez YK Cyber Store. Il réunit des cours et des exercices
> corrigés pour tes révisions.
>
> Voici une façon de travailler : relis la notion, essaie l'exercice sans regarder la correction, puis compare les
> étapes pour repérer ton erreur.
>
> L'objectif, c'est de comprendre ta démarche, pas seulement de retenir une réponse.
>
> Pour tes prochaines révisions, commande ton ebook chez YK Cyber Store.

## Décisions

- Avatar et voix : **HeyGen**, par le CLI `heygen` (outil prévu par HyperFrames / media-use), avec la clé API de
  l'utilisateur lue dans `HEYGEN_API_KEY` (secret de l'environnement, jamais collé dans la conversation).
- Réseau : l'utilisateur autorise `*.heygen.com` et `*.heygen.ai` dans les réglages de l'environnement.
- Couverture de l'ebook : fournie par l'utilisateur, rangée dans `marketing/yk-cyber-store/ebook/`.
- Format : vertical 1080 × 1920 en priorité, environ 30 s (≈ 80 mots). Une version 16:9 est possible ensuite.
- L'avatar est une IA : à la publication, cocher « contenu généré par IA » sur TikTok et Meta.

## Références HeyGen (documentation fournie par l'utilisateur)

- Clé API : créée par l'utilisateur sur https://platform.heygen.com/api-keys ; en-tête `X-Api-Key`.
- API : `https://api.heygen.com`, en **v3** (les v1 et v2 ne sont plus prises en charge après le 31 octobre 2026).
  Vérifier la clé avec `GET /v3/users/me` ; vidéo d'avatar puis suivi avec `GET /v3/videos/{video_id}`.
- Les vidéos terminées sont servies depuis `files.heygen.ai` : d'où `*.heygen.ai` dans les domaines autorisés.
- Index de la documentation : https://developers.heygen.com/llms.txt et règles pour agents :
  https://developers.heygen.com/docs/for-ai-agents.md (à lire avant les premiers appels).

## Étapes pour la session suivante

1. Vérifier l'accès : `HEYGEN_API_KEY` présent et `api.heygen.com` joignable.
2. Installer le CLI `heygen` (instructions vérifiées de developers.heygen.com/cli), puis
   `npx hyperframes media-use resolve --doctor`.
3. `heygen avatar list --ownership public` : montrer à l'utilisateur 3 ou 4 avatars de femmes noires africaines
   (images fixes) et le laisser choisir avant toute génération.
4. `heygen voice list` : proposer 2 ou 3 voix françaises féminines naturelles, avec un court extrait audio.
5. Générer la vidéo de l'avatar en 9:16 avec le script exact (`heygen video create … --wait`), sans sous-titres.
6. Monter dans HyperFrames (route `/talking-head-recut` : la vidéo de l'avatar reste intacte, les habillages
   s'ajoutent par-dessus), puis épreuves en images avant le rendu final.

## Montage prévu (≈ 30 s)

| Temps | Voix | À l'écran |
| --- | --- | --- |
| 0 – 4 s | « Tu es en finance ou en comptabilité… devoir de maths financières ? » | Accroche en gros dès la 1re seconde : « DEVOIR DE MATHS FINANCIÈRES ? » |
| 4 – 8 s | « Tu connais tes formules… tu bloques ? » | « TU BLOQUES ? » + formules qui s'emmêlent, zoom sur l'avatar |
| 8 – 14 s | « Regarde cet ebook… exercices corrigés pour tes révisions. » | La couverture de l'ebook entre à l'écran ; « Cours + exercices corrigés » |
| 14 – 22 s | « Voici une façon de travailler… repérer ton erreur. » | 3 cartes : 1 Relis la notion · 2 Essaie sans la correction · 3 Compare les étapes |
| 22 – 26 s | « L'objectif, c'est de comprendre ta démarche… » | « COMPRENDRE > RETENIR » |
| 26 – 31 s | « Pour tes prochaines révisions, commande ton ebook chez YK Cyber Store. » | Fin : couverture + « Commande chez YK Cyber Store » (+ contact si fourni) |

Tout au long : sous-titres mot à mot très lisibles (beaucoup regardent sans le son), coupes ou zooms toutes les
2 à 3 s, musique légère sous la voix et bruitages discrets, son à −14 / −16 LUFS.

À demander à l'utilisateur : le contact à afficher à la fin (numéro WhatsApp, page, lien de commande) et le prix
éventuel.
