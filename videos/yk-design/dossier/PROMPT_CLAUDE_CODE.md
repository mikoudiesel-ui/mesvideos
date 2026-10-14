# Construire la publicité Y-K Design à partir de ce dossier

Tu es un directeur artistique et un développeur motion design confirmé. Construis et rends la publicité de mes services de montage pour boutiques, à partir des fichiers de ce dossier. Elle présente **Y-K Design**, mon monogramme **YK, option B**, mes concepts publicitaires et mon contact **+225 07 12 35 46 02**. L’objet de la vidéo est de me faire contacter pour réaliser des montages publicitaires en motion design. Les produits servent d’exemples créatifs ; la vidéo ne vend pas directement ces produits.

La référence est `reference/REFERENCE.mp4`. Reproduis sa structure, son énergie, ses changements d’échelle, ses défilements, ses interactions, ses pauses et sa synchronisation au son, avec l’identité et les textes Y-K Design. Les maquettes sont dans `maquettes/scene_01.webp` à `scene_17.png`. Les images des scènes 01–12 sont principalement des planches d’états ; leurs titres, repères de temps et badges MAQUETTE n’appartiennent pas au film. Les scènes 13–17 montrent des images clés seules. Les proportions des planches restent illustratives : la timeline et les spécifications ci-dessous définissent le rendu.

## Livrable et format

Livre un projet éditable, un MP4 final et les commandes pour relancer le rendu. Master : **1920 × 1080, 16:9, 30 images/seconde, exactement 623 images, soit 20,7666667 s**. Les plages sont `[début, fin exclusive)`. La dernière image est f622. Le passage 117 n’est pas une coupe : la galerie reste continue. Une version verticale est un travail d’adaptation distinct ; ne transforme pas arbitrairement le master demandé en 9:16.

Le MP4 doit utiliser H.264, yuv420p, fréquence constante 30 i/s, qualité visuelle équivalente à CRF 18–20, audio AAC stéréo 48 kHz à 192–256 kb/s et faststart. Garde la durée vidéo exacte ; les informations de priming AAC ne doivent pas décaler le son. Ne livre pas un diaporama des planches.

## Fichiers qui font autorité

- `BRAND_CONFIG.json` : marque, couleurs, textes, contact, polices et assets.
- `TIMELINE_YK_DESIGN.json` : les 17 plages, repères et attaques audio candidates.
- `timeline/scenes/SCENE_XX.json` : détails de reconstruction de chaque scène.
- `assets/images/monogramme_YK.webp` : véritable asset séparé avec transparence ; même forme dans toute la vidéo.
- `assets/images/baskets.webp`, `parfum.png`, `sac.png` : trois affiches indépendantes, à réutiliser dans la galerie et la couronne.
- `assets/CARTES.json` : trois affiches et trois gros plans de ces mêmes images. Construis les détails par masque et recadrage, sans générer de nouveaux produits.
- `assets/images/curseur_clair.svg`, `curseur_sombre.svg`, `spinner.svg` : éléments UI éditables.
- `assets/fonts/Inter-400.woff2`, `Inter-700.woff2`, `EBGaramond-700.woff2` : polices locales avec leurs licences.
- `assets/audio/AUDIO_MASTER.flac` : mix de référence aligné et atténué uniformément de 4,1 dB. `AUDIO_ORIGINAL.m4a` conserve le mix source.
- `PLAN_DE_PRODUCTION.pdf` et `LECTEUR_STORYBOARD.html` : lecture du dossier, pas des assets à animer en bloc.

Les affiches séparées sont la source canonique des produits : elles peuvent présenter de petites différences par rapport aux générations des planches. Dans le film, réutilise les mêmes fichiers partout. Tous les textes de marque, l’offre, les boutons, le champ et le numéro doivent être de vrais calques éditables. Si tu redessines le monogramme en SVG, conserve précisément sa silhouette ; n’invente pas un autre logo.

## Version légère du dossier

Les 21 images sont encodées en WebP sans perte : pixels, dimensions, textes et transparence conservés. Le son utilise FLAC sans perte, avec des échantillons décodés identiques au master WAV. Tous les autres éléments, dont le prompt complet, les 17 scènes, le PDF et la référence vidéo, sont conservés.

## Contrat sonore

Si le moteur exige un WAV, décode le FLAC localement avec `ffmpeg -i assets/audio/AUDIO_MASTER.flac -c:a pcm_s24le assets/audio/AUDIO_MASTER.wav`, puis pointe le moteur vers ce WAV. Ce décodage ne change pas les échantillons ni le timing.

Le fichier FLAC est un **mix complet**, musique et effets déjà réunis. Place-le à t=0, vitesse 1, sans décalage, découpage, changement de tempo, bouclage, nouvelle compression dynamique ou nouveaux effets superposés. Il comporte 996 800 échantillons par canal à 48 kHz, soit exactement 623/30 secondes. Les mesures déjà effectuées sont environ −14 LUFS et −1,2 dBTP après atténuation uniforme ; vérifie l’encodage final sans modifier le caractère du mix.

Les candidats d’attaques dans le JSON sont des repères de flux spectral à précision approximative de 10 ms. Ils ne prouvent ni le nom de la musique, ni un BPM exact, ni la nature de chaque bruit. Ne force pas toutes les actions sur une grille BPM inventée. Garde les actions de clic, frappe, punch-in et coupe aux moments de la référence. Écoute le rendu et compare-le au fichier fourni. Pas de voix off supplémentaire.

## Direction artistique

Rouge de marque à plat **#BD0F28**, clair **#F9F9F9**, carte sombre **#262626**. Utilise Inter pour le texte de l’agence et l’interface. Les styles éditoriaux des concepts produits restent visibles dans leurs affiches. Recrée les fonds de scène avec les valeurs de configuration : les éventuelles textures ou nuances des maquettes générées ne doivent pas provoquer de variations de rouge dans le film.

La profondeur vient de l’échelle, du recadrage, des décalages de colonnes et des calques. Pas de rotations 3D décoratives, d’effets aléatoires ou de transitions ajoutées à chaque plan. Les photos restent nettes et les cartes de la couronne restent droites. Aucun mannequin de la boutique Daya, logo Pinterest, contenu automobile ou élément de l’ancien projet ne doit apparaître ici. Les trois concepts sont des exemples, pas un portefeuille de clients inventés. Aucun tarif, témoignage, délai ou résultat commercial n’est fourni.

## Réalisation des 17 scènes

| Scène | Images | Temps | Visuel et action |
|---|---:|---:|---|
| 01 | 0–35 | 0–1,20 s | Monogramme géant qui recule, passe légèrement sous sa taille finale, puis se stabilise. |
| 02 | 36–77 | 1,20–2,60 s | Monogramme à gauche, révélation Y-K Design à droite, début de montée. |
| 03 | 78–116 | 2,60–3,90 s | Galerie de concepts en quatre colonnes, entrées décalées, EXEMPLES CRÉATIFS. |
| 04 | 117–151 | 3,90–5,07 s | Même galerie en défilement ascendant continu. |
| 05 | 152–233 | 5,07–7,80 s | Des publicités + mots créatives / dynamiques / sur mesure / pour boutiques. |
| 06 | 234–283 | 7,80–9,47 s | Je réalise vos montages, punch-in, puis vos montages seul. |
| 07 | 284–327 | 9,47–10,93 s | Six cartes déployées en couronne, mouvement horaire sans rotation des images. |
| 08 | 328–343 | 10,93–11,47 s | Survol parfum, bouton Créer ma publicité, appui bref. |
| 09 | 344–367 | 11,47–12,27 s | Punch-in et recentrage du parfum, texte qui quitte le bord gauche. |
| 10 | 368–437 | 12,27–14,60 s | Interface de projet, champ Votre boutique tapé, bouton Préparer le montage. |
| 11 | 438–458 | 14,60–15,30 s | Appui et spinner blanc fini dans le même bouton. |
| 12 | 459–523 | 15,30–17,47 s | Carte Montages pour boutiques et numéro, zoom puis pause de lecture. |
| 13 | 524–554 | 17,47–18,50 s | Intéressé ? Écrivez-moi. + contact sur clair. |
| 14 | 555–572 | 18,50–19,10 s | AVEC énorme, blanc sur rouge. |
| 15 | 573–583 | 19,10–19,47 s | Monogramme rouge sur clair. |
| 16 | 584–595 | 19,47–19,87 s | Y-K Design très grand, blanc sur rouge. |
| 17 | 596–622 | 19,87–20,77 s | Signature compacte + offre + contact, fin nette. |

### 01–04 : identité et galerie

Le recul de l’ouverture est très rapide ; observe les images 0, 6, 12 et 30 de la référence. Les repères mesurés de largeur à reconstruire au master sont environ 154 px à f6, 71 px à f12 et 90 px à f30 pour la silhouette visible. Le logo initial déborde franchement du cadre. Ne maintiens pas une taille géante pendant une seconde entière. Tiens compte des marges transparentes du WebP pour régler sa largeur visible. La scène 02 conserve cette taille, révèle le nom et monte vers la galerie. La typographie du nom est compacte comme la référence.

Dans les scènes 03 et 04, chaque colonne est un groupe autonome masqué, de positions fixes et de cartes séparées. Alterne les affiches entières avec leurs détails et quelques cartes typographiques STYLE, SIGNATURE, ALLURE. Préserve le même produit au sein de chaque concept. Le défilement doit continuer au passage f117 ; couper seulement à f152.

### 05–06 : mon offre de montage

Texte exact de S05 : préfixe **Des publicités** ; mots **créatives**, **dynamiques**, **sur mesure**, **pour boutiques**. Intervalles du mot : f152–181, f182–197, f198–213, f214–233. Cartouche clair et mot rouge, masque vertical propre. Les mots arrivent, tiennent, puis repartent ; ils ne clignotent pas sans lecture.

Texte exact de S06 : **Je réalise** dans le cartouche, puis **vos montages** en clair à droite. Observe le punch-in f257. Le premier groupe sort à gauche, le second reste centré. À f284, réduire vos montages pour laisser de la place aux six cartes. Les mots identifient explicitement mon service : ne les remplacer ni par une accroche de vente du parfum, ni par une formule qui fait croire que je vends les produits.

### 07–09 : couronne et sélection

Six cartes, chacune environ 250 px de côté à l’état de couronne, angles arrondis. Ordre horaire : affiche baskets, affiche parfum, détail baskets, détail sac, détail parfum, affiche sac. Le rayon indicatif est 400 px ; adapte-le pour préserver marges, texte central et absence de collision. Calcule les positions par angle, avec une progression horaire continue. Les cartes restent à rotation 0 : la couronne déplace les centres, pas les photos. Garde la continuité des positions de S07 à S08.

Le parfum est le concept sélectionné. À S08, un curseur blanc survole sa carte placée à droite ; un voile sombre discret apparaît sur elle seule. Bouton exact **Créer ma publicité**, deux lignes si nécessaire. État pressé f343. Pas de doublon de curseur.

À f344, punch-in de tout le groupe, échelle indicative 2,4. Puis translater le groupe pour mettre le parfum près du centre. La carte agrandie reste autour de 592 px de côté ; une fois le punch-in terminé, la translation ne doit pas faire varier sa taille. Le texte vos montages sort à gauche et les cartes périphériques dépassent des bords par le zoom. Vers f356, parfum presque centré ; f367 prépare la coupe. Garde le même poster et le même bouton. Ne remplace pas une image en plein zoom.

### 10–12 : démonstration du projet et coordonnées

À f368, coupe sur une page de projet Y-K Design claire avec un modal blanc arrondi. En-tête de modal **Votre projet publicitaire**, sous-titre **Montage sur mesure pour votre boutique**, vignette du même parfum, champ **Nom du projet**, valeur tapée **Votre boutique**, bouton rouge **Préparer le montage**. Le fond de page est légèrement flouté sous un voile clair ; aucun ordinateur ni navigateur filmé.

La frappe est pré-calculée dans `SCENE_10.json`, de f380 à f416. Les états illustrés par les maquettes ne sont pas des captures exactes au frame ; utilise ces événements et la référence pour le rendu. Le curseur devient sombre sur la page claire et rejoint le bouton avant f438. Cette interface est une démonstration de création de projet. Ne simule pas de paiement, commande envoyée, avis client ou compte authentifié.

S11 reprend exactement la même géométrie. Le bouton s’appuie puis affiche un spinner blanc, rotation contrôlée par le temps et terminée à f459. Pas de boucle indépendante en CSS.

À S12, le modal ferme et la carte sombre affiche deux lignes : **Montages pour boutiques** puis **+225 07 12 35 46 02**, avec la même vignette à gauche. Le numéro est une coordonnée fournie, pas un champ aléatoire. Le zoom de contact arrive autour de f483 / 16,10 s, puis tient jusqu’à f524. La carte conserve des marges et le numéro doit se lire sans chevauchement. Ne raccourcis pas cette pause pour ajouter une transition.

### 13–17 : appel à contact et signature

S13 : fond clair, **Intéressé ?** puis **Écrivez-moi.**, rouge, numéro en dessous. Pop bref et maintien lisible. S14, S15 et S16 suivent les coupes franches de la référence aux frames 555, 573, 584. S14 AVEC blanc sur rouge ; S15 monogramme rouge sur clair ; S16 Y-K Design blanc sur rouge. Ce sont des flashes d’identité ; n’allonge pas les transitions.

S17 commence à f596 : bloc compact, monogramme à gauche du nom, dessous **Montages publicitaires pour boutiques**, puis **+225 07 12 35 46 02**. Le numéro a déjà été montré plus longtemps en S12 et S13. Maintenir la signature jusqu’à f622. Pas de fondu au noir. La dernière composition compacte ne correspond pas à la taille géante de l’ouverture : ne prétends pas obtenir une boucle parfaite sans vérifier ce raccord.

## Construction technique

Utilise les capacités HyperFrames installées si disponibles : HTML/CSS, GSAP et une composition déterministe. Consulte les instructions et la CLI de la version réellement installée avant d’inventer des commandes. Si HyperFrames n’est pas disponible, choisis un moteur vidéo adapté avec un rendu au frame, en gardant les mêmes calques et timing. Commence par inspecter le dossier, le runtime et la référence, puis implémente réellement le projet.

Crée une seule timeline maîtresse pausée et contrôlée par le temps de composition. Enregistre-la après sa construction. Charge les polices et images avant de mesurer les blocs ; fixe ensuite leurs positions et dimensions. Anime x/y, scale et rotation des calques internes. Respecte les phases de vie des clips du moteur. Pas de Date.now(), Math.random(), CSS animé non seekable ou setTimeout pour les événements de frappe. Aucune dérive entre lecture, seek et export.

Mets toutes les copies dans BRAND_CONFIG et regroupe les assets dans un registre. Un même identifiant d’affiche doit correspondre au même fichier de S03 jusqu’à S12. Le bouton et le texte des UI doivent rester des éléments éditables. Le masque de galerie, celui des mots et les arrondis des cartes doivent garder une géométrie stable lors de l’animation.

## Validation et livraison

1. Génère des snapshots aux keyframes du JSON, compare les cadrages, tailles et textes au dossier et les rythmes à la référence. Vérifie aussi f151/152, f367/368, f523/524, f554/555, f572/573, f583/584 et f595/596.
2. Vérifie les 623 images vidéo, 30 i/s, 1920×1080, absence de frame noire et absence d’asset manquant. Contrôle les accents, la marque Y-K Design, les six cartes droites et le numéro exact à chaque apparition.
3. Vérifie le son : alignement à t=0, aucune vitesse modifiée, aucun second bruit de clic ou de frappe. Compare à l’écoute avec le mix fourni.
4. Exécute les vérifications adaptées au moteur et sa version, corrige les problèmes puis rends le MP4. Ne prétends pas avoir terminé une vidéo si seul le code existe.
5. Livre `YK_DESIGN_PUBLICITE_1080P.mp4`, le projet éditable, la configuration, les assets et un README contenant les commandes de prévisualisation et de rendu effectivement vérifiées.

Fais les choix d’implémentation ordinaires et avance jusqu’au rendu. Si une dépendance ou le rendu bloque, donne l’erreur précise et les fichiers réellement produits. Le dossier est suffisamment défini pour commencer sans redemander la marque, le numéro, les produits, le format ou les textes.
