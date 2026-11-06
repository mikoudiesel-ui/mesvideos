---
format: 1080x1920
duration: "38.20s"
message: "Chaque « demain » te coûte un rêve ; l'ebook « Plus malin que le diable » démasque la petite voix qui te fait attendre."
arc: Hook → Problem → Cost → Diagnosis → Reveal → Benefits → Offer → CTA
audience: "Personnes de 25 à 55 ans qui repoussent un projet, sur Facebook et Instagram (Reels, Stories, fil)"
mode: autonomous
captions: disabled
music: "pre-mixed with voice and SFX in assets/audio/mix.wav (mounted at root by the orchestrator)"
direction: "V2 neuromarketing : même monde que la V1 (../plus-malin-que-le-diable), rythme plus rapide, code couleur du guide (douleur rouge, bénéfice vert, bouton vert texte blanc)"
styleframes: "../plus-malin-que-le-diable/styleframes/png/A1.png, A3.png"
patterns: ../patterns/STORYBOARD-CRAFT.md, ../patterns/PATTERNS.md
---

## Video direction

- **One world** (frame.md, reference/planner.html): the night desk with the paper planner, the post-it « Commencer », the horned shadow; then the gold light behind the torn page. Frames 1-4 = PROBLEM (night), frame 5 = REVEAL (tear to gold), frames 6-7 = SOLUTION and CTA (gold world). Each frame paints its own full-bleed ground as a `class="clip"` layer.
- **Seams**: a viral ad cuts fast. Seams are hard cuts on a camera whip (8 px blur on both sides) unless a handoff says otherwise; no element is born or dies in the 2 images around a seam.
- **Text** (readable without sound): every sentence is a subtitle centred in the band y 1330 to 1470, word by word on the cues. ONE key word per sentence in a box. Colour code of the neuromarketing guide: **pains in a red box** (#e2372b, white text), **benefits in a green box** (#22b573, white text), the brand name gets the gold peak stroke. Nothing else in the band, nothing below y 1500 except the CTA arrow of frame 7.
- **Motion grammar**: elements arrive too big and blurred then settle (expo.out), an event every 0.3 to 0.6 s (faster than the V1), the camera drifts and never stops; no bounce.
- **Visible copy**: exactly the quoted copy of the Scene lines, nothing else. French typography (’, « », non-breaking spaces before : ? !).
- **Negative list**: fake testimonial, fake scarcity, invented number, horror imagery, giant word (except the day names, the counter and the hook post-it), slideshow, hesitating cursor.

**VOIX** : timings in onsets.json (frame-local cues below).

**SON** (global times) : impact-bass-1 0.10 · pop 0.45 · whoosh-short 2.52 · pop 3.00 · whoosh-short 4.70 · whoosh-short 7.32 · key-press 7.90 to 8.80 · whoosh 9.38 · whoosh-cinematic 13.60 · impact-bass-2 13.70 · sparkle 15.80 · pop 18.60 · pop 19.80 · pop 22.00 · whoosh-short 22.88 · click 24.70 · ping 25.10

## Frame 1: Awa, l'accroche · 0.00 → 2.52

- scene: Hook with the presenter: the photo of Awa on her sofa holding the tablet (AI image, assets/img/awa-photo.webp), the camera punches in on her face; a red post-it « Demain » slams onto the wall at the top right; « rêve » in a red box; small tag « Image IA »
- duration: 2.52s
- transition_in: cut
- status: outline
- src: compositions/frames/01-awa-accroche.html
- voiceover: "Chaque « demain » te coûte un rêve."
- type: hook
- blueprint: kinetic-type-beats (Adapt)
- focal: Awa's face, then the post-it « Demain »
- rules: motion-blur-streak
- world: dark
- handoff_in: aucun (ouverture du film) ; première image = la photo d'Awa plein cadre (cover 1080x1920), légèrement zoomée sur son visage, le tag « Image IA » en haut à gauche
- handoff_out: à 2.52 : aucun raccord de caméra (coupe franche voulue) ; whip down in progress, blur 8 px on the whole frame ; the post-it « Demain » still on the wall

Word cues: Chaque@0.32 demain@0.71 te@1.28 coûte@1.45 un@1.75 rêve@1.91

Scene 1 (0.00 à 2.52 s) : P1, Awa et le post-it
  TEXTE ÉCRAN : subtitle « Chaque « demain » te coûte un rêve. » word by word, [boîte : rêve] red at 1.89 ; the post-it reads « Demain » (Fraunces 600, 72 px) with a « ☐ » square under it ; tag « Image IA » (Instrument Sans 500, 24 px, #f1e8d8 on rgba(0,0,0,.45), radius 24, padding 8 18) at left 40, top 60, on screen the whole frame
  IMAGE DE DÉPART : handoff_in.
  ÉTAPES : 0.00 the photo fills the frame (object-fit cover, focus on her face) with a warm grade ; 0.00 à 0.30 a fast punch-in toward her face (scale 1.10 → 1.22, power3.out) ; 0.40 the red-tinted post-it « Demain » (reference post-it, 0.9× size) slams onto the wall at the top right (centre about x 800, y 330), too big and blurred (scale 2.6 → 1, blur 18 → 0, rotate 14 → 6 deg, 0.25 s expo.out) and the whole frame shakes once (x ±10 px, 3 steps, 0.15 s) ; 0.71 the word « Demain » pulses red once ; 1.28 a red crack draws across the post-it ; 1.89 red box on « rêve. » ; 2.35 subtitle leaves ; 2.38 whip down, blur 0 → 8 px
  PISTE CAMÉRA : after the punch-in a slow drift scale 1.22 → 1.26 ; 2.38 à 2.52 whip down y 0 → -200, blur 8 px
  COUCHES ET PROFONDEUR : the photo with a soft vignette ; the post-it on the wall ; the subtitle band over her dark trousers (add a soft dark gradient under the band for legibility)
  OBJET-PONT ET VECTEUR : vector down
  SON : impact-bass-1 at 0.40 ; pop at 0.65
  IMAGE CLÉ : 2.00 : Awa smiling, the cracked post-it « Demain » on the wall, « rêve » in the red box

## Frame 2: La semaine · 2.52 → 7.32

- scene: The planner page « Lundi »: the post-it « Commencer » lands; the page flips to « Dimanche », the post-it is still there, unchecked; the lamp dims
- duration: 4.80s
- transition_in: cut
- status: outline
- src: compositions/frames/02-semaine.html
- voiceover: "Lundi, tu te promets de commencer. Dimanche... rien n'a bougé."
- type: pain_point
- blueprint: spatial-pan-stations (Adapt)
- focal: post-it « Commencer »
- rules: motion-blur-streak
- world: dark
- handoff_in: aucun raccord de caméra (coupe franche voulue) ; whip down landing, blur 8 px → 0 in 0.2 s ; page « Lundi » / « 3 NOVEMBRE » (reference page) in place
- handoff_out: à 4.80 : aucun raccord de caméra (coupe franche voulue) ; push in toward the post-it in progress, blur 8 px ; page « Dimanche » with the post-it unchecked ; lamp at 70 %

Word cues: Lundi@0.32 tu@0.91 te@1.04 promets@1.18 de@1.42 commencer@1.55 Dimanche@2.65 rien@3.77 n'a@3.92 bougé@4.06

Scene 1 (0.00 à 2.40 s) : P1, la promesse du lundi
  TEXTE ÉCRAN : subtitle « Lundi, tu te promets de commencer. » word by word, [boîte : commencer] RED at 1.53
  IMAGE DE DÉPART : handoff_in.
  ÉTAPES : 0.00 land from the whip (0.2 s) ; 0.32 « Lundi, » ; 0.45 the post-it « Commencer » (reference) slams in from the camera (scale 1.8 → 1, blur 14 → 0, 0.3 s expo.out) at (470, 700) ; 0.90 its shadow tightens ; 1.53 red box ; 1.90 the checkbox pulses ; 2.15 subtitle leaves ; 2.20 page « Lundi » flips up fast (rotateX 0 → -100, 0.25 s power3.in) revealing « Mercredi » then at 2.40 « Mercredi » flips too (0.15 s) revealing « Dimanche » / « 9 NOVEMBRE » ; the post-it rides each page and re-appears on « Dimanche » at (470, 600)
  PISTE CAMÉRA : drift scale 1.00 → 1.08 ; slight shake on each flip
  COUCHES ET PROFONDEUR : pencil foreground ; page ; desk
  OBJET-PONT ET VECTEUR : the post-it survives the flips
  SON : pop at 0.45 ; whoosh-short at 2.20
  IMAGE CLÉ : 1.70 : post-it « Commencer » on « Lundi », red box on « commencer. »

Scene 2 (2.40 à 4.80 s) : P2, dimanche, rien
  TEXTE ÉCRAN : subtitle « Dimanche… rien n’a bougé. » word by word, [boîte : rien] red at 3.75 ; « 23:12 » in small date style in the page header from 3.00
  IMAGE DE DÉPART : Scene 1 end.
  ÉTAPES : 2.65 « Dimanche… » ; 3.00 the lamp dims to 70 % (0.5 s) ; 3.75 red box ; 4.20 a speck of dust crosses the empty page ; 4.55 subtitle leaves ; 4.60 push in toward the post-it, blur 0 → 8 px
  PISTE CAMÉRA : drift scale 1.08 → 1.12 ; 4.60 à 4.80 push in scale 1.25
  COUCHES ET PROFONDEUR : same
  OBJET-PONT ET VECTEUR : vector forward
  SON : whoosh-short at 4.60
  IMAGE CLÉ : 4.20 : the empty Sunday page, the post-it still unchecked, red box on « rien »

## Frame 3: Le coût · 7.32 → 9.38

- scene: Loss aversion: a big red counter « semaines perdues » rolls 1 → 52 over the dimmed planner
- duration: 2.06s
- transition_in: cut
- status: outline
- src: compositions/frames/03-cout.html
- voiceover: "Encore une semaine perdue."
- type: pain_point
- blueprint: kinetic-type-beats (Adapt)
- focal: the counter
- rules: counting-dynamic-scale
- world: dark
- handoff_in: aucun raccord de caméra (coupe franche voulue) ; push in landing, blur 8 → 0 in 0.2 s ; page « Dimanche » dimmed behind (blur 6 px, opacity .5)
- handoff_out: à 2.06 : aucun raccord de caméra (coupe franche voulue) ; whip right in progress, blur 8 px ; counter on « 52 »

Word cues: Encore@0.49 une@0.78 semaine@0.98 perdue@1.27

Scene 1 (0.00 à 2.06 s) : P1, le compteur
  TEXTE ÉCRAN : subtitle « Encore une semaine perdue. » word by word, [boîte : perdue] red at 1.25 ; counter: a number in Instrument Sans 700, 300 px, colour #e2372b, centred at y 620, with the label « semaines perdues » (Instrument Sans 500, 44 px, ink) under it at y 820
  IMAGE DE DÉPART : handoff_in.
  ÉTAPES : 0.10 the counter rushes in from the camera on « 1 » (scale 2 → 1, blur 12 → 0, 0.25 s) ; 0.30 label appears ; 0.40 à 1.60 the number rolls 1 → 52 (tabular digits, accelerating: power2.in, each change a hard value step; it grows from scale 1 to 1.12 with the value) ; 1.25 red box ; 1.60 « 52 » lands with a small shake (x ±6, 0.12 s) ; 1.85 subtitle leaves ; 1.90 whip right, blur 8 px
  PISTE CAMÉRA : drift scale 1.00 → 1.04
  COUCHES ET PROFONDEUR : dimmed page background ; counter sharp
  OBJET-PONT ET VECTEUR : vector right
  SON : key-press ticks while rolling ; pop at 1.60
  IMAGE CLÉ : 1.65 : « 52 semaines perdues » in red over the dark planner

## Frame 4: La petite voix · 9.38 → 13.57

- scene: The horned shadow rises behind the planner page; red eyes open on « petite voix »
- duration: 4.19s
- transition_in: cut
- status: outline
- src: compositions/frames/04-petite-voix.html
- voiceover: "Ce n'est pas un manque de talent, c'est une petite voix."
- type: pain_point
- blueprint: zoom-out-workspace-reveal (Adapt)
- focal: the horned shadow
- rules: depth-of-field-blur
- world: dark
- handoff_in: aucun raccord de caméra (coupe franche voulue) ; whip landing from the left, blur 8 → 0 in 0.2 s ; page « Dimanche » with the post-it unchecked, lamp at 70 %
- handoff_out: à 4.19 : aucun raccord de caméra (coupe franche voulue) ; the lamp goes off, the frame is near black, only the two red eyes glow

Word cues: Ce@0.58 n'est@0.72 pas@0.85 un@0.99 manque@1.13 de@1.37 talent@1.51 c'est@2.56 une@2.72 petite@3.15 voix@3.60

Scene 1 (0.00 à 4.19 s) : P1, l'ombre
  TEXTE ÉCRAN : subtitle « Ce n’est pas un manque de talent, » [boîte : talent] GREEN (#22b573, white text) at 1.49 — the reader's talent is a benefit ; then « c’est une petite voix. » [boîte : petite voix] RED at 3.13
  IMAGE DE DÉPART : handoff_in.
  ÉTAPES : 0.58 words ; 1.00 the post-it gets a soft gold rim ; 1.49 green box ; 2.30 chunk swap ; 2.40 the horned shadow (reference) rises from the bottom right of the page (y +400 → 0, scale .7 → 1, 0.5 s power3.out) ; 3.13 red box ; 3.60 two red eyes open (scaleY 0 → 1, 0.12 s) ; 3.80 subtitle leaves ; 3.90 the lamp goes off (0.2 s), only the eyes glow
  PISTE CAMÉRA : drift scale 1.05 → 1.10 ; 2.40 à 3.30 pull back slightly to show the shadow whole
  COUCHES ET PROFONDEUR : pencil foreground ; page ; shadow ; desk
  OBJET-PONT ET VECTEUR : the eyes → black
  SON : whoosh (low) at 2.40
  IMAGE CLÉ : 3.65 : the shadow over the page with red eyes, « petite voix » in the red box

## Frame 5: Awa, la révélation · 13.57 → 17.38

- scene: Black, a gold crack tears the frame open onto Awa holding the tablet; the tablet screen now shows the cover of « Plus malin que le diable »; the camera pushes into the tablet until the cover fills the frame exactly where frame 6 starts
- duration: 3.81s
- transition_in: cut
- status: outline
- src: compositions/frames/05-awa-revelation.html
- voiceover: "Et ce livre la démasque : Plus malin que le diable."
- type: turn
- blueprint: camera-journey (Adapt)
- focal: the tablet with the cover
- rules: depth-of-field-blur
- world: light
- handoff_in: aucun raccord de caméra (coupe franche voulue) ; near black, two red eyes fading
- handoff_out: à 3.81 : the cover at left 260, top 360, 560×800, rotate -3deg, sharp, on the gold ground (pm-gold + pm-gold-halo) : the tablet and Awa have left the frame by a push-in that ends in a quick crossfade (0.25 s) from the tablet screen to this cover ; no subtitle

Word cues: Et@0.41 ce@0.57 livre@0.74 la@1.03 démasque@1.19 Plus@2.22 malin@2.42 que@2.77 le@2.97 diable@3.17

Scene 1 (0.00 à 3.81 s) : P1, la tablette
  TEXTE ÉCRAN : subtitle « Et ce livre la démasque : » [boîte : démasque] GREEN at 1.17 ; then « Plus malin que le diable. » [trait : malin] gold at 2.42 ; tag « Image IA » top left while Awa is on screen
  IMAGE DE DÉPART : handoff_in.
  ÉTAPES : 0.00 the red eyes fade ; 0.25 a vertical gold crack draws at x 540 ; 0.60 the black tears open in two halves sliding apart (x ∓560, 0.5 s power3.out) onto the photo of Awa with a warm gold grade and a gold glow around the tablet ; the tablet screen shows the reference cover (.pm-cover) mapped onto the screen quad with a CSS matrix3d (the original screen corners in the 941×1672 photo are about TL (497, 588), TR (831, 592), BR (826, 1118), BL (470, 1110): check them on the image and adjust), with a soft screen glare ; 1.17 green box ; 1.40 à 3.30 the camera pushes into the tablet (power2.inOut) ; 1.90 chunk swap ; 2.42 gold stroke under « malin » ; 2.80 a gold sweep crosses the cover on the screen ; 3.30 à 3.55 the push ends with the cover on the tablet near left 260, top 360, 560×800 and crossfades to the flat reference cover on the gold ground exactly at that position ; 3.60 subtitle leaves
  PISTE CAMÉRA : 0.60 à 1.10 push through the tear (scale 1.15 → 1.00) ; 1.40 à 3.30 push into the tablet
  COUCHES ET PROFONDEUR : torn halves foreground ; Awa photo ; tablet sharp ; gold glow
  OBJET-PONT ET VECTEUR : the cover → frame 6
  SON : whoosh-cinematic at 0.03 ; impact-bass-2 at 0.13 ; sparkle at 2.23
  IMAGE CLÉ : 2.60 : Awa holding the tablet showing « Plus malin que le diable », « malin » underlined in gold

## Frame 6: Les bénéfices · 17.38 → 22.88

- scene: The cover moves up; three green-ticked benefit lines fall in under it, one per phrase
- duration: 5.50s
- transition_in: cut
- status: outline
- src: compositions/frames/06-benefices.html
- voiceover: "Tu vas reconnaître ses ruses, lui répondre, et passer enfin à l'action."
- type: benefits
- blueprint: kinetic-type-beats (Adapt)
- focal: the benefit list
- rules: waterfall-entry
- world: light
- handoff_in: à 0.00 : the cover centred at left 260, top 360, rotate -3deg, sharp, on the gold ground (pm-gold + pm-gold-halo) ; camera slow drift ; no subtitle
- handoff_out: à 5.50 : the cover scaled .62 at the top (centred, top 120) ; the three ticked benefit lines under it ; no subtitle ; camera drift

Word cues: Tu@0.29 vas@0.43 reconnaître@0.57 ses@1.04 ruses@1.18 lui@2.00 répondre@2.12 et@3.20 passer@3.44 enfin@3.88 à@4.31 l'action@4.56

Scene 1 (0.00 à 5.50 s) : P1, trois coches
  TEXTE ÉCRAN : subtitle « Tu vas reconnaître ses ruses, » [boîte : ruses] GREEN at 1.16 ; « lui répondre, » [boîte : répondre] GREEN at 2.10 ; « et passer enfin à l’action. » [boîte : l’action] GREEN at 4.54 ; each chunk replaces the previous. Benefit lines (Instrument Sans 700, 54 px, ink #f1e8d8, each with a green round tick ✓ 64 px #22b573 on the left), stacked at x 140, y 860 / 990 / 1120: « Reconnaître ses ruses », « Lui répondre », « Passer à l’action »
  IMAGE DE DÉPART : handoff_in.
  ÉTAPES : 0.10 the cover moves up and scales to .62 (0.5 s power3.inOut) ; 0.57 line 1 falls in (y -40 → 0, blur 8 → 0, 0.3 s expo.out) and its tick pops (scale 0 → 1, 0.2 s) at 1.18 ; 2.00 line 2 falls in, tick at 2.12 ; 3.44 line 3 falls in, tick at 4.56 ; 4.80 the three ticks pulse green once together ; 5.30 subtitle leaves
  PISTE CAMÉRA : drift scale 1.00 → 1.03 linear
  COUCHES ET PROFONDEUR : gold halo ; cover ; list
  OBJET-PONT ET VECTEUR : the list → the CTA
  SON : pop at 1.18, 2.12, 4.56
  IMAGE CLÉ : 4.90 : the cover on top, three green-ticked benefits under it

## Frame 7: L'offre · 22.88 → 31.08

- scene: The offer, colour-coded like the neuromarketing guide: the benefit lines slide out; a gold BONUS card, a blue guarantee badge and the gold price « 990 F » fall in one by one under the cover
- duration: 8.20s
- transition_in: cut
- status: outline
- src: compositions/frames/06b-offre.html
- voiceover: "En bonus : Réfléchissez et devenez riche. Satisfait ou remboursé. Et tout ça pour seulement neuf cent quatre-vingt-dix francs."
- type: offer
- blueprint: kinetic-type-beats (Adapt)
- focal: the offer rows
- rules: counting-dynamic-scale
- world: light
- handoff_in: à 0.00 : the cover scaled .62 at the top (centred, top 120) ; the three ticked benefit lines under it ; no subtitle ; camera drift
- handoff_out: à 8.20 : three offer rows at x 140 (cover .62 at the top, centred, top 120): row 1 at y 860 = a gold pill « BONUS » (Instrument Sans 700, 30 px, #1b1612 on #f4b53f, radius 30, padding 8 22) followed by « Réfléchissez et devenez riche » (Instrument Sans 700, 44 px, #f4b53f) ; row 2 at y 990 = a blue shield icon 64 px (#3b82f6, white check inside) followed by « Satisfait ou remboursé » (Instrument Sans 700, 54 px, #f1e8d8) ; row 3 at y 1100 = « 990 F » (Fraunces 900, 120 px, #f4b53f, gold glow) ; no subtitle ; camera drift

Word cues: En@0.26 bonus@0.47 Réfléchissez@1.30 et@1.86 devenez@2.02 riche@2.45 Satisfait@3.72 ou@4.25 remboursé@4.47 Et@5.82 tout@6.08 ça@6.33 pour@6.59 seulement@6.84 990@7.49 F@7.74

Scene 1 (0.00 à 8.20 s) : P1, bonus, garantie, prix
  TEXTE ÉCRAN : subtitle « En bonus : Réfléchissez et devenez riche. » [boîte : bonus] GOLD (.pm-box.gold, dark text) at 0.45 ; then « Satisfait ou remboursé. » [boîte : remboursé] BLUE (#3b82f6, white text) at 4.45 ; then « Et tout ça pour seulement 990 F. » [boîte : 990 F] GOLD at 7.47 ; each chunk replaces the previous ; the three rows as in handoff_out
  IMAGE DE DÉPART : handoff_in.
  ÉTAPES : 0.10 the benefit lines slide out to the left fast (x -900, 0.3 s power3.in) ; 0.40 row 1 « BONUS » pill pops (scale 0 → 1, 0.2 s) and at 1.28 its title rushes in from the camera (scale 1.6 → 1, blur 10 → 0, 0.35 s expo.out) with a gold sparkle burst (finite) ; 2.60 a gold sheen sweeps across row 1 ; 3.40 chunk swap ; 3.70 row 2 falls in (y -40 → 0, blur 8 → 0, 0.3 s), its shield pops at 4.47 and pulses blue once ; 5.60 chunk swap ; 5.80 row 3 « 990 F » rushes in from the camera (scale 2 → 1, blur 14 → 0, 0.3 s expo.out) and lands with a small shake at 7.49, its gold glow swells once ; 7.95 subtitle leaves
  PISTE CAMÉRA : drift scale 1.00 → 1.03 linear, compensated like frame 6 so the last image lands on handoff_out numbers
  COUCHES ET PROFONDEUR : gold halo ; cover ; rows
  OBJET-PONT ET VECTEUR : the rows → the CTA
  SON : sparkle at 0.32 ; pop at 1.32 ; chime at 3.74 ; pop at 5.84 ; impact-bass-1 at 7.22
  IMAGE CLÉ : 7.80 : the cover on top, BONUS card, blue guarantee and « 990 F » in gold under it

## Frame 8: L'appel à l'action · 31.08 → 38.20

- scene: End card: the cover, the green button « Oui, je le veux maintenant » (white text); a cursor clicks it; the post-it « Commencer » lands on the cover and gets ticked; an arrow points down to the ad's link
- duration: 7.12s
- transition_in: cut
- status: outline
- src: compositions/frames/07-fin.html
- voiceover: "Clique sur « Je le veux ». Ta prochaine semaine commence maintenant."
- type: cta
- blueprint: cta-morph-press (Adapt)
- focal: the green button
- rules: cursor-click-ripple
- world: light
- handoff_in: à 0.00 : three offer rows at x 140 (cover .62 at the top, centred, top 120): row 1 at y 860 = a gold pill « BONUS » (Instrument Sans 700, 30 px, #1b1612 on #f4b53f, radius 30, padding 8 22) followed by « Réfléchissez et devenez riche » (Instrument Sans 700, 44 px, #f4b53f) ; row 2 at y 990 = a blue shield icon 64 px (#3b82f6, white check inside) followed by « Satisfait ou remboursé » (Instrument Sans 700, 54 px, #f1e8d8) ; row 3 at y 1100 = « 990 F » (Fraunces 900, 120 px, #f4b53f, gold glow) ; no subtitle ; camera drift
- handoff_out: à 7.12 : end of film ; cover, ticked post-it, green button, arrow ; living hold

Word cues: Clique@0.52 sur@0.83 Je@1.00 le@1.17 veux@1.35 Ta@2.30 prochaine@2.46 semaine@2.85 commence@3.25 maintenant@3.64

Scene 1 (0.00 à 7.12 s) : P1, le clic
  TEXTE ÉCRAN : subtitle « Clique sur « Je le veux ». » [boîte : Je le veux] GREEN at 0.98 ; then « Ta prochaine semaine commence maintenant. » [trait : maintenant] gold at 3.64 ; button copy « Oui, je le veux maintenant » (the reference .pm-cta restyled: background #22b573, text #ffffff, glow rgba(34,181,115,.45)) at left 110, top 1150
  IMAGE DE DÉPART : handoff_in.
  ÉTAPES : 0.10 the three offer rows slide out left fast (0.25 s) ; 0.20 the cover returns to scale 1 at left 260, top 260 (0.5 s power3.inOut) ; 0.50 the green button rises from below (y +200 → 0, blur 8 → 0, 0.4 s expo.out) ; 0.98 green box ; 1.20 the cursor arrives from the right in one curved move (0.45 s power3.out) and clicks the button at 1.80 (press .96 + white ripple) ; 2.20 the post-it « Commencer » (scale .6) flies onto the cover's top-right corner ; 2.60 its tick draws (stroke-dashoffset 60 → 0, 0.3 s) ; 3.64 gold stroke under « maintenant » ; 4.30 a green arrow ↓ draws under the subtitle (y 1480 to 1600, x 540) ; 4.50 à 7.12 living hold: halo breathes once, dust in the light, the arrow nudges down twice (finite)
  PISTE CAMÉRA : drift scale 1.00 → 1.03 linear, never stops
  COUCHES ET PROFONDEUR : halo ; cover ; post-it ; button ; cursor
  OBJET-PONT ET VECTEUR : end
  SON : click at 1.80 ; ping at 2.60
  IMAGE CLÉ : 1.82 : the cursor clicking the green button under the cover
