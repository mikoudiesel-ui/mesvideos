# Prompt à copier dans Claude Code

Construis une vidéo motion design éditable pour BIKINIS SHOP, compte TikTok @daya_na990, à partir du dossier joint. L’objectif est de présenter la collection et d’inciter à écrire à la boutique sur TikTok.

Je t’autorise à créer le projet, préparer les assets, réaliser les animations, lancer les contrôles et exporter un MP4. Avance jusqu’à un rendu vérifié. Le dossier contient une maquette détaillée ; les images guident la composition, les textes, la profondeur et les raccords.

## Documents et priorité

Lis PLAN_PRODUCTION.md, TIMELINE_14_SCENES.json, ASSETS.md et les quatre planches dans planches/. Inspecte les 14 images dans sequences/. SCENES_INTERACTIVES.html permet de parcourir la maquette ; PLANCHE_PRODUCTION_14_SCENES.pdf contient une page par scène.

Les images sont des illustrations générées à partir du contexte de la boutique. Elles ne sont pas des photos vérifiées du catalogue. N’invente pas de prix, promotion, stock, disponibilité, livraison, avis, rating, chiffre social ni promesse de paiement. Le dialogue S05 est un exemple. Le showroom S09 est un décor virtuel.

Les photos HD réelles que je fournis ont priorité pour les produits. Si elles manquent, avance avec les références illustratives et livre une vidéo clairement nommée MAQUETTE, avec un discret marquage de maquette. N’annonce pas une publicité catalogue finale dans ce cas. Liste les assets à remplacer sans arrêter le travail indépendant.

## Master et scènes

Format : 1080 × 1920, 30 i/s, exactement 794 images, soit 26.466667 s. La durée des planches n’est pas implicite : les limites exactes viennent du JSON. Les fins y sont exclusives. Respecte les 14 scènes et leur ordre.

| Scène | Temps | Images | Fonction | Texte principal |
|---|---|---|---|---|
| S01 | 0.00–1.80 s | 0–53 | Ouverture produit | VOTRE PROCHAIN / COUP DE CŒUR. |
| S02 | 1.80–3.80 s | 54–113 | Recherche TikTok | TROUVEZ / VOTRE STYLE |
| S03 | 3.80–5.30 s | 114–158 | Profil de la boutique | BIKINIS. / COULEURS. STYLE. |
| S04 | 5.30–7.80 s | 159–233 | Sélection dans la galerie | LEQUEL / VOUS PLAÎT ? |
| S05 | 7.80–9.60 s | 234–287 | Question par message | UN MODÈLE / VOUS PLAÎT ? |
| S06 | 9.60–11.80 s | 288–353 | Produit héros en profondeur | VOTRE / COUP DE CŒUR. |
| S07 | 11.80–13.90 s | 354–416 | Détails du modèle | LES DÉTAILS / FONT LE STYLE. |
| S08 | 13.90–17.80 s | 417–533 | Choix du modèle | VOTRE STYLE. / VOTRE CHOIX. |
| S09 | 17.80–19.00 s | 534–569 | Showroom virtuel | LA BOUTIQUE / DANS VOTRE POCHE. |
| S10 | 19.00–20.70 s | 570–620 | Carte de sélection | VOTRE / SÉLECTION |
| S11 | 20.70–21.90 s | 621–656 | Photo du modèle | LE MODÈLE / EN DÉTAIL |
| S12 | 21.90–23.00 s | 657–689 | Contact par message | UN MESSAGE / POUR COMMENCER. |
| S13 | 23.00–25.50 s | 690–764 | Signature et appel à l’action | VOTRE PROCHAIN LOOK / COMMENCE ICI. |
| S14 | 25.50–26.47 s | 765–793 | Raccord de boucle | Sans texte |

Conserve @daya_na990 exactement. CTA final exact : « Écrivez-nous sur TikTok ». Aucun prix ou chiffre social n’est nécessaire.

## Construction attendue

Les planches et les scènes PNG sont des références de keyframes, pas le film lui-même. Construis des éléments séparés pour les titres, boutons, téléphone, recherche, cartes produit, sélection, détails, halos et mains. Un simple diaporama de 14 PNG avec des fondus ne satisfait pas ce projet.

Recompose tous les textes et interfaces en éléments éditables. Utilise les vraies photos pour les produits si disponibles ; sinon des découpes illustratives peuvent servir au prototype. Les panneaux générés ont des proportions variables : reconstruis dans le master 9:16, sans étirer les mannequins et sans agrandir artificiellement les textes de la planche.

Utilise HyperFrames et GSAP si disponibles. Lis les skills installés correspondant à core, creative, animation, studio et audio. Dans le dépôt mesvideos déjà préparé, conserve la version CLI 0.8.143 ; dans un autre environnement, vérifie la version disponible et sa documentation avant de choisir les commandes. Si le dépôt existant contient videos/daya-livraison-iso/, crée le nouveau projet dans videos/daya-motion-social/ et conserve l’ancienne vidéo.

Une sous-composition par scène ; IDs uniques ; une timeline pausée par composition, enregistrée après construction sous la clé de son data-composition-id. Attributs de timing conformes à la version HyperFrames utilisée. Fonts, JS et médias locaux ; pas de ressources réseau pendant le rendu. Les transitions fonctionnent quand on cherche directement un instant, pas seulement après lecture depuis zéro.

Sépare le mouvement de caméra sur un parent et le mouvement d’entrée sur ses enfants. États initial/final explicites, transformations sans concurrence, pas d’aléatoire non initialisé ni de clock système. Le produit reste lisible pendant les poses. Easing et durées de départ sont indiqués dans le plan, ajuste la fluidité en conservant les limites des scènes.

Direction : charbon, crème, corail lumineux, mannequins dorés/noirs et décor chaud. Titres en serif capitale ; UI en sans serif. Les polices locales livrées sont des substituts cohérents. Respecte la hiérarchie et les marges proposées, valide le cadrage mobile.

Les éléments se raccordent : halo→recherche, avatar→profil, vignette→carte, carte→message, photo→produit en profondeur, détail→widgets, téléphone→showroom, carte favorite→photo, vignette→Message, trace→signature. Ajuste S14 pour rejoindre l’état initial réel de S01 ; la dernière image de maquette n’est pas une obligation de pose finale.

## Musique et sound design

Le fichier assets/audio/SON_TEMOIN_26S.wav est une création originale de démonstration, pas la musique de référence. Tu peux l’utiliser pour un premier rendu. Le 120 BPM est proposé. Les cues sonores du JSON donnent les instants à respecter ou à améliorer : recherche, sélection, reveal, widgets, favori, bouton Message, signature. Une musique autorisée fournie peut remplacer le témoin. Pas de voix off par défaut.

Mix WAV stéréo 48 kHz, musique sous les accents, absence de saturation. Pour un final, mesure environ −16 LUFS intégrés et une crête vraie ≤ −1 dBTP après encodage. Ne prétends pas avoir mesuré la musique de la vidéo TikTok.

## Vérification et livraison

Réalise la source et les 14 scènes, puis les transitions et le son. Lance les contrôles adaptés au moteur/version ; corrige les erreurs réellement détectées. Capture les milieux de scène, les changements de scène ± une image, le frame 0 et le frame 793. Vérifie que le CTA et le handle restent lisibles de 23,3 à 25,3 s.

Exporte le MP4 et vérifie le nombre d’images, les dimensions, la fréquence, l’audio et le décodage complet. Livre le MP4, le projet éditable, les assets locaux, les 14 captures et un court compte-rendu. Signale les vrais assets manquants ; distingue maquette et publicité catalogue finale. Termine le rendu dans le périmètre disponible, pas seulement un plan.
