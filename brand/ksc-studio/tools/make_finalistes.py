#!/usr/bin/env python3
"""Mises en situation des logos finalistes de KSC STUDIO, à faire voter autour de soi.

A = Objectif, B = Viseur (les deux pistes choisies), C = Fusion (le viseur du B et l'objectif du A).
Chaque page compare les trois dans la même situation : logos, profil réseaux sociaux, façade, cartes
de visite, filigrane sur photo. Les photos sont générées (tools/photos.py), aucune photo réelle.

    python3 -I brand/ksc-studio/tools/make_logos.py        # logos (dont la fusion)
    python3 -I brand/ksc-studio/tools/make_finalistes.py   # → KSC_STUDIO_finalistes.pdf + planches/finalistes/
"""

import importlib.util
from pathlib import Path

TOOLS = Path(__file__).resolve().parent


def load(name):
    spec = importlib.util.spec_from_file_location(name, TOOLS / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ml = load("make_logos")
ph = load("photos")
ROOT = ml.ROOT
PDF = "KSC_STUDIO_finalistes.pdf"

FINALISTES = [
    ("A", "Objectif", "01-objectif", "Fort et lisible de loin, dans la continuité de votre logo actuel."),
    ("B", "Viseur", "02-viseur", "Épuré et haut de gamme : vos initiales dans le viseur."),
    ("C", "Fusion", "07-fusion", "Nouveau : le viseur du B et l'objectif du A réunis."),
]

CSS = """
@page{size:1080px 1350px;margin:0}
body{margin:0;background:#F4F1EC;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{width:1080px;height:1350px;background:#F4F1EC;font-family:Jost;color:#111518;position:relative;overflow:hidden;break-after:page}
.page:last-child{break-after:auto}
.kicker{position:absolute;left:56px;top:46px;font-weight:500;font-size:14px;letter-spacing:.34em;color:#8A8178}
h1{position:absolute;left:56px;top:70px;margin:0;font-family:Montserrat;font-weight:800;font-size:46px;letter-spacing:-.01em}
h1 span{color:#FF741F}
.pitch{position:absolute;left:56px;top:136px;width:940px;font-size:20px;line-height:1.45;color:#4A4642}
.abs{position:absolute}
.panel{position:absolute;border-radius:20px;overflow:hidden;display:flex;align-items:center;justify-content:center}
.panel img.logo{max-width:76%;max-height:70%;display:block}
.badge{display:inline-flex;align-items:center;justify-content:center;width:44px;height:44px;border-radius:50%;
  background:#FF741F;color:#fff;font-family:Montserrat;font-weight:800;font-size:22px}
.label{position:absolute;display:flex;align-items:center;gap:14px;font-family:Montserrat;font-weight:800;font-size:24px}
.label small{font-family:Jost;font-weight:400;font-size:17px;color:#6B645D}
.foot{position:absolute;left:56px;right:56px;top:1296px;display:flex;justify-content:space-between;font-size:13px;
  letter-spacing:.2em;text-transform:uppercase;color:#8A8178}
.phone{position:absolute;width:300px;height:600px;border-radius:44px;background:#0B0D10;box-shadow:0 24px 50px rgba(0,0,0,.28)}
.screen{position:absolute;left:11px;top:11px;right:11px;bottom:11px;border-radius:34px;background:#fff;overflow:hidden}
.status{display:flex;justify-content:space-between;padding:12px 22px 0;font-size:12px;font-weight:500}
.prof{display:flex;flex-direction:column;align-items:center;padding:14px 16px 10px}
.prof img{width:92px;height:92px;border-radius:50%}
.prof .name{font-family:Montserrat;font-weight:800;font-size:16px;margin-top:10px}
.prof .bio{font-size:12.5px;color:#6B645D;text-align:center;line-height:1.4;margin-top:4px}
.btns{display:flex;gap:8px;margin-top:12px;width:100%}
.btns span{flex:1;text-align:center;font-size:12px;font-weight:500;padding:7px 0;border-radius:9px;background:#EEECE8}
.btns span.on{background:#FF741F;color:#fff}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:2px;margin-top:6px}
.grid div{aspect-ratio:1;background-size:cover;background-position:center}
.front{position:absolute;left:56px;width:968px;height:280px;border-radius:20px;overflow:hidden;
  background:linear-gradient(180deg,#EDE7DE,#DDD5C9)}
.front .brick{position:absolute;inset:0;opacity:.35;background:
  repeating-linear-gradient(0deg,transparent 0 25px,#C9BFB1 25px 27px),
  repeating-linear-gradient(90deg,transparent 0 63px,#CFC5B8 63px 65px)}
.sign{position:absolute;left:214px;top:26px;width:540px;height:120px;border-radius:10px;background:#111518;
  box-shadow:0 14px 26px rgba(0,0,0,.35);display:flex;align-items:center;justify-content:center}
.sign img{max-width:74%;max-height:68%}
.glow{position:absolute;top:-30px;width:300px;height:230px;background:radial-gradient(closest-side,rgba(255,236,200,.75),rgba(255,236,200,0))}
.lamp{position:absolute;top:8px;width:46px;height:12px;border-radius:6px;background:#2A2D31}
.shop{position:absolute;left:96px;right:96px;top:166px;bottom:0;background:#2A2D31;border-radius:6px 6px 0 0;
  display:grid;grid-template-columns:1fr 150px 1fr;gap:8px;padding:8px 8px 0}
.shop div{background:linear-gradient(135deg,#6E8592 0%,#3D4C57 45%,#5E7380 46%,#34424C 100%)}
.cards{position:absolute;left:56px;width:968px;height:280px;border-radius:20px;background:#DCD5CA}
.card{position:absolute;top:30px;width:340px;height:220px;border-radius:9px;box-shadow:0 18px 32px rgba(0,0,0,.25);overflow:hidden}
.card.front-side{display:flex;align-items:center;justify-content:center}
.card.front-side img{max-width:64%;max-height:56%}
.card.back-side{background:#fff}
.card.back-side img{position:absolute;left:26px;top:24px;height:58px}
.card .lines{position:absolute;left:28px;bottom:24px;font-size:15px;line-height:1.55;color:#8A8178}
.card .lines b{color:#111518;font-weight:500}
.card .bar{position:absolute;right:0;top:0;bottom:0;width:10px;background:#FF741F}
.photo{position:absolute;width:474px;height:280px;border-radius:20px;overflow:hidden;background-size:cover;background-position:center}
.photo img{position:absolute;right:20px;bottom:18px;max-width:34%;max-height:30%;opacity:.92}
"""


def logo(slug, variant):
    f = ROOT / "logos" / slug / f"ksc-{slug[3:]}-{variant}.svg"
    if not f.exists():
        raise SystemExit(f"{f} manquant : lancer d'abord tools/make_logos.py")
    return f.as_uri()


def header(kicker, title, pitch):
    return f'<div class="kicker">{kicker}</div><h1>{title}</h1><div class="pitch">{pitch}</div>'


def label(x, y, letter, name, small=""):
    s = f"<small>{small}</small>" if small else ""
    return f'<div class="label" style="left:{x}px;top:{y}px"><span class="badge">{letter}</span>{name}{s}</div>'


def foot(k):
    return f'<div class="foot"><span>KSC STUDIO · Finalistes</span><span>{k} / 5</span></div>'


def page_logos():
    out = header("KSC STUDIO · LES FINALISTES", "A, B <span>ou</span> C ?",
                 "Vos deux logos préférés, et une 3<sup>e</sup> option qui les réunit. Montrez ce document autour "
                 "de vous et notez la lettre qui plaît le plus.")
    for i, (letter, name, slug, desc) in enumerate(FINALISTES):
        top = 236 + i * 352
        out += label(56, top, letter, name, desc)
        out += (f'<div class="panel" style="left:56px;top:{top + 64}px;width:568px;height:264px;background:#fff">'
                f'<img class="logo" src="{logo(slug, "clair")}"></div>'
                f'<div class="panel" style="left:644px;top:{top + 64}px;width:380px;height:264px;background:#111518">'
                f'<img class="logo" src="{logo(slug, "sombre")}"></div>')
    return out + foot(1)


def page_social(tiles):
    out = header("KSC STUDIO · LES FINALISTES", "Sur les réseaux <span>·</span> en photo de profil",
                 "C'est là que vos clients vous découvrent : le logo doit se lire en tout petit, dans un rond.")
    grid = "".join(f'<div style="background-image:url({t})"></div>' for t in tiles)
    for i, (letter, name, slug, _) in enumerate(FINALISTES):
        x = 56 + i * 334
        out += label(x + 6, 250, letter, name)
        out += (f'<div class="phone" style="left:{x}px;top:312px"><div class="screen">'
                f'<div class="status"><span>12:00</span><span>●●● ▮</span></div>'
                f'<div class="prof"><img src="{logo(slug, "icone")}"><div class="name">KSC STUDIO</div>'
                f'<div class="bio">Studio photo<br>Réservez votre séance en message</div>'
                f'<div class="btns"><span class="on">Suivre</span><span>Message</span></div></div>'
                f'<div class="grid">{grid}</div></div></div>')
    out += ('<div class="abs" style="left:56px;top:950px;width:968px;font-size:17px;line-height:1.5;color:#4A4642">'
            'Avatars à taille réelle, comme dans une liste d\'abonnés :</div>')
    for i, (letter, name, slug, _) in enumerate(FINALISTES):
        x = 56 + i * 330
        out += (f'<div class="panel" style="left:{x}px;top:996px;width:308px;height:240px;background:#fff;'
                f'flex-direction:column;gap:14px">'
                f'<div style="display:flex;align-items:center;gap:16px">'
                f'<img src="{logo(slug, "icone")}" style="width:96px;height:96px">'
                f'<img src="{logo(slug, "icone")}" style="width:48px;height:48px">'
                f'<img src="{logo(slug, "icone")}" style="width:28px;height:28px"></div>'
                f'<div style="font-size:15px;color:#6B645D;letter-spacing:.12em">{letter} · {name.upper()}</div></div>')
    return out + foot(2)


def page_facade():
    out = header("KSC STUDIO · LES FINALISTES", "Sur votre façade",
                 "L'enseigne se lit de loin et de nuit : le logo doit rester net et clair à plusieurs mètres.")
    for i, (letter, name, slug, _) in enumerate(FINALISTES):
        top = 236 + i * 348
        out += label(56, top, letter, name)
        out += (f'<div class="front" style="top:{top + 46}px"><div class="brick"></div>'
                f'<div class="glow" style="left:180px"></div><div class="glow" style="left:488px"></div>'
                f'<div class="lamp" style="left:307px"></div><div class="lamp" style="left:615px"></div>'
                f'<div class="sign"><img src="{logo(slug, "sombre")}"></div>'
                f'<div class="shop"><div></div><div></div><div></div></div></div>')
    return out + foot(3)


def page_cards():
    out = header("KSC STUDIO · LES FINALISTES", "Cartes de visite",
                 "Recto et verso au format standard 85 × 55 mm. Vos coordonnées remplaceront les lignes grises.")
    for i, (letter, name, slug, _) in enumerate(FINALISTES):
        top = 236 + i * 348
        out += label(56, top, letter, name)
        out += (f'<div class="cards" style="top:{top + 46}px">'
                f'<div class="card front-side" style="left:114px;background:#111518"><img src="{logo(slug, "sombre")}"></div>'
                f'<div class="card back-side" style="left:514px"><img src="{logo(slug, "clair")}"><div class="bar"></div>'
                f'<div class="lines"><b>Prénom NOM · Photographe</b><br>06 XX XX XX XX<br>votre@email.fr<br>@votre_compte</div>'
                f'</div></div>')
    return out + foot(4)


def page_photos(photo_a, photo_b):
    out = header("KSC STUDIO · LES FINALISTES", "En filigrane sur vos photos",
                 "Sur chaque photo partagée par vos clients, le logo signe votre travail et vous fait connaître.")
    for i, (letter, name, slug, _) in enumerate(FINALISTES):
        top = 236 + i * 348
        out += label(56, top, letter, name)
        for k, ph_uri in enumerate((photo_a, photo_b)):
            out += (f'<div class="photo" style="left:{56 + k * 494}px;top:{top + 46}px;background-image:url({ph_uri})">'
                    f'<img src="{logo(slug, "sombre")}"></div>')
    return out + foot(5)


def main():
    tmp = ROOT / ".finalistes"
    tmp.mkdir(exist_ok=True)
    shots = {
        "coucher": ph.sunset(), "portrait": ph.portrait(), "montagnes": ph.mountains(), "ville": ph.trails(),
        "plage": ph.beach(), "objet": ph.product(),
        "portrait2": ph.portrait(seed=7, back=((90, 120, 140), (20, 28, 36)), rim=(255, 230, 200)),
        "coucher2": ph.sunset(seed=8, warm=0.6), "objet2": ph.product(seed=9, back=((210, 226, 240), (150, 180, 210))),
    }
    uris = {}
    for k, im in shots.items():
        f = tmp / f"{k}.jpg"
        im.save(f, quality=90)
        uris[k] = f.as_uri()
    tiles = [uris[k] for k in ("coucher", "portrait", "montagnes", "ville", "plage", "objet", "portrait2", "coucher2", "objet2")]
    pages = [page_logos(), page_social(tiles), page_facade(), page_cards(), page_photos(uris["coucher"], uris["portrait2"])]
    names = ["1-logos", "2-reseaux", "3-facade", "4-cartes", "5-filigrane"]
    out = ROOT / "planches" / "finalistes"
    out.mkdir(parents=True, exist_ok=True)

    def doc(body, title):
        return (f'<html><head><meta charset="utf-8"><title>{title}</title><style>{ml.font_face()}{CSS}</style></head>'
                f'<body>{body}</body></html>')

    jobs = []
    for name, body in zip(names, pages):
        f = tmp / f"{name}.html"
        f.write_text(doc(f'<div class="page">{body}</div>', f"KSC STUDIO · finalistes · {name}"))
        jobs.append({"file": str(f), "out": str(out / f"ksc-finalistes-{name}.png"), "width": 1080, "height": 1350, "scale": 2})
    f = tmp / "document.html"
    f.write_text(doc("".join(f'<div class="page">{b}</div>' for b in pages), "KSC STUDIO · Finalistes A, B ou C"))
    jobs.append({"file": str(f), "out": str(ROOT / PDF), "width": 1080, "height": 1350, "pdf": True})
    ml.render(jobs)
    for f in tmp.iterdir():
        f.unlink()
    tmp.rmdir()
    print("écrit", ROOT / PDF, "et", len(names), "planches dans", out)


if __name__ == "__main__":
    main()
