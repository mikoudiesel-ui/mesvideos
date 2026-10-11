---
format: 1080x1920
fps: 30
frames: 794
duration: 26.466667s
message: "Découvrez la collection BIKINIS SHOP et écrivez-nous sur TikTok (@daya_na990)."
audience: "Clientes TikTok à la recherche d'un bikini coloré"
mode: collaborative
bpm: 120
---

Quatorze sous-compositions (une par scène) sur la piste 1, posées exactement sur les limites de
`reference/TIMELINE_14_SCENES.json`. Le décor de boutique (`compositions/decor.html`, piste 0) court
sur toute la durée : sa lumière, son flou et ses palmiers changent par scène sans jamais couper, et
son état final égale l'image 0 pour la boucle. Le marquage maquette est sur la piste 2, le mix audio
sur la piste 10.

`mode: collaborative` : l'utilisateur a demandé à valider des planches d'images avant tout rendu MP4
(`captures/PLANCHE_*.jpg`).

Recherche catalogue faite avant de construire : « phone mockup », « neon glow outline », « search bar
typing », « chat message bubble typing », « like heart pop », « end card call to action ». Les blocs
trouvés (device-frame-stage, outline-draw, chat-message…) n'imposent pas la géométrie partagée dont
les raccords ont besoin d'une scène à l'autre ; téléphone, néons et cartes sont donc construits à la
main dans `assets/css/daya.css`.

## Musique (tools/make_music.py)

Afro-house tropical originale, 120 BPM, la mineur (Am9 – Fmaj9 – Cmaj9 – G6/9, montée Dm9 – E7). Les
mesures commencent à 1,8 s + 2 s·n, si bien que les coupes 1,8 / 3,8 / 7,8 / 11,8 / 17,8 s tombent sur un
premier temps. Intro sans batterie, interface filtrée (S02–S03), groove complet sur la coupe de S04,
pause et montée avant le produit héros (impact sur la coupe 9,6 s, drop au premier temps 9,8 s), respiration
en S10–S11, montée en S12, impact et cloches de signature sur 23,0 s, drop final au premier temps 23,8 s
(le bouton est en place dès 23,3 s), sortie filtrée dont les queues reviennent au début : la boucle TikTok
est continue. Chaque détail a sa note : vignettes S03, inserts et repères S07, widgets S08, cœur S10,
inserts S11, appui sur Message S12, reflet du bouton S13. Nappes et basse « pompent » sur la grosse caisse.

## Passe d'auto-correction avant le rendu final

- Titres : apparition flou → net (technique du composant `soft-blur-in` du catalogue), sortie en flou.
- Reflets lumineux masqués par la silhouette sur le mannequin (S01, S06, S13), sur la carte sélectionnée (S04) et sur le bouton « Écrivez-nous sur TikTok » (S13) — technique du composant `shimmer-sweep`.
- Halos et anneau qui pulsent sur la grosse caisse pendant les drops (S06, S09, S13).
- S02 : aperçu des trois modèles sous le résultat ; il se range dans la grille du profil (raccord S02 → S03).
- S08 : les coques des widgets scintillent pendant le chargement au lieu de rester vides.
- S07 : traits et repères plus épais et plus lumineux.
- Grain de pellicule très léger sur toute la vidéo (`assets/img/grain.png`, déplacé toutes les 2 images ; technique du composant `grain-overlay`, pilotée par GSAP).

## Géométrie partagée (raccords)

Le mannequin (`assets/img/bleu-detoure.png`, 870×1668) est toujours placé par (x, y, échelle) depuis
son coin haut gauche, centre visuel x = 458 px de l'image. Les cartes produit sont des éléments
630×960 (galerie) ou 620×1120 (grande carte) mis à l'échelle uniformément : coins et image restent
identiques d'une scène à l'autre.

| Coupe | Élément partagé | État à la coupe |
| --- | --- | --- |
| S01 → S02 | anneau au sol → anneau d'avatar ; cercle de lumière → contour de recherche ; produit → avatar | cercle (300, 1080) r 70 ; rect (215, 790, 580×115, r 57,5) ; mannequin (223,67 ; 1005 ; ×0,1667) découpé en disque |
| S02 → S03 | avatar, nom, handle, téléphone | avatar centre (510, 680) r 110 ; nom 52 px haut 800 ; handle haut 866 ; téléphone (170, 420, 680×1160) |
| S03 → S04 | les trois cartes de la grille | bleue (310,25 ; 668 ; ×0,65), rose (56,75 ; 716 ; ×0,55), verte (626,75 ; 716 ; ×0,55) |
| S04 → S05 | carte bleue → photo jointe | (230, 650, ×0,4444) = 280×427 |
| S05 → S06 | photo → carte héros | même état ; S06 la fait avancer et libère la tête du cadre |
| S06 → S07 | produit ; vignettes rondes → inserts | produit (133,5 ; 412,8 ; ×0,6475) ; disques de 150 px aux centres (765, 600) (765, 1150) (220, 1390) |
| S07 → S08 | inserts → coques de widgets | 300×220 en (620, 620 / 890 / 1160) |
| S08 → S09 | téléphone → cadre du showroom | téléphone 520×1030 ×1,06, centre (530, 1035,9) |
| S09 → S10 | showroom réduit sous la carte | caméra ×0,62 autour de (530, 490), descendue de 610 px |
| S10 → S11 | photo de la carte → grande carte | carte 620×1120 en (100, 450) |
| S11 → S12 | grande carte → vignette | (90, 600, ×0,371) = 230×415 |
| S12 → S13 | trace → anneau ; vignette → produit | ellipse (510, 1270, 280×48) ; mannequin (284,8 ; 459,4 ; ×0,4916) |
| S13 → S14 | halo → cercle | ellipse (510, 1159, 286×123,6) ; mannequin (257,5 ; 494,2 ; ×0,5513) |
| S14 → S01 | boucle | ellipse (510, 1340, 294,4×50,6) opacité 0,5 ; mannequin invisible ×0,92 |

## Frame 1 — Ouverture produit

- duration: 1.8s (images 0–53)
- poster: 0.9s
- transition_in: boucle depuis S14
- status: animated
- src: compositions/s01-ouverture.html
- rules: ambient-glow-bloom (halo), spring-pop-entrance sans rebond (0,92 → 1), card-morph-anchor (sortie)
- text: « VOTRE PROCHAIN / COUP DE CŒUR. » · BIKINIS SHOP · @daya_na990

## Frame 2 — Recherche TikTok

- duration: 2.0s (images 54–113)
- poster: 2.8s
- transition_in: match-cut (contour de recherche, avatar)
- status: animated
- src: compositions/s02-recherche.html
- rules: discrete-text-sequence (saisie lissée du handle), grid-card-assemble (aperçu des modèles), press-release-spring (sélection), card-morph-anchor (vers le profil)
- text: « TROUVEZ / VOTRE STYLE » · champ @daya_na990 · onglets Top / Utilisateurs / Vidéos / LIVE

## Frame 3 — Profil de la boutique

- duration: 1.5s (images 114–158)
- poster: 4.53s
- transition_in: match-cut (avatar, nom, handle, téléphone)
- status: animated
- src: compositions/s03-profil.html
- rules: grille raccordée depuis l'aperçu de S02, viewport-change (descente vers la grille)
- text: « BIKINIS. / COULEURS. STYLE. » · bouton Message · aucune statistique sociale

## Frame 4 — Sélection dans la galerie

- duration: 2.5s (images 159–233)
- poster: 6.53s
- transition_in: match-cut (cartes de la grille)
- status: animated
- src: compositions/s04-galerie.html
- rules: depth-of-field-blur (cartes latérales), multi-phase-camera (poussée douce), card-morph-anchor (vers la photo jointe)
- text: « LEQUEL / VOUS PLAÎT ? »

## Frame 5 — Question par message

- duration: 1.8s (images 234–287)
- poster: 8.7s
- transition_in: match-cut (photo jointe)
- status: animated
- src: compositions/s05-message.html
- rules: discrete-text-sequence (brouillon), press-release-spring (envoi)
- text: « UN MODÈLE / VOUS PLAÎT ? » · brouillon « Bonjour, ce modèle est disponible ? » · EXEMPLE DE MESSAGE

## Frame 6 — Produit héros en profondeur

- duration: 2.2s (images 288–353)
- poster: 10.7s
- transition_in: match-cut (photo → carte héros)
- status: animated
- src: compositions/s06-heros.html
- rules: 3d-camera-flight (inclinaison commune, retour à plat), split-tilt-cards (cartes latérales), card-morph-anchor (vignettes → inserts)
- text: « VOTRE / COUP DE CŒUR. » · carte Détails

## Frame 7 — Détails du modèle

- duration: 2.1s (images 354–416)
- poster: 12.83s
- transition_in: match-cut (produit, vignettes rondes)
- status: animated
- src: compositions/s07-details.html
- rules: card-morph-anchor (disque → cadre → coque de widget), svg-path-draw (traits), coordinate-target-zoom (zoom lent)
- text: « LES DÉTAILS / FONT LE STYLE. »

## Frame 8 — Choix du modèle

- duration: 3.9s (images 417–533)
- poster: 15.83s
- transition_in: match-cut (coques de widgets)
- status: animated
- src: compositions/s08-choix.html
- rules: spring-pop-entrance (options aux images 18, 24, 30), sine-wave-loop (pulsation unique), multi-phase-camera (avancée vers le showroom)
- text: « VOTRE STYLE. / VOTRE CHOIX. » · Modèle · Couleur · Disponibilité « Sur demande »

## Frame 9 — Showroom virtuel

- duration: 1.2s (images 534–569)
- poster: 18.4s
- transition_in: match-cut (téléphone → cadre néon)
- status: animated
- src: compositions/s09-showroom.html
- rules: zoom-out-workspace-reveal (ouverture d'angle), ambient-glow-bloom
- text: « LA BOUTIQUE / DANS VOTRE POCHE. » · décor virtuel, sans adresse

## Frame 10 — Carte de sélection

- duration: 1.7s (images 570–620)
- poster: 19.83s
- transition_in: match-cut (showroom réduit)
- status: animated
- src: compositions/s10-selection.html
- rules: titlecard-reveal, press-release-spring + particle-burst (cœur, une seule fois), svg-path-draw (trait lumineux)
- text: « VOTRE / SÉLECTION » · aucun témoignage ni classement

## Frame 11 — Photo du modèle

- duration: 1.2s (images 621–656)
- poster: 21.3s
- transition_in: match-cut (photo → grande carte)
- status: animated
- src: compositions/s11-modele.html
- rules: card-morph-anchor (vers la vignette), waterfall-entry (inserts)
- text: « LE MODÈLE / EN DÉTAIL »

## Frame 12 — Contact par message

- duration: 1.1s (images 657–689)
- poster: 22.43s
- transition_in: match-cut (vignette)
- status: animated
- src: compositions/s12-contact.html
- rules: cursor-click-ripple (doigt, onde), press-release-spring (bouton Message), svg-path-draw (trace)
- text: « UN MESSAGE / POUR COMMENCER. » · aucun achat ni paiement montré

## Frame 13 — Signature et appel à l'action

- duration: 2.5s (images 690–764)
- poster: 24.23s
- transition_in: match-cut (anneau, produit)
- status: animated
- src: compositions/s13-signature.html
- rules: logo-assemble-lockup (signature), ambient-glow-bloom
- text: « VOTRE PROCHAIN LOOK / COMMENCE ICI. » · BIKINIS SHOP · @daya_na990 · « Écrivez-nous sur TikTok » lisible de 23,3 à 25,3 s

## Frame 14 — Raccord de boucle

- duration: 0.9667s (images 765–793)
- poster: 25.97s
- transition_in: match-cut (halo → cercle)
- status: animated
- src: compositions/s14-boucle.html
- rules: card-morph-anchor (cercle → anneau au sol de l'image 0)
- text: (aucun)
