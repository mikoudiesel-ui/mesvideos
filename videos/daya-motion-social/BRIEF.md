---
workflow: general-video
flow: automation
storyboard: no
message: "Découvrez la collection BIKINIS SHOP et écrivez-nous sur TikTok (@daya_na990)."
destination: tiktok
aspect: 1080x1920
language: fr
audience: "Clientes TikTok à la recherche d'un bikini coloré"
length: 26.467s
angle: "Parcours social en 14 scènes : produit → recherche → profil → sélection → message → signature"
---

## Intent

Vidéo motion design éditable pour BIKINIS SHOP, compte TikTok @daya_na990, construite à partir du
dossier « DAYA 14 SCÈNES » fourni par l'utilisateur (reference/). Objectif du dossier : « présenter la
collection et inciter à écrire à la boutique sur TikTok ». Le dossier fixe le timing exact
(794 images à 30 i/s, 26,4667 s, 14 scènes, fins exclusives) dans `reference/TIMELINE_14_SCENES.json`.

Consigne de l'utilisateur pendant la production : « envoie-moi les détails de la vidéo en images
détaillées avant de générer la vidéo ; on va corriger les défauts avant de lancer la vidéo ».
Après les planches, l'utilisateur a validé le rendu (« vas y génère la vidéo »).

## Assets

- reference/sequences/S01–S14.png, reference/planches/ — maquettes illustratives du dossier ; elles guident la composition et servent de source aux découpes produit (tools/prep_assets.py).
- reference/audio/SON_TEMOIN_26S.wav — son témoin original du dossier (pas la musique TikTok), remplacé par la musique composée pour la vidéo.
- assets/fonts/DejaVu* — substituts locaux livrés avec le dossier (titres en serif, interface en sans).

## Customizations

- Raccords demandés par le dossier entre chaque scène (halo → recherche, avatar → profil, vignette → carte, carte → message, photo → produit en profondeur, détail → widgets, téléphone → showroom, carte favorite → photo, vignette → Message, trace → signature) et S14 qui rejoint l'image 0.
- Musique : « une music de base super stylé qui met en avant les détails de la vidéo ». Choix de l'utilisateur : composition originale (pas de compte HeyGen connecté). Première version afro-house tropical en la mineur (`tools/make_music_afrohouse.py`) ; puis « change la musique de fond » : nu-disco / French touch 120 BPM en fa majeur, composée et synthétisée dans `tools/make_music_nudisco.py`, calée à l'image près sur les mêmes coupes et détails. L'afro-house reste disponible en alternative.
- Bruitages d'interface synthétisés sur les cues du JSON (sans doubler les impacts et notes de signature de la musique) ; sous chaque bruitage les aigus de la musique s'effacent d'environ 6 dB ; mix vers −16 LUFS intégrés et crête vraie ≤ −1 dBTP.
- « Auto-analyse et auto-correction » demandées avant le rendu : la passe appliquée est décrite dans STORYBOARD.md.
- Marquage discret « MAQUETTE · VISUELS ILLUSTRATIFS » tant que les photos réelles manquent.

## Notes

- Aucun prix, promotion, stock, délai, livraison, avis, note ou chiffre social. Le dialogue S05 est marqué « EXEMPLE DE MESSAGE » et sans réponse de la boutique ; le widget Disponibilité indique « Sur demande ».
- Le logo TikTok n'est pas reproduit : interface stylisée et icône de message sur le bouton final.
- Version CLI conservée : hyperframes 0.8.143 (demande du dossier pour le dépôt mesvideos).
- Le Studio (localhost) n'est pas joignable depuis l'app de l'utilisateur : la revue se fait sur les planches d'images puis sur le MP4.
