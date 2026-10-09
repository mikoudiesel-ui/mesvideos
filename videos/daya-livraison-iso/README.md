# Pub @daya_na990 : livraison de bikinis en 3D isométrique

Pub verticale (1080×1920, 30 i/s, 40 s) faite avec [HyperFrames](https://hyperframes.heygen.com).
On y suit une ville balnéaire en 3D isométrique (Three.js) : la commande passée sur TikTok devient un colis,
préparé à l'atelier, chargé dans le van et livré de porte en porte, jusqu'à la plage.

## Structure

| Fichier | Rôle |
| --- | --- |
| `index.html` | Composition principale : canvas 3D, flash de raccord, flou de vitesse, slots des sous-compositions, bande-son |
| `assets/js/world.js` | Le monde 3D (île, ville, boutique, van, personnages, caméra). Tout est une fonction du temps `t` |
| `assets/js/models.js` | Modèles low-poly (maisons, van, personnages, bikinis, colis, palmiers…) |
| `assets/js/textures.js` | Textures dessinées : imprimés des bikinis, écran du téléphone, enseignes, icônes |
| `compositions/captions.html` | Les 8 sous-titres « stickers » |
| `compositions/endcard.html` | Carte de fin : @daya_na990 et « Commande sur TikTok » |
| `compositions/background.html` | Fond dégradé « golden hour » |
| `tools/make_soundtrack.py` | Musique 120 BPM et bruitages, générés et calés sur l'image |
| `BRIEF.md`, `STORYBOARD.md` | Le brief et le découpage scène par scène |

## Modifier

- **Nom de la boutique** : remplace `daya_na990` dans `assets/js/world.js` (enseignes, van),
  `assets/js/textures.js` (écran du téléphone) et `compositions/endcard.html`.
- **Textes** : `compositions/captions.html`. Les horaires d'apparition sont dans le tableau `caps`.
- **Musique / bruitages** : modifie `tools/make_soundtrack.py`, puis lance `python3 tools/make_soundtrack.py`.

## Commandes

```bash
npx hyperframes lint      # vérification rapide
npx hyperframes check     # vérification complète (lint, rendu, mise en page, contraste)
npx hyperframes snapshot --at 2,12,28,38   # images fixes
npx hyperframes render --output renders/daya-livraison-iso.mp4
```
