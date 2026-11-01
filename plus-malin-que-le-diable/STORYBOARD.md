---
format: 1080x1920
duration: "38.50s"
message: "La procrastination est une petite voix qui te fait attendre ; l'ebook « Plus malin que le diable » démasque ses ruses et te donne de quoi lui répondre."
arc: Hook → Problem → Pivot → Turn → Payoff → CTA
audience: "Personnes de 25 à 55 ans qui repoussent un projet personnel ou professionnel, sur Facebook et Instagram (Reels, Stories, fil)"
mode: autonomous
captions: disabled
music: "pre-mixed with voice and SFX in assets/audio/mix.wav (mounted at root by the orchestrator)"
direction: "Mélange : A « Le calendrier de la nuit » (le monde), C « Le téléphone » (le gag et les excuses en notifications), B « Le théâtre d'ombres » (l'ombre aux yeux rouges qui rétrécit à la révélation)"
styleframes: "styleframes/png/A1.png (1.8 s), styleframes/png/C2.png (17.3 s), styleframes/png/A3.png (26.6 s)"
patterns: ../patterns/STORYBOARD-CRAFT.md, ../patterns/PATTERNS.md
---

## Video direction

- **One world** (frame.md): the night desk with the paper planner, the phone lying on it, the horned shadow cast on the page. Frames 1-6 = PROBLEM on the night desk; frame 7 = PIVOT on black; frames 8-10 = SOLUTION in gold light behind the torn page, end card included. Each frame paints its own full-bleed ground as a `class="clip"` layer.
- **Invisible seams**: every frame enters with `cut`; each seam falls at the top of the blur of a camera move and the `handoff_out` of frame N is copied word for word into the `handoff_in` of frame N+1. Wanted exceptions: 22.05 (cut to black for the pivot) and 25.41 (the black tears open on gold).
- **Text** (readable without sound): every sentence of the voice is a `subtitle` centred in the band y 1330 to 1470 (nothing else in it, nothing below y 1500) that arrives WORD BY WORD on the timestamps given in each frame (`word@seconds`, frame-local). Exactly ONE word or group per sentence sits in the `key-word-box` (red before the pivot, gold after), named [boîte : …]. Typographic moment: the pivot line only (frame 7).
- **Peaks**: 3 peaks [trait : …]: « malin » (frame 8), « répondre » (frame 9), « dessous » is NOT one; the third is « talent » (frame 5). Gold tapered stroke under THE word.
- **One thing to look at**: the camera isolates the subject of the sentence; a clear zoom in one direction, never a back-and-forth; no decor without meaning, no line crossing a sentence.
- **Real interfaces**: a generic modern phone lock screen (alarm card, notifications); no brand logo. The ebook cover is a placeholder until the real one arrives.
- **Motion grammar**: two speeds, gestures of 1 to 6 images (expo.out) and linear drifts that never stop; elements arrive too big and blurred then settle; no frozen hold; no "effect" transition.
- **Visible copy**: exactly the quoted copy of the Scene lines, nothing else.
- **Negative list**: slideshow, screensaver, doubled object, colored text instead of the box, giant word (except day names and the pivot), horror imagery, fake proof, hesitating cursor, several objects moving during a seam.

**MONDE**
- Acte 1 (0.00 à 22.05) : le bureau de nuit ; stations Lundi (page 1), Mercredi (page 2), Dimanche (page 3), le téléphone posé sur la page (x 540, y 760), l'ombre à droite de la page ; fond canvas + halo de lampe froide + grain
- Acte 2 (22.05 à 25.41) : noir pur, la phrase de bascule
- Acte 3 (25.41 à 38.50) : la lumière dorée derrière la page déchirée ; stations la couverture (540, 820), la liste des ruses, le bouton (540, 1180)
- Couleurs de rôle : rouge diable = la petite voix (boîte, cornes, yeux, ratures) ; or = la solution (lumière, traits, bouton, boîte après la bascule)

**SIGNATURES**
- Mécanisme 1 « le post-it qui glisse » : 0.60, 4.20, 7.00, 33.10 (il revient et se coche)
- Mécanisme 2 « l'ombre qui grandit » : 14.95, 16.90, 18.60, 19.95, puis elle rétrécit à 26.30
- Registres de texte : subtitle word by word (blur 6 → 0, y 8 → 0, 0.14 s) ; key-word box (scaleX from the left 0.16 s) ; peak stroke (draw 0.35 s) ; typographic moment (letters converge 0.5 s)
- Rimes : le lundi du début revient à la fin, la case « Commencer » cochée (33.10 répond à 0.60)

**PARTITION CAMÉRA** (global times) : 0.00 drift in 1 %/s cam-page · 0.55 push to cam-postit · 3.10 whip down (page turn) · 6.20 whip down (page turn) · 9.60 tilt to cam-phone · 12.30 pull back + pan right to cam-shadow · 16.20 push in on the phone (notifications) · 21.90 cut to black · 25.41 tear opens, push through · 30.90 pull back to cover + post-it · 34.40 settle to end card framing

**VOIX** : timings in onsets.json ; silences over 0.4 s, each written as a shot with its silent action : 1.00 à 1.50 (le post-it se colle) · 2.65 à 3.90 (la page se tourne) · 4.60 à 5.20 (le post-it glisse) · 5.85 à 6.90 (la page se tourne) · 9.40 à 12.70 (gag : l'alarme répétée) · 15.80 à 16.85 (l'ombre se retourne vers le téléphone) · 21.40 à 22.70 (le téléphone s'éteint) · 24.60 à 26.20 (silence noir, puis la déchirure) · 30.75 à 31.55 (les ruses barrées) · 35.70 à 38.50 (fin vivante)

**COUPES** (quota of the voice) : 22.05 · « Et » · bascule sur noir ; 25.41 · « Plus » · le noir se déchire sur l'or

**RYTHME** : douleur 9 plans / 10 s dans l'accroche, 5 plans / 10 s ensuite ; solution 4 plans / 10 s

**SON** (global times, on the gestures) : pop 0.60 · whoosh-short 3.10 · whoosh-short 6.20 · pop 7.00 · notification (signature) 10.40 · click 11.10 · whoosh 12.30 · pop 16.90 · pop 18.60 · pop 19.95 · whoosh 22.05 · whoosh 25.45 · pop 29.40 · pop 30.20 · ping 33.10 · click 36.20

## Frame 1: Lundi · 0.00 → 3.30

- scene: The planner page « Lundi » under the cold lamp; the post-it « Commencer » slams in from the camera and sticks
- duration: 3.30s
- transition_in: cut
- status: outline
- src: compositions/frames/01-lundi.html
- voiceover: "Lundi, tu te promets de commencer."
- type: hook
- blueprint: spatial-pan-stations (Adapt)
- focal: post-it « Commencer »
- rules: depth-of-field-blur, motion-blur-streak
- world: dark
- handoff_in: aucun (ouverture du film) ; première image = la page « Lundi » déjà en place, plein cadre, lumière de lampe froide, rien d'autre
- handoff_out: à 3.30 : cam(0, -260, 1.35, 0, 0) blur 8 px ; whip down in progress (fast, power3.in) ; page « Lundi » flipping up around its top rings at rotateX -70deg revealing page « Mercredi » under it ; post-it « Commencer » on page 1 flipping away with it ; lamp cold ; no text ; grain 16 %

Word cues: Lundi@0.49 tu@1.51 te@1.66 promets@1.81 de@2.08 commencer@2.23

Scene 1 (0.00 à 1.40 s) : P1, la page « Lundi » et le post-it qui arrive
  TEXTE ÉCRAN : subtitle « Lundi, » at 0.49 ; écart synchro
  IMAGE DE DÉPART : handoff_in.
  ÉTAPES : 0.00 page in place, day « Lundi » sharp ; 0.20 the lamp halo flickers once (opacity .8 → 1, 0.1 s) ; 0.49 « Lundi, » ; 0.60 post-it « Commencer » enters from the camera scale 1.8 → 1, blur 14 → 0, rotate 12 → 5 deg, 0.4 s expo.out, lands at (470, 700) ; 1.00 its shadow tightens ; 1.20 the pencil in the foreground rolls 20 px
  PISTE CAMÉRA : drift scale 1.00 → 1.02 linear ; 0.55 à 1.20 push to cam-postit (scale 1.02 → 1.25) power3.out
  COUCHES ET PROFONDEUR : blurred pencil bottom-left cut by the edge ; sharp page and post-it ; desk softly blurred
  OBJET-PONT ET VECTEUR : the post-it → the task we watch for the whole act
  SON : pop at 0.60
  IMAGE CLÉ : 0.80 : the post-it still big and blurred, landing on « Lundi » (styleframe A1)

Scene 2 (1.40 à 3.30 s) : P2, la promesse
  TEXTE ÉCRAN : subtitle « Lundi, tu te promets de commencer. » word by word from 1.51, [boîte : commencer] at 2.21 ; écart synchro
  IMAGE DE DÉPART : cam-postit.
  ÉTAPES : 1.51 words arrive ; 1.90 the checkbox « ☐ » of the post-it pulses once (scale 1 → 1.15 → 1, 0.3 s) ; 2.21 box on « commencer » ; 2.70 subtitle leaves (blur 6, 0.14 s) ; 2.90 page starts to flip (rotateX 0 → -70deg, 0.4 s power3.in)
  PISTE CAMÉRA : drift scale 1.25 → 1.30 ; 3.00 à 3.30 whip down y 0 → -260, scale 1.35, blur 0 → 8 px
  COUCHES ET PROFONDEUR : same
  OBJET-PONT ET VECTEUR : vector down, the page flips upward
  SON : whoosh-short at 3.10
  IMAGE CLÉ : 2.30 : post-it « Commencer » sharp, subtitle with the red box on « commencer. »

## Frame 2: Mercredi · 3.30 → 6.37

- scene: Page « Mercredi »: the post-it « Commencer » slides off the day and lands on Thursday's corner, pushed by an invisible finger
- duration: 3.07s
- transition_in: cut
- status: outline
- src: compositions/frames/02-mercredi.html
- voiceover: "Mercredi, tu repousses."
- type: pain_point
- blueprint: spatial-pan-stations (Adapt)
- focal: post-it « Commencer »
- rules: motion-blur-streak
- world: dark
- handoff_in: à 0.00 : cam(0, -260, 1.35, 0, 0) blur 8 px ; whip down in progress (fast, power3.in) ; page « Lundi » flipping up around its top rings at rotateX -70deg revealing page « Mercredi » under it ; post-it « Commencer » on page 1 flipping away with it ; lamp cold ; no text ; grain 16 %
- handoff_out: à 3.07 : cam(0, -260, 1.35, 0, 0) blur 8 px ; whip down in progress (fast, power3.in) ; page « Mercredi » flipping up at rotateX -70deg revealing page « Dimanche » under it ; post-it « Commencer » stuck at the bottom-right corner of page « Mercredi », flipping away with it ; lamp cold ; no text ; grain 16 %

Word cues: Mercredi@0.63 tu@1.95 repousses@2.11

Scene 1 (0.00 à 3.07 s) : P1, le post-it repoussé
  TEXTE ÉCRAN : subtitle « Mercredi, tu repousses. » word by word from 0.63, [boîte : repousses] at 2.09 ; écart synchro
  IMAGE DE DÉPART : handoff_in.
  ÉTAPES : 0.00 page 1 finishes flipping out (rotateX -70 → -100, 0.15 s) ; 0.20 cam settles, blur 8 → 0 ; 0.63 « Mercredi, » ; 0.90 the post-it « Commencer » is already on « Mercredi » at (470, 600) ; 1.30 it slides right and down to the page corner (x +260, y +320, rotate 5 → -8 deg, 0.45 s power3.inOut) with a motion blur 6 px ; 1.80 a faint « Jeudi → » mark appears where it lands (Instrument Sans 30 px, ink-mute) ; 2.09 box on « repousses » ; 2.60 subtitle leaves ; 2.70 page flips
  PISTE CAMÉRA : 0.00 à 0.30 land from the whip (y -260 → 0, scale 1.35 → 1.05, power3.out) ; drift pan follows the post-it x +40 px ; 2.80 à 3.07 whip down y 0 → -260, scale 1.35, blur 8 px
  COUCHES ET PROFONDEUR : blurred pencil foreground ; sharp page ; desk
  OBJET-PONT ET VECTEUR : the post-it keeps moving → it will be found on Sunday
  SON : whoosh-short at 0.00 (end of the previous one) ; slide (paper) at 1.30 ; whoosh-short at 2.90
  IMAGE CLÉ : 1.60 : the post-it mid-slide toward the corner, « Mercredi » sharp behind

## Frame 3: Dimanche · 6.37 → 10.20

- scene: Page « Dimanche », late: the post-it lands crumpled on the empty page; the lamp dims; the phone slides into frame on the page
- duration: 3.83s
- transition_in: cut
- status: outline
- src: compositions/frames/03-dimanche.html
- voiceover: "Dimanche soir... rien n'a bougé."
- type: pain_point
- blueprint: spatial-pan-stations (Adapt)
- focal: the empty page and the post-it unchecked
- rules: depth-of-field-blur
- world: dark
- handoff_in: à 0.00 : cam(0, -260, 1.35, 0, 0) blur 8 px ; whip down in progress (fast, power3.in) ; page « Mercredi » flipping up at rotateX -70deg revealing page « Dimanche » under it ; post-it « Commencer » stuck at the bottom-right corner of page « Mercredi », flipping away with it ; lamp cold ; no text ; grain 16 %
- handoff_out: à 3.83 : cam(0, 120, 1.10, 0, 0) blur 6 px ; tilt down toward the phone in progress (power3.inOut) ; page « Dimanche » with the post-it unchecked at (470, 600) ; phone lying on the page at (150, 760) 780×1130 screen black ; lamp at 70 % ; no text ; grain 16 %

Word cues: Dimanche@0.56 soir@1.15 rien@2.31 n'a@2.49 bougé@2.67

Scene 1 (0.00 à 2.20 s) : P1, dimanche soir
  TEXTE ÉCRAN : subtitle « Dimanche soir… » word by word from 0.56 ; écart synchro
  IMAGE DE DÉPART : handoff_in.
  ÉTAPES : 0.00 page 2 finishes flipping out ; 0.20 settle ; 0.56 « Dimanche » ; 0.63 the post-it falls on the page from above (y -200 → 0, rotate -14 → 4, 0.35 s expo.out), its checkbox still empty ; 1.15 « soir… » ; 1.30 the lamp dims (cold halo 100 → 70 %, 0.6 s) ; 1.80 the clock line « 23:12 » in small date style appears on the page header
  PISTE CAMÉRA : land from the whip (0.3 s) ; drift scale 1.05 → 1.08
  COUCHES ET PROFONDEUR : pencil foreground ; page ; desk darker
  OBJET-PONT ET VECTEUR : the empty checkbox → the gag
  SON : paper drop at 0.63
  IMAGE CLÉ : 1.00 : the post-it just landed on the empty Sunday page

Scene 2 (2.20 à 3.83 s) : P2, rien n'a bougé
  TEXTE ÉCRAN : subtitle « rien n'a bougé. » word by word from 2.31, [boîte : rien] at 2.29 ; écart synchro
  IMAGE DE DÉPART : Scene 1 end.
  ÉTAPES : 2.31 words ; 2.29 box on « rien » ; 2.80 the 7 page rules of Sunday stay empty: a tiny dust particle drifts across (the only movement) ; 3.10 subtitle leaves ; 3.20 the phone slides in from the bottom onto the page (y +500 → 0, 0.5 s power3.out), screen black
  PISTE CAMÉRA : 3.40 à 3.83 tilt down toward the phone (y 0 → 120, scale 1.08 → 1.10), blur 0 → 6 px
  COUCHES ET PROFONDEUR : same
  OBJET-PONT ET VECTEUR : the phone → the gag
  SON : soft slide at 3.20
  IMAGE CLÉ : 2.70 : the empty page, the red box on « rien »

## Frame 4: Le gag de l'alarme · 10.20 → 12.50

- scene: Silent gag: Monday 7:00, the alarm « Commencer mon projet » lights the phone; a thumb swipes « Répéter »; a tiny horned reflection smiles in the black glass
- duration: 2.30s
- transition_in: cut
- status: outline
- src: compositions/frames/04-alarme.html
- voiceover: ""
- type: pain_point
- blueprint: device-surface-showcase (Adapt)
- focal: the alarm card
- rules: cursor-click-ripple
- world: dark
- handoff_in: à 0.00 : cam(0, 120, 1.10, 0, 0) blur 6 px ; tilt down toward the phone in progress (power3.inOut) ; page « Dimanche » with the post-it unchecked at (470, 600) ; phone lying on the page at (150, 760) 780×1130 screen black ; lamp at 70 % ; no text ; grain 16 %
- handoff_out: à 2.30 : cam(220, 0, 1.15, 0, 0) blur 8 px ; pull back + pan right in progress (power3.inOut) ; phone screen back to black with a faint red horned reflection fading ; page « Dimanche » visible on the right half ; lamp at 70 % ; no text ; grain 16 %

Word cues: none (silent gag)

Scene 1 (0.00 à 2.30 s) : P1, l'alarme répétée
  TEXTE ÉCRAN : aucun texte sauf l'interface (« lundi 3 novembre », « 7:00 », « Alarme », « Commencer mon projet », « Répéter », « Arrêter »)
  IMAGE DE DÉPART : handoff_in.
  ÉTAPES : 0.00 settle ; 0.20 the screen lights up (lock screen, « lundi 3 novembre », « 7:00 ») ; 0.25 the alarm card drops in too big and blurred (scale 1.18 → 1, blur 5 → 0, 0.35 s) ; 0.40 the phone vibrates (x ±6 px, 6 steps over 0.6 s) ; 0.80 « Répéter » and « Arrêter » pills appear ; 0.90 a thumb shape (soft dark round) comes from the bottom in one move and presses « Répéter » (ripple) ; 1.30 the screen goes black ; 1.40 in the black glass a small horned silhouette with a smile appears (opacity 0 → .5, 0.3 s) ; 1.90 it fades
  PISTE CAMÉRA : settle on cam-phone (0.3 s) ; drift scale 1.10 → 1.12 ; 2.00 à 2.30 pull back + pan right (x 0 → 220, scale 1.15), blur 8 px
  COUCHES ET PROFONDEUR : phone sharp ; page around it ; lamp
  OBJET-PONT ET VECTEUR : the horned reflection → becomes the shadow on the page
  SON : notification (signature, two-tone) at 0.40 ; click at 0.95
  IMAGE CLÉ : 0.95 : the thumb pressing « Répéter » on « Commencer mon projet »

## Frame 5: La petite voix · 12.50 → 16.33

- scene: The horned shadow rises on the planner page behind the phone; red eyes open on « petite voix »
- duration: 3.83s
- transition_in: cut
- status: outline
- src: compositions/frames/05-petite-voix.html
- voiceover: "Ce n'est pas un manque de talent. C'est une petite voix."
- type: pain_point
- blueprint: zoom-out-workspace-reveal (Adapt)
- focal: the horned shadow
- rules: depth-of-field-blur
- world: dark
- handoff_in: à 0.00 : cam(220, 0, 1.15, 0, 0) blur 8 px ; pull back + pan right in progress (power3.inOut) ; phone screen back to black with a faint red horned reflection fading ; page « Dimanche » visible on the right half ; lamp at 70 % ; no text ; grain 16 %
- handoff_out: à 3.83 : cam(0, 0, 1.20, 0, 0) blur 6 px ; push toward the phone in progress (power3.in) ; horned shadow at full size over the right of the page, two red eyes lit ; phone on the page, screen lighting up ; lamp at 70 % ; no text ; grain 16 %

Word cues: Ce@0.28 n'est@0.44 pas@0.59 un@0.75 manque@0.90 de@1.18 talent@1.33 C'est@2.45 une@2.58 petite@2.81 voix@3.15

Scene 1 (0.00 à 2.30 s) : P1, pas un manque de talent
  TEXTE ÉCRAN : subtitle « Ce n'est pas un manque de talent. » word by word from 0.28, [trait : talent] at 1.33 (gold stroke, the only gold before the pivot: the reader's own talent) ; écart synchro
  IMAGE DE DÉPART : handoff_in.
  ÉTAPES : 0.00 settle ; 0.28 words ; 0.90 the post-it « Commencer » on the page gets a soft gold rim light (it is still possible) ; 1.33 stroke under « talent » ; 1.80 the lamp flickers ; 2.10 subtitle leaves
  PISTE CAMÉRA : land (0.3 s) ; drift scale 1.10 → 1.13
  COUCHES ET PROFONDEUR : pencil foreground ; page ; desk
  OBJET-PONT ET VECTEUR : the flicker → the shadow arrives
  SON : none
  IMAGE CLÉ : 1.50 : the page, the post-it, « talent » underlined in gold

Scene 2 (2.30 à 3.83 s) : P2, la petite voix
  TEXTE ÉCRAN : subtitle « C'est une petite voix. » word by word from 2.45, [boîte : petite voix] at 2.79 ; écart synchro
  IMAGE DE DÉPART : Scene 1 end.
  ÉTAPES : 2.40 the horned shadow rises from the bottom right of the page (y +400 → 0, scale .7 → 1, 0.6 s power3.out, multiply, blur 10) ; 2.79 box ; 3.15 two small red eyes open in the shadow (scaleY 0 → 1, 0.12 s) ; 3.50 subtitle leaves ; 3.55 the phone screen starts lighting
  PISTE CAMÉRA : 2.40 à 3.40 pull back slightly to show the shadow whole (scale 1.13 → 1.05) ; 3.55 à 3.83 push toward the phone (scale 1.20), blur 6 px
  COUCHES ET PROFONDEUR : shadow cast over page ; phone ; desk
  OBJET-PONT ET VECTEUR : the eyes → the sender of the notifications
  SON : whoosh (low) at 2.40
  IMAGE CLÉ : 3.20 : the horned shadow over the page with red eyes, « petite voix » in the red box

## Frame 6: Les excuses · 16.33 → 22.05

- scene: The phone screen: three notifications from « La petite voix » fall one by one; behind the phone the shadow grows at each one
- duration: 5.72s
- transition_in: cut
- status: outline
- src: compositions/frames/06-excuses.html
- voiceover: "Elle te dit d'attendre, que ce n'est pas pour toi, que demain ce sera mieux."
- type: pain_point
- blueprint: device-surface-showcase (Adapt)
- focal: the notifications
- rules: waterfall-entry
- world: dark
- handoff_in: à 0.00 : cam(0, 0, 1.20, 0, 0) blur 6 px ; push toward the phone in progress (power3.in) ; horned shadow at full size over the right of the page, two red eyes lit ; phone on the page, screen lighting up ; lamp at 70 % ; no text ; grain 16 %
- handoff_out: à 5.72 : black screen everywhere (cut wanted) ; the phone screen has just gone off, the lamp off ; no text

Word cues: Elle@0.55 te@0.81 dit@0.96 d'attendre@1.11 que@2.22 ce@2.34 n'est@2.46 pas@2.58 pour@2.70 toi@2.82 que@3.59 demain@3.82 ce@4.59 sera@4.71 mieux@4.92

Scene 1 (0.00 à 5.72 s) : P1, trois notifications
  TEXTE ÉCRAN : subtitle « Elle te dit d'attendre, » from 0.55 [boîte : attendre] at 1.09 ; then « que ce n'est pas pour toi, » from 2.22 [boîte : pas pour toi] at 2.56 ; then « que demain, ce sera mieux. » from 3.59 [boîte : demain] at 3.80 ; each chunk replaces the previous ; notification copy: « Attends encore un peu. », « Ce n'est pas pour toi. », « Demain, ce sera mieux. », app name « La petite voix », « maintenant », time « 23:47 »
  IMAGE DE DÉPART : handoff_in.
  ÉTAPES : 0.00 settle on the phone, lock screen « 23:47 » ; 0.57 notification 1 falls (y -60 → 0, 0.3 s expo.out) ; 0.60 the shadow behind the phone grows (scale 1 → 1.12) ; 1.09 box « attendre » ; 2.10 chunk swap ; 2.24 notification 2 falls, pushes 1 down ; 2.27 shadow 1.12 → 1.25 ; 2.56 box ; 3.45 chunk swap ; 3.61 notification 3 falls ; 3.64 shadow 1.25 → 1.40, its horns now reach the top of the page ; 3.80 box « demain » ; 4.50 the post-it « Commencer » visible beside the phone slowly slides out of frame (x +300, 0.8 s) ; 5.30 subtitle leaves ; 5.50 phone screen off, lamp off (0.15 s)
  PISTE CAMÉRA : land (0.3 s) on cam-phone ; slow push in scale 1.20 → 1.32 linear for the whole shot ; no move at the end (cut)
  COUCHES ET PROFONDEUR : phone sharp ; shadow behind, multiply ; desk
  OBJET-PONT ET VECTEUR : the light goes off → the pivot on black
  SON : pop at 0.57, 2.24, 3.61
  IMAGE CLÉ : 3.90 : three notifications of « La petite voix » stacked, the shadow huge behind (styleframe C2)

## Frame 7: La bascule · 22.05 → 25.41

- scene: Black. « Et si tu étais plus malin qu'elle ? » converges in the centre; silence; a thin gold crack appears in the black
- duration: 3.36s
- transition_in: cut
- status: outline
- src: compositions/frames/07-bascule.html
- voiceover: "Et si tu étais plus malin qu'elle ?"
- type: pivot
- blueprint: kinetic-type-beats (Adapt)
- focal: the pivot line
- rules: discrete-text-sequence
- world: dark
- handoff_in: aucun raccord de caméra (coupe franche voulue) ; noir pur, rien à l'écran
- handoff_out: à 3.36 : black with a vertical gold crack at x 540 from y 300 to y 1300, 6 px wide, glowing (gold-glow), starting to open ; the pivot line gone ; no subtitle

Word cues: Et@0.69 si@0.87 tu@1.05 étais@1.23 plus@1.56 malin@1.74 qu'elle@2.06

Scene 1 (0.00 à 3.36 s) : P1, la question
  TEXTE ÉCRAN : typographic moment, centred at y 760, Fraunces 900 96 px max, 3 lines « Et si tu étais / plus malin / qu'elle ? », word by word on the cues, no subtitle in the band ; « malin » in italic
  IMAGE DE DÉPART : handoff_in.
  ÉTAPES : 0.69 « Et » ; each word converges (letters x spread → 0, blur 12 → 0, 0.4 s expo.out) on its cue ; 2.06 « qu'elle ? » ; 2.40 hold, the line slowly scales 1 → 1.03 (living layer) ; 2.80 the line fades (blur 6, 0.2 s) ; 3.00 a vertical gold crack draws from the centre up and down (scaleY 0 → 1, 0.3 s power2.out)
  PISTE CAMÉRA : drift scale 1.00 → 1.03 linear
  COUCHES ET PROFONDEUR : black ; text ; the crack
  OBJET-PONT ET VECTEUR : the crack → the tear of the page
  SON : whoosh at 0.00 (low impact, music cut) ; silence ; soft riser 2.90 à 3.36
  IMAGE CLÉ : 2.30 : the whole question centred on black

## Frame 8: Plus malin que le diable · 25.41 → 31.14

- scene: The crack tears the black like a page; gold light floods; the ebook cover rises from the tear; the horned shadow shrinks in a corner; the excuses are crossed out
- duration: 5.73s
- transition_in: cut
- status: outline
- src: compositions/frames/08-revelation.html
- voiceover: "Plus malin que le diable. Un ebook qui démasque ses ruses, une par une."
- type: turn
- blueprint: camera-journey (Adapt)
- focal: the ebook cover
- rules: depth-of-field-blur, svg-path-draw
- world: light
- handoff_in: à 0.00 : black with a vertical gold crack at x 540 from y 300 to y 1300, 6 px wide, glowing (gold-glow), starting to open ; the pivot line gone ; no subtitle
- handoff_out: à 5.73 : cam(0, 0, 1.00, 0, 0) blur 6 px ; pull back in progress (power3.inOut) ; cover centred at (260, 360) 560×800 rotate -3deg on gold ground ; three crossed-out excuses fading at the left ; tiny horned shadow bottom-right ; no text ; grain

Word cues: Plus@0.83 malin@1.02 que@1.34 le@1.53 diable@1.71 Un@2.69 ebook@2.81 qui@3.02 démasque@3.14 ses@3.59 ruses@3.94 une@4.74 par@4.97 une@5.09

Scene 1 (0.00 à 2.50 s) : P1, la déchirure et la couverture
  TEXTE ÉCRAN : subtitle « Plus malin que le diable. » word by word from 0.83, [trait : malin] at 1.02 ; écart synchro
  IMAGE DE DÉPART : handoff_in.
  ÉTAPES : 0.00 the crack tears open: two torn paper halves (paper colour, jagged edge) slide apart left and right (x ∓600, rotate ∓7 deg, 0.6 s power3.out) ; 0.05 gold light floods from the centre (radial 0 → 55 %, 0.4 s) ; 0.30 the cover rises from the tear, too big and blurred (scale 1.4 → 1, blur 12 → 0, 0.6 s expo.out) to (260, 360) ; 0.83 words ; 1.02 gold stroke under « malin » ; 1.40 the cover's horns glint (a gold sweep across the cover, 0.4 s) ; 2.20 subtitle leaves
  PISTE CAMÉRA : 0.00 à 0.60 push through the tear (scale 1.15 → 1.00) power3.out ; drift scale 1.00 → 1.02
  COUCHES ET PROFONDEUR : torn halves blurred foreground at the edges ; sharp cover ; gold halo
  OBJET-PONT ET VECTEUR : the cover → stays to the end
  SON : whoosh at 0.05 ; music drop at 0.83
  IMAGE CLÉ : 1.20 : the cover in gold light between the torn halves, « malin » underlined (styleframe A3)

Scene 2 (2.50 à 5.73 s) : P2, les ruses démasquées
  TEXTE ÉCRAN : subtitle « Un ebook qui démasque ses ruses, une par une. » word by word from 2.69, [boîte : ruses] at 3.92 (gold box) ; three excuse labels left of the cover in Fraunces 600 44 px: « Attends encore un peu. », « Ce n'est pas pour toi. », « Demain, ce sera mieux. »
  IMAGE DE DÉPART : Scene 1 end.
  ÉTAPES : 2.60 the cover slides right (x +160) to make room ; 2.80 the small horned shadow appears bottom-right, then shrinks (scale 1 → .3, 0.8 s) ; 3.20 the three excuses fall in on the left, stacked ; 3.92 box ; 3.99 excuse 1 crossed out by a red stroke drawn left to right (0.25 s) ; 4.76 excuse 2 crossed ; 5.11 excuse 3 crossed ; 5.40 the excuses fade left ; 5.45 subtitle leaves
  PISTE CAMÉRA : drift pan x +20 px ; 5.45 à 5.73 pull back toward cam-cover, blur 6 px
  COUCHES ET PROFONDEUR : excuses mid-ground ; cover sharp ; shadow tiny background
  OBJET-PONT ET VECTEUR : the crossed-out list → the post-it comes back
  SON : pop at 3.99, 4.76, 5.11
  IMAGE CLÉ : 5.20 : three excuses crossed out, the cover on the right, the shadow tiny

## Frame 9: De quoi lui répondre · 31.14 → 34.59

- scene: The post-it « Commencer » flies back onto the cover's corner and its box gets ticked; « Télécharge-le maintenant » brings the gold button up
- duration: 3.45s
- transition_in: cut
- status: outline
- src: compositions/frames/09-repondre.html
- voiceover: "Et te donne de quoi lui répondre. Télécharge-le maintenant,"
- type: payoff
- blueprint: camera-journey (Adapt)
- focal: the ticked post-it, then the button
- rules: svg-path-draw
- world: light
- handoff_in: à 0.00 : cam(0, 0, 1.00, 0, 0) blur 6 px ; pull back in progress (power3.inOut) ; cover centred at (260, 360) 560×800 rotate -3deg on gold ground ; three crossed-out excuses fading at the left ; tiny horned shadow bottom-right ; no text ; grain
- handoff_out: à 3.45 : cam(0, 0, 1.00, 0, 0) blur 4 px ; settle in progress ; cover at (260, 260) 560×800 with the ticked post-it on its top-right corner ; gold button « Télécharger l'ebook » at (110, 1150) 860×120 ; no subtitle ; grain

Word cues: Et@0.42 te@0.56 donne@0.70 de@0.95 quoi@1.10 lui@1.24 répondre@1.38 Télécharge-le@2.10 maintenant@2.83

Scene 1 (0.00 à 3.45 s) : P1, la case cochée et le bouton
  TEXTE ÉCRAN : subtitle « Et te donne de quoi lui répondre. » from 0.42, [trait : répondre] at 1.38 ; then « Télécharge-le maintenant, » from 2.10, [boîte : maintenant] at 2.81 (gold box) ; button copy « Télécharger l'ebook »
  IMAGE DE DÉPART : handoff_in.
  ÉTAPES : 0.20 settle ; 0.42 words ; 0.60 the post-it « Commencer » flies in from the top left (rotation, blur 8 → 0, 0.4 s expo.out) and sticks on the cover's top-right corner ; 1.20 a pencil tick draws in its box « ☐ → ☑ » (svg path, 0.3 s) ; 1.38 stroke under « répondre » ; 1.95 chunk swap ; 2.10 the cover moves up (y -100, 0.4 s) ; 2.20 the gold button rises from below (y +200 → 0, blur 8 → 0, 0.4 s expo.out) ; 2.81 box ; 3.20 subtitle leaves
  PISTE CAMÉRA : drift scale 1.00 → 1.02 ; 3.10 à 3.45 settle
  COUCHES ET PROFONDEUR : cover ; post-it ; button ; gold halo
  OBJET-PONT ET VECTEUR : the button → the click
  SON : ping at 1.20 ; pop at 2.20
  IMAGE CLÉ : 1.40 : the ticked post-it on the cover, « répondre » underlined

## Frame 10: Le lien · 34.59 → 38.50

- scene: End card: the cover, the ticked post-it, the button « Télécharger l'ebook »; a cursor arrives and clicks; an arrow points down to the link; living hold
- duration: 3.91s
- transition_in: cut
- status: outline
- src: compositions/frames/10-fin.html
- voiceover: "Le lien est juste en dessous."
- type: cta
- blueprint: cta-morph-press (Adapt)
- focal: the button
- rules: cursor-click-ripple
- world: light
- handoff_in: à 0.00 : cam(0, 0, 1.00, 0, 0) blur 4 px ; settle in progress ; cover at (260, 260) 560×800 with the ticked post-it on its top-right corner ; gold button « Télécharger l'ebook » at (110, 1150) 860×120 ; no subtitle ; grain
- handoff_out: à 3.91 : end of film ; the same end card, the arrow under the button ; light hold

Word cues: le@0.17 lien@0.29 est@0.40 juste@0.52 en@0.73 dessous@0.84

Scene 1 (0.00 à 3.91 s) : P1, le clic
  TEXTE ÉCRAN : subtitle « Le lien est juste en dessous. » from 0.17, [boîte : en dessous] at 0.71 (gold box) — placed in the band y 1330 to 1470, the button sits above it ; button copy « Télécharger l'ebook »
  IMAGE DE DÉPART : handoff_in.
  ÉTAPES : 0.17 words ; 0.71 box ; 1.20 a gold arrow ↓ draws under the subtitle toward the bottom of the screen (svg path, 0.35 s), pointing to the ad's button ; 1.50 a cursor arrives from the right in one curved move (0.45 s power3.out) onto the button ; 1.95 click: press scale .96 + ripple ring ; 2.20 the button glows ; 2.40 à 3.91 living hold: gold halo breathes once (opacity .5 → .7 → .5 over 1.5 s, finite), cover drift scale 1.00 → 1.015, dust particles in the light
  PISTE CAMÉRA : drift scale 1.00 → 1.02 linear, never stops
  COUCHES ET PROFONDEUR : cover ; button ; cursor ; halo
  OBJET-PONT ET VECTEUR : end
  SON : click at 1.95
  IMAGE CLÉ : 2.00 : the cursor clicking « Télécharger l'ebook » under the cover
