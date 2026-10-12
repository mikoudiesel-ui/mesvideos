---
format: 1080x1920
duration: 26.5s
message: "BIKINI SHOP (@daya_na990) : tu trouves ton bikini sur TikTok, tu commandes en un message, il arrive à ta porte."
arc: Point → Logo → Recherche → Profil → Grille → Vidéo → DM → Préparation → Plan plage → Commande → Avis → Livraison → Conclusion → Signature → (boucle)
mode: autonomous
fps: 30
bpm: 120
audio: musique originale 120 BPM (assets/audio/music.wav, tools/make_music.py), creusée sous la voix
voiceover: Gemini TTS, voix Laomedeia (énergique), 12 phrases (assets/voice/plan.json)
---

Une seule composition (`index.html`) et une seule timeline GSAP (`assets/js/timeline.js`).
Chaque scène est une `<section class="clip">` dont la fenêtre déborde un peu sur ses voisines pour
les transitions (flou de mouvement + perspective 3D). Le minutage suit l'analyse de la vidéo de référence (±0,25 s).

## Frame 1 — Le point corail

- time: 0.0 → 1.0
- scene: Un losange corail lumineux au centre, halo qui pulse ; il tourne et grossit
- src: index.html#s1
- rules: pulse halo, scale + rotation (power2.in)

## Frame 2 — Logo BIKINI SHOP

- time: 1.0 → 2.0
- scene: Le wordmark néon apparaît dans un flash ; grésillement néon ; un cercle blanc se dessine à 1,5 s
- src: index.html#s2
- rules: blur-in + brightness, svg stroke draw, whip-out

## Frame 3 — Recherche TikTok

- time: 2.0 → 3.5
- scene: Écran de recherche incliné en 3D qui se redresse ; « daya_na990 » se tape ; onglet Utilisateurs ; résultat BIKINI SHOP
- src: index.html#s3
- text: « Recherches récentes » (bikini été, maillot de bain deux pièces, bikini corail)

## Frame 4 — Profil TikTok

- time: 3.5 → 5.0
- scene: Zoom sur l'avatar ; en-tête BIKINI SHOP ; compteurs qui défilent ; bio ; Suivre / Message ; la grille monte
- src: index.html#s4
- note: compteurs PROVISOIRES

## Frame 5 — Scroll de la grille

- time: 5.0 → 6.0
- scene: La grille défile en 3D avec flou ; la tuile « bikini corail » (248 k vues) se détache, cerclée de corail
- src: index.html#s4

## Frame 6 — Vidéo TikTok + vues

- time: 6.0 → 8.0
- scene: La tuile devient la vidéo plein cadre (rail J'aime / Avis / Partager, légende) ; pastille en verre « 13 k → 96 k → 248 k vues » ; push-in
- src: index.html#s6
- asset: assets/photos/tiktok-bikini.svg (→ vraie vidéo)

## Frame 7 — Message privé

- time: 8.0 → 9.5
- scene: DM 10:42 ; « Coucou ! Le bikini corail est dispo en M ? » ; photo du bikini ; réponse corail « Oui ! Dispo en M, je te l'emballe ? »
- src: index.html#s7

## Frame 8 — Vue éclatée + checklist

- time: 9.5 → 11.5
- scene: Le DM se sépare en couches de verre empilées en isométrique ; le bikini descend ; trois plateformes ; puces « Taille vérifiée », « Emballé avec soin », « Envoyé à ta porte »
- src: index.html#s7

## Frame 9 — Plan cinéma plage

- time: 11.5 → 14.0
- scene: Coupe plein écran sur la plage au coucher du soleil, push-in ; plaque en verre inclinée « BIKINI SHOP @daya_na990 » à 13,5 s
- src: index.html#s9
- asset: assets/photos/cinema-plage.svg (→ vraie vidéo)

## Frame 10 — Révélation du téléphone

- time: 14.0 → 15.0
- scene: Noir ; un petit téléphone à bord corail (profil TikTok dessus) apparaît puis grandit
- src: index.html#s10

## Frame 11 — « Ta commande, en 1 clic. »

- time: 15.0 → 18.0
- scene: Titre qui se précise depuis le flou ; tuiles-icônes en perspective ; statuts « Commande confirmée », « Colis préparé », « En route vers chez toi » ; zoom qui traverse ; bulles blanches floues
- src: index.html#s10

## Frame 12 — Boutique 3D + avis

- time: 18.0 → 21.0
- scene: Maquette isométrique de la boutique (toit corail, enseigne BIKINI SHOP, palmiers, sable, mer) ; carte d'avis qui tombe ; 5 étoiles ; citation mot par mot
- src: index.html#s12
- note: avis PROVISOIRE

## Frame 13 — Livraison

- time: 21.0 → 22.5
- scene: Photo de la cliente qui reçoit son colis à la porte ; pastille « Livraison · Bikini corail · Colis remis ✓ »
- src: index.html#s13
- asset: assets/photos/livraison-colis.svg

## Frame 14 — « Ton été commence ici. »

- time: 22.5 → 24.0
- scene: Texte qui se précise ; trait néon corail en spirale ; une main tend le colis et se balance ; explosion de halo + étincelles
- src: index.html#s14
- asset: assets/photos/main-colis.svg

## Frame 15 — Signature + boucle

- time: 24.0 → 26.5
- scene: Logo néon BIKINI SHOP, « @daya_na990 », « Bikinis · Maillots · Livrés chez toi », « Commande sur TikTok » ; tout se contracte vers le point corail du début
- src: index.html#s15

## Voix off

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
