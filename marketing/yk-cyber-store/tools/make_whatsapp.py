#!/usr/bin/env python3
"""Messages promo de YK Cyber Store pour l'ebook « La Clé des Maths Financières », en images de conversation
WhatsApp vues depuis le téléphone d'un client : seule la boutique parle (aucun faux avis de client).

    python3 -I marketing/yk-cyber-store/tools/make_whatsapp.py

Écrit whatsapp/YK-Cyber-Store_message-<n>-<nom>.png (1080 × 1350) et whatsapp/apercu.png (les trois côte à côte).
Les textes sont dans MESSAGES : *texte* s'affiche en gras, comme dans WhatsApp.
"""

import html
import json
import os
import re
import subprocess
import tempfile
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "whatsapp"
FONTS = ROOT / "fonts"
RENDER = ROOT.parent.parent / "brand" / "ksc-studio" / "tools" / "render.cjs"  # Chromium de Playwright
W, H = 1080, 1350

BOUTIQUE = "YK Cyber Store"
MESSAGES = [  # (nom de fichier, [(heure, texte), ...])
    ("declic", [
        ("12:40", "📘 *La Clé des Maths Financières* est disponible chez *YK Cyber Store* !"),
        ("12:40", "Intérêts simples et composés, annuités, emprunts… Si les formules te donnent des sueurs froides, "
                  "ce guide est fait pour toi 😊"),
        ("12:40", "Chaque notion est expliquée simplement, avec la méthode de calcul étape par étape."),
        ("12:41", "👉 Écris-nous « CLÉ » pour le recevoir."),
    ]),
    ("examen", [
        ("18:05", "⏳ Ton examen de maths financières approche ?"),
        ("18:05", "Avec le guide 📘 *La Clé des Maths Financières*, tu révises l’essentiel : des formules expliquées "
                  "clairement et des calculs d’intérêts et d’emprunts détaillés pas à pas."),
        ("18:06", "📩 Disponible maintenant chez *YK Cyber Store*. Réponds « JE VEUX » pour le recevoir."),
    ]),
    ("question", [
        ("09:12", "❓ La question qu’on nous pose le plus : « Je ne suis pas fort en maths, ce guide est-il pour moi ? »"),
        ("09:12", "✅ Oui ! *La Clé des Maths Financières* part des bases et explique chaque formule avec des mots "
                  "simples, puis avec des exemples concrets."),
        ("09:13", "📘 Disponible chez *YK Cyber Store*. Écris-nous pour le recevoir 😊"),
    ]),
]


def fmt(s):
    """Échappe le texte et met en gras les passages *entre astérisques*."""
    return re.sub(r"\*([^*]+)\*", r"<b>\1</b>", html.escape(s))


def wallpaper():
    """Fond de discussion : beige avec de petits symboles de calcul, très discrets."""
    symbols = [("%", 40, 60), ("+", 150, 30), ("×", 260, 90), ("√", 330, 40), ("Σ", 90, 170), ("€", 210, 200),
               ("÷", 310, 160), ("=", 30, 280), ("π", 140, 300), ("%", 250, 330), ("+", 345, 260)]
    marks = "".join(f"<text x='{x}' y='{y}' font-size='38' font-family='Roboto, sans-serif'>{html.escape(t)}</text>"
                    for t, x, y in symbols)
    svg = (f"<svg xmlns='http://www.w3.org/2000/svg' width='380' height='380'><g fill='#cfc4b4' "
           f"fill-opacity='0.6'>{marks}</g></svg>")  # apostrophes : l'URL est entre guillemets dans le CSS
    return "data:image/svg+xml;utf8," + svg.replace("#", "%23").replace("<", "%3C").replace(">", "%3E")


ICONS = {
    "back": '<path d="M30 12 L14 28 L30 44" fill="none" stroke="#3b4a54" stroke-width="5" stroke-linecap="round" '
            'stroke-linejoin="round"/>',
    "video": '<rect x="4" y="14" width="36" height="28" rx="6" fill="none" stroke="#3b4a54" stroke-width="4.5"/>'
             '<path d="M40 24 L54 16 V40 L40 32" fill="none" stroke="#3b4a54" stroke-width="4.5" '
             'stroke-linejoin="round"/>',
    "call": '<path d="M16 8 C10 8 6 13 7 19 C9 33 23 47 37 49 C43 50 48 46 48 40 L48 36 L38 31 L32 37 C25 34 '
            '22 31 19 24 L25 18 L20 8 Z" fill="none" stroke="#3b4a54" stroke-width="4.5" stroke-linejoin="round"/>',
    "emoji": '<circle cx="28" cy="28" r="20" fill="none" stroke="#8696a0" stroke-width="4"/><circle cx="21" cy="24" '
             'r="2.6" fill="#8696a0"/><circle cx="35" cy="24" r="2.6" fill="#8696a0"/><path d="M19 33 Q28 41 37 33" '
             'fill="none" stroke="#8696a0" stroke-width="4" stroke-linecap="round"/>',
    "clip": '<path d="M36 18 L20 34 C16 38 21 44 26 40 L42 24 C49 17 40 8 33 15 L16 32 C9 39 19 49 26 42 L39 29" '
            'fill="none" stroke="#8696a0" stroke-width="4" stroke-linecap="round"/>',
    "camera": '<rect x="7" y="16" width="42" height="30" rx="6" fill="none" stroke="#8696a0" stroke-width="4"/>'
              '<circle cx="28" cy="31" r="8" fill="none" stroke="#8696a0" stroke-width="4"/>'
              '<path d="M20 16 L24 10 H32 L36 16" fill="none" stroke="#8696a0" stroke-width="4"/>',
    "mic": '<rect x="21" y="9" width="14" height="25" rx="7" fill="#fff"/><path d="M15 27 C15 43 41 43 41 27 M28 40 '
           'V47" fill="none" stroke="#fff" stroke-width="4" stroke-linecap="round"/>',
}


def icon(name, size=56):
    return f'<svg width="{size}" height="{size}" viewBox="0 0 56 56">{ICONS[name]}</svg>'


CSS = """
@font-face{font-family:Roboto;font-weight:400;src:url('__F__/roboto-latin-400-normal.woff2') format('woff2')}
@font-face{font-family:Roboto;font-weight:500;src:url('__F__/roboto-latin-500-normal.woff2') format('woff2')}
@font-face{font-family:Roboto;font-weight:700;src:url('__F__/roboto-latin-700-normal.woff2') format('woff2')}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1350px;overflow:hidden;font-family:Roboto,'Noto Color Emoji',sans-serif;color:#111b21}
.screen{display:flex;flex-direction:column;width:1080px;height:1350px;background:#efeae2 url("__WP__")}
header{display:flex;align-items:center;gap:22px;height:176px;padding:0 34px 0 22px;background:#fff;
  box-shadow:0 2px 3px rgba(0,0,0,.08);flex:none}
.avatar{width:112px;height:112px;border-radius:50%;display:flex;align-items:center;justify-content:center;
  background:linear-gradient(135deg,#0f2b46,#1b6f8a);color:#fff;font-weight:700;font-size:44px;letter-spacing:1px}
.who{flex:1}
.name{font-size:50px;font-weight:500;line-height:1.15}
.sub{font-size:34px;color:#667781;margin-top:4px}
.tools{display:flex;gap:46px}
.chat{flex:1;display:flex;flex-direction:column;justify-content:flex-end;padding:26px 40px 22px}
.day{align-self:center;background:#fff;color:#54656f;font-size:31px;font-weight:500;padding:12px 26px;
  border-radius:18px;margin-bottom:30px;box-shadow:0 1px 1px rgba(0,0,0,.08);letter-spacing:.5px}
.bubble{position:relative;align-self:flex-start;max-width:88%;background:#fff;border-radius:24px;
  padding:20px 28px 16px;margin-top:10px;font-size:45px;line-height:1.36;box-shadow:0 1px 1.5px rgba(0,0,0,.13)}
.bubble.first{border-top-left-radius:0;margin-top:0}
.bubble.first:before{content:"";position:absolute;left:-20px;top:0;border-top:26px solid #fff;
  border-left:22px solid transparent}
.bubble b{font-weight:700}
.time{float:right;font-size:29px;color:#667781;margin:22px 0 -6px 26px;line-height:1}
footer{display:flex;align-items:center;gap:18px;padding:0 24px 34px;flex:none}
.input{flex:1;display:flex;align-items:center;gap:22px;height:124px;padding:0 30px;background:#fff;border-radius:62px;
  box-shadow:0 1px 1.5px rgba(0,0,0,.1)}
.placeholder{flex:1;font-size:44px;color:#8696a0}
.send{width:124px;height:124px;border-radius:50%;background:#00a884;display:flex;align-items:center;
  justify-content:center}
"""


def page(bubbles):
    rows = []
    for i, (hour, s) in enumerate(bubbles):
        rows.append(f'<div class="bubble{" first" if i == 0 else ""}">{fmt(s)}<span class="time">{hour}</span></div>')
    css = CSS.replace("__F__", FONTS.as_uri()).replace("__WP__", wallpaper())
    return f"""<!doctype html><html lang="fr"><head><meta charset="utf-8"><style>{css}</style></head><body>
<div class="screen">
  <header>{icon("back")}<div class="avatar">YK</div>
    <div class="who"><div class="name">{BOUTIQUE}</div><div class="sub">Compte professionnel</div></div>
    <div class="tools">{icon("video", 60)}{icon("call", 56)}</div></header>
  <div class="chat"><div class="day">AUJOURD’HUI</div>{"".join(rows)}</div>
  <footer><div class="input">{icon("emoji")}<div class="placeholder">Message</div>{icon("clip")}{icon("camera")}</div>
    <div class="send">{icon("mic", 64)}</div></footer>
</div></body></html>"""


def render(jobs):
    path = Path(tempfile.mkstemp(suffix=".json")[1])
    path.write_text(json.dumps(jobs))
    env = dict(os.environ)
    env["NODE_PATH"] = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()
    subprocess.run(["node", str(RENDER), str(path)], check=True, env=env)
    path.unlink()


def main():
    OUT.mkdir(exist_ok=True)
    outs = []
    with tempfile.TemporaryDirectory() as tmp:
        jobs = []
        for n, (name, bubbles) in enumerate(MESSAGES, 1):
            src = Path(tmp) / f"{name}.html"
            src.write_text(page(bubbles))
            out = OUT / f"YK-Cyber-Store_message-{n}-{name}.png"
            jobs.append({"file": str(src), "out": str(out), "width": W, "height": H})
            outs.append(out)
        render(jobs)
    k = 0.42
    tiles = [Image.open(o).convert("RGB").resize((round(W * k), round(H * k)), Image.LANCZOS) for o in outs]
    gap = 30
    board = Image.new("RGB", (len(tiles) * tiles[0].width + (len(tiles) + 1) * gap, tiles[0].height + 2 * gap),
                      (230, 232, 235))
    for i, t in enumerate(tiles):
        board.paste(t, (gap + i * (t.width + gap), gap))
    board.save(OUT / "apercu.png")
    print(len(outs), "images dans", OUT)


if __name__ == "__main__":
    main()
