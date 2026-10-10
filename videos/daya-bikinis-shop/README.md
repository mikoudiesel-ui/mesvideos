# Bikini Shop (@daya_na990) : présentation en motion design

Vidéo TikTok verticale (1080×1920, 30 i/s, 40 s) faite avec [HyperFrames](https://hyperframes.heygen.com).
Elle présente la boutique : ce qu'elle vend, à qui elle s'adresse, pourquoi commander chez elle, puis
l'appel à l'action (abonnement + numéro). Voix off française (Kokoro, voix « ff_siwis », générée localement).

Rendu : `renders/daya-bikinis-shop-tiktok.mp4`

## Scènes

| # | Temps | Fichier | Voix off |
| --- | --- | --- | --- |
| 1 | 0 – 4,2 s | `compositions/s1-hook.html` | « Cet été, tous les regards seront sur toi. » |
| 2 | 4,2 – 10,4 s | `compositions/s2-shop.html` | « Découvre Bikini Shop : la boutique de maillots de bain de Daya, sur TikTok. » |
| 3 | 10,4 – 16,4 s | `compositions/s3-catalogue.html` | « Bikinis, maillots une pièce, paréos et hauts tops… de nouveaux modèles à chaque arrivage. » |
| 4 | 16,4 – 22 s | `compositions/s4-pour-qui.html` | « Pour toutes les femmes qui veulent briller à la plage, à la piscine, ou en vacances. » |
| 5 | 22 – 32 s | `compositions/s5-valeur.html` | prix dès 1 000 F, arrivages en live, commande en un message, livraison |
| 6 | 32 – 40 s | `compositions/s6-cta.html` | « Abonne-toi, et commande dès maintenant au 07 99 00 45 50. » |

`compositions/bg.html` : le mur orange des shootings (halo, texte fantôme, feuilles). `index.html` monte les
scènes, les volets ronds entre les scènes, les 8 répliques de voix off et la bande-son.

## Images

- `assets/img/t-*.jpg` et `assets/img/avatar.png` : découpées dans les captures du profil TikTok
  (`python3 -I tools/crop_screens.py capture1.webp capture2.webp`).
- `assets/img/m/*.png` : les vrais mannequins de la boutique, détourés (rembg) puis nettoyés
  (`tools/clean_cutouts.py`). Les sources étant des miniatures, ils sont un peu flous : avec les photos
  originales de la boutique, on les remplace fichier par fichier sans toucher au reste.

## Modifier

- **Textes à l'écran** : dans chaque `compositions/s*.html`.
- **Voix off** : `tools/vo_lines.tsv`, puis pour une ligne :
  `npx hyperframes tts "texte" -v ff_siwis -o assets/audio/vo/l3.wav` (nécessite `pip install kokoro-onnx soundfile`).
  Si la durée change, ajuste `data-start`/`data-duration` dans `index.html` et les tableaux `VO` du script son.
- **Musique / bruitages** : `python3 tools/make_soundtrack.py` (groove afro-pop 104 BPM, baissé sous la voix).

## Commandes

```bash
npx hyperframes check
npx hyperframes snapshot --at 3,8,14,20,26,36
npx hyperframes render --output renders/daya-bikinis-shop-tiktok.mp4
```
