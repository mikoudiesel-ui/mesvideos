---
format: 1080x1920
duration: 40s
message: "Commande ton bikini sur TikTok (@daya_na990) : il arrive directement à ta porte."
arc: Hook (1 clic) → La ville commande → L'atelier prépare → Départ → Tournée de porte en porte → Plage → Signature
audience: Clientes TikTok + entreprises (portfolio motion design)
mode: autonomous
fps: 30
bpm: 120
---

Un seul monde 3D continu (Three.js, caméra orthographique isométrique) dans `index.html`, avec des
calques de texte HTML/GSAP par-dessus. Toutes les scènes partagent la même île : c'est une seule
composition à phases internes (« multi-scene merge »), pilotée par un seul voyage de caméra.
La grille musicale est à 120 BPM (1 temps = 0,5 s, 1 mesure = 2 s) et les coupes tombent sur les mesures.

## Frame 1 — Hook : 1 clic

- scene: Un smartphone 3D monte en tournoyant ; sur la boutique @daya_na990, un doigt appuie sur « Commander », puis la commande est confirmée
- duration: 4.6s
- poster: 2.8s
- transition_in: cut
- status: animated
- src: index.html
- blueprint: cta-morph-press (le bouton devient la confirmation) + spring-pop-entrance
- text: « Ton bikini, » / « en 1 clic. »

Le bouton rose se presse (press-release-spring), une onde part de l'écran et la carte se change en
« Commande confirmée ». L'écran affiche ensuite le suivi de commande : une carte vue de dessus de l'île,
rendue en direct.

## Frame 2 — Plongée dans l'écran → la ville

- scene: La caméra plonge dans la carte du téléphone, ressort au-dessus de la vraie île vue de dessus, puis bascule en isométrique
- duration: 2.4s (4.6 → 7.0)
- poster: 6.4s
- transition_in: match-cut (écran → monde)
- status: animated
- src: index.html
- blueprint: zoom-out-workspace-reveal (variante inversée : push-in puis tilt-to-flatten inversé, 3d-camera-flight)

Coup signature : la carte de suivi devient le monde. On passe de la vue du dessus à l'isométrique,
avec un léger orbit pour que le relief se lise tout de suite.

## Frame 3 — La ville commande

- scene: Des épingles roses « +1 » sautent au-dessus de 5 maisons, sur le temps
- duration: 3.0s (7.0 → 10.0)
- poster: 9.2s
- transition_in: continuous camera
- status: animated
- src: index.html
- blueprint: constellation-hub (des nœuds qui poppent autour d'un centre) + spring-pop-entrance
- text: « Les commandes arrivent… »

## Frame 4 — L'atelier prépare

- scene: La caméra pousse vers la boutique, le toit s'envole (vue en coupe), les bikinis volent du portant jusque dans le carton, qui se ferme seul
- duration: 7.0s (10.0 → 17.0)
- poster: 13.4s
- transition_in: camera push-in
- status: animated
- src: index.html
- blueprint: camera-journey (A : l'action déclenche la conséquence) + multi-phase-camera
- text: « Préparé avec soin » / « emballé avec amour »

## Frame 5 — Départ

- scene: Les colis sautent dans le van, les portes claquent, coup de klaxon, le van démarre et l'itinéraire se trace au sol
- duration: 3.0s (17.0 → 20.0)
- poster: 18.6s
- transition_in: continuous camera
- status: animated
- src: index.html
- rules: svg-path-draw (tracé de route, en 3D), motion-blur-streak
- text: « En route ! »

## Frame 6 — La tournée, de porte en porte

- scene: Le livreur sort, marche jusqu'à la porte, sonne ; la cliente ouvre et reçoit son colis (cœurs, « Livré ✓ »). Au 2e arrêt, la cliente ouvre le carton et le bikini jaillit. Puis accéléré : chaque épingle devient une coche
- duration: 12.0s (20.0 → 32.0)
- poster: 23.4s
- transition_in: continuous camera
- status: animated
- src: index.html
- blueprint: spatial-pan-stations (une caméra traverse des stations sur un même monde) + particle-burst
- text: « De porte en porte » / « Livré chez toi ✓ »

## Frame 7 — La plage

- scene: La cliente, sur la plage sous un parasol, porte son nouveau bikini et fait coucou ; les vagues bougent et des cœurs s'envolent
- duration: 4.0s (32.0 → 36.0)
- poster: 34.0s
- transition_in: camera glide
- status: animated
- src: index.html
- rules: ambient-glow-bloom, sine-wave-loop
- text: « Ton été commence ici. »

## Frame 8 — Signature

- scene: La caméra recule, l'île entière apparaît couverte de coches, et le logo @daya_na990 se construit avec l'appel à l'action « Commande sur TikTok »
- duration: 4.0s (36.0 → 40.0)
- poster: 38.6s
- transition_in: camera pull-back
- status: animated
- src: index.html
- blueprint: logo-assemble-lockup
- text: « @daya_na990 » / « Bikinis livrés chez toi » / « Commande sur TikTok »
