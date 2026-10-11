"""Génère les images provisoires (SVG) de assets/photos/.

Chaque fichier occupe la place d'une vraie photo : remplace-le par ton image
(même nom, extension .jpg/.png) et change l'extension dans index.html.
Usage : python3 tools/make_placeholders.py
"""
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets" / "photos"
OUT.mkdir(parents=True, exist_ok=True)

# Silhouette de voiture de sport (vue de profil) dans une boîte 400×140.
CAR = (
    "M12,108 L28,84 Q60,72 118,64 L168,42 Q198,30 248,32 L302,52 "
    "Q360,58 386,74 L394,100 L382,112 L344,112 A26,26 0 0 0 292,112 "
    "L118,112 A26,26 0 0 0 66,112 Z"
)


def car(x, y, s, color, opacity=1.0):
    return (
        f'<g transform="translate({x} {y}) scale({s})" opacity="{opacity}">'
        f'<path d="{CAR}" fill="{color}"/>'
        f'<path d="M176,46 L206,38 L246,38 L286,56 L176,60 Z" fill="#000" opacity=".35"/>'
        f'<circle cx="92" cy="112" r="22" fill="#111"/><circle cx="92" cy="112" r="10" fill="#777"/>'
        f'<circle cx="318" cy="112" r="22" fill="#111"/><circle cx="318" cy="112" r="10" fill="#777"/>'
        "</g>"
    )


def person(x, y, s, color):
    return (
        f'<g transform="translate({x} {y}) scale({s})">'
        f'<circle cx="0" cy="0" r="34" fill="#e8c3a0"/>'
        f'<path d="M-62,190 Q-60,60 0,52 Q60,60 62,190 Z" fill="{color}"/>'
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


# Grille du profil (tuiles carrées 600×600)
tiles = [
    ("grid-01", "#2b3440", "#0e1116", car(100, 300, 1.0, "#d9dde3"), "Nissan GT-R"),
    ("grid-02", "#3a2a22", "#120c0a", person(300, 230, 1.6, "#22324f"), "client + clés"),
    ("grid-03", "#1d2633", "#090b0f", car(100, 300, 1.0, "#1f4fa8"), "arrivage"),
    ("grid-04", "#3b3b3b", "#121212", car(100, 300, 1.0, "#f2f2f2"), "Porsche blanche"),
    ("grid-05", "#4a1a1d", "#160809", car(100, 300, 1.0, "#e11d2a"), "Boxster S rouge"),
    ("grid-06", "#2e3a2a", "#0c100b", person(300, 230, 1.6, "#d8c8b0"), "livraison"),
]
for name, a, b, body, label in tiles:
    svg(name, 600, 600, a, b, body, label)

# Reel : Boxster rouge devant « LA CAGE », parasols rouges, deux personnes
reel_body = (
    '<rect x="0" y="380" width="1080" height="700" fill="#cfc6b8"/>'
    '<text x="540" y="520" fill="#2b2b2b" font-family="sans-serif" font-weight="700" font-size="96" text-anchor="middle">LA CAGE</text>'
    '<path d="M120,760 L260,690 L400,760 Z" fill="#c8141f"/><path d="M680,760 L820,690 L960,760 Z" fill="#c8141f"/>'
    + person(330, 980, 2.2, "#d8c3a2")
    + person(760, 980, 2.2, "#3c6fb5")
    + car(40, 1280, 2.5, "#e11d2a")
    + '<rect x="0" y="1630" width="1080" height="290" fill="#55504a"/>'
)
svg("reel-boxster", 1080, 1920, "#9fb4c8", "#3d3a36", reel_body, "reel-boxster.jpg (vidéo du reel, 9:16)")

# Photo reçue dans le DM : homme en blazer marine, Porsche rouge en showroom
dm_body = (
    '<rect x="0" y="560" width="900" height="340" fill="#d9d9d9"/>'
    + car(380, 640, 1.3, "#e11d2a")
    + person(260, 330, 2.6, "#1d2b4a")
)
svg("dm-showroom", 900, 900, "#f1efe9", "#bdbab3", dm_body, "dm-showroom.jpg")

# Plan cinéma : Porsche 911 gris-bleu à contre-jour doré (à remplacer par la vidéo)
cine_body = (
    '<circle cx="540" cy="860" r="420" fill="#ffcf7a" opacity=".55"/>'
    '<rect x="0" y="1180" width="1080" height="740" fill="#1a1612"/>'
    + car(40, 1000, 2.5, "#7d8fa3")
    + '<rect x="40" y="1300" width="1000" height="60" fill="#ffcf7a" opacity=".18"/>'
)
svg("cinema-911", 1080, 1920, "#1b120c", "#6b4a22", cine_body, "cinema-911.mp4 (vidéo plein écran)")

# Livraison : Porsche 718 Spyder bleue devant le garage, couple + vendeur
liv_body = (
    '<rect x="0" y="260" width="900" height="560" fill="#f3f3f3"/>'
    '<rect x="0" y="230" width="900" height="50" fill="#1f5fa8"/>'
    '<text x="450" y="380" fill="#c8141f" font-family="sans-serif" font-weight="900" font-size="64" text-anchor="middle">4ROUES</text>'
    + person(150, 640, 1.7, "#e7d9c4")
    + person(260, 640, 1.7, "#2f3b54")
    + person(760, 640, 1.7, "#151a24")
    + car(220, 870, 1.25, "#2366c8")
    + '<rect x="0" y="1040" width="900" height="160" fill="#5c5a57"/>'
)
svg("livraison-718", 900, 1200, "#a9c6e4", "#6d6b68", liv_body, "livraison-718.jpg")

# Boxster rouge « 3D » vue de 3/4 (à remplacer par un rendu PNG détouré)
box_body = car(20, 40, 1.4, "#e11d2a")
(OUT / "boxster-3d.svg").write_text(
    '<svg xmlns="http://www.w3.org/2000/svg" width="600" height="240" viewBox="0 0 600 240">'
    f"{box_body}"
    '<text x="300" y="232" fill="#fff" opacity=".7" font-family="sans-serif" font-size="18" text-anchor="middle">'
    "PLACEHOLDER · boxster-3d.png (détouré)</text></svg>\n"
)

# Main + clé 3 boutons (à remplacer par une photo PNG détourée)
(OUT / "main-cle.svg").write_text(
    """<svg xmlns="http://www.w3.org/2000/svg" width="520" height="620" viewBox="0 0 520 620">
<path d="M520,430 L330,430 Q280,430 270,390 L250,300 Q245,270 275,268 Q300,268 308,300 L318,340 L520,330 Z" fill="#d9a77f"/>
<rect x="300" y="420" width="220" height="200" rx="40" fill="#1b2235"/>
<line x1="200" y1="40" x2="236" y2="186" stroke="#c9c9c9" stroke-width="10"/>
<circle cx="196" cy="34" r="22" fill="none" stroke="#c9c9c9" stroke-width="8"/>
<rect x="160" y="180" width="150" height="250" rx="64" fill="#121214"/>
<circle cx="235" cy="250" r="22" fill="#2a2a2e"/><circle cx="235" cy="315" r="22" fill="#2a2a2e"/>
<circle cx="235" cy="380" r="22" fill="#e11d2a"/>
<text x="260" y="600" fill="#fff" opacity=".7" font-family="sans-serif" font-size="18" text-anchor="middle">PLACEHOLDER · main-cle.png</text>
</svg>
"""
)
print("ok", sorted(p.name for p in OUT.iterdir()))
