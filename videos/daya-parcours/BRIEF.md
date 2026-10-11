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

## Notes

- Aucun logo officiel fourni : le logo « BIKINI SHOP » est un wordmark recréé en SVG (`<template id="logo-tpl">` dans `index.html`).
- Valeurs **provisoires** à remplacer par les vraies : compteurs du profil (Abonnements / Followers / J'aime), vues de la vidéo (13 k → 248 k), vues des tuiles de la grille, avis client (nom, texte, article).
- On n'invente ni prix ni délai de livraison.
- Pas d'audio : la piste de la vidéo de référence n'a pas été analysée. Une musique d'été peut être ajoutée ensuite.
- Le Studio (localhost) n'est pas joignable depuis l'app de l'utilisateur : la revue se fait sur le MP4 rendu.
