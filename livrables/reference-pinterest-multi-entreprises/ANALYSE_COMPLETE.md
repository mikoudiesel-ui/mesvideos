# Analyse de la référence Pinterest — adaptation à d’autres entreprises

La référence a été examinée au moyen de ses 623 images, de planches de frames exactes et de mesures audio. Ce dossier prépare une reproduction de sa mécanique ; il ne contient pas une nouvelle publicité déjà rendue.

## Ce qui est établi

- Vidéo horizontale 16:9, 1024 × 576, 30 i/s, 623 images : 20,7667 s.
- Publicité Pinterest, avec illustrations, galerie, texte animé et parcours de création d’un tableau.
- Animation 2D et interfaces ; aucun ordinateur filmé dans cette référence.
- Un seul mix stéréo HE-AACv2, 44,1 kHz. Aucun stem musique/clavier/clic indépendant.
- Coupes de fond aux frames 152, 368, 524, 555, 573, 584, 596 ; mouvements continus entre ces coupes.
- Les images source sont fortement compressées : débit vidéo environ 234 kbit/s, audio environ 32 kbit/s. Le master final doit utiliser les assets originaux HD de la nouvelle entreprise.

## Ce qui relève d’une reconstruction

La police exacte, le logiciel original, les expressions, les keyframes d’auteur et les noms des sons n’ont pas été identifiés. Les courbes, structures de calques et valeurs proposées reproduisent le résultat visible ; elles ne prétendent pas révéler le projet source.

Les grands raccords sont datés à la frame. Certains départs de gestes continus, frappe et passages de mots sont approximatifs et doivent être affinés sur les frames fournies. Les attaques audio mesurées sont des candidats de transitoires à 10 ms près, pas un catalogue de sons isolés. Les descriptions de fonctions sonores indiquent leur association au geste, pas une identification certaine d’instrument ou de sample.

## Direction visuelle

L’identité s’exprime avec un fond très clair, un aplat de marque et du texte à fort contraste. Valeurs des zones plates décodées : #F9F9F9 dans le début, #BD0F28 dans les séquences rouges, #FFFFFF dans la fin. Le fichier compressé ne permet pas d’en conclure le nuancier officiel. La composition utilise beaucoup d’espace vide et change brutalement d’échelle à des moments précis.

La typographie est une sans-serif. Le message peut rester petit au centre pour préparer un agrandissement spectaculaire. Les fenêtres et cartes ont des coins arrondis ; le cartouche du rouleau de mots est rectangulaire. La profondeur provient de l’échelle, du cadrage, des superpositions et de l’atténuation du fond. Une scène 3D n’est pas nécessaire.

L’unité vient des assets : la carte choisie réapparaît dans la page, la fenêtre et la notification. Chaque marque doit conserver cette continuité de produit ou de réalisation. Les cartes défilent, gravitent et sont sélectionnées ; elles ne servent pas simplement d’illustrations indépendantes.

## Son et synchronisation

Le fichier `AUDIO_ORIGINAL.m4a` conserve les 451 paquets AAC du MP4, vérifiés par hashes de données. Le WAV fourni est décodé depuis le même début, rééchantillonné à 48 kHz, coupé uniquement à la fin du film et atténué uniformément de 4,1 dB. Il contient 996800 échantillons par canal, soit exactement 623/30 s. Il n’a subi ni changement de vitesse, ni compression dynamique, ni remplacement de sons.

Mesures : mix source vers -9,9 LUFS, 2,9 dBTP décodés ; WAV atténué vers -14,0 LUFS, -1,2 dBTP, avec la même plage dynamique mesurée de 2,4 LU. Les dépassements du mix décodé sont traités par le gain global ; il ne faut pas en conclure l’état du master avant la compression AAC.

Les attaques présentent fréquemment des espacements proches de 0,20 s, soit 6 frames, et des regroupements à 0,40 s. Le mix présente aussi d’autres périodicités. Un BPM musical exact n’est donc pas certifié. Garder le fichier à 1,000×, à t=0, reproduit le rythme plus fidèlement qu’un tempo inventé.

Les coupes ne sont pas systématiquement au sommet d’un pic. Exemple : coupe à 19,100 s, attaque candidate à 19,190 s. Reprendre l’écart observé plutôt que « corriger » la référence. L’anticipation, l’arrivée et la stabilisation sont trois moments différents : un mouvement peut commencer avant le bruit et s’arrêter après.

Ne superposer aucun SFX de remplacement au master pour la version fidèle : le clavier, les clics ou les transitions présents dans le mix seraient doublés. Si le projet exige une autre bande-son, les repères deviennent une cue sheet, mais les timbres d’origine ne peuvent pas être retrouvés exactement à partir des mesures seules.

## Plan par plan

### S01 — Emblème géant, recul rapide et stabilisation

**Temps :** 0.0000–1.2000 s ; frames 0–35 ; 36 images.

**Visible :** Fond presque blanc. À la première image, le symbole Pinterest rouge est très grand et déborde du cadre. Il se contracte rapidement vers le centre, devient légèrement plus petit que sa taille finale, puis se stabilise. Aucun ordinateur ne figure dans cette référence.

**Composition :** Centre (512, 288) dans la source 1024 × 576. Largeur mesurée du masque rouge : 82 px à f6, 38 px à f12, environ 48 px à f30. La largeur initiale exacte dépasse le cadre et ne peut pas être déduite de sa boîte visible.

**Méthode proposée :** Un SVG de l’emblème de la nouvelle marque, transform-origin au centre. Construire le recul en plusieurs phases ; conserver le léger sous-dépassement et le retour à la taille de repos. Les durées et valeurs mesurées priment sur le nom de l’easing.

**Repères audio :** Attaque spectrale forte à 0,260 s ; autres attaques à 0,340 et 0,440 s. Elles se produisent pendant la fin du recul et le rebond de taille, pas lors d’une nouvelle scène.

![Emblème géant, recul rapide et stabilisation](scenes/S01.jpg)

### S02 — Déploiement du nom à côté du symbole

**Temps :** 1.2000–2.6000 s ; frames 36–77 ; 42 images.

**Visible :** Le symbole glisse progressivement vers la gauche ; le mot Pinterest se révèle à sa droite. L’ensemble devient un bloc marque centré. La révélation du nom se déroule principalement vers 1,7–2,2 s.

**Composition :** Bloc final approximatif x404–622, y264–312 dans la source. Le symbole seul passe du centre x512 à environ x428 quand le nom devient lisible. La géométrie doit être recalculée pour le nouveau nom.

**Méthode proposée :** Deux calques : emblème et nom. Déplacer le symbole pour centrer le bloc final et révéler le nom avec un masque horizontal, éventuellement une opacité décalée par lettre. Garder les coordonnées pré-calculées.

**Repères audio :** Attaques à 1,790 ; 1,870 ; 1,980 ; 2,070 ; 2,150 ; 2,250 s pendant la révélation. Ce sont des repères du mix, pas la preuve de six effets isolés.

![Déploiement du nom à côté du symbole](scenes/S02.jpg)

### S03 — La marque monte ; la galerie se construit

**Temps :** 2.6000–3.9000 s ; frames 78–116 ; 39 images.

**Visible :** Le bloc marque monte. Des images arrondies apparaissent en décalage, principalement de droite vers la gauche au début, puis les images complémentaires remplissent les colonnes. Les cartes combinent déplacement vertical et disparition progressive de leur aspect pâle.

**Composition :** Galerie de quatre colonnes de hauteurs différentes, et non une grille de cases identiques. Les principales cartes mesurent environ 200–205 px de large dans la source ; les gouttières valent environ 16–20 px. Les ratios des images sont variés.

**Méthode proposée :** Préparer 12–16 images de la nouvelle entreprise. Quatre colonnes indépendantes ; cartes avec masques arrondis. Reprendre les délais observés d’environ 0,20 s entre plusieurs apparitions. Le bloc marque doit sortir par le haut lorsque la galerie progresse.

**Repères audio :** Attaques à 2,790 ; 2,990 ; 3,200 ; 3,400 ; 3,590 s. Faire correspondre les arrivées des cartes à cette séquence, en conservant les mouvements continus entre les accents.

![La marque monte ; la galerie se construit](scenes/S03.jpg)

### S04 — Défilement de la galerie

**Temps :** 3.9000–5.0667 s ; frames 117–151 ; 35 images.

**Visible :** Les colonnes continuent de monter et révèlent d’autres images. Le logo quitte le cadre. Les nouvelles vignettes peuvent encore arriver avec une opacité faible avant de devenir nettes. La valeur élevée de changement visuel à f117 ne constitue pas une coupe franche : la galerie reste continue.

**Composition :** Les images dépassent le bord supérieur et sont masquées par le cadre. Les espaces variables entre les cartes maintiennent la structure en colonnes. Le fond reste proche de #F9F9F9.

**Méthode proposée :** Animer les groupes de colonnes en y ; les différences de hauteur créent le rythme. Ajouter les entrées individuelles aux cartes nouvellement révélées. Terminer exactement avant f152, puis couper au fond de marque.

**Repères audio :** Attaques à 3,990 ; 4,190 ; 4,390 ; 4,590 ; 4,790 ; 4,990 s. L’accent de 4,990 s précède légèrement la coupe de 5,0667 s.

![Défilement de la galerie](scenes/S04.jpg)

### S05 — Phrase fixe et mots défilants dans un cartouche

**Temps :** 5.0667–7.8000 s ; frames 152–233 ; 82 images.

**Visible :** Coupe franche sur fond rouge. Texte source : « Thousand of » en blanc, puis un cartouche blanc avec un mot rouge. Les mots visibles successifs sont Inspirations, Illustration, Motion, Design. Leur remplacement s’effectue verticalement dans le masque ; pendant le passage, deux mots peuvent être partiellement visibles.

**Composition :** Phrase centrée et assez petite : environ 40–44 px dans la source pour la ligne complète, selon l’étape. Le cartouche est rectangulaire, sans arrondi marqué. Le groupe se recentre lorsque la largeur du mot change.

**Méthode proposée :** Conserver un préfixe stable et animer une bande verticale de mots dans overflow:hidden. Repères visuels approximatifs des remplacements : 6,07 ; 6,60 ; 7,13 s. Ils doivent être ajustés en comparant les images locales, pas présentés comme des coupes. Choisir quatre mots courts liés à l’entreprise, sans inventer de promesse chiffrée.

**Repères audio :** Attaques fortes proches des remplacements à 6,160 ; 6,820 ; 7,260 s ; accent à 7,790 s pour la transformation suivante. Le son reste celui du mix complet.

![Phrase fixe et mots défilants dans un cartouche](scenes/S05.jpg)

### S06 — Transformation du message et punch-in typographique

**Temps :** 7.8000–9.4667 s ; frames 234–283 ; 50 images.

**Visible :** Le cartouche devient « All You Need » ; le préfixe s’efface. « Is Here » se révèle à droite, avec des espacements et des apparitions progressives. À f257, la composition subit un agrandissement très rapide, puis la première partie sort à gauche. « Is Here » reste au centre.

**Composition :** Le message passe d’un petit bloc centré à une phrase surdimensionnée qui dépasse les bords. Le cadrage fait partie de l’effet. « Is Here » devient ensuite le centre de la composition.

**Méthode proposée :** Deux groupes de texte et un masque. Conserver la transformation à partir de f234, le punch-in à f257 et l’état central avant f284. Adapter à « Votre solution » / « est ici », ou à une formulation équivalente courte de la nouvelle marque. Préserver la temporalité malgré la longueur différente du texte.

**Repères audio :** Attaques à 7,790 ; 7,990 ; 8,190 ; 8,420 ; 8,600 ; 8,790 ; 9,000 ; 9,190 s. L’image amplifie le message entre ces accents, sans quantifier artificiellement toute l’animation sur une grille régulière.

![Transformation du message et punch-in typographique](scenes/S06.jpg)

### S07 — Six cartes se déploient autour du message

**Temps :** 9.4667–10.9333 s ; frames 284–327 ; 44 images.

**Visible :** Six cartes carrées arrondies apparaissent groupées autour du message, puis s’écartent en couronne. Les cartes restent verticales tandis que leurs positions avancent globalement dans le sens horaire. Ce n’est pas une rotation individuelle de toutes les photos sur elles-mêmes.

**Composition :** À f288, cartes d’environ 133 × 133 px dans la source. Le centre est proche de (512,288), la couronne de rayon approximatif 200–230 px. Exemple observé : carte supérieure gauche centrée à (445,129) à f288, puis (473,87) à f300 et (541,77) à f312.

**Méthode proposée :** Six produits, réalisations ou services de la nouvelle marque. Un calque par carte. Calculer x/y par trajectoire circulaire ou keyframes équivalentes, en conservant l’orientation de chaque image. L’expansion radiale précède la rotation. Le message reste lisible au centre.

**Repères audio :** Attaques à 9,390 ; 9,580 ; 9,990 ; 10,390 ; 10,590 ; 10,780 s. Repère 9,580 s dans la phase d’expansion. Les cartes poursuivent leur mouvement entre les coups.

![Six cartes se déploient autour du message](scenes/S07.jpg)

### S08 — Le curseur cible une carte

**Temps :** 10.9333–11.4667 s ; frames 328–343 ; 16 images.

**Visible :** Un curseur blanc rejoint la carte du personnage au chapeau. La carte s’assombrit au survol ; un bouton rouge « Save » apparaît dans son angle supérieur droit. La couronne et le cadrage commencent à favoriser cette carte.

**Composition :** Conserver la même image héro dans la galerie, la couronne, la carte sélectionnée et les étapes d’interface suivantes. Cette continuité est une partie essentielle du raccord.

**Méthode proposée :** Curseur SVG animé indépendamment, voile de survol séparé, bouton séparé. Pour une autre entreprise, « Save » devient une action pertinente : sélectionner, voir, ajouter à la sélection, etc. Ne pas simuler une fonction sans rapport avec son parcours réel.

**Repères audio :** Attaques proches à 10,990 ; 11,210 ; 11,390 s. L’attribution précise à un clic ou à la musique ne peut pas être prouvée par le mix stéréo seul ; garder la piste évite de deviner.

![Le curseur cible une carte](scenes/S08.jpg)

### S09 — Agrandissement de la carte sélectionnée

**Temps :** 11.4667–12.2667 s ; frames 344–367 ; 24 images.

**Visible :** À f344, punch-in très rapide sur la carte survolée. Le texte « Is Here » glisse hors du cadre à gauche pendant que la carte et le bouton Save prennent de la place. Le curseur reste au contact du bouton.

**Composition :** La carte sélectionnée conserve son contenu et ses arrondis. Les autres cartes se retrouvent partiellement hors cadre. La scène garde le fond rouge jusqu’à f368.

**Méthode proposée :** Agrandir et déplacer le groupe de scène tout en préservant le point d’intérêt carte/bouton. Préparer le raccord vers la fiche produit ou réalisation de la nouvelle marque, en réutilisant le même visuel.

**Repères audio :** Attaques à 11,900 ; 11,990 ; 12,200 s pendant ce mouvement ; accent à 12,390 s lors de l’arrivée de l’interface suivante.

![Agrandissement de la carte sélectionnée](scenes/S09.jpg)

### S10 — Interface, fenêtre modale et saisie

**Temps :** 12.2667–14.6000 s ; frames 368–437 ; 70 images.

**Visible :** Coupe vers une page Pinterest. Une fenêtre blanche arrondie apparaît devant un arrière-plan atténué. Titre « Create a board », image héro, champ « Board name » puis saisie progressive de « Character Illustration ». Le curseur noir se dirige vers le bouton rouge « Create ». La saisie est visible environ de 12,65 à 13,80 s.

**Composition :** À f420 : fenêtre approximative x184–840, y82–495, soit 64 % de la largeur et 72 % de la hauteur de la source. Image centrale environ 275 × 155 px. Champ x222–801, y340–421 ; bouton x223–801, y432–474. Ces mesures sont raster et approximatives.

**Méthode proposée :** Reconstituer la fenêtre avec du texte et des composants éditables. Garder le fond atténué pendant la lecture. Adapter l’action : nommer une sélection, demander un devis, réserver une visite ou choisir un modèle, selon l’entreprise. Pré-calculer un calendrier de frappe ; conserver l’intervalle de saisie même si le nouveau texte comporte moins de caractères.

**Repères audio :** Attaques nombreuses entre 12,480 et 13,790 s, puis 14,160 ; 14,590 s. Elles fournissent la zone de rythme de la saisie et de la validation. Le mix ne fournit pas une piste clavier isolée.

![Interface, fenêtre modale et saisie](scenes/S10.jpg)

### S11 — Validation et chargement

**Temps :** 14.6000–15.3000 s ; frames 438–458 ; 21 images.

**Visible :** Le texte du bouton disparaît et un petit indicateur blanc de chargement tourne à sa place. La fenêtre et son image restent visibles jusqu’au début de la transition de confirmation.

**Composition :** Même bouton, même position et même image. Le chargement dure environ 0,70 s dans ce découpage ; son commencement exact est à ajuster de quelques images lors du raccord.

**Méthode proposée :** Faire succéder l’état normal, l’appui, puis le chargement du même bouton. Rotation finie et déterministe du spinner, pilotée par la timeline. Préserver le temps de retour visuel sans inventer un paiement ou une vente réalisée.

**Repères audio :** Attaques à 14,590 ; 14,790 ; 15,000 ; 15,190 ; 15,260 s. Conserver cette séquence entière.

![Validation et chargement](scenes/S11.jpg)

### S12 — La fenêtre cède la place à une confirmation

**Temps :** 15.3000–17.4667 s ; frames 459–523 ; 65 images.

**Visible :** La fenêtre disparaît pendant qu’une notification sombre arrondie apparaît, reprenant la même vignette. Texte : « Saved to » puis « Character Illustration ». Un agrandissement de cadrage autour de 16,1 s rapproche la confirmation. Elle reste lisible jusqu’à la coupe de f524.

**Composition :** La vignette à gauche et le texte à droite forment un seul bloc de confirmation. L’arrière-plan conserve la page produit, atténuée. Le raccord repose sur le même asset, pas sur un nouveau produit arbitraire.

**Méthode proposée :** Transformer le parcours en confirmation adaptée à l’entreprise : sélection enregistrée, demande envoyée ou rendez-vous demandé. Reprendre la vignette, l’intitulé et le choix précédents. Assurer une pause de lecture après le rapprochement.

**Repères audio :** Attaques à 15,790 ; 16,060 ; 16,200 ; 16,390 ; 16,500 ; 16,990 ; 17,390 s. Garder le zoom et la lecture dans cette plage, puis couper à 17,4667 s.

![La fenêtre cède la place à une confirmation](scenes/S12.jpg)

### S13 — Slogan sur fond blanc

**Temps :** 17.4667–18.5000 s ; frames 524–554 ; 31 images.

**Visible :** Coupe franche vers le blanc pur. « Pin Your Interest » se révèle brièvement puis reste centré en rouge. La scène ménage une respiration après la démonstration d’interface.

**Composition :** Texte de petite taille au centre ; beaucoup d’espace blanc. Le slogan source n’est pas une phrase à réutiliser telle quelle pour toutes les marques.

**Méthode proposée :** Une promesse courte et vérifiable pour la nouvelle entreprise. Révélation discrète au début, puis maintien lisible. Garder la coupe suivante à f555.

**Repères audio :** Attaques à 17,650 ; 17,790 ; 17,990 ; 18,200 ; 18,390 s. Le son reste actif pendant la respiration visuelle.

![Slogan sur fond blanc](scenes/S13.jpg)

### S14 — Mot de liaison géant

**Temps :** 18.5000–19.1000 s ; frames 555–572 ; 18 images.

**Visible :** Coupe franche vers le rouge. « With » apparaît en très grand blanc et occupe une partie importante du cadre. Maintien 18 images.

**Composition :** Mot centré, haut contraste, forte rupture d’échelle avec le slogan précédent.

**Méthode proposée :** Utiliser « Avec » en français ou un mot équivalent court ; conserver 18 images, sans allonger l’outro.

**Repères audio :** Repère de coupe : 18,500 s. Les transitoires voisins du mix sont à 18,510 et 18,590 s ; leur nature exacte n’est pas déduite.

![Mot de liaison géant](scenes/S14.jpg)

### S15 — Emblème seul sur blanc

**Temps :** 19.1000–19.4667 s ; frames 573–583 ; 11 images.

**Visible :** Coupe franche vers le blanc ; emblème Pinterest rouge, beaucoup plus grand que le logo de repos de l’introduction. Maintien 11 images.

**Composition :** L’emblème est centré ; son diamètre est d’environ 300 px dans la source.

**Méthode proposée :** SVG de la nouvelle marque ; conserver la rupture fond/échelle et les 11 images.

**Repères audio :** Repère de coupe : 19,100 s. Une attaque mesurée se situe à 19,190 s. Ne pas déplacer arbitrairement cette coupe jusqu’à l’attaque.

![Emblème seul sur blanc](scenes/S15.jpg)

### S16 — Nom géant sur la couleur de marque

**Temps :** 19.4667–19.8667 s ; frames 584–595 ; 12 images.

**Visible :** Coupe franche vers le rouge ; le nom Pinterest est blanc et très grand. Maintien 12 images.

**Composition :** Nom centré sur une seule ligne. Le corps doit s’adapter à la longueur du nom de l’entreprise.

**Méthode proposée :** Nom réel de l’entreprise, sans récupération du logotype Pinterest. Adapter sa taille aux marges plutôt que changer la durée.

**Repères audio :** Repère de coupe : 19,4667 s ; attaque voisine à 19,620 s. Conserver les positions temporelles de la référence.

![Nom géant sur la couleur de marque](scenes/S16.jpg)

### S17 — Signature finale compacte

**Temps :** 19.8667–20.7667 s ; frames 596–622 ; 27 images.

**Visible :** Coupe franche vers le blanc. Le bloc complet emblème + nom est petit et centré. Il reste en place jusqu’à la dernière image. La fin ne reprend pas l’emblème géant de la toute première image : une boucle parfaitement raccordée n’est pas démontrée.

**Composition :** Même échelle approximative que le bloc marque du début après stabilisation. Durée 27 images, soit 0,90 s.

**Méthode proposée :** Réutiliser le bloc de marque de S02. Conserver les 27 images de maintien. Pour une version de fidélité, ne pas ajouter de nouvelle scène CTA qui rallongerait la musique.

**Repères audio :** Attaques à 20,010 et 20,210 s avant la fin. La vidéo finit à 20,7667 s ; la piste source dépasse ce point d’environ 11 ms selon ses métadonnées.

![Signature finale compacte](scenes/S17.jpg)

## Changer d’entreprise en gardant la mécanique

| Fonction de la référence | Adaptation métier |
|---|---|
| Logo Pinterest | Emblème et nom de l’entreprise |
| Galerie d’inspirations | Produits, réalisations, lieux, services ou usages |
| Inspirations / Illustration / Motion / Design | Quatre bénéfices ou catégories courts, réels |
| All You Need / Is Here | Proposition de valeur en deux groupes courts |
| Six cartes en couronne | Six offres, produits ou exemples représentatifs |
| Carte personnage sélectionnée | Un visuel héro conservé dans tout le parcours |
| Save / Create a board | Action cohérente avec le service |
| Character Illustration | Nom du choix, projet, produit ou demande |
| Saved to… | Confirmation du même choix, sans résultat commercial inventé |
| Pin Your Interest / With / Pinterest | Promesse courte / Avec / identité de marque |

Exemples : boutique → choisir un modèle et enregistrer une sélection ; agence → choisir une réalisation et demander un devis ; immobilier → sélectionner un bien et demander une visite ; restaurant → choisir une offre et préparer une réservation. La maquette montre un parcours, elle n’effectue aucune transaction réelle.

## Lecture des fichiers

`LECTEUR_ANALYSE.html` est un lecteur hors ligne : la vidéo et le WAV restent dans le même dossier. Les boutons des scènes donnent accès aux bons moments du MP4. `PLAN_VISUEL.pdf` contient une page par séquence. `SYNCHRONISATION_AUDIO.png` montre les changements visuels et les attaques audio mesurées. `PROMPT_MAITRE_CLAUDE_CODE.md` est le prompt complet, directement copiable. `TIMELINE_REFERENCE.json` conserve la timeline et les repères détaillés.

Les planches `DETAIL_*.jpg` indiquent des numéros de frames exacts. Les planches `CONTACT_APPROX_*.jpg` sont seulement des aperçus à 2 images/seconde : leurs libellés ne doivent pas servir de mesure fine.
