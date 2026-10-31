# Pub Facebook en motion design : « La Clé des Maths Financières » (YK Cyber Store)

Plan validé avec l'utilisateur, à reprendre dans la session qui pourra ouvrir la boutique Chariow.

## Demande

- Analyser la page produit de la boutique : https://fqtmtnep.mychariow.co/prd_nh380f7k
  (titre, prix et promotion, description, couverture, visuels, avis réellement affichés, bouton d'achat).
- En faire une **vidéo publicitaire en motion design** pour Facebook Ads, qui attire la clientèle et fait vendre.

## Décisions de l'utilisateur

- Formats : **4:5** (1080 × 1350, fil Facebook et Instagram) **et 9:16** (1080 × 1920, Reels et Stories).
- Durée : **15 secondes**.
- Son : **voix off qui présente le produit** (demande ajoutée ensuite par l'utilisateur, qui me laisse choisir la
  voix) + musique originale en fond, plus basse sous la voix ; les mots clés restent écrits à l'écran pour ceux qui
  regardent sans le son.
- Voix choisie : **féminine, française, naturelle, chaleureuse et dynamique**, comme une grande sœur qui conseille ;
  si HeyGen propose un accent naturel d'Afrique francophone, le préférer (public visé). Générée par la synthèse
  vocale de HeyGen (même accès que `PLAN_VIDEO_PUB.md` : `*.heygen.com`, `*.heygen.ai` et `HEYGEN_API_KEY`) ;
  faire écouter 2 extraits à l'utilisateur avant le montage.
- Texte de la voix off (≈ 38 mots, 14 à 15 s), à ajuster avec les infos de la page (par exemple le prix) :

> Tu bloques en maths financières ? Découvre La Clé des Maths Financières, l'ebook de YK Cyber Store : des cours et
> des exercices corrigés pour tes révisions. Relis, essaie, compare… et comprends ta démarche. Commande-le
> maintenant chez YK Cyber Store !
- La page Chariow est analysée par la session elle-même : l'utilisateur autorise `*.mychariow.co` dans les réglages
  réseau de l'environnement (si les images viennent d'un autre domaine, le signaler et le faire autoriser).

## Ce que l'on sait déjà du produit

- Ebook « La Clé des Maths Financières », vendu par YK Cyber Store.
- Pour les étudiants en finance et en comptabilité qui préparent un devoir ou un examen de maths financières.
- Contenu annoncé par l'utilisateur : des cours et des exercices corrigés pour les révisions. Méthode conseillée :
  relire la notion, essayer l'exercice sans regarder la correction, puis comparer les étapes pour repérer son erreur.
- Tout le reste (prix, sommaire, nombre de pages, couverture) vient de la page Chariow : ne rien inventer.

## Route HyperFrames

`/product-launch-video`, intention « vendre » (pub), capture de la page Chariow pour les couleurs et les visuels,
voix off HeyGen sur le texte ci-dessus (`VO_MODE` : texte réécrit pour 15 s, validé avant génération) ;
musique originale composée localement, comme pour `videos/daya-motion-social`, baissée sous la voix.

## Structure proposée (15 s)

| Temps | Rôle | À l'écran |
| --- | --- | --- |
| 0 – 2 s | Accroche | « Tu bloques en maths financières ? » en très gros, formules qui s'emmêlent |
| 2 – 5 s | Problème | « Tu connais tes formules… mais l'exercice te bloque » |
| 5 – 9 s | Produit | La couverture de l'ebook entre à l'écran ; « Cours + exercices corrigés » |
| 9 – 12 s | Bénéfice | La méthode en 3 mots : Relis · Essaie · Compare ; « Comprends ta démarche » |
| 12 – 15 s | Appel à l'achat | Couverture + prix (si la page l'affiche) + « Commande chez YK Cyber Store » + lien |

Règles : accroche dans la 1re seconde, produit visible avant 5 s, textes hors des zones couvertes par l'interface des
Reels (haut et bas), aucune promesse de résultat garanti ni faux avis (règles publicitaires de Meta), marque visible
à la fin. Sortie H.264 + AAC, son à −14 LUFS environ.
