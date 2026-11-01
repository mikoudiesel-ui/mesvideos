"""Writes the 9 styleframes (A1 to C3) of plus-malin-que-le-diable, 1080x1920."""
import pathlib
here = pathlib.Path(__file__).parent
HORNS = ('<svg class="horns" viewBox="0 0 220 120"><path d="M30 118 C10 70 18 28 52 4 C44 44 60 76 92 96 Z" fill="#e2372b"/>'
         '<path d="M190 118 C210 70 202 28 168 4 C176 44 160 76 128 96 Z" fill="#e2372b"/></svg>')
COVER = ('<div class="cover" style="{s}"><div class="k">EBOOK</div><div class="t">Plus malin <i>que le</i> diable</div>'
         + HORNS + '<div class="a">Démasque ses ruses</div></div>')
def sub(html): return f'<div class="sub">{html}</div>'
def page(name, label, body, bg):
    (here / f"{name}.html").write_text(f"""<!doctype html><html lang="fr"><head><meta charset="utf-8">
<link rel="stylesheet" href="base.css"><style>body{{background:{bg};}}</style></head>
<body class="grain">{body}<div class="tag">{label}</div></body></html>""", encoding="utf-8")

# ---------------- A. Le calendrier de la nuit ----------------
AG = "radial-gradient(90% 60% at 50% 35%, #2a2a3f 0%, #0e0b12 75%)"
def agenda(day, extra="", style=""):
    return f"""<div class="abs" style="left:110px;top:230px;width:860px;height:1000px;background:var(--papier);color:var(--encre);
 border-radius:14px;box-shadow:0 50px 120px rgba(0,0,0,.6);transform:rotate(-2deg);{style}">
 <div style="position:absolute;top:0;left:0;right:0;height:70px;background:#d9cdb6;border-radius:14px 14px 0 0"></div>
 {''.join(f'<div style="position:absolute;top:22px;left:{120+i*130}px;width:24px;height:24px;border-radius:50%;background:#0e0b12"></div>' for i in range(5))}
 <div style="position:absolute;top:120px;left:70px;font:900 150px/1 Fraunces;letter-spacing:-.02em">{day}</div>
 <div style="position:absolute;top:290px;left:74px;font:500 30px 'Instrument Sans';color:#8a7f6e;letter-spacing:.2em">3 NOVEMBRE</div>
 {''.join(f'<div style="position:absolute;left:70px;right:70px;top:{400+i*90}px;border-top:2px solid #d8ccb5"></div>' for i in range(7))}
 {extra}</div>"""
POSTIT = lambda txt, st: f"""<div class="abs" style="width:420px;height:330px;background:#ffd64a;color:var(--encre);
 box-shadow:0 30px 60px rgba(0,0,0,.35);font:600 64px/1.05 Fraunces;padding:60px 40px;{st}">{txt}</div>"""
page("A1", "A1 · 1,8 s · Lundi, tu te promets de commencer", agenda("Lundi") +
     POSTIT("Commencer<br><span style='font:500 30px Instrument Sans'>mon projet ☐</span>",
            "left:500px;top:640px;transform:rotate(6deg) scale(1.35);filter:blur(7px);opacity:.92") +
     POSTIT("Commencer<br><span style='font:500 30px Instrument Sans'>mon projet ☐</span>",
            "left:470px;top:700px;transform:rotate(4deg);opacity:.0") +
     sub('Lundi, tu te promets de <span class="box">commencer.</span>'), AG)
SHADOW = """<svg class="abs" style="left:300px;top:420px;width:760px;height:900px;opacity:.55;filter:blur(10px);mix-blend-mode:multiply" viewBox="0 0 380 450">
 <path d="M190 120 C120 120 90 170 92 230 C60 260 40 330 40 450 L340 450 C340 330 320 260 288 230 C290 170 260 120 190 120Z" fill="#2b0d10"/>
 <path d="M140 140 C110 90 118 40 150 10 C146 60 160 100 180 122Z M240 140 C270 90 262 40 230 10 C234 60 220 100 200 122Z" fill="#2b0d10"/></svg>"""
page("A2", "A2 · 17,3 s · Elle te dit d'attendre", agenda("Mercredi",
     extra='<div style="position:absolute;top:410px;left:80px;font:600 40px Fraunces;color:#b7ab95;text-decoration:line-through">Commencer</div>', style="transform:rotate(-2deg) translateX(-60px)") +
     SHADOW +
     POSTIT("Demain.<br><span style='font:500 30px Instrument Sans'>promis</span>", "left:560px;top:560px;transform:rotate(-7deg)") +
     sub('Elle te dit <span style="white-space:nowrap">d’<span class="box">attendre,</span></span>'),
     "radial-gradient(70% 50% at 80% 20%, #4a2f22 0%, #0e0b12 70%)")
page("A3", "A3 · 26,6 s · Plus malin que le diable", f"""
 <div class="abs" style="left:-40px;top:160px;width:600px;height:1150px;background:var(--papier);clip-path:polygon(0 0,100% 0,82% 14%,96% 30%,78% 47%,92% 63%,74% 80%,90% 100%,0 100%);transform:translateX(-120px) rotate(-6deg);filter:blur(4px)"></div>
 <div class="abs" style="left:560px;top:160px;width:600px;height:1150px;background:var(--papier);clip-path:polygon(18% 0,100% 0,100% 100%,10% 100%,26% 80%,8% 63%,22% 47%,4% 30%,18% 14%);transform:translateX(160px) rotate(7deg);filter:blur(4px)"></div>
 <div class="abs" style="inset:0;background:radial-gradient(40% 30% at 50% 42%, rgba(244,181,63,.55), transparent 70%)"></div>
 {COVER.format(s="left:260px;top:360px;transform:rotate(-3deg)")}
 {sub('Plus <span class="trait">malin</span> que le diable.')}""", "#120d0a")

# ---------------- B. Le théâtre d'ombres ----------------
WALL = "radial-gradient(55% 40% at 50% 38%, #e9c48d 0%, #a2683a 45%, #2b1710 100%)"
PERSON = """<svg class="abs" style="left:150px;top:620px;width:620px;height:760px" viewBox="0 0 310 380">
 <circle cx="150" cy="70" r="48" fill="#1b100c"/><path d="M60 380 C60 220 90 140 150 135 C210 140 240 220 240 380Z" fill="#1b100c"/>
 <rect x="-40" y="250" width="380" height="16" fill="#1b100c"/><rect x="190" y="200" width="110" height="52" rx="4" fill="#1b100c"/></svg>"""
page("B1", "B1 · 1,8 s · Lundi, tu te promets de commencer", f"""
 <div class="abs" style="left:0;right:0;top:250px;text-align:center;font:900 230px/1 Fraunces;color:#1b100c;opacity:.85;transform:scale(1.25);filter:blur(5px)">Lundi</div>
 {PERSON}{sub('Lundi, tu te promets de <span class="box">commencer.</span>')}""", WALL)
DEVIL = """<svg class="abs" style="left:380px;top:300px;width:700px;height:1050px;filter:blur(3px)" viewBox="0 0 350 525">
 <path d="M175 150 C110 150 85 200 88 260 C55 290 30 380 30 525 L330 525 C330 380 300 290 262 260 C265 200 240 150 175 150Z" fill="#120806"/>
 <path d="M120 165 C80 110 90 45 135 5 C128 70 145 120 165 150Z M230 165 C270 110 260 45 215 5 C222 70 205 120 185 150Z" fill="#120806"/>
 <ellipse cx="148" cy="232" rx="9" ry="5" fill="#e2372b"/><ellipse cx="202" cy="232" rx="9" ry="5" fill="#e2372b"/></svg>"""
page("B2", "B2 · 17,3 s · Elle te dit d'attendre", f"""{DEVIL}
 <div style="transform:translateX(-90px) scale(.9);transform-origin:50% 100%">{PERSON}</div>
 {sub('Elle te dit <span style="white-space:nowrap">d’<span class="box">attendre,</span></span>')}""",
     "radial-gradient(45% 35% at 30% 45%, #c9935c 0%, #6b3a20 50%, #160a07 100%)")
page("B3", "B3 · 26,6 s · Plus malin que le diable", f"""
 <div class="abs" style="inset:0;background:radial-gradient(45% 30% at 50% 40%, rgba(255,226,160,.95), rgba(244,181,63,.35) 45%, transparent 75%)"></div>
 <svg class="abs" style="left:800px;top:1180px;width:120px;height:180px;opacity:.8" viewBox="0 0 350 525"><path d="M175 150 C110 150 85 200 88 260 C55 290 30 380 30 525 L330 525 C330 380 300 290 262 260 C265 200 240 150 175 150Z M120 165 C80 110 90 45 135 5 C128 70 145 120 165 150Z M230 165 C270 110 260 45 215 5 C222 70 205 120 185 150Z" fill="#120806"/></svg>
 {COVER.format(s="left:260px;top:330px;box-shadow:0 0 160px rgba(244,181,63,.6),0 60px 120px rgba(0,0,0,.5)")}
 {sub('Plus <span class="trait">malin</span> que le diable.')}""", "#3a2414")

# ---------------- C. Le téléphone ----------------
def phone(inner, st=""):
    return f"""<div class="abs" style="left:150px;top:150px;width:780px;height:1130px;border-radius:90px;background:#050407;
 box-shadow:0 0 0 14px #2a2630,0 80px 160px rgba(0,0,0,.7);overflow:hidden;{st}">
 <div class="abs" style="left:300px;top:24px;width:180px;height:50px;border-radius:30px;background:#000;z-index:5"></div>{inner}</div>"""
LOCK = "background:linear-gradient(180deg,#2b2440 0%,#140f1d 100%)"
page("C1", "C1 · 1,8 s · Lundi, tu te promets de commencer", phone(f"""
 <div class="abs" style="inset:0;{LOCK}"></div>
 <div class="abs" style="left:0;right:0;top:130px;text-align:center;font:500 38px 'Instrument Sans';color:#cfc6dd">lundi 3 novembre</div>
 <div class="abs" style="left:0;right:0;top:170px;text-align:center;font:700 200px/1 'Instrument Sans';color:#f3eefb;letter-spacing:-.03em">7:00</div>
 <div class="abs" style="left:50px;right:50px;top:470px;padding:40px;border-radius:44px;background:rgba(255,255,255,.14);transform:scale(1.18);filter:blur(5px)">
  <div style="font:500 30px 'Instrument Sans';color:#cfc6dd">⏰ Alarme</div>
  <div style="font:700 50px/1.1 'Instrument Sans';margin-top:12px">Commencer mon projet</div></div>""") +
     sub('Lundi, tu te promets de <span class="box">commencer.</span>'), "#09070c")
def notif(txt, top, st=""):
    return f"""<div class="abs" style="left:40px;right:40px;top:{top}px;padding:30px 34px;border-radius:40px;background:rgba(40,34,48,.92);display:flex;gap:26px;align-items:center;{st}">
 <div style="width:86px;height:86px;flex:none;border-radius:22px;background:#2a0f12;display:flex;align-items:center;justify-content:center">
  <svg viewBox="0 0 220 120" style="width:62px"><path d="M30 118 C10 70 18 28 52 4 C44 44 60 76 92 96 Z" fill="#e2372b"/><path d="M190 118 C210 70 202 28 168 4 C176 44 160 76 128 96 Z" fill="#e2372b"/></svg></div>
 <div><div style="font:700 30px 'Instrument Sans';color:#f3eefb">La petite voix <span style="color:#8d8496;font-weight:500"> · maintenant</span></div>
 <div style="font:500 40px/1.15 'Instrument Sans';color:#e8e2f0;margin-top:6px">{txt}</div></div></div>"""
page("C2", "C2 · 17,3 s · Elle te dit d'attendre", phone(f"""
 <div class="abs" style="inset:0;{LOCK}"></div>
 <div class="abs" style="left:0;right:0;top:120px;text-align:center;font:700 140px/1 'Instrument Sans';color:#f3eefb;opacity:.5">23:47</div>
 {notif("Attends encore un peu.", 330, "transform:scale(1.12);filter:blur(4px);opacity:.9")}
 {notif("Ce n'est pas pour toi.", 540, "opacity:.75")}
 {notif("Demain, ce sera mieux.", 730, "opacity:.5")}""") +
     sub('Elle te dit <span style="white-space:nowrap">d’<span class="box">attendre,</span></span>'), "#09070c")
page("C3", "C3 · 26,6 s · Plus malin que le diable", phone(f"""
 <div class="abs" style="inset:0;background:radial-gradient(70% 50% at 50% 40%,#3a2a12 0%,#0b0806 80%)"></div>
 <div style="position:absolute;left:110px;top:120px;transform:scale(1.0);transform-origin:0 0">{COVER.format(s="position:relative;left:0;top:0")}</div>
 <div class="abs" style="left:110px;right:110px;top:980px;height:110px;border-radius:60px;background:var(--or);color:var(--encre);display:flex;align-items:center;justify-content:center;font:700 42px 'Instrument Sans'">Télécharger l'ebook</div>""") +
     sub('Plus <span class="trait">malin</span> que le diable.'), "#0b0806")
print("9 styleframes written")
