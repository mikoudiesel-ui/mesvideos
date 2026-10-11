"""Génère les images provisoires (SVG) de assets/photos/ pour la pub @daya_na990.

Chaque fichier occupe la place d'une vraie photo ou vidéo de la boutique : remplace-le
par ton image (même nom, extension .jpg/.png/.mp4) et change l'extension dans index.html.
Usage : python3 tools/make_placeholders.py
"""
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets" / "photos"
OUT.mkdir(parents=True, exist_ok=True)


def bikini(x, y, s, color, accent="#fff"):
    """Haut + bas de bikini (vue à plat) dans une boîte d'environ 300×330."""
    return (
        f'<g transform="translate({x} {y}) scale({s})">'
        # bretelles + haut
        f'<path d="M60,10 L100,90 M240,10 L200,90" stroke="{color}" stroke-width="8" fill="none"/>'
        f'<path d="M30,140 Q40,70 100,70 Q140,80 150,130 Q160,80 200,70 Q260,70 270,140 Q200,170 150,140 Q100,170 30,140 Z" fill="{color}"/>'
        f'<path d="M30,140 Q0,150 -20,140 M270,140 Q300,150 320,140" stroke="{color}" stroke-width="7" fill="none"/>'
        f'<circle cx="150" cy="132" r="7" fill="{accent}"/>'
        # bas
        f'<path d="M40,220 L260,220 Q240,250 190,290 Q160,320 150,330 Q140,320 110,290 Q60,250 40,220 Z" fill="{color}"/>'
        f'<path d="M40,220 Q10,215 -10,225 M260,220 Q290,215 310,225" stroke="{color}" stroke-width="7" fill="none"/>'
        "</g>"
    )


def person(x, y, s, top, skin="#c68863"):
    return (
        f'<g transform="translate({x} {y}) scale({s})">'
        f'<path d="M-30,-10 Q-40,-60 0,-62 Q40,-60 30,-10 L36,40 L-36,40 Z" fill="#2b1d1a"/>'
        f'<circle cx="0" cy="0" r="32" fill="{skin}"/>'
        f'<path d="M-50,190 Q-56,60 0,50 Q56,60 50,190 Z" fill="{skin}"/>'
        f'<path d="M-38,92 Q0,110 38,92 L36,118 Q0,128 -36,118 Z" fill="{top}"/>'
        f'<path d="M-40,168 L40,168 L22,196 L-22,196 Z" fill="{top}"/>'
        "</g>"
    )


def svg(name, w, h, top, bottom, body, label):
    fs = max(18, w // 26)
    doc = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
<defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="{top}"/><stop offset="1" stop-color="{bottom}"/></linearGradient></defs>
<rect width="{w}" height="{h}" fill="url(#g)"/>
{body}
<rect x="{fs}" y="{h - fs * 3.2:.0f}" width="{w - fs * 2}" height="{fs * 2.2:.0f}" rx="{fs * 0.5:.0f}" fill="#000" opacity=".45"/>
<text x="{w / 2:.0f}" y="{h - fs * 1.75:.0f}" fill="#fff" opacity=".85" font-family="sans-serif" font-size="{fs}" text-anchor="middle">PLACEHOLDER · {label}</text>
</svg>
"""
    (OUT / f"{name}.svg").write_text(doc)


SEA = '<rect x="0" y="{y}" width="{w}" height="{h}" fill="#3ccfcf"/>'

# Grille du profil TikTok (tuiles 3:4, 600×800)
tiles = [
    ("grid-01", "#ffd9c7", "#ffb79f", bikini(150, 220, 1.0, "#ff4f70"), "bikini corail"),
    ("grid-02", "#bfeee9", "#3ccfcf", person(300, 300, 1.7, "#ffc93c"), "porté plage"),
    ("grid-03", "#fff0c2", "#f3d3a4", bikini(150, 220, 1.0, "#16a6a0"), "bikini turquoise"),
    ("grid-04", "#2a1b3d", "#4a2f63", bikini(150, 220, 1.0, "#ffc93c", "#2a1b3d"), "bikini soleil"),
    ("grid-05", "#ffe3d0", "#ff8fa6", bikini(150, 220, 1.0, "#e23a5c"), "bikini corail (vidéo)"),
    ("grid-06", "#d3f0ea", "#a9d98c", person(300, 300, 1.7, "#ff4f70"), "essayage"),
]
for name, a, b, body, label in tiles:
    svg(name, 600, 800, a, b, body, label)

# Vidéo TikTok mise en avant (9:16) : modèle en bikini corail à la plage
vid_body = (
    '<circle cx="800" cy="420" r="150" fill="#ffc93c" opacity=".9"/>'
    '<rect x="0" y="900" width="1080" height="260" fill="#3ccfcf"/>'
    '<rect x="0" y="1140" width="1080" height="780" fill="#f3d3a4"/>'
    + person(540, 820, 3.6, "#ff4f70", "#c68863")
)
svg("tiktok-bikini", 1080, 1920, "#ffb79f", "#ffe3d0", vid_body, "tiktok-bikini.mp4 (vidéo TikTok, 9:16)")

# Photo reçue dans le DM : bikini posé à plat
svg("dm-bikini", 900, 900, "#fff4e8", "#ffe3d0", bikini(300, 260, 1.0, "#ff4f70"), "dm-bikini.jpg")

# Plan cinéma : plage au coucher du soleil (à remplacer par une vidéo)
cine_body = (
    '<circle cx="540" cy="900" r="300" fill="#ffc93c" opacity=".85"/>'
    '<rect x="0" y="980" width="1080" height="300" fill="#e2765f" opacity=".85"/>'
    '<rect x="0" y="1260" width="1080" height="660" fill="#e2b47e"/>'
    + person(540, 1060, 3.4, "#ff4f70", "#8d5a3b")
)
svg("cinema-plage", 1080, 1920, "#2a1b3d", "#ff8a6b", cine_body, "cinema-plage.mp4 (vidéo plein écran)")

# Livraison : la cliente reçoit son colis à la porte
liv_body = (
    '<rect x="520" y="240" width="300" height="800" rx="10" fill="#1fa5a1"/>'
    '<circle cx="790" cy="660" r="12" fill="#ffc93c"/>'
    '<rect x="0" y="1040" width="900" height="160" fill="#f1e4d2"/>'
    + person(670, 640, 2.0, "#ff4f70", "#e9b48f")
    + '<rect x="250" y="760" width="230" height="170" rx="10" fill="#d9a066"/>'
    '<rect x="250" y="800" width="230" height="20" fill="#ff4f70"/>'
    + person(250, 640, 2.0, "#2c3e6b", "#8d5a3b")
)
svg("livraison-colis", 900, 1200, "#ffe3d0", "#fff0c2", liv_body, "livraison-colis.jpg")

# Bikini « 3D » détouré (vue éclatée)
(OUT / "bikini-3d.svg").write_text(
    '<svg xmlns="http://www.w3.org/2000/svg" width="600" height="420" viewBox="0 0 600 420">'
    + bikini(150, 20, 1.05, "#ff4f70")
    + '<text x="300" y="412" fill="#fff" opacity=".7" font-family="sans-serif" font-size="18" text-anchor="middle">'
    "PLACEHOLDER · bikini-3d.png (détouré)</text></svg>\n"
)

# Main qui tient le colis kraft (à remplacer par une photo PNG détourée)
(OUT / "main-colis.svg").write_text(
    """<svg xmlns="http://www.w3.org/2000/svg" width="520" height="620" viewBox="0 0 520 620">
<rect x="110" y="170" width="300" height="230" rx="14" fill="#d9a066"/>
<path d="M110,170 L170,120 L470,120 L410,170 Z" fill="#e8b67c"/>
<path d="M410,170 L470,120 L470,350 L410,400 Z" fill="#c08547"/>
<rect x="110" y="250" width="300" height="34" fill="#ff4f70"/>
<path d="M410,250 L470,200 L470,234 L410,284 Z" fill="#e23a5c"/>
<path d="M240,120 Q260,60 300,80 Q320,110 280,124 M300,120 Q340,70 370,100 Q370,124 330,124" stroke="#ff4f70" stroke-width="10" fill="none"/>
<path d="M520,470 L330,470 Q280,470 270,430 L262,390 Q258,370 290,370 L520,370 Z" fill="#c68863"/>
<text x="260" y="600" fill="#fff" opacity=".7" font-family="sans-serif" font-size="18" text-anchor="middle">PLACEHOLDER · main-colis.png</text>
</svg>
"""
)
print("ok", sorted(p.name for p in OUT.iterdir()))
