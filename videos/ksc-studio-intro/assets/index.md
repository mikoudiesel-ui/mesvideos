# Assets — intro KSC STUDIO

| Rôle | Fichier | Provenance |
| --- | --- | --- |
| hero (logo) | `assets/ksc-vertical-negatif.svg` | Logo A · Objectif choisi par l'utilisateur, version négatif ; généré par `brand/ksc-studio/tools/make_logos.py` (copie figée de `brand/ksc-studio/kit-objectif/1_logo/vertical/`). Les pièces animées (K, S, objectif, lettres de STUDIO) sont recalculées à l'identique par `tools/build_intro.py`. |
| son | `assets/audio/ksc-intro-son.wav` | Bruitages et nappe synthétisés localement par `tools/build_intro.py` (aucun son externe). |
| GSAP | `assets/vendor/gsap.min.js` | GSAP 3.14.2, copie locale pour un rendu hors ligne et déterministe. |
| flash | `compositions/editorial-flash-overlay.html` | Bloc du catalogue HyperFrames, adapté au 1080×1920 et calé sur le déclic (0,75 s). |
