---
workflow: general-video
flow: automation
storyboard: no
message: "BIKINI SHOP (@daya_na990) : tu trouves ton bikini sur TikTok, tu commandes en un message, il arrive à ta porte."
destination: tiktok
aspect: 1080x1920
language: fr
audience: "Clientes TikTok (bikinis d'été)"
length: 28.5s
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
- Voix off : « ajoute un modèle de voix off hyper avancé qui fait la description de la boutique de A à Z », puis « change la voix, une voix plus énergique, toujours avec Gemini ». Gemini TTS (voix Laomedeia, très énergique), 12 phrases qui suivent le parcours : TikTok → message → préparation → commande → livraison à la porte.
- Vraies images : « change les bikinis par les vraies images de bikini de la boutique », puis « extrait les images des bikinis de la photo » avec deux captures du profil TikTok. 15 vignettes « bikini sur mannequin » + 4 coupées, et la photo de profil, extraites par tools/extract_tiktok_tiles.py (compteur incrusté effacé, agrandies ×4 par EDSR ; les photos montrées en grand sont recadrées pour retirer le texte incrusté du haut). Les vignettes centrées sur des personnes ne sont pas utilisées (seule celle du maillot beige montre, en petit, la photo d'un mannequin qui le porte).
- Numéro de téléphone : à la proposition « ajouter ton numéro à la fin pour que les clientes commandent directement », réponse « oui vas-y ». Le numéro de la bio TikTok (07 99 00 45 50) est affiché dans un bouton d'appel sur la signature ; la fin est allongée d'une mesure (2 s, vidéo de 28,5 s) pour qu'on ait le temps de le lire.
- Musique : d'abord la piste du TikTok de référence (4.roues), puis « change la musique de fond, ça ne va pas avec le style de la vidéo ; trouve-moi une musique plus choc qui va attirer la clientèle ». Remplacée par une création originale à 120 BPM (tools/make_music.py), calée sur les transitions, libre de droits.

## Notes

- Aucun logo officiel fourni : le logo « BIKINI SHOP » est un wordmark recréé en SVG (`<template id="logo-tpl">` dans `index.html`).
- Chiffres réels relevés sur la capture du profil : 2368 suivis, 2863 followers, 14.5K j'aime ; vues de chaque vignette ; la vidéo mise en avant (bikini rouge) a 2562 vues. Seul l'avis client (scène 12) reste **inventé**. Le nom affiché sur TikTok est « Bikinis shop » ; la vidéo garde « BIKINI SHOP », le nom donné par l'utilisateur. Le numéro de la bio (07 99 00 45 50) est affiché à la fin, à la demande de l'utilisateur ; certaines vignettes en portent un dans leur texte incrusté, illisible à la taille de la grille, et retiré des photos montrées en grand.
- On n'invente ni prix ni délai de livraison.
- Ancienne musique (`.media/audio/bgm/bgm_001.m4a`, plus utilisée) : extraite du TikTok fourni (AAC 32 kb/s, 26,45 s, ~109 BPM, fondu de sortie 24 → 26 s qui sert la boucle). Les transitions mesurées dans la référence (1,9 s, 3,6 s, 6,1 s, 8,0 s, 17,7 s) tombent à ±0,1 s de notre timeline, donc la synchro est celle de l'original. Volume : la piste source est à -31,6 LUFS ; gain statique +17,5 dB + limiteur suréchantillonné → -14 LUFS, crête vraie -1,8 dBTP (pas de loudnorm dynamique, qui écraserait le fondu final). Voix non vérifiable automatiquement (modèle de transcription non téléchargeable depuis l'environnement) ; l'analyse spectrale ne montre que de la musique.
- Voix off : le texte n'invente ni prix, ni délai, ni zone de livraison. « Écris-nous en message, on te répond » suppose que la commande passe par message privé : à confirmer par l'utilisateur. Musique creusée sous la voix (carve, force 0,5) : la voix passe 10 à 21 dB au-dessus.
- Le Studio (localhost) n'est pas joignable depuis l'app de l'utilisateur : la revue se fait sur le MP4 rendu.
