# Gabarit 4.roues : squelette des 15 scènes

Squelette HyperFrames (HTML + GSAP, 1080×1920, 26,5 s) qui reproduit la mise en scène de la pub 4.roues
analysée : recherche Instagram → profil → reel → DM → vue éclatée → plan cinéma → « Transaction sécurisée »
→ garage isométrique + avis → livraison → « Vous repartez tranquille. » → signature, en boucle.

Il sert de **gabarit**. La version utilisée pour la boutique **BIKINI SHOP (@daya_na990)** est
dans [`../daya-parcours`](../daya-parcours).

- `index.html` : les scènes et le style ; `assets/js/timeline.js` : la timeline GSAP (heures de l'analyse).
- `assets/photos/` : placeholders SVG (régénérés par `python3 tools/make_placeholders.py`).
- Le logo 4ROUES est recréé en SVG (`<template id="logo-tpl">`).

```bash
npx hyperframes check
npx hyperframes render --output renders/4roues-parcours.mp4
```
