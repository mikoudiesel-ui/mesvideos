# Compte-rendu — BIKINIS SHOP / @daya_na990, motion social 14 scènes (MAQUETTE)

## Livrables

| Livrable | Emplacement |
| --- | --- |
| Vidéo | `renders/DAYA_MOTION_SOCIAL_MAQUETTE.mp4` |
| Projet éditable HyperFrames / GSAP | `index.html`, `compositions/`, `assets/css/daya.css` |
| Assets locaux | `assets/img/`, `assets/audio/`, `assets/fonts/`, `assets/vendor/gsap.min.js` |
| 14 captures (milieux de scène) | `captures/S01_milieu_image027.jpg` … `S14_milieu_image779.jpg` |
| Planches de revue | `captures/PLANCHE_A_14_scenes.jpg`, `PLANCHE_B_raccords_*.jpg`, `PLANCHE_C_detail_*.jpg`, `PLANCHE_D_controle_mp4.jpg` |
| Musique originale | `assets/audio/musique_daya_nudisco_120bpm.wav` (`tools/make_music_nudisco.py`) ; première version afro-house gardée en alternative (`musique_daya_afrohouse_120bpm.wav`, `tools/make_music_afrohouse.py`) |
| Dossier source | `reference/` (plan, timeline JSON, prompt, planches, séquences, son témoin) |

## Ce qui a été construit

- 14 sous-compositions, une par scène, posées exactement sur les limites de `reference/TIMELINE_14_SCENES.json` : 1080×1920, 30 i/s, 794 images, 26,467 s.
- Textes et interfaces recomposés en éléments éditables (titres, téléphone, recherche, profil, cartes, widgets, carte favorite, bouton final) ; aucun PNG de planche n'est repris tel quel.
- Raccords demandés par le dossier, vérifiés image par image de part et d'autre de chaque coupe (planches B), et boucle de l'image 793 vers l'image 0.
- Caméra sur les parents, entrées sur les enfants ; timelines GSAP en pause, seek-safe, sans hasard ni horloge.
- Musique originale composée pour la vidéo : nu-disco / French touch, 120 BPM, fa majeur (basse en octaves, guitare rythmique, cordes pompées, cuivres en clave, syndrums, harpe et célesta sur les détails). Elle remplace la première version afro-house à la demande « change la musique de fond », avec le même calage à l'image près sur les coupes et sur chaque détail. Bruitages d'interface lisibles par-dessus (les aigus de la musique s'effacent sous chaque clic) ; mix à −16 LUFS.
- Passe d'auto-analyse et d'auto-correction avant le rendu (détail dans `STORYBOARD.md`) : titres flou → net, reflets lumineux, pulsations sur la grosse caisse, aperçu S02 raccordé à la grille S03, scintillement des widgets, traits S07 renforcés, grain de pellicule.

## Contrôles

| Contrôle | Résultat |
| --- | --- |
| `hyperframes check` (CLI 0.8.143) | lint 0, exécution 0, mise en page 0, mouvement 0, contraste 24/24 conformes WCAG AA |
| Carte d'animation | aucune zone morte |
| Vidéo | H.264 (yuv420p), 1080×1920, 30 i/s, **794 images**, 26,467 s |
| Audio | AAC 48 kHz stéréo ; **−16,1 LUFS** intégrés et crête vraie **−5,0 dBTP**, mesurés sur le MP4 encodé |
| Changement de musique | images identiques au rendu précédent (16 images comparées, écart nul) ; seul le son change |
| Décodage complet | sans erreur (`ffmpeg -f null`) |
| Bouton « Écrivez-nous sur TikTok » | présent et net aux images 699, 714, 729, 744 et 759 (de 23,3 à 25,3 s) |
| Raccords | vérifiés sur le MP4 : image avant, première image et image suivante de chaque coupe, boucle 793 → 0 (`captures/PLANCHE_B_raccords_*.jpg`) |
| Rendu | 3 min 46 s, capture beginframe, GPU logiciel |

Les planches A, B, C et D et les 14 captures sont tirées du MP4 final (`tools/verify_render.py`,
`tools/review_sheets.py`).

## Maquette ou publicité finale

C'est une **maquette** : les produits sont des découpes des illustrations du dossier (agrandies 3 à 4 fois,
donc un peu douces), le rose et le vert sont présentés en cartes photo, et la mention « MAQUETTE · VISUELS
ILLUSTRATIFS » reste visible. Rien n'est inventé : ni prix, ni stock, ni délai, ni avis, ni chiffre social ;
le message de S05 est marqué « EXEMPLE DE MESSAGE » et le widget Disponibilité indique « Sur demande ».

Pour une publicité catalogue finale, fournir :

- photos HD du modèle bleu fleuri (idéalement détouré), du rose et du vert ;
- un gros plan du bleu (fleur, motif, liens) ;
- l'avatar ou le logo de la boutique ;
- une musique autorisée si l'on veut remplacer la composition originale.

Les remplacer dans `assets/img/` sous les mêmes noms et proportions suffit : les raccords reposent sur ces
dimensions. Retirer ensuite la mention maquette (`compositions/maquette.html`) et relancer le rendu.
