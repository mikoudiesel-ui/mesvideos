---
workflow: general-video
flow: automation
storyboard: no
message: "BIKINI SHOP (@daya_na990) : tu trouves ton bikini sur TikTok, tu commandes en un message, il arrive à ta porte."
destination: tiktok
aspect: 1080x1920
language: fr
audience: "Clientes TikTok (bikinis d'été)"
length: 26.5s
angle: "Le parcours cliente filmé comme une interface : recherche TikTok → profil → vidéo → DM → préparation → commande → avis → livraison → signature, en boucle"
---

## Intent

L'utilisateur a fourni l'analyse motion design d'une pub de 26 s (concession 4.roues) : 15 scènes,
caméra 3D en perspective, flou de mouvement aux transitions, textes qui se précisent depuis le flou,
compteurs qui défilent, vue éclatée en couches, maquette isométrique, boucle sur le point de départ.
Il a ensuite demandé : « je veux que la vidéo soit essentiellement basée sur la boutique daya »,
puis : « le nom de la boutique c'est BIKINI SHOP, n'oublie pas ce détail là ».

On garde donc la mise en scène et le minutage de l'analyse, et on remplace tout le contenu par la
boutique **BIKINI SHOP** (compte TikTok **@daya_na990**).

## Customizations

- Nom affiché partout : **BIKINI SHOP** (logo, en-tête du profil, carte du DM, enseigne de la boutique 3D, signature finale). Le compte TikTok reste **@daya_na990**.
- Instagram → **TikTok** (la boutique vend sur TikTok) : recherche « Utilisateurs », profil TikTok (Abonnements / Followers / J'aime), vidéo avec le rail J'aime / Avis / Partager.
- Voitures → **bikinis** ; remise des clés → **colis remis à la porte**.
- Palette : nuit prune `#120a1c`, corail néon `#ff4f70` (même corail que la pub isométrique précédente), crème `#fff4e8`.
- Typo : Unbounded (titres, déjà utilisée dans la pub isométrique) + Inter (interface TikTok).
- Squelette prêt à recevoir les vrais médias : chaque photo/vidéo est un placeholder nommé dans `assets/photos/`.
- Voix off : « ajoute un modèle de voix off hyper avancé qui fait la description de la boutique de A à Z ». Gemini TTS (voix Leda), 12 phrases qui suivent le parcours : TikTok → message → préparation → commande → livraison à la porte.
- Vraies images : « change les bikinis par les vraies images de bikini de la boutique ». En attente des photos (tiktok.com est bloqué par le réseau de l'environnement ; l'utilisateur doit les envoyer).
- Musique : « utilise une musique identique à celle de la vidéo pour l'ajouter à la vidéo de bikini shop ». La piste audio du TikTok de référence (4.roues) est reprise telle quelle et calée à 0 s, comme dans l'original.

## Notes

- Aucun logo officiel fourni : le logo « BIKINI SHOP » est un wordmark recréé en SVG (`<template id="logo-tpl">` dans `index.html`).
- Valeurs **provisoires** à remplacer par les vraies : compteurs du profil (Abonnements / Followers / J'aime), vues de la vidéo (13 k → 248 k), vues des tuiles de la grille, avis client (nom, texte, article).
- On n'invente ni prix ni délai de livraison.
- Musique (`.media/audio/bgm/bgm_001.m4a`) : extraite du TikTok fourni (AAC 32 kb/s, 26,45 s, ~109 BPM, fondu de sortie 24 → 26 s qui sert la boucle). Les transitions mesurées dans la référence (1,9 s, 3,6 s, 6,1 s, 8,0 s, 17,7 s) tombent à ±0,1 s de notre timeline, donc la synchro est celle de l'original. Volume : la piste source est à -31,6 LUFS ; gain statique +17,5 dB + limiteur suréchantillonné → -14 LUFS, crête vraie -1,8 dBTP (pas de loudnorm dynamique, qui écraserait le fondu final). Voix non vérifiable automatiquement (modèle de transcription non téléchargeable depuis l'environnement) ; l'analyse spectrale ne montre que de la musique.
- Voix off : le texte n'invente ni prix, ni délai, ni zone de livraison. « Écris-nous en message, on te répond » suppose que la commande passe par message privé : à confirmer par l'utilisateur. Musique creusée sous la voix (carve, force 0,8).
- Le Studio (localhost) n'est pas joignable depuis l'app de l'utilisateur : la revue se fait sur le MP4 rendu.
