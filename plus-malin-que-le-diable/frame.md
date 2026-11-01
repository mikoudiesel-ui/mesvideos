---
version: 2
name: "Plus malin que le diable: ad frame"
description: >
  Video-first frame spec for the Facebook ad of the ebook « Plus malin que le diable », 9:16 vertical, built on
  ../patterns/PATTERNS.md. Metaphor: procrastination is a little devil that pushes the task « Commencer » from day to
  day in a paper planner at night. Two worlds: the PROBLEM lives on the night desk (dark, cold blue lamp light, the
  planner page, the phone, the horned shadow); the SOLUTION lives in warm gold light behind the torn page. One accent
  per role: devil red for the key-word box of the problem and the devil's marks, gold for the solution and its peaks.
  The sentence of the voice is a subtitle in the centre band that arrives word by word.
unit: 1080×1920
principle: readable without sound · one thing to look at at a time · the voice cues every reveal · the first 3 s stop the thumb

colors:
  canvas: "#0e0b12"          # night desk (problem)
  canvas-2: "#1a1420"        # lamp halo on the desk
  lamp-cold: "#2a2a3f"       # cold radial lamp light
  paper: "#f1e8d8"           # planner page
  paper-2: "#d9cdb6"         # planner header strip, page rules #d8ccb5
  postit: "#ffd64a"          # the post-it « Commencer » (an object, not an accent)
  ink: "#f1e8d8"             # text on dark
  ink-dark: "#1b1612"        # text on paper
  ink-mute: "#8d8496"
  devil: "#e2372b"           # accent of the problem: key-word box, horns, red eyes, crossed-out strokes
  devil-shadow: "#2b0d10"    # the horned shadow (multiply on the page)
  gold: "#f4b53f"            # accent of the solution: light, peak strokes, CTA button, key-word box after the pivot
  gold-glow: "#ffe2a0"
  gold-ground: "#120d0a"     # warm dark ground of the solution, lit by gold radials

fonts:
  Fraunces: { files: ["assets/fonts/fraunces-latin-600-normal.woff2 (600)", "assets/fonts/fraunces-latin-900-normal.woff2 (900)", "assets/fonts/fraunces-latin-600-italic.woff2 (600 italic)"] }
  Instrument Sans: { files: ["assets/fonts/instrument-sans-latin-500-normal.woff2 (500)", "assets/fonts/instrument-sans-latin-700-normal.woff2 (700)"] }

typography:
  subtitle:   { fontFamily: "Instrument Sans", px: 62, weight: 700, lineHeight: 72, tracking: "-0.01em", note: "the sentence of the voice, centred horizontally, inside the band y 1330 to 1470 (nothing else in it; below y 1500 is covered by the Reels interface and stays empty of text), 2 lines at most, about 26 characters per line, word by word on its timestamps, text-shadow 0 4px 24px rgba(0,0,0,.55)" }
  type:       { fontFamily: "Fraunces", px: 96, weight: 900, lineHeight: 1.0, note: "ONLY the typographic moments: the diagnosis line « C'est une petite voix. » is NOT one; the pivot « Et si tu étais plus malin qu'elle ? » IS one (centred at y 760, 96 px max, no subtitle meanwhile)" }
  day:        { fontFamily: "Fraunces", px: 150, weight: 900, note: "the planner day name: Lundi, Mercredi, Dimanche" }
  date:       { fontFamily: "Instrument Sans", px: 30, weight: 500, tracking: "0.2em", upper: true, color: "#8a7f6e" }
  postit:     { fontFamily: "Fraunces", px: 64, weight: 600 }
  phone-time: { fontFamily: "Instrument Sans", px: 200, weight: 700, tracking: "-0.03em" }
  notif:      { fontFamily: "Instrument Sans", px: 40, weight: 500, note: "app name 30 px 700" }
  cta:        { fontFamily: "Instrument Sans", px: 46, weight: 700 }

components:
  ground-night:
    background: "canvas + radial lamp-cold at 50% 35% (90% 60%), static film grain 16% overlay. Full-duration class=\"clip\" layer."
  ground-gold:
    background: "gold-ground + radial gold (40% 30% at 50% 42%, 55%) behind the cover + grain. Full-duration class=\"clip\" layer."
  planner-page:
    look: "the world: a paper planner page 860×1000 at (110, 230), rotate -2deg, radius 14px, header strip 70 px paper-2 with 5 dark rings, day name in `day` at (70, 120) inside the page, date under it, 7 rules every 90 px from y 400. Shadow 0 50px 120px rgba(0,0,0,.6). Defined ONCE in reference/planner.html and copied verbatim."
    stations: "Lundi = page 1, Mercredi = page 2, Dimanche = page 3: a page turn is a flip around the top ring edge (rotateX 0 → -95deg, 0.35 s power3.in) revealing the next page under it."
  postit:
    look: "420×330, postit yellow, shadow 0 30px 60px rgba(0,0,0,.35), text « Commencer » in `postit` + « mon projet ☐ » 30 px Instrument Sans. Arrives too big (scale 1.35) and blurred (7 px) from the camera, settles (0.4 s expo.out) with a slight rotation 4 to 6 deg."
  devil-shadow:
    look: "a head-and-shoulders silhouette with two horns, devil-shadow, opacity .55, mix-blend multiply, blur 10 px, cast on the page from the right; its scale is the signature (it grows at every excuse); two small devil-red eyes only in frame 5 and 6."
  phone:
    look: "a modern phone 780×1130 at (150, 150), radius 90px, black bezel 14 px, dynamic island; lock screen gradient #2b2440 → #140f1d, date 38 px, time `phone-time`. Generic modern lock screen, no brand logo."
  alarm-card:
    look: "lock-screen card rgba(255,255,255,.14), radius 44px: « Alarme » 30 px + « Commencer mon projet » 50 px 700; two pill buttons « Répéter » and « Arrêter » appear on the swipe."
  notif-card:
    look: "rgba(40,34,48,.92), radius 40px, 86 px app tile (#2a0f12) with two red horns, app name « La petite voix » + « maintenant » in ink-mute, message 40 px. Falls from above (y -60 → 0, 0.3 s expo.out) and pushes the previous one down."
  ebook-cover:
    look: "560×800 book, radius 10/18px, radial #3a1414 → #07060a, spine highlight; « EBOOK » 24 px gold tracking .35em; title Fraunces 900 96 px « Plus malin » + italic devil-red « que le » + « diable »; two small red horns under the title; « Démasque ses ruses » 26 px ink-mute. PLACEHOLDER until the user sends the real cover (assets/img/cover.png replaces it 1:1)."
  key-word-box:
    look: "small rectangle, devil red before the pivot, gold (with ink-dark text) after it, radius 10px, padding 0 14px; traces from the left (scaleX 0 → 1, 0.16 s power3.out) 0 to 2 frames before the word."
    rule: "ONE box per sentence, on the word named [boîte : …]."
  peak-stroke:
    look: "gold tapered brush stroke 10 px under THE key word, slight rising curve, draws from the left 0.35 s power2.out. Named [trait : …]."
  cursor:
    description: "white arrow with dark outline + shadow; arrives in ONE curved move (0.45 s power3.out) and clicks directly: press scale .85 0.06 s + gold ripple ring."
  cta-button:
    description: "gold pill 860×120, radius 60px, « Télécharger l'ebook » in `cta`, ink-dark; a soft gold glow; pressed by the cursor."

negative:
  - "Nothing but the subtitle in the band y 1330 to 1470; no text below y 1500 (Reels interface); no text right of x 980 above y 1500 (like/share column)."
  - "No colored text: the key-word box and the gold peak stroke are the only emphasis."
  - "No giant word except the day names of the planner (they are the decor) and the pivot line (96 px max)."
  - "No horror imagery (no blood, no flames, no scary face): the devil is a mischievous shadow, never gore. Facebook ad policy."
  - "No fake proof: no stars, no testimonial, no sales counter, no price."
  - "No bouncy/elastic eases, no repeat:-1, no letterSpacing tween, no emoji except the ☐ / ☑ of the post-it."
  - "No camera back-and-forth; one thing to look at at a time."
---

# Plus malin que le diable: frame spec

The film has two worlds. **The problem** plays on the night desk: a paper planner under a cold lamp, the post-it
« Commencer » that slides from Monday to Sunday, the phone whose alarm gets snoozed, and a horned shadow that grows on
the page each time an excuse lands (the excuses arrive as notifications from « La petite voix »). A single **pivot**
(« Et si tu étais plus malin qu'elle ? », alone on black) freezes everything, then the page tears in two and gold light
pours through the tear: the **solution** is the ebook cover rising from the tear, the excuses crossed out one by one,
the post-it « Commencer » ticked at last, and a gold button « Télécharger l'ebook » clicked by a cursor.

Everything the viewer reads as narration is Instrument Sans 62 px in the centre band, word by word, with one key word
per sentence in a small box (red before the pivot, gold after). Fraunces is the voice of the objects: day names,
post-its, the pivot line, the cover title.

## Camera kit (all frames)

- A `#cam` wrapper holds the world; the camera moves it (x, y, scale, rotation); a slow linear drift never stops
  (0.6 to 1 %/s scale-in or 8 to 14 px/s pan), plus dated moves (0.5 to 0.8 s power3.inOut) toward the next subject.
- Seams fall at the peak of a camera move with 6 to 10 px motion blur on #cam (filter blur) on both sides.
- Depth: blurred foreground (pencil, edge of a mug, cut by the frame edge), sharp subject, softly blurred desk.

## Reference framings

- `cam-page`: planner page whole, scale 1, centred (frames 1 to 3).
- `cam-postit`: scale 1.35 toward the post-it (x -120, y -120).
- `cam-phone`: the phone lying on the page, seen from above, scale 1.1 (frame 4, frame 6).
- `cam-shadow`: scale 1.15 toward the right half of the page where the shadow grows (frame 5).
- `cam-cover`: the cover centred at y 420 to 1220, scale 1 (frames 8 and 9).
