# Prompt maître — reproduire la mécanique de cette publicité avec une autre entreprise

Copier le texte entre les lignes « DÉBUT DU PROMPT » et « FIN DU PROMPT » dans Claude Code. Placer le dossier complet dans son projet. Remplir `BRIEF_ENTREPRISE.json` ou remplacer les champs ci-dessous.

--- DÉBUT DU PROMPT ---

Tu dois CONSTRUIRE et RENDRE une publicité en motion design pour une nouvelle entreprise en reproduisant la grammaire visuelle, la temporalité et le dialogue image/son de la référence fournie. Poursuis jusqu’au projet éditable et au MP4 vérifié.

## Entrées

- Entreprise : [NOM].
- Offre ou produit principal : [OFFRE].
- Public visé : [PUBLIC].
- Action finale pertinente : [ACTION].
- Couleur principale et couleur claire : [COULEURS].
- Logo SVG ou PNG transparent : [FICHIER].
- Photos/visuels de 12–16 produits, services ou réalisations, dont un visuel héro réutilisé pendant toute la démonstration : [DOSSIER].
- Trois ou quatre bénéfices courts et prouvés : [BÉNÉFICES].
- Source de vérité : `REFERENCE.mp4`, `ANALYSE_COMPLETE.md`, `TIMELINE_REFERENCE.json`, `AUDIO_REFERENCE_GAIN_MOINS_4_1_DB.wav`, `AUDIO_ORIGINAL.m4a` et les captures `scenes/`.

Lis d’abord les assets et les instructions du projet. Demande en une seule fois uniquement les informations essentielles réellement manquantes. Si seuls des assets HD manquent, construis la maquette avec des éléments provisoires clairement identifiés et rends sa prévisualisation.

## Contrat de fidélité

La référence est une publicité Pinterest de 623 images, à 30 images/seconde, en 1024 × 576, soit 20,7666667 s de vidéo. Le master demandé est 1920 × 1080, à 30 images/seconde, EXACTEMENT 623 images. Conserve le 16:9 pour la première réalisation. Une déclinaison verticale nécessite une recomposition spécifique ; elle ne remplace pas ce master.

Remplace l’identité Pinterest, les illustrations et le parcours métier par ceux de l’entreprise. Préserve les changements d’échelle, le déroulement, les temps de lecture, les apparitions décalées, les raccords entre les mêmes assets et les coupes finales.

Respecte les bornes en images de la timeline. Les plages sont `[start_frame, end_frame)` ; à 30 i/s, `t = frame / 30`. Les bornes de segments descriptifs ne signifient pas toutes une coupe. Les vraies coupes de fond sont f152, f368, f524, f555, f573, f584 et f596. Les passages très rapides de composition sont notamment f257, f284 et f344. Il faut observer leurs images voisines pour reproduire leur aspect.

## Son : priorité absolue

Utilise `AUDIO_REFERENCE_GAIN_MOINS_4_1_DB.wav` comme UNIQUE mix audio de la première version. Il contient la musique ET les effets du fichier original, décodés à partir de t=0, avec une baisse globale de 4,1 dB et une longueur correspondant au film. Cette baisse conserve les rapports de niveaux et les timings. Le fichier AAC `AUDIO_ORIGINAL.m4a` est fourni comme témoin extrait sans réencodage.

Place le WAV à t=0, à vitesse 1,000, sans time-stretch, décalage, changement de hauteur, re-découpage, fondu automatique ni traitement dynamique supplémentaire. Évite de superposer des clics ou des whooshes de remplacement : ils doubleraient les bruits déjà présents. Fais bouger les images sur cette bande-son.

Les analyses révèlent une subdivision fréquente voisine de 0,20 s, soit 6 images, et plusieurs regroupements à 0,40 s, soit 12 images. Cela ne certifie pas un BPM musical. Les horodatages réels et la piste originale sont prioritaires ; n’invente pas un tempo puis ne recale pas le montage sur lui.

Les attaques de `TIMELINE_REFERENCE.json` sont des pics mesurés dans un mix, pas des stems ni des catégories de SFX certifiées. Une coupe originale peut précéder une attaque. Reproduis cette relation au lieu d’aligner systématiquement chaque coupe sur le pic le plus proche.

Les mouvements doivent fonctionner comme une chorégraphie : anticipation avant un accent, arrivée ou changement d’échelle autour de l’accent, puis courte stabilisation. Toutes les actions n’exigent pas un son ajouté et tout coup musical n’exige pas un nouvel objet.

Si une seconde version impose une nouvelle bande-son, conserve les positions des accents et actions dans une cue sheet ; remplace les familles de sons après écoute. Signale qu’un remplacement ne garantit plus une reproduction sonore identique. La version de fidélité demandée conserve le mix fourni.

## Découpage obligatoire

### S01 — 0.0000–1.2000 s ; f0–f35

**Référence :** Fond presque blanc. À la première image, le symbole Pinterest rouge est très grand et déborde du cadre. Il se contracte rapidement vers le centre, devient légèrement plus petit que sa taille finale, puis se stabilise. Aucun ordinateur ne figure dans cette référence.

**Reconstruction :** Un SVG de l’emblème de la nouvelle marque, transform-origin au centre. Construire le recul en plusieurs phases ; conserver le léger sous-dépassement et le retour à la taille de repos. Les durées et valeurs mesurées priment sur le nom de l’easing.


### S02 — 1.2000–2.6000 s ; f36–f77

**Référence :** Le symbole glisse progressivement vers la gauche ; le mot Pinterest se révèle à sa droite. L’ensemble devient un bloc marque centré. La révélation du nom se déroule principalement vers 1,7–2,2 s.

**Reconstruction :** Deux calques : emblème et nom. Déplacer le symbole pour centrer le bloc final et révéler le nom avec un masque horizontal, éventuellement une opacité décalée par lettre. Garder les coordonnées pré-calculées.


### S03 — 2.6000–3.9000 s ; f78–f116

**Référence :** Le bloc marque monte. Des images arrondies apparaissent en décalage, principalement de droite vers la gauche au début, puis les images complémentaires remplissent les colonnes. Les cartes combinent déplacement vertical et disparition progressive de leur aspect pâle.

**Reconstruction :** Préparer 12–16 images de la nouvelle entreprise. Quatre colonnes indépendantes ; cartes avec masques arrondis. Reprendre les délais observés d’environ 0,20 s entre plusieurs apparitions. Le bloc marque doit sortir par le haut lorsque la galerie progresse.


### S04 — 3.9000–5.0667 s ; f117–f151

**Référence :** Les colonnes continuent de monter et révèlent d’autres images. Le logo quitte le cadre. Les nouvelles vignettes peuvent encore arriver avec une opacité faible avant de devenir nettes. La valeur élevée de changement visuel à f117 ne constitue pas une coupe franche : la galerie reste continue.

**Reconstruction :** Animer les groupes de colonnes en y ; les différences de hauteur créent le rythme. Ajouter les entrées individuelles aux cartes nouvellement révélées. Terminer exactement avant f152, puis couper au fond de marque.


### S05 — 5.0667–7.8000 s ; f152–f233

**Référence :** Coupe franche sur fond rouge. Texte source : « Thousand of » en blanc, puis un cartouche blanc avec un mot rouge. Les mots visibles successifs sont Inspirations, Illustration, Motion, Design. Leur remplacement s’effectue verticalement dans le masque ; pendant le passage, deux mots peuvent être partiellement visibles.

**Reconstruction :** Conserver un préfixe stable et animer une bande verticale de mots dans overflow:hidden. Repères visuels approximatifs des remplacements : 6,07 ; 6,60 ; 7,13 s. Ils doivent être ajustés en comparant les images locales, pas présentés comme des coupes. Choisir quatre mots courts liés à l’entreprise, sans inventer de promesse chiffrée.


### S06 — 7.8000–9.4667 s ; f234–f283

**Référence :** Le cartouche devient « All You Need » ; le préfixe s’efface. « Is Here » se révèle à droite, avec des espacements et des apparitions progressives. À f257, la composition subit un agrandissement très rapide, puis la première partie sort à gauche. « Is Here » reste au centre.

**Reconstruction :** Deux groupes de texte et un masque. Conserver la transformation à partir de f234, le punch-in à f257 et l’état central avant f284. Adapter à « Votre solution » / « est ici », ou à une formulation équivalente courte de la nouvelle marque. Préserver la temporalité malgré la longueur différente du texte.


### S07 — 9.4667–10.9333 s ; f284–f327

**Référence :** Six cartes carrées arrondies apparaissent groupées autour du message, puis s’écartent en couronne. Les cartes restent verticales tandis que leurs positions avancent globalement dans le sens horaire. Ce n’est pas une rotation individuelle de toutes les photos sur elles-mêmes.

**Reconstruction :** Six produits, réalisations ou services de la nouvelle marque. Un calque par carte. Calculer x/y par trajectoire circulaire ou keyframes équivalentes, en conservant l’orientation de chaque image. L’expansion radiale précède la rotation. Le message reste lisible au centre.


### S08 — 10.9333–11.4667 s ; f328–f343

**Référence :** Un curseur blanc rejoint la carte du personnage au chapeau. La carte s’assombrit au survol ; un bouton rouge « Save » apparaît dans son angle supérieur droit. La couronne et le cadrage commencent à favoriser cette carte.

**Reconstruction :** Curseur SVG animé indépendamment, voile de survol séparé, bouton séparé. Pour une autre entreprise, « Save » devient une action pertinente : sélectionner, voir, ajouter à la sélection, etc. Ne pas simuler une fonction sans rapport avec son parcours réel.


### S09 — 11.4667–12.2667 s ; f344–f367

**Référence :** À f344, punch-in très rapide sur la carte survolée. Le texte « Is Here » glisse hors du cadre à gauche pendant que la carte et le bouton Save prennent de la place. Le curseur reste au contact du bouton.

**Reconstruction :** Agrandir et déplacer le groupe de scène tout en préservant le point d’intérêt carte/bouton. Préparer le raccord vers la fiche produit ou réalisation de la nouvelle marque, en réutilisant le même visuel.


### S10 — 12.2667–14.6000 s ; f368–f437

**Référence :** Coupe vers une page Pinterest. Une fenêtre blanche arrondie apparaît devant un arrière-plan atténué. Titre « Create a board », image héro, champ « Board name » puis saisie progressive de « Character Illustration ». Le curseur noir se dirige vers le bouton rouge « Create ». La saisie est visible environ de 12,65 à 13,80 s.

**Reconstruction :** Reconstituer la fenêtre avec du texte et des composants éditables. Garder le fond atténué pendant la lecture. Adapter l’action : nommer une sélection, demander un devis, réserver une visite ou choisir un modèle, selon l’entreprise. Pré-calculer un calendrier de frappe ; conserver l’intervalle de saisie même si le nouveau texte comporte moins de caractères.


### S11 — 14.6000–15.3000 s ; f438–f458

**Référence :** Le texte du bouton disparaît et un petit indicateur blanc de chargement tourne à sa place. La fenêtre et son image restent visibles jusqu’au début de la transition de confirmation.

**Reconstruction :** Faire succéder l’état normal, l’appui, puis le chargement du même bouton. Rotation finie et déterministe du spinner, pilotée par la timeline. Préserver le temps de retour visuel sans inventer un paiement ou une vente réalisée.


### S12 — 15.3000–17.4667 s ; f459–f523

**Référence :** La fenêtre disparaît pendant qu’une notification sombre arrondie apparaît, reprenant la même vignette. Texte : « Saved to » puis « Character Illustration ». Un agrandissement de cadrage autour de 16,1 s rapproche la confirmation. Elle reste lisible jusqu’à la coupe de f524.

**Reconstruction :** Transformer le parcours en confirmation adaptée à l’entreprise : sélection enregistrée, demande envoyée ou rendez-vous demandé. Reprendre la vignette, l’intitulé et le choix précédents. Assurer une pause de lecture après le rapprochement.


### S13 — 17.4667–18.5000 s ; f524–f554

**Référence :** Coupe franche vers le blanc pur. « Pin Your Interest » se révèle brièvement puis reste centré en rouge. La scène ménage une respiration après la démonstration d’interface.

**Reconstruction :** Une promesse courte et vérifiable pour la nouvelle entreprise. Révélation discrète au début, puis maintien lisible. Garder la coupe suivante à f555.


### S14 — 18.5000–19.1000 s ; f555–f572

**Référence :** Coupe franche vers le rouge. « With » apparaît en très grand blanc et occupe une partie importante du cadre. Maintien 18 images.

**Reconstruction :** Utiliser « Avec » en français ou un mot équivalent court ; conserver 18 images, sans allonger l’outro.


### S15 — 19.1000–19.4667 s ; f573–f583

**Référence :** Coupe franche vers le blanc ; emblème Pinterest rouge, beaucoup plus grand que le logo de repos de l’introduction. Maintien 11 images.

**Reconstruction :** SVG de la nouvelle marque ; conserver la rupture fond/échelle et les 11 images.


### S16 — 19.4667–19.8667 s ; f584–f595

**Référence :** Coupe franche vers le rouge ; le nom Pinterest est blanc et très grand. Maintien 12 images.

**Reconstruction :** Nom réel de l’entreprise, sans récupération du logotype Pinterest. Adapter sa taille aux marges plutôt que changer la durée.


### S17 — 19.8667–20.7667 s ; f596–f622

**Référence :** Coupe franche vers le blanc. Le bloc complet emblème + nom est petit et centré. Il reste en place jusqu’à la dernière image. La fin ne reprend pas l’emblème géant de la toute première image : une boucle parfaitement raccordée n’est pas démontrée.

**Reconstruction :** Réutiliser le bloc de marque de S02. Conserver les 27 images de maintien. Pour une version de fidélité, ne pas ajouter de nouvelle scène CTA qui rallongerait la musique.


## Direction artistique et adaptation

Utilise une grande couleur de marque, une couleur claire et un contraste fort. Les backgrounds de la source mesurés sur zones plates sont environ #F9F9F9 dans l’introduction, #BD0F28 dans les séquences rouges et #FFFFFF dans la fin. Ce sont les valeurs du fichier compressé, pas la preuve du nuancier officiel. Remplace le rouge par la couleur de la nouvelle identité et adapte le texte clair/foncé pour la lisibilité.

Choisis une sans-serif compatible avec la marque. La police exacte de la référence n’a pas été identifiée ; Inter, Arial ou une police de marque locale peuvent servir de reconstruction. Fais des textes vivants et éditables. Ajuste le corps et la largeur des groupes à la nouvelle marque ; garde la cadence de la vidéo.

Conserve les quatre colonnes masonry et les six cartes en couronne. Les cartes restent droites quand leurs positions tournent. Le visuel héro reste identique dans la couronne, le survol, la fiche, la modale et la confirmation. Le curseur, le bouton, le voile de survol, les champs et le spinner sont des éléments séparés.

L’interface doit démontrer UNE action adaptée à l’entreprise. Exemples : e-commerce → créer une sélection ; agence → déposer une demande de devis ; immobilier → demander une visite ; restaurant → préparer une réservation. Reprends une interface existante si elle est fournie, sinon construis une maquette cohérente identifiée comme telle. Utilise uniquement des prix, avis, chiffres et promesses fournis ou vérifiables.

Écris des textes courts. Pour le bloc des mots défilants, un préfixe possible est « Tout pour » avec quatre mots liés à l’offre. Le message suivant peut être « Votre solution » / « est ici ». Pour la fin : promesse courte → « Avec » → emblème → nom de l’entreprise → bloc de marque compact. Il s’agit d’exemples d’adaptation, pas de textes imposés à une entreprise inconnue.

## Réalisation technique

Utilise HyperFrames et les skills disponibles du projet, avec GSAP pour les calques 2D. Vérifie la version réellement installée avant d’employer des API. La référence ne prouve pas l’usage d’After Effects ou d’un moteur 3D ; ces outils ne sont pas nécessaires à ce style.

Crée un fichier `BRAND_CONFIG` qui regroupe marque, couleurs, slogans, mots défilants, images, nom du choix et action de l’interface. Changer d’entreprise doit remplacer cette configuration et ses assets, en conservant la timeline musicale.

Crée des composants réutilisables : BrandLockup, MasonryGallery, WordRoller, TypographicPunch, OrbitCards, AnimatedCursor, SelectionCard, ActionModal, LoadingButton, ConfirmationToast et BrandOutro.

Utilise une timeline déterministe, pausée et pilotée par le temps de composition. Enregistre-la après sa construction complète. Calcule les dimensions une seule fois après chargement des assets et des polices, puis utilise x/y/scale/rotation pour les déplacements. Anime les calques internes ; respecte le cycle de vie des clips HyperFrames.

Les masques conservent leur géométrie de cadrage. Le défilement des mots se fait dans un conteneur overflow:hidden. Le curseur suit une trajectoire explicite ; le calendrier de frappe est pré-calculé ; la rotation du spinner possède une durée finie. Tous les mouvements doivent être identiques lors d’un seek, d’une prévisualisation et du rendu.

Les courbes exactes utilisées par l’auteur ne sont pas connues. Déduis-les du mouvement visible et ajuste-les par comparaison : recul rapide avec léger sous-dépassement pour le logo ; accélération puis ralentissement pour les colonnes et le curseur ; transition verticale brève pour les mots ; trajectoire continue pour la couronne ; punch-in très rapide aux raccords typographiques. Ne remplace pas toute la chorégraphie par la même courbe ou le même effet de rebond.

Rends les raccords finaux S14–S17 avec des coupes franches. Conserve leurs durées respectives : 18, 11, 12 et 27 images. L’identité visuelle change ; leur rythme reste identique. Ne prétends pas construire une boucle parfaite si l’ouverture et la fermeture ne correspondent pas.

## Vérification et livrables

Fournis d’abord une planche des scènes à partir du rendu réel, puis poursuis la construction et le rendu sans t’arrêter à une proposition.

Vérifie les images avant/après les raccords, notamment f151/152, f256/257, f283/284, f343/344, f367/368, f458/459, f523/524, f554/555, f572/573, f583/584 et f595/596. Vérifie aussi les maintiens de lecture de la saisie et de la confirmation.

Exécute les vérifications HyperFrames adaptées : lint, check et snapshots de plusieurs scènes. Vérifie l’absence de débordement accidentel, d’assets manquants, de texte illisible et de frames noires. Les dépassements typographiques prévus de S06 font partie de l’effet et doivent être distingués des erreurs.

Rends un MP4 H.264, 1920 × 1080, 30 i/s, 623 images, yuv420p, avec signalisation Rec.709 et audio AAC 48 kHz. Un débit de 12–20 Mbit/s ou un réglage CRF 18–20 peut servir de départ. Vérifie les paramètres réellement disponibles dans la version installée.

Le fichier WAV fourni a été mesuré vers -14,0 LUFS et -1,2 dBTP avant encodage final. Contrôle le mix après encodage AAC ; corrige seulement le gain global si ses pics l’exigent. La fréquence de lecture et les offsets restent inchangés. Vérifie la synchronisation sur le début ET la fin pour détecter une dérive.

Livre le projet éditable, la configuration de marque, les assets, le storyboard du rendu, la timeline avec repères audio, le MP4 final et les commandes pour modifier la marque et relancer le rendu. Si un rendu échoue, fournis le blocage exact et les éléments déjà réalisés ; n’annonce pas un MP4 qui n’existe pas.

--- FIN DU PROMPT ---
