#!/usr/bin/env python3
"""Kit de marque KSC STUDIO pour le logo retenu : A · Objectif.

Produit le dossier `kit-objectif/` et son archive `KSC_STUDIO_kit_logo.zip` :
logos (vertical, horizontal, initiales, symbole ; couleur, négatif, noir, blanc ; SVG, PNG, PDF),
réseaux sociaux, filigranes, carte de visite à imprimer, favicons, charte graphique PDF, l'intro vidéo
du logo (rendue par videos/ksc-studio-intro) et un LISEZ-MOI.

    python3 -I brand/ksc-studio/tools/make_kit.py            # tout le kit
    python3 -I brand/ksc-studio/tools/make_kit.py --paquet   # seulement l'intro, le LISEZ-MOI et l'archive

Les coordonnées de la carte de visite sont dans CONTACT ; tant que PLACEHOLDER vaut True, ce sont des
exemples affichés en gris.
"""

import importlib.util
import shutil
import sys
import zipfile
from pathlib import Path

from PIL import Image

TOOLS = Path(__file__).resolve().parent


def load(name):
    spec = importlib.util.spec_from_file_location(name, TOOLS / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ml = load("make_logos")
ph = load("photos")
ROOT = ml.ROOT
KIT = ROOT / "kit-objectif"
ZIP = ROOT / "KSC_STUDIO_kit_logo.zip"
INTRO = ROOT.parent.parent / "videos" / "ksc-studio-intro" / "renders" / "KSC_STUDIO_intro-logo.mp4"
ORANGE, NOIR, BLANC = ml.ORANGE, ml.NOIR, ml.BLANC

# coordonnées de la carte de visite : exemples tant que les vraies ne sont pas fournies
CONTACT = {"nom": "Prénom NOM", "metier": "Photographe", "tel": "06 XX XX XX XX", "mail": "votre@email.fr",
           "reseau": "@votre_compte", "ville": "Votre ville"}
PLACEHOLDER = True

VERSIONS = {  # nom : (encre des initiales, couleur de STUDIO, objectif d'une seule couleur)
    "couleur": (NOIR, ORANGE, False),
    "negatif": (BLANC, ORANGE, False),
    "noir": (NOIR, NOIR, True),
    "blanc": (BLANC, BLANC, True),
}


# ------------------------------------------------------------------ logos
def symbol(ring, mono):
    F = 400.0
    Ro, t = 0.364 * F, 0.19 * F
    if mono:
        return ml.lens_c_mono(0, 0, Ro, t, 78, ring)
    return ml.lens_c(0, 0, Ro, t, 78, ring, ORANGE, NOIR, BLANC)


def square(content, box, bg, fill_ratio, D=1000.0):
    """Carré plein (photo de profil, icône d'appli) : le dessin centré, sans coins transparents."""
    w, h = box[2] - box[0], box[3] - box[1]
    k = fill_ratio * D / max(w, h)
    tx, ty = D / 2 - k * (box[0] + box[2]) / 2, D / 2 - k * (box[1] + box[3]) / 2
    body = (f'<rect width="{D}" height="{D}" fill="{bg}"/>'
            f'<g transform="matrix({ml.n(k)} 0 0 {ml.n(k)} {ml.n(tx)} {ml.n(ty)})">{content}</g>')
    return ml.Logo(body, (0, 0, D, D), margin=0)


def logos():
    out = {}
    for v, (ink, studio, mono) in VERSIONS.items():
        out[("vertical", v)] = ml.Logo(*ml.objectif_mark(ink, studio, mono=mono))
        out[("horizontal", v)] = ml.Logo(*ml.objectif_mark(ink, studio, mono=mono, layout="horizontal"))
        out[("initiales", v)] = ml.Logo(*ml.objectif_mark(ink, None, mono=mono))
        out[("symbole", v)] = ml.Logo(*symbol(ink, mono))
    return out


# ------------------------------------------------------------------ pages HTML
def font_face():
    faces = [(400, "montserrat-400"), (500, "montserrat-500"), (600, "montserrat-600"), (700, "montserrat-700"),
             (800, "montserrat-800")]
    return "".join(f"@font-face{{font-family:Montserrat;font-weight:{w};src:url({(ROOT / 'fonts' / f'{n}.ttf').as_uri()})}}"
                   for w, n in faces)


def doc(body, css, title="KSC STUDIO"):
    return (f'<html><head><meta charset="utf-8"><title>{title}</title><style>{font_face()}'
            f'body{{margin:0;font-family:Montserrat;-webkit-print-color-adjust:exact;print-color-adjust:exact}}{css}'
            f'</style></head><body>{body}</body></html>')


def uri(f):
    return f.as_uri()


SOCIAL_CSS = """
.c{position:relative;overflow:hidden;background:#111518;color:#fff}
.glow{position:absolute;border-radius:50%;background:radial-gradient(closest-side,rgba(255,116,31,.32),rgba(255,116,31,0))}
.mid{position:absolute;left:0;right:0;display:flex;justify-content:center}
.pill{display:inline-block;background:#FF741F;color:#fff;font-weight:700;border-radius:999px}
"""


def social(files, photo):
    h_neg, v_neg = uri(files[("horizontal", "negatif")]), uri(files[("vertical", "negatif")])
    pages = {
        "ksc-couverture-facebook.png": (1640, 624, f"""<div class="c" style="width:1640px;height:624px">
<div class="glow" style="left:1080px;top:-260px;width:900px;height:900px"></div>
<div class="mid" style="top:206px"><img src="{h_neg}" style="width:720px"></div>
<div class="mid" style="top:420px;font-size:28px;font-weight:500;letter-spacing:.06em;color:#B9B3AC">Réservez votre séance photo en message</div></div>"""),
        "ksc-banniere-youtube.png": (2560, 1440, f"""<div class="c" style="width:2560px;height:1440px">
<div class="glow" style="left:1500px;top:100px;width:1400px;height:1400px"></div>
<div class="mid" style="top:600px"><img src="{h_neg}" style="width:1100px"></div></div>"""),
        "ksc-modele-story.png": (1080, 1920, f"""<div class="c" style="width:1080px;height:1920px">
<div class="glow" style="left:400px;top:1200px;width:1100px;height:1100px"></div>
<div class="mid" style="top:110px"><img src="{v_neg}" style="width:330px"></div>
<div style="position:absolute;left:100px;top:420px;width:880px;height:900px;border-radius:36px;background:url({photo}) center/cover"></div>
<div class="mid" style="top:1400px;font-size:66px;font-weight:800;line-height:1.12;text-align:center">Réservez votre<br>séance photo</div>
<div class="mid" style="top:1622px"><span class="pill" style="font-size:36px;padding:26px 58px">Écrivez-nous en message</span></div></div>"""),
        "ksc-post-nouveau-logo.png": (1080, 1350, f"""<div class="c" style="width:1080px;height:1350px">
<div class="glow" style="left:140px;top:240px;width:800px;height:800px"></div>
<div class="mid" style="top:250px;font-size:26px;font-weight:700;letter-spacing:.42em;color:#FF741F">NOUVELLE IDENTITÉ</div>
<div class="mid" style="top:420px"><img src="{v_neg}" style="width:620px"></div>
<div class="mid" style="top:930px;font-size:44px;font-weight:600">Nouveau logo, même passion.</div>
<div class="mid" style="top:1190px;font-size:22px;font-weight:500;letter-spacing:.3em;color:#8B9096">KSC STUDIO · STUDIO PHOTO</div></div>"""),
    }
    return pages


CARD_CSS = """
@page{size:91mm 61mm;margin:0}
.card{position:relative;width:91mm;height:61mm;overflow:hidden;break-after:page}
.card:last-child{break-after:auto}
.lines{position:absolute;left:9mm;bottom:8.5mm;font-size:7.4pt;line-height:1.5;color:#4A4642}
.lines .nom{font-weight:600;font-size:9.4pt;color:#111518}
.lines .metier{font-weight:600;color:#FF741F;margin-bottom:1.6mm}
.ph{color:#A39A90}
"""


def card(files):
    v_neg, h_col = uri(files[("vertical", "negatif")]), uri(files[("horizontal", "couleur")])
    cls = ' class="ph"' if PLACEHOLDER else ""
    c = CONTACT
    recto = (f'<div class="card" style="background:#111518;display:flex;align-items:center;justify-content:center">'
             f'<img src="{v_neg}" style="width:40mm"></div>')
    verso = (f'<div class="card" style="background:#fff">'
             f'<img src="{h_col}" style="position:absolute;left:9mm;top:9mm;width:38mm">'
             f'<div style="position:absolute;right:0;top:0;bottom:0;width:8mm;background:#FF741F"></div>'
             f'<div class="lines"><div class="nom"><span{cls}>{c["nom"]}</span></div>'
             f'<div class="metier">{c["metier"]}</div>'
             f'<div{cls}>{c["tel"]}</div><div{cls}>{c["mail"]}</div><div{cls}>{c["reseau"]} · {c["ville"]}</div></div></div>')
    return recto, verso


CHARTE_CSS = """
@page{size:1080px 1350px;margin:0}
.page{position:relative;width:1080px;height:1350px;background:#F4F1EC;color:#111518;overflow:hidden;break-after:page}
.page:last-child{break-after:auto}
.kicker{position:absolute;left:56px;top:46px;font-weight:600;font-size:13px;letter-spacing:.34em;color:#8A8178}
h1{position:absolute;left:56px;top:70px;margin:0;font-weight:800;font-size:44px}
h1 span{color:#FF741F}
.pitch{position:absolute;left:56px;top:134px;width:960px;font-size:18px;line-height:1.5;color:#4A4642;font-weight:400}
.box{position:absolute;border-radius:18px;overflow:hidden;display:flex;align-items:center;justify-content:center}
.box img{max-width:70%;max-height:62%}
.cap{position:absolute;font-size:14px;line-height:1.45;color:#4A4642}
.cap b{display:block;color:#111518;font-size:15px;font-weight:700;margin-bottom:2px}
.sw{position:absolute;width:300px;height:190px;border-radius:18px;overflow:hidden;background:#fff}
.sw div.c{height:110px}
.sw div.t{padding:12px 16px;font-size:13px;line-height:1.5;color:#4A4642}
.sw div.t b{color:#111518;font-size:15px}
.no{position:absolute;width:224px;height:196px;border-radius:16px;background:#fff;overflow:hidden}
.no .art{position:absolute;left:0;right:0;top:0;height:150px;display:flex;align-items:center;justify-content:center;overflow:hidden}
.no .lab{position:absolute;left:0;right:0;bottom:0;height:46px;display:flex;align-items:center;gap:8px;padding-left:14px;font-size:13px;font-weight:600}
.no .lab i{font-style:normal;display:inline-flex;width:22px;height:22px;border-radius:50%;background:#D93025;color:#fff;align-items:center;justify-content:center;font-size:13px}
.foot{position:absolute;left:56px;right:56px;top:1296px;display:flex;justify-content:space-between;font-size:12px;letter-spacing:.2em;text-transform:uppercase;color:#8A8178}
"""


def charte(files, photo):
    f = lambda layout, v: uri(files[(layout, v)])  # noqa: E731
    foot = lambda k: f'<div class="foot"><span>KSC STUDIO · Charte graphique</span><span>{k} / 3</span></div>'  # noqa: E731
    p1 = f"""<div class="page">
<div class="kicker">KSC STUDIO · CHARTE GRAPHIQUE</div><h1>Le logo <span>·</span> versions</h1>
<div class="pitch">Utilisez toujours les fichiers fournis, sans les redessiner. La version couleur est la version
principale ; les autres servent quand le fond ou la technique d'impression l'imposent.</div>
<div class="box" style="left:56px;top:236px;width:968px;height:440px;background:#fff"><img src="{f("vertical", "couleur")}" style="max-height:66%"></div>
<div class="cap" style="left:56px;top:690px"><b>Couleur · version principale</b>Sur fond blanc ou clair : site, documents, cartes, réseaux.</div>
<div class="box" style="left:56px;top:770px;width:304px;height:330px;background:#111518"><img src="{f("vertical", "negatif")}"></div>
<div class="box" style="left:388px;top:770px;width:304px;height:330px;background:#fff"><img src="{f("vertical", "noir")}"></div>
<div class="box" style="left:720px;top:770px;width:304px;height:330px;background:#FF741F"><img src="{f("vertical", "blanc")}"></div>
<div class="cap" style="left:56px;top:1114px;width:300px"><b>Négatif</b>Sur fond sombre et en filigrane sur les photos.</div>
<div class="cap" style="left:388px;top:1114px;width:300px"><b>Noir · une couleur</b>Tampon, gravure, broderie, photocopie, impression noir et blanc.</div>
<div class="cap" style="left:720px;top:1114px;width:300px"><b>Blanc · une couleur</b>Sur fond orange ou foncé, textile, adhésif de vitrine.</div>
{foot(1)}</div>"""
    p2 = f"""<div class="page">
<div class="kicker">KSC STUDIO · CHARTE GRAPHIQUE</div><h1>Déclinaisons <span>·</span> couleurs <span>·</span> police</h1>
<div class="pitch">Chaque format a sa version : la plus lisible à la place disponible.</div>
<div class="box" style="left:56px;top:212px;width:968px;height:230px;background:#fff"><img src="{f("horizontal", "couleur")}" style="max-width:62%"></div>
<div class="cap" style="left:56px;top:454px"><b>Horizontale</b>Bandeaux, en-tête de site, enseigne large, signature d'e-mail.</div>
<div class="box" style="left:56px;top:528px;width:304px;height:220px;background:#fff"><img src="{f("initiales", "couleur")}"></div>
<div class="box" style="left:388px;top:528px;width:304px;height:220px;background:#EAE5DD"><img src="{uri(files["icone-ronde"])}" style="max-height:78%"></div>
<div class="box" style="left:720px;top:528px;width:304px;height:220px;background:#fff"><img src="{f("symbole", "couleur")}" style="max-height:56%"></div>
<div class="cap" style="left:56px;top:760px;width:300px"><b>Initiales</b>Quand la place manque (tampon, sticker, coin de photo).</div>
<div class="cap" style="left:388px;top:760px;width:300px"><b>Icône ronde</b>Photo de profil des réseaux et de WhatsApp.</div>
<div class="cap" style="left:720px;top:760px;width:300px"><b>Symbole</b>Favicon du site, très petits formats.</div>
<div class="sw" style="left:56px;top:868px"><div class="c" style="background:#FF741F"></div><div class="t"><b>Orange KSC</b><br>#FF741F · RVB 255 116 31<br>CMJN indicatif 0 / 60 / 90 / 0</div></div>
<div class="sw" style="left:388px;top:868px"><div class="c" style="background:#111518"></div><div class="t"><b>Noir KSC</b><br>#111518 · RVB 17 21 24<br>CMJN indicatif 0 / 0 / 0 / 100</div></div>
<div class="sw" style="left:720px;top:868px"><div class="c" style="background:#fff;border-bottom:1px solid #E6E1D9"></div><div class="t"><b>Blanc</b><br>#FFFFFF · RVB 255 255 255<br>fond et respiration</div></div>
<div class="cap" style="left:56px;top:1076px;width:968px">Couleurs d'impression indicatives : demandez une épreuve à l'imprimeur pour valider l'orange.</div>
<div class="box" style="left:56px;top:1122px;width:968px;height:150px;box-sizing:border-box;background:#fff;justify-content:flex-start;padding-left:34px;gap:34px">
<div style="font-size:84px;font-weight:800;line-height:1">Aa</div>
<div style="font-size:15px;line-height:1.6;color:#4A4642"><b style="color:#111518;font-size:17px">Montserrat</b> · police du logo, gratuite (usage commercial autorisé)<br>
Titres : <b style="color:#111518">ExtraBold</b> · Sous-titres : <b style="color:#111518">SemiBold</b> · Textes : Regular / Medium</div></div>
{foot(2)}</div>"""
    neg = f("vertical", "negatif")
    col = f("vertical", "couleur")
    p3 = f"""<div class="page">
<div class="kicker">KSC STUDIO · CHARTE GRAPHIQUE</div><h1>Règles d'utilisation</h1>
<div class="pitch">Un logo toujours identique, partout, c'est ce qui le rend reconnaissable et qui donne confiance.</div>
<div class="box" style="left:56px;top:212px;width:470px;height:330px;background:#fff">
  <div style="position:relative;padding:34px;outline:2px dashed #FF741F;outline-offset:0"><img src="{col}" style="display:block;width:250px"></div></div>
<div class="cap" style="left:56px;top:556px;width:470px"><b>Zone de protection</b>Laissez autour du logo au moins la hauteur des lettres de STUDIO : ni texte ni bord de page dans cette marge.</div>
<div class="box" style="left:554px;top:212px;width:470px;height:330px;background:#fff;gap:40px">
  <div style="text-align:center"><img src="{col}" style="width:120px;display:block;margin:0 auto 12px"><span style="font-size:13px;color:#4A4642">25 mm · 120 px</span></div>
  <div style="text-align:center"><img src="{f("initiales", "couleur")}" style="width:60px;display:block;margin:0 auto 12px"><span style="font-size:13px;color:#4A4642">12 mm · 48 px</span></div></div>
<div class="cap" style="left:554px;top:556px;width:470px"><b>Taille minimale</b>En dessous, utilisez les initiales seules, puis le symbole.</div>
<div style="position:absolute;left:56px;top:660px;font-weight:700;font-size:20px">À ne pas faire</div>
<div class="no" style="left:56px;top:702px"><div class="art"><img src="{col}" style="width:110px;transform:scaleX(1.55)"></div><div class="lab"><i>✕</i>Déformer</div></div>
<div class="no" style="left:304px;top:702px"><div class="art"><img src="{col}" style="width:120px;filter:hue-rotate(170deg)"></div><div class="lab"><i>✕</i>Changer les couleurs</div></div>
<div class="no" style="left:552px;top:702px"><div class="art"><img src="{col}" style="width:120px;filter:drop-shadow(6px 6px 2px rgba(0,0,0,.6))"></div><div class="lab"><i>✕</i>Ajouter des effets</div></div>
<div class="no" style="left:800px;top:702px"><div class="art" style="background:url({photo}) center/cover"><img src="{col}" style="width:120px"></div><div class="lab"><i>✕</i>Couleur sur photo</div></div>
<div style="position:absolute;left:56px;top:944px;font-weight:700;font-size:20px">Bons réflexes</div>
<div class="box" style="left:56px;top:986px;width:470px;height:270px;background:url({photo}) center/cover">
  <img src="{neg}" style="position:absolute;right:22px;bottom:20px;width:96px;opacity:.88"></div>
<div class="cap" style="left:554px;top:990px;width:470px;font-size:15px;line-height:1.7">
<b>En filigrane</b>Version négatif, en bas à droite, environ 15 % de la largeur de la photo, opacité 80 à 90 %.<br><br>
<b>Partout le même</b>Même logo sur l'enseigne, les cartes, le site et tous les réseaux : changez toutes les photos de profil le même jour.</div>
{foot(3)}</div>"""
    return [p1, p2, p3]


LISEZ_MOI = """KSC STUDIO · kit du logo (version A · Objectif)
==================================================

Quel fichier utiliser ?
- Imprimeur, enseigne, textile, grands formats : fichiers .pdf ou .svg (vectoriels, agrandissables sans perte).
- Réseaux sociaux, site web, documents, WhatsApp : fichiers .png (fond transparent).

1_logo/
  vertical/     le logo principal : KSC au-dessus de STUDIO
  horizontal/   KSC et STUDIO sur une ligne (bandeaux, site web, enseigne large)
  initiales/    KSC seul, quand la place manque
  symbole/      l'objectif seul (favicon, très petits formats)
  Chaque version existe en 4 couleurs :
    couleur   pour fond blanc ou clair (version principale)
    negatif   pour fond sombre et en filigrane sur les photos
    noir      une seule couleur (tampon, gravure, broderie, impression noir et blanc)
    blanc     une seule couleur sur fond orange ou foncé (textile, adhésif de vitrine)

2_reseaux-sociaux/
  ksc-photo-de-profil.png      Instagram, TikTok, Facebook, WhatsApp (le rond est déjà prévu)
  ksc-couverture-facebook.png  1640 x 624
  ksc-banniere-youtube.png     2560 x 1440
  ksc-modele-story.png         story 1080 x 1920 « Réservez votre séance photo »
  ksc-post-nouveau-logo.png    post 1080 x 1350 pour annoncer le nouveau logo

3_filigrane/   logo à poser sur vos photos : en bas à droite, environ 15 % de la largeur, opacité 80 à 90 %

4_carte-de-visite/
  ksc-carte-de-visite.pdf      2 pages (recto, verso), 85 x 55 mm + 3 mm de fond perdu : à envoyer à l'imprimeur
  ksc-carte-recto.png, ksc-carte-verso.png   aperçus
{carte}

5_site-web/   favicon.ico, icônes 16 à 512 px, apple-touch-icon.png
{video}
KSC_STUDIO_charte-graphique.pdf : versions, couleurs, police, tailles minimales, règles d'utilisation.

Couleurs : orange #FF741F (RVB 255 116 31), noir #111518 (RVB 17 21 24), blanc.
Police : Montserrat (gratuite, usage commercial autorisé : fonts.google.com/specimen/Montserrat).
"""


# ------------------------------------------------------------------ production
def main():
    if KIT.exists():
        shutil.rmtree(KIT)
    tmp = ROOT / ".kit"
    tmp.mkdir(exist_ok=True)
    jobs, files = [], {}

    def save_logo(logo, folder, name, png_w):
        d = KIT / folder
        d.mkdir(parents=True, exist_ok=True)
        svg = d / f"{name}.svg"
        svg.write_text(logo.svg())
        jobs.append(ml.png_job(logo, d / f"{name}.png", round(png_w / logo.aspect)))
        wmm = 150.0
        hmm = wmm / logo.aspect
        page = tmp / f"{name}.html"
        page.write_text(doc(f'<img src="{svg.as_uri()}" style="display:block;width:{wmm}mm;height:{hmm}mm">',
                            f"@page{{size:{wmm}mm {hmm:.3f}mm;margin:0}}", name))
        jobs.append({"file": str(page), "out": str(d / f"{name}.pdf"), "width": 800, "height": 600, "pdf": True})
        return svg

    all_logos = logos()
    for (layout, v), logo in all_logos.items():
        files[(layout, v)] = save_logo(logo, f"1_logo/{layout}", f"ksc-{layout}-{v}", 2000 if layout != "symbole" else 1000)

    # icônes : rond pour les profils, carrés pleins pour les applis et le favicon
    ini_neg = ml.objectif_mark(BLANC, None)
    icon_round = ml.icon(ini_neg[0], ini_neg[1], NOIR, fill_ratio=0.64)
    d = KIT / "1_logo" / "initiales"
    files["icone-ronde"] = d / "ksc-icone-ronde.svg"
    files["icone-ronde"].write_text(icon_round.svg())
    jobs.append(ml.png_job(icon_round, d / "ksc-icone-ronde.png", 1000))
    social_dir = KIT / "2_reseaux-sociaux"
    social_dir.mkdir(parents=True)
    profile = square(ini_neg[0], ini_neg[1], NOIR, 0.64)
    jobs.append(ml.png_job(profile, social_dir / "ksc-photo-de-profil.png", 1080) | {"transparent": False})
    web = KIT / "5_site-web"
    web.mkdir(parents=True)
    sym = symbol(BLANC, False)
    fav = ml.icon(sym[0], sym[1], NOIR, shape="square", fill_ratio=0.72)
    for px in (16, 32, 48):
        jobs.append(ml.png_job(fav, web / f"favicon-{px}.png", px))
    app = square(ini_neg[0], ini_neg[1], NOIR, 0.7)
    for px, name in ((180, "apple-touch-icon.png"), (192, "icon-192.png"), (512, "icon-512.png")):
        jobs.append(ml.png_job(app, web / name, px) | {"transparent": False})

    # photos d'ambiance pour les modèles et la charte
    photo = tmp / "photo.jpg"
    ph.sunset(1200, 1200).save(photo, quality=90)
    for name, (w, h, body) in social(files, photo.as_uri()).items():
        page = tmp / f"{name}.html"
        page.write_text(doc(body, SOCIAL_CSS, name))
        jobs.append({"file": str(page), "out": str(social_dir / name), "width": w, "height": h})

    # filigranes
    wm = KIT / "3_filigrane"
    wm.mkdir(parents=True)
    for v in ("negatif", "blanc"):
        logo = all_logos[("vertical", v)]
        jobs.append(ml.png_job(logo, wm / f"ksc-filigrane-{v}.png", round(1500 / logo.aspect)))

    # carte de visite
    cd = KIT / "4_carte-de-visite"
    cd.mkdir(parents=True)
    recto, verso = card(files)
    page = tmp / "carte.html"
    page.write_text(doc(recto + verso, CARD_CSS, "KSC STUDIO · carte de visite"))
    jobs.append({"file": str(page), "out": str(cd / "ksc-carte-de-visite.pdf"), "width": 344, "height": 230, "pdf": True})
    for side, html in (("recto", recto), ("verso", verso)):
        page = tmp / f"carte-{side}.html"
        page.write_text(doc(html, CARD_CSS, side))
        jobs.append({"file": str(page), "out": str(cd / f"ksc-carte-{side}.png"), "width": 344, "height": 230, "scale": 3.125})

    # charte graphique
    pages = charte(files, photo.as_uri())
    page = tmp / "charte.html"
    page.write_text(doc("".join(pages), CHARTE_CSS, "KSC STUDIO · charte graphique"))
    jobs.append({"file": str(page), "out": str(KIT / "KSC_STUDIO_charte-graphique.pdf"), "width": 1080, "height": 1350, "pdf": True})
    prev = ROOT / "planches" / "kit"
    prev.mkdir(parents=True, exist_ok=True)
    for k, body in enumerate(pages, 1):
        page = tmp / f"charte-{k}.html"
        page.write_text(doc(body, CHARTE_CSS, f"charte {k}"))
        jobs.append({"file": str(page), "out": str(prev / f"ksc-charte-{k}.png"), "width": 1080, "height": 1350, "scale": 2})

    ml.render(jobs)
    # favicon.ico multi-tailles
    ico = [Image.open(web / f"favicon-{px}.png") for px in (16, 32, 48)]
    ico[2].save(web / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)], append_images=ico[:2])
    shutil.rmtree(tmp)
    package()


def package():
    """Intro vidéo, LISEZ-MOI et archive à télécharger, sans refaire les autres fichiers du kit."""
    video = ""
    if INTRO.exists():
        d = KIT / "6_video"
        d.mkdir(exist_ok=True)
        shutil.copy2(INTRO, d / "ksc-intro-logo.mp4")
        video = ("\n6_video/      ksc-intro-logo.mp4 : intro animée du logo, 3 s avec le son, verticale 1080 x 1920,\n"
                 "              à placer au début de vos Reels, TikTok et stories\n")
    note = ("  ATTENTION : la carte contient des coordonnées d'exemple (en gris) ; la version finale\n"
            "  sera faite avec vos vraies coordonnées.") if PLACEHOLDER else ""
    (KIT / "LISEZ-MOI.txt").write_text(LISEZ_MOI.format(carte=note, video=video), encoding="utf-8")

    ZIP.unlink(missing_ok=True)
    with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(KIT.rglob("*")):
            if f.is_file():
                z.write(f, Path("KSC_STUDIO_kit_logo") / f.relative_to(KIT))
    n = sum(1 for f in KIT.rglob("*") if f.is_file())
    print(f"{n} fichiers dans {KIT}, archive {ZIP} ({ZIP.stat().st_size / 1e6:.1f} Mo)")


if __name__ == "__main__":
    package() if "--paquet" in sys.argv else main()
