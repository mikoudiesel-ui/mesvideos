#!/usr/bin/env python3
"""Propositions de logo pour KSC STUDIO (studio photo), construites sur les initiales K S C.

Chaque piste est dessinée en vectoriel : le texte est converti en tracés à partir de polices libres
(licence SIL OFL 1.1, utilisables commercialement, voir fonts/), si bien que les SVG s'ouvrent partout
(Illustrator, Inkscape, Canva, imprimeur) sans police à installer. Couleurs de départ relevées sur le
logo actuel : orange #FF741F et noir #111518.

    python3 -I brand/ksc-studio/tools/make_logos.py
    → brand/ksc-studio/logos/<piste>/*.svg et *.png
"""

import argparse
import json
import math
import os
import subprocess
from dataclasses import dataclass
from pathlib import Path

from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parent.parent
ORANGE = "#FF741F"  # relevé sur le logo actuel
ORANGE_FONCE = "#D9560B"
NOIR = "#111518"
BLANC = "#FFFFFF"
IVOIRE = "#F7F2EA"
OR = "#C9A45C"  # or champagne de la piste Couture


def n(v):
    return f"{v:.2f}".rstrip("0").rstrip(".")


def pt(p):
    return f"{n(p[0])},{n(p[1])}"


def union(*boxes):
    return (min(b[0] for b in boxes), min(b[1] for b in boxes), max(b[2] for b in boxes), max(b[3] for b in boxes))


# ------------------------------------------------------------------ texte vectorisé
class Font:
    def __init__(self, name):
        self.tt = TTFont(ROOT / "fonts" / f"{name}.ttf")
        self.gs = self.tt.getGlyphSet()
        self.cmap = self.tt.getBestCmap()
        self.upm = self.tt["head"].unitsPerEm
        self.cap = self.tt["OS/2"].sCapHeight / self.upm  # hauteur de capitale en em

    def adv(self, ch):
        return self.tt["hmtx"][self.cmap[ord(ch)]][0]

    def bounds(self, ch):
        p = BoundsPen(self.gs)
        self.gs[self.cmap[ord(ch)]].draw(p)
        return p.bounds

    def draw(self, ch, matrix):
        """Contour du glyphe en chemin SVG ; `matrix` (a, b, c, d, e, f) part des unités de la police."""
        pen = SVGPathPen(self.gs, ntos=lambda v: n(v))
        self.gs[self.cmap[ord(ch)]].draw(TransformPen(pen, matrix))
        return pen.getCommands()


_FONTS = {}


def font(name):
    if name not in _FONTS:
        _FONTS[name] = Font(name)
    return _FONTS[name]


class Line:
    """Une ligne de texte : positions des glyphes, boîtes d'encre ; y vers le bas, ligne de base en 0."""

    def __init__(self, f, text, size, tracking=0.0, kern=None):
        self.f, self.text, self.size = f, text, size
        s = size / f.upm
        x = 0.0
        self.glyphs = []  # (caractère, origine x, boîte d'encre)
        for i, ch in enumerate(text):
            if ch != " ":
                b = f.bounds(ch)
                self.glyphs.append((ch, x, (x + b[0] * s, -b[3] * s, x + b[2] * s, -b[1] * s)))
            x += f.adv(ch) * s
            if i + 1 < len(text):
                x += tracking * size + (kern or {}).get(text[i:i + 2], 0.0) * size
        self.ink = union(*[g[2] for g in self.glyphs])
        self.dx = self.dy = 0.0

    @property
    def width(self):
        return self.ink[2] - self.ink[0]

    @property
    def height(self):
        return self.ink[3] - self.ink[1]

    def place(self, left=None, cx=None, right=None, baseline=None, top=None, cy=None, bottom=None):
        """Place la boîte d'encre ; renvoie la boîte placée."""
        if cx is not None:
            self.dx = cx - (self.ink[0] + self.ink[2]) / 2
        elif left is not None:
            self.dx = left - self.ink[0]
        elif right is not None:
            self.dx = right - self.ink[2]
        if baseline is not None:
            self.dy = baseline
        elif top is not None:
            self.dy = top - self.ink[1]
        elif cy is not None:
            self.dy = cy - (self.ink[1] + self.ink[3]) / 2
        elif bottom is not None:
            self.dy = bottom - self.ink[3]
        return self.box

    @property
    def box(self):
        return (self.ink[0] + self.dx, self.ink[1] + self.dy, self.ink[2] + self.dx, self.ink[3] + self.dy)

    def gbox(self, i):
        b = self.glyphs[i][2]
        return (b[0] + self.dx, b[1] + self.dy, b[2] + self.dx, b[3] + self.dy)

    def path(self, only=None):
        s = self.size / self.f.upm
        return "".join(self.f.draw(ch, (s, 0, 0, -s, x + self.dx, self.dy))
                       for i, (ch, x, _) in enumerate(self.glyphs) if only is None or i in only)


def fit(f, text, size, width):
    """Interlettrage (en fraction de la taille) qui donne à la ligne la largeur d'encre voulue."""
    w0 = Line(f, text, size).width
    return (width - w0) / ((len(text) - 1) * size)


def p(d, fill, extra=""):
    return f'<path d="{d}" fill="{fill}"{extra}/>'


@dataclass
class Logo:
    body: str
    box: tuple
    defs: str = ""
    margin: float = 0.08  # marge autour du dessin, en fraction de la plus grande dimension

    def svg(self):
        x0, y0, x1, y1 = self.box
        m = self.margin * max(x1 - x0, y1 - y0)
        vx, vy, vw, vh = x0 - m, y0 - m, x1 - x0 + 2 * m, y1 - y0 + 2 * m
        defs = f"<defs>{self.defs}</defs>" if self.defs else ""
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{n(vx)} {n(vy)} {n(vw)} {n(vh)}" '
                f'width="{n(vw)}" height="{n(vh)}">{defs}{self.body}</svg>')

    @property
    def aspect(self):
        x0, y0, x1, y1 = self.box
        m = self.margin * max(x1 - x0, y1 - y0)
        return (x1 - x0 + 2 * m) / (y1 - y0 + 2 * m)


def icon(content, box, bg, shape="circle", fill_ratio=0.62, defs=""):
    """Icône carrée (avatar) : le dessin `content` (boîte `box`) centré sur un disque ou un carré arrondi."""
    D = 1000.0
    w, h = box[2] - box[0], box[3] - box[1]
    k = fill_ratio * D / max(w, h)
    tx, ty = D / 2 - k * (box[0] + box[2]) / 2, D / 2 - k * (box[1] + box[3]) / 2
    back = (f'<circle cx="{n(D / 2)}" cy="{n(D / 2)}" r="{n(D / 2)}" fill="{bg}"/>' if shape == "circle"
            else f'<rect width="{n(D)}" height="{n(D)}" rx="{n(D * 0.22)}" fill="{bg}"/>')
    return Logo(back + f'<g transform="matrix({n(k)} 0 0 {n(k)} {n(tx)} {n(ty)})">{content}</g>', (0, 0, D, D), defs, margin=0)


# ------------------------------------------------------------------ piste 1 : Objectif
def lens_c(cx, cy, Ro, t, gap_deg, ring, lens, pupil, glint, gap=None):
    """C dessiné comme un objectif : anneau ouvert à droite, verre orange, pupille, reflets."""
    a = math.radians(gap_deg / 2)
    Ri = Ro - t
    P = lambda r, th: (cx + r * math.cos(th), cy + r * math.sin(th))  # noqa: E731
    d = (f"M{pt(P(Ro, a))} A{n(Ro)},{n(Ro)} 0 1 1 {pt(P(Ro, -a))} L{pt(P(Ri, -a))} "
         f"A{n(Ri)},{n(Ri)} 0 1 0 {pt(P(Ri, a))} Z")
    Rl = Ri - (0.21 * t if gap is None else gap)  # blanc entre l'anneau et le verre
    Rp = 0.46 * Rl
    rg = (Rl + Rp) / 2
    a1, a2 = math.radians(196), math.radians(244)
    out = p(d, ring)
    out += f'<circle cx="{n(cx)}" cy="{n(cy)}" r="{n(Rl)}" fill="{lens}"/>'
    out += f'<circle cx="{n(cx)}" cy="{n(cy)}" r="{n(Rp)}" fill="{pupil}"/>'
    out += (f'<path d="M{pt(P(rg, a1))} A{n(rg)},{n(rg)} 0 0 1 {pt(P(rg, a2))}" fill="none" stroke="{glint}" '
            f'stroke-width="{n(0.3 * (Rl - Rp))}" stroke-linecap="round"/>')
    gx, gy = P(rg, math.radians(266))
    out += f'<circle cx="{n(gx)}" cy="{n(gy)}" r="{n(0.17 * (Rl - Rp))}" fill="{glint}"/>'
    return out, (cx - Ro, cy - Ro, cx + Ro, cy + Ro)


def objectif_mark(ink, studio):
    f = font("montserrat-800")
    F = 400.0
    word = Line(f, "KSC", F, kern={"KS": -0.01, "SC": 0.035})
    word.place(left=0, baseline=0)
    cb = word.gbox(2)
    Ro = (cb[3] - cb[1]) / 2
    lens, lbox = lens_c(cb[0] + Ro, (cb[1] + cb[3]) / 2, Ro, 0.19 * F, 78, ink, ORANGE, NOIR, BLANC)
    body = p(word.path(only={0, 1}), ink) + lens
    top = union(word.gbox(0), word.gbox(1), lbox)
    out = [body, top]
    if studio:
        g = font("montserrat-700")
        size = 0.36 * F
        st = Line(g, "STUDIO", size, tracking=fit(g, "STUDIO", size, top[2] - top[0]))
        st.place(left=top[0], top=top[3] + 0.17 * f.cap * F)
        out = [body + p(st.path(), studio), union(top, st.box)]
    return out


def objectif():
    clair = objectif_mark(NOIR, ORANGE)
    sombre = objectif_mark(BLANC, ORANGE)
    mono = objectif_mark(BLANC, None)
    return {
        "clair": Logo(*clair),
        "sombre": Logo(*sombre),
        "icone": icon(mono[0], mono[1], NOIR, fill_ratio=0.64),
    }


# ------------------------------------------------------------------ piste 2 : Viseur
def focus_frame(box, cap, sw, accent, dot):
    """Repères de mise au point autour de `box`, et le point de mise au point dans le coin haut droit."""
    x0, y0, x1, y1 = box[0] - 0.62 * cap, box[1] - 0.52 * cap, box[2] + 0.62 * cap, box[3] + 0.52 * cap
    arm = 0.36 * cap
    d = (f"M{n(x0)},{n(y0 + arm)} L{n(x0)},{n(y0)} L{n(x0 + arm)},{n(y0)} "
         f"M{n(x1 - arm)},{n(y0)} L{n(x1)},{n(y0)} L{n(x1)},{n(y0 + arm)} "
         f"M{n(x1)},{n(y1 - arm)} L{n(x1)},{n(y1)} L{n(x1 - arm)},{n(y1)} "
         f"M{n(x0 + arm)},{n(y1)} L{n(x0)},{n(y1)} L{n(x0)},{n(y1 - arm)}")
    body = f'<path d="{d}" fill="none" stroke="{accent}" stroke-width="{n(sw)}" stroke-linejoin="miter"/>'
    if dot:
        body += f'<circle cx="{n(x1 - arm * 0.62)}" cy="{n(y0 + arm * 0.62)}" r="{n(0.05 * cap)}" fill="{accent}"/>'
    return body, (x0 - sw / 2, y0 - sw / 2, x1 + sw / 2, y1 + sw / 2)


def viseur_mark(ink, accent, tagline):
    f = font("jost-400")
    F = 300.0
    cap = f.cap * F
    word = Line(f, "KSC", F, tracking=0.17)
    box = word.place(cx=0, cy=0)
    body, frame = focus_frame(box, cap, 0.07 * F, accent, dot=True)
    body += p(word.path(), ink)
    if not tagline:
        return body, frame
    g = font("jost-500")
    t = Line(g, "STUDIO PHOTO", 0.15 * F, tracking=0.5)
    t.place(cx=0, top=frame[3] + 0.42 * cap)
    return body + p(t.path(), tagline), union(frame, t.box)


def viseur():
    clair = viseur_mark(NOIR, ORANGE, NOIR)
    sombre = viseur_mark(BLANC, ORANGE, BLANC)
    mono = viseur_mark(BLANC, ORANGE, None)
    return {
        "clair": Logo(*clair),
        "sombre": Logo(*sombre),
        "icone": icon(mono[0], mono[1], NOIR, fill_ratio=0.66),
    }


# ------------------------------------------------------------------ piste 3 : Couture
def couture_mark(ink, wordmark):
    """Monogramme de maison de couture : capitales Didot italiques, S en vedette, K bas et C haut."""
    Fs = 600.0
    it = font("bodoni-moda-500i")
    s = Line(it, "S", Fs)
    sb = s.place(cx=0, cy=0)
    k, c = Line(it, "K", 0.66 * Fs), Line(it, "C", 0.66 * Fs)
    cap = sb[3] - sb[1]
    kb = k.place(right=sb[0] + 0.03 * k.width, cy=0.045 * cap)
    cb = c.place(left=sb[2] - 0.02 * c.width, cy=-0.045 * cap)
    mono = union(sb, kb, cb)
    R = 0.57 * (mono[2] - mono[0])
    sh = -(mono[0] + mono[2]) / 2  # centre optique du monogramme dans le cercle
    body = (f'<g transform="translate({n(sh)} 0)">{p(k.path(), ink)}{p(s.path(), ink)}{p(c.path(), ink)}</g>'
            f'<circle cx="0" cy="0" r="{n(R)}" fill="none" stroke="{ink}" stroke-width="{n(0.006 * Fs)}"/>')
    box = (-R - 0.003 * Fs, -R - 0.003 * Fs, R + 0.003 * Fs, R + 0.003 * Fs)
    if not wordmark:
        return body, box
    w = Line(font("bodoni-moda-500"), "KSC STUDIO", 0.17 * Fs, tracking=0.3)
    wb = w.place(cx=0, top=box[3] + 0.16 * Fs)
    rule_y = wb[3] + 0.09 * Fs
    t = Line(font("jost-400"), "PHOTOGRAPHIE", 0.07 * Fs, tracking=0.62)
    tb = t.place(cx=0, top=rule_y + 0.09 * Fs)
    body += p(w.path(), ink) + p(t.path(), ink)
    body += (f'<line x1="{n(-0.09 * Fs)}" y1="{n(rule_y)}" x2="{n(0.09 * Fs)}" y2="{n(rule_y)}" '
             f'stroke="{ink}" stroke-width="{n(0.004 * Fs)}"/>')
    return body, union(box, wb, tb)


def couture():
    mono = couture_mark(OR, False)
    return {
        "clair": Logo(*couture_mark(NOIR, True)),
        "sombre": Logo(*couture_mark(OR, True)),
        "icone": icon(mono[0], mono[1], NOIR, fill_ratio=0.8),
    }


# ------------------------------------------------------------------ piste 4 : Signature
def swash(x0, x1, y, h, wmax, color, samples=80):
    """Trait calligraphique effilé (épais au milieu, fin aux extrémités), légèrement montant."""
    P0, P1, P2, P3 = (x0, y + 0.55 * h), (x0 + 0.32 * (x1 - x0), y + 1.15 * h), (x0 + 0.7 * (x1 - x0), y - 0.05 * h), (x1, y - 0.6 * h)
    left, right = [], []
    for i in range(samples + 1):
        t = i / samples
        bx = (1 - t) ** 3 * P0[0] + 3 * (1 - t) ** 2 * t * P1[0] + 3 * (1 - t) * t ** 2 * P2[0] + t ** 3 * P3[0]
        by = (1 - t) ** 3 * P0[1] + 3 * (1 - t) ** 2 * t * P1[1] + 3 * (1 - t) * t ** 2 * P2[1] + t ** 3 * P3[1]
        dx = 3 * (1 - t) ** 2 * (P1[0] - P0[0]) + 6 * (1 - t) * t * (P2[0] - P1[0]) + 3 * t ** 2 * (P3[0] - P2[0])
        dy = 3 * (1 - t) ** 2 * (P1[1] - P0[1]) + 6 * (1 - t) * t * (P2[1] - P1[1]) + 3 * t ** 2 * (P3[1] - P2[1])
        ln = math.hypot(dx, dy)
        w = wmax * math.sin(math.pi * t) ** 0.75 / 2
        left.append((bx - dy / ln * w, by + dx / ln * w))
        right.append((bx + dy / ln * w, by - dx / ln * w))
    pts = left + right[::-1]
    return p("M" + " L".join(pt(q) for q in pts) + " Z", color), (x0, y - 0.6 * h - wmax, x1, y + 1.15 * h + wmax)


SCRIPT = ("corinthia-700", {"KS": -0.02, "SC": -0.03})


def signature_mark(ink, accent, tagline, script=SCRIPT):
    name, kern = script
    f = font(name)
    F = 420.0
    word = Line(f, "KSC", F, kern=kern)
    wb = word.place(left=0, baseline=0)
    body = p(word.path(), ink)
    sw, swb = swash(wb[0] + 0.1 * word.width, wb[2] + 0.03 * word.width, 0.17 * F, 0.1 * F, 0.036 * F, accent)
    body += sw
    box = union(wb, swb)
    if not tagline:
        return body, box
    t = Line(font("jost-400"), "STUDIO PHOTO", 0.085 * F, tracking=0.55)
    tb = t.place(right=wb[2], top=swb[3] + 0.1 * F)
    return body + p(t.path(), tagline), union(box, tb)


def signature():
    clair = signature_mark(NOIR, ORANGE, NOIR)
    sombre = signature_mark(BLANC, ORANGE, BLANC)
    mono = signature_mark(BLANC, ORANGE, None)
    return {
        "clair": Logo(*clair),
        "sombre": Logo(*sombre),
        "icone": icon(mono[0], mono[1], NOIR, fill_ratio=0.7),
    }


# ------------------------------------------------------------------ piste 5 : Planche contact
def lens_disc(cx, cy, R, lens, pupil, glint):
    Rp = 0.46 * R
    rg = (R + Rp) / 2
    P = lambda r, a: (cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a)))  # noqa: E731
    out = f'<circle cx="{n(cx)}" cy="{n(cy)}" r="{n(R)}" fill="{lens}"/><circle cx="{n(cx)}" cy="{n(cy)}" r="{n(Rp)}" fill="{pupil}"/>'
    out += (f'<path d="M{pt(P(rg, 196))} A{n(rg)},{n(rg)} 0 0 1 {pt(P(rg, 244))}" fill="none" stroke="{glint}" '
            f'stroke-width="{n(0.3 * (R - Rp))}" stroke-linecap="round"/>')
    gx, gy = P(rg, 266)
    return out + f'<circle cx="{n(gx)}" cy="{n(gy)}" r="{n(0.17 * (R - Rp))}" fill="{glint}"/>'


def contact_tile(cell, letter, D=600.0):
    """Carré 2×2 façon planche contact : K, S, C puis l'objectif."""
    g = 0.05 * D
    c = (D - g) / 2
    r = 0.045 * D
    f = font("montserrat-800")
    out = ""
    for i, ch in enumerate("KSC "):
        x, y = (i % 2) * (c + g), (i // 2) * (c + g)
        if ch == " ":
            out += f'<rect x="{n(x)}" y="{n(y)}" width="{n(c)}" height="{n(c)}" rx="{n(r)}" fill="{ORANGE}"/>'
            out += lens_disc(x + c / 2, y + c / 2, 0.3 * c, NOIR, ORANGE, BLANC)
            continue
        out += f'<rect x="{n(x)}" y="{n(y)}" width="{n(c)}" height="{n(c)}" rx="{n(r)}" fill="{cell}"/>'
        t = Line(f, ch, 0.6 * c)
        t.place(cx=x + c / 2, cy=y + c / 2)
        out += p(t.path(), letter)
    return out, (0, 0, D, D)


def contact_mark(cell, letter, text):
    tile, tb = contact_tile(cell, letter)
    if not text:
        return tile, tb
    D = tb[2]
    f = font("montserrat-800")
    k = Line(f, "KSC", 0.5 * D)
    g = font("montserrat-600")
    st = Line(g, "STUDIO PHOTO", 0.12 * D, tracking=fit(g, "STUDIO PHOTO", 0.12 * D, k.width))
    gap = 0.1 * D
    top = 0.5 * D - (k.height + gap + st.height) / 2  # bloc de texte centré sur le carré
    kb = k.place(left=D + 0.16 * D, top=top)
    sb = st.place(left=kb[0], top=kb[3] + gap)
    return tile + p(k.path(), text) + p(st.path(), ORANGE), union(tb, kb, sb)


def contact():
    clair = contact_mark(NOIR, BLANC, NOIR)
    sombre = contact_mark("#262B30", BLANC, BLANC)
    tile = contact_tile(NOIR, BLANC)
    return {
        "clair": Logo(*clair),
        "sombre": Logo(*sombre),
        "icone": icon(tile[0], tile[1], BLANC, shape="square", fill_ratio=0.74),
    }


# ------------------------------------------------------------------ piste 6 : Cachet
def arc_text(f, text, size, cx, cy, r, center_deg, tracking, color, bottom=False):
    """Texte posé sur un cercle : en haut il se lit dans le sens horaire, en bas il reste droit."""
    s = size / f.upm
    advs = [f.adv(ch) * s for ch in text]
    total = sum(advs) + tracking * size * (len(text) - 1)
    out, cum = "", 0.0
    for ch, a in zip(text, advs):
        mid = cum + a / 2
        if bottom:
            th = math.radians(center_deg) + (total / 2 - mid) / r
            T, U = (math.sin(th), -math.cos(th)), (-math.cos(th), -math.sin(th))
        else:
            th = math.radians(center_deg) - (total / 2 - mid) / r
            T, U = (-math.sin(th), math.cos(th)), (math.cos(th), math.sin(th))
        px, py = cx + r * math.cos(th), cy + r * math.sin(th)
        if ch != " ":
            e, ff = px - a / 2 * T[0], py - a / 2 * T[1]
            out += f.draw(ch, (s * T[0], s * T[1], s * U[0], s * U[1], e, ff))
        cum += a + tracking * size
    return p(out, color)


def aperture(cx, cy, R, uid, colors, ratio=0.4, rot=-90.0, gap=None):
    """Diaphragme à 6 lamelles (ouverture hexagonale), lamelles séparées par un masque."""
    gap = 0.07 * R if gap is None else gap
    V = [(cx + ratio * R * math.cos(math.radians(rot + 60 * k)), cy + ratio * R * math.sin(math.radians(rot + 60 * k))) for k in range(6)]

    def hit(o, u):
        bx, by = o[0] - cx, o[1] - cy
        b = u[0] * bx + u[1] * by
        t = -b + math.sqrt(b * b - (bx * bx + by * by - R * R))
        return (o[0] + t * u[0], o[1] + t * u[1])

    Pk, seps = [], ""
    for k in range(6):
        a, b = V[k], V[(k + 1) % 6]
        ln = math.hypot(b[0] - a[0], b[1] - a[1])
        u = ((b[0] - a[0]) / ln, (b[1] - a[1]) / ln)
        q = hit(b, u)
        Pk.append(q)
        far = (q[0] + u[0] * 0.2 * R, q[1] + u[1] * 0.2 * R)
        seps += f"M{pt(b)} L{pt(far)} "
    blades = ""
    for k in range(6):
        a0 = math.atan2(Pk[k][1] - cy, Pk[k][0] - cx)
        a1 = math.atan2(Pk[(k + 1) % 6][1] - cy, Pk[(k + 1) % 6][0] - cx)
        if a1 < a0:
            a1 += 2 * math.pi
        arc = " L".join(pt((cx + R * math.cos(a0 + (a1 - a0) * i / 16), cy + R * math.sin(a0 + (a1 - a0) * i / 16))) for i in range(17))
        d = f"M{pt(V[(k + 1) % 6])} L{arc} L{pt(V[(k + 2) % 6])} Z"
        blades += p(d, colors[k % len(colors)])
    defs = (f'<mask id="{uid}" maskUnits="userSpaceOnUse" x="{n(cx - 2 * R)}" y="{n(cy - 2 * R)}" width="{n(4 * R)}" height="{n(4 * R)}">'
            f'<rect x="{n(cx - 2 * R)}" y="{n(cy - 2 * R)}" width="{n(4 * R)}" height="{n(4 * R)}" fill="#fff"/>'
            f'<path d="{seps}" stroke="#000" stroke-width="{n(gap)}" fill="none"/></mask>')
    return f'<g mask="url(#{uid})">{blades}</g>', defs


def cachet_mark(ink, accent, uid):
    R = 400.0
    body = f'<circle cx="0" cy="0" r="{n(0.975 * R)}" fill="none" stroke="{ink}" stroke-width="{n(0.05 * R)}"/>'
    body += f'<circle cx="0" cy="0" r="{n(0.69 * R)}" fill="none" stroke="{ink}" stroke-width="{n(0.014 * R)}"/>'
    g = font("montserrat-700")
    size = 0.135 * R / g.cap
    body += arc_text(g, "KSC STUDIO", size, 0, 0, 0.745 * R, -90, 0.28, ink)
    body += arc_text(g, "PHOTOGRAPHIE", size, 0, 0, 0.745 * R + g.cap * size, 90, 0.22, ink, bottom=True)
    for a in (180, 0):
        x = 0.825 * R * math.cos(math.radians(a))
        body += f'<circle cx="{n(x)}" cy="0" r="{n(0.03 * R)}" fill="{accent}"/>'
    ap, defs = aperture(0, -0.26 * R, 0.17 * R, uid, (accent,), ratio=0.42)
    body += ap
    f = font("montserrat-800")
    k = Line(f, "KSC", 0.46 * R)
    k.place(cx=0, top=-0.02 * R)
    body += p(k.path(), ink)
    rule = 0.34 * R
    body += f'<rect x="{n(-rule / 2)}" y="{n(0.36 * R)}" width="{n(rule)}" height="{n(0.025 * R)}" fill="{accent}"/>'
    return body, (-R, -R, R, R), defs


def cachet():
    clair = cachet_mark(NOIR, ORANGE, "cachet-clair")
    sombre = cachet_mark(BLANC, ORANGE, "cachet-sombre")
    ic = cachet_mark(BLANC, ORANGE, "cachet-icone")
    return {
        "clair": Logo(clair[0], clair[1], clair[2], margin=0.04),
        "sombre": Logo(sombre[0], sombre[1], sombre[2], margin=0.04),
        "icone": icon(ic[0], ic[1], NOIR, fill_ratio=0.86, defs=ic[2]),
    }


# ------------------------------------------------------------------ piste 7 : Fusion (Objectif + Viseur)
def fusion_mark(ink, accent, tagline):
    """Les deux finalistes réunies : initiales fines du Viseur, C en objectif orange, cadre de mise au point."""
    f = font("jost-500")
    F = 300.0
    cap = f.cap * F
    word = Line(f, "KSC", F, tracking=0.17)
    word.place(cx=0, cy=0)
    cb = word.gbox(2)
    Ro = (cb[3] - cb[1]) / 2
    stem = (f.bounds("I")[2] - f.bounds("I")[0]) / f.upm * F  # l'anneau a l'épaisseur du fût des lettres
    lens, lbox = lens_c(cb[0] + Ro, (cb[1] + cb[3]) / 2, Ro, stem, 70, ink, accent, NOIR, BLANC, gap=0.1 * Ro)
    box = union(word.gbox(0), word.gbox(1), lbox)
    body, frame = focus_frame(box, cap, 0.07 * F, accent, dot=False)
    body += p(word.path(only={0, 1}), ink) + lens
    if not tagline:
        return body, frame
    t = Line(font("jost-500"), "STUDIO PHOTO", 0.15 * F, tracking=0.5)
    t.place(cx=(frame[0] + frame[2]) / 2, top=frame[3] + 0.42 * cap)
    return body + p(t.path(), tagline), union(frame, t.box)


def fusion():
    mono = fusion_mark(BLANC, ORANGE, None)
    return {
        "clair": Logo(*fusion_mark(NOIR, ORANGE, NOIR)),
        "sombre": Logo(*fusion_mark(BLANC, ORANGE, BLANC)),
        "icone": icon(mono[0], mono[1], NOIR, fill_ratio=0.66),
    }


CONCEPTS = [
    ("01-objectif", objectif),
    ("02-viseur", viseur),
    ("03-couture", couture),
    ("04-signature", signature),
    ("05-planche-contact", contact),
    ("06-cachet", cachet),
    ("07-fusion", fusion),
]

# présentation de chaque piste sur sa planche
PISTES = {
    "01-objectif": dict(
        titre="Objectif",
        phrase="Votre logo actuel, en plus fort et plus net : le C devient un objectif photo dessiné, "
               "lisible de loin, impeccable en petit comme sur une enseigne.",
        pour="Tous publics · enseigne · réseaux sociaux",
        couleurs=[ORANGE, NOIR, BLANC], polices="Montserrat", carte=(NOIR, BLANC)),
    "02-viseur": dict(
        titre="Viseur",
        phrase="Épuré et haut de gamme : vos initiales cadrées comme dans le viseur d'un appareil, "
               "avec le point de mise au point orange.",
        pour="Portraits · entreprises · mode",
        couleurs=[ORANGE, NOIR, BLANC], polices="Jost", carte=(NOIR, BLANC)),
    "03-couture": dict(
        titre="Couture",
        phrase="Un monogramme de maison de luxe, en capitales Didot italiques et or champagne : "
               "le registre qui fait accepter des tarifs premium.",
        pour="Mariages · grossesse · portraits premium",
        couleurs=[OR, NOIR, IVOIRE], polices="Bodoni Moda, Jost", carte=(NOIR, IVOIRE)),
    "04-signature": dict(
        titre="Signature",
        phrase="Votre signature d'artiste, soulignée d'un trait orange : posée en filigrane sur chaque "
               "photo livrée, chaque partage devient une publicité.",
        pour="Mariages · familles · artistes",
        couleurs=[ORANGE, NOIR, BLANC], polices="Corinthia, Jost", carte=(NOIR, BLANC)),
    "05-planche-contact": dict(
        titre="Planche contact",
        phrase="Vos initiales rangées comme les images d'une planche contact, la quatrième case est "
               "l'objectif : un carré iconique, taillé pour Instagram et TikTok.",
        pour="Réseaux sociaux · jeunes clients · événementiel",
        couleurs=[ORANGE, NOIR, BLANC], polices="Montserrat", carte=(NOIR, BLANC)),
    "06-cachet": dict(
        titre="Cachet",
        phrase="Un tampon rond façon label d'atelier, avec le diaphragme en orange : stickers, "
               "pochettes de tirages, sacs, t‑shirts. Il inspire confiance et savoir-faire.",
        pour="Tirages · packaging · merchandising",
        couleurs=[ORANGE, NOIR, BLANC], polices="Montserrat", carte=(NOIR, BLANC)),
}


# ------------------------------------------------------------------ export
def render(jobs):
    path = ROOT / ".render_jobs.json"
    path.write_text(json.dumps(jobs))
    env = dict(os.environ)
    env["NODE_PATH"] = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()
    subprocess.run(["node", str(ROOT / "tools" / "render.cjs"), str(path)], check=True, env=env)
    path.unlink()


def png_job(logo, out, height):
    w = round(height * logo.aspect)
    style = f'style="display:block;width:{w}px;height:{height}px" '
    html = '<html><body style="margin:0;background:transparent">' + logo.svg().replace("<svg ", "<svg " + style, 1) + "</body></html>"
    return {"html": html, "out": str(out), "width": w, "height": height, "transparent": True}


def preview_job(files, out):
    """Planche de contrôle : chaque SVG sur fond clair et sur fond sombre."""
    cells = "".join(
        f'<div style="background:{"#111518" if "sombre" in f.name or "icone" in f.name else "#F4F1EC"};padding:24px;'
        f'display:flex;align-items:center;justify-content:center;height:300px">'
        f'<img src="{f.as_uri()}" style="max-width:100%;max-height:100%"></div>' for f in files)
    page = ROOT / ".preview.html"
    page.write_text(f'<html><body style="margin:0;background:#888"><div style="display:grid;'
                    f'grid-template-columns:repeat(3,1fr);gap:8px;padding:8px;width:1484px">{cells}</div></body></html>')
    rows = (len(files) + 2) // 3
    return {"file": str(page), "out": str(out), "width": 1500, "height": rows * 356 + 16}


# ------------------------------------------------------------------ planches de présentation
def bokeh_photo(path, W=1400, H=900, seed=11):
    """Photo d'ambiance générée (lumières floues de soirée) pour montrer le logo en filigrane."""
    import numpy as np
    from PIL import Image, ImageFilter

    rng = np.random.default_rng(seed)
    y, x = np.mgrid[0:H, 0:W].astype(float)
    t = (y / H)[..., None]
    img = np.array([22, 26, 40]) * (1 - t) + np.array([70, 40, 30]) * t
    light = np.zeros((H, W, 3))
    palette = np.array([[255, 168, 88], [255, 214, 160], [255, 122, 52], [255, 236, 214], [255, 190, 120]])
    for _ in range(85):
        cx, cy, r = rng.uniform(0, W), rng.uniform(-0.05 * H, 0.9 * H), rng.uniform(16, 95)
        d = np.hypot(x - cx, y - cy)
        disc = np.clip((r - d) / 2.5, 0, 1) * (0.75 + 0.25 * np.clip(d / r, 0, 1))
        rim = np.clip(1 - np.abs(d - r + 3) / 3, 0, 1) * 0.3
        light += (disc + rim)[..., None] * palette[rng.integers(len(palette))] * rng.uniform(0.06, 0.3)
    img = img + light
    vig = 1 - 0.55 * np.clip(np.hypot((x - W / 2) / (W / 2), (y - H / 2) / (H / 2)) - 0.35, 0, 1) ** 1.4
    img = np.clip(img * vig[..., None], 0, 255).astype(np.uint8)
    Image.fromarray(img).filter(ImageFilter.GaussianBlur(1.2)).save(path, quality=92)


def font_face():
    faces = [("Jost", 400, "jost-400"), ("Jost", 500, "jost-500"), ("Montserrat", 800, "montserrat-800")]
    return "".join(f"@font-face{{font-family:{fam};font-weight:{w};src:url({(ROOT / 'fonts' / f'{name}.ttf').as_uri()})}}"
                   for fam, w, name in faces)


BOARD_CSS = """
@page{size:1080px 1350px;margin:0}
body{margin:0;background:#F4F1EC;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{width:1080px;height:1350px;background:#F4F1EC;font-family:Jost;color:#111518;position:relative;overflow:hidden;break-after:page}
.page:last-child{break-after:auto}
.ensemble .avatars figure{width:150px;font-size:11px;white-space:nowrap}
.kicker{position:absolute;left:56px;top:46px;font-weight:500;font-size:14px;letter-spacing:.34em;color:#8A8178}
h1{position:absolute;left:56px;top:70px;margin:0;font-family:Montserrat;font-weight:800;font-size:46px;letter-spacing:-.01em}
h1 span{color:#FF741F}
.pitch{position:absolute;left:56px;top:136px;width:930px;font-size:20px;line-height:1.45;color:#4A4642}
.pour{position:absolute;left:56px;top:206px;font-weight:500;font-size:14px;letter-spacing:.2em;color:#111518;text-transform:uppercase}
.panel{position:absolute;border-radius:22px;overflow:hidden;display:flex;align-items:center;justify-content:center}
.panel img.logo{max-width:78%;max-height:72%;display:block}
.tag{position:absolute;left:20px;top:16px;font-weight:500;font-size:12px;letter-spacing:.26em;text-transform:uppercase}
.avatars{display:flex;align-items:flex-end;gap:34px}
.avatars figure{margin:0;text-align:center;font-size:12px;letter-spacing:.14em;color:#6B645D;text-transform:uppercase}
.avatars img{display:block;margin:0 auto 10px}
.card{position:absolute;width:232px;height:150px;border-radius:7px;box-shadow:0 16px 30px rgba(0,0,0,.28);display:flex;align-items:center;justify-content:center}
.card img{max-width:68%;max-height:58%}
.foot{position:absolute;left:56px;right:56px;top:1278px;display:flex;align-items:center;gap:18px;font-size:14px;color:#6B645D;letter-spacing:.06em}
.sw{width:26px;height:26px;border-radius:50%;box-shadow:inset 0 0 0 1px rgba(0,0,0,.15)}
"""


PDF = "KSC_STUDIO_propositions_logo.pdf"  # document unique à envoyer : vue d'ensemble + 6 planches


def html_doc(pages, title):
    return (f'<html><head><meta charset="utf-8"><title>{title}</title><style>{font_face()}{BOARD_CSS}</style></head>'
            f'<body>{"".join(pages)}</body></html>')


def board_page(i, meta, files, photo):
    s = meta
    c_dark, c_light = s["carte"]
    sw = "".join(f'<div class="sw" style="background:{c}"></div><div>{c}</div>' for c in s["couleurs"])
    icon_uri = files["icone"].as_uri()
    avatars = "".join(f'<figure><img src="{icon_uri}" style="width:{px}px;height:{px}px">{lab}</figure>'
                      for px, lab in ((150, "Photo de profil"), (72, "Appli"), (34, "Onglet")))
    return f"""<div class="page">
<div class="kicker">KSC STUDIO · PROPOSITION DE LOGO {i} / {len(PISTES)}</div>
<h1>Piste {i} <span>·</span> {s["titre"]}</h1>
<div class="pitch">{s["phrase"]}</div>
<div class="pour">Idéal pour : {s["pour"]}</div>
<div class="panel" style="left:56px;top:250px;width:968px;height:392px;background:#FFFFFF">
  <div class="tag" style="color:#8A8178">Version principale</div><img class="logo" src="{files["clair"].as_uri()}"></div>
<div class="panel" style="left:56px;top:662px;width:516px;height:270px;background:{NOIR}">
  <div class="tag" style="color:#8B9096">Sur fond sombre</div><img class="logo" src="{files["sombre"].as_uri()}"></div>
<div class="panel" style="left:592px;top:662px;width:432px;height:270px;background:#EAE5DD">
  <div class="tag" style="color:#8A8178">Avatar</div><div class="avatars" style="margin-top:26px">{avatars}</div></div>
<div class="panel" style="left:56px;top:952px;width:484px;height:300px;background:#DCD5CA">
  <div class="tag" style="color:#6B645D">Cartes de visite</div>
  <div class="card" style="left:24px;top:62px;background:{c_dark};transform:rotate(-6deg)"><img src="{files["sombre"].as_uri()}"></div>
  <div class="card" style="left:228px;top:122px;background:{c_light};transform:rotate(5deg)"><img src="{files["clair"].as_uri()}"></div></div>
<div class="panel" style="left:560px;top:952px;width:464px;height:300px;background:url({photo.as_uri()}) center/cover">
  <div class="tag" style="color:#FFFFFFCC">Filigrane sur vos photos</div>
  <img src="{files["sombre"].as_uri()}" style="position:absolute;right:22px;bottom:20px;max-width:34%;max-height:30%;opacity:.9"></div>
<div class="foot">{sw}<div style="margin-left:auto">Police : {s["polices"]} (libre, usage commercial)</div></div>
</div>"""


def overview_page(all_files):
    cells, icons = "", ""
    for k, (slug, meta) in enumerate(PISTES.items()):
        f = all_files[slug]
        x, y = 56 + (k % 2) * 494, 236 + (k // 2) * 300
        cells += (f'<div class="panel" style="left:{x}px;top:{y}px;width:474px;height:280px;background:#FFFFFF">'
                  f'<div class="tag" style="color:#8A8178">{k + 1} · {meta["titre"]}</div>'
                  f'<img class="logo" src="{f["clair"].as_uri()}" style="max-width:76%;max-height:70%;margin-top:14px"></div>')
        icons += f'<figure><img src="{f["icone"].as_uri()}" style="width:108px;height:108px">{k + 1} · {meta["titre"]}</figure>'
    return f"""<div class="page ensemble">
<div class="kicker">KSC STUDIO · PROPOSITIONS DE LOGO</div>
<h1>6 pistes <span>·</span> vos initiales K S C</h1>
<div class="pitch">Choisissez une ou deux pistes : je les affine ensuite (couleurs, slogan, déclinaisons, kit réseaux sociaux, logo animé pour vos vidéos).</div>
{cells}
<div class="panel" style="left:56px;top:1136px;width:968px;height:196px;background:#EAE5DD">
  <div class="tag" style="color:#8A8178">En photo de profil</div><div class="avatars" style="gap:8px;margin-top:30px">{icons}</div></div>
</div>"""


def boards(all_files):
    tmp = ROOT / ".boards"
    tmp.mkdir(exist_ok=True)
    photo = tmp / "photo.jpg"
    bokeh_photo(photo)
    out = ROOT / "planches"
    out.mkdir(exist_ok=True)
    pages = [("00-ensemble", overview_page(all_files))]
    pages += [(slug, board_page(k + 1, meta, all_files[slug], photo)) for k, (slug, meta) in enumerate(PISTES.items())]
    jobs = []
    for slug, page in pages:  # une image par planche
        f = tmp / f"{slug}.html"
        f.write_text(html_doc([page], f"KSC STUDIO · {slug}"))
        jobs.append({"file": str(f), "out": str(out / f"ksc-planche-{slug}.png"), "width": 1080, "height": 1350, "scale": 2})
    f = tmp / "document.html"  # et toutes les planches dans un PDF, logos restés vectoriels
    f.write_text(html_doc([page for _, page in pages], "KSC STUDIO · Propositions de logo"))
    jobs.append({"file": str(f), "out": str(ROOT / PDF), "width": 1080, "height": 1350, "pdf": True})
    return jobs, tmp


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", help="ne produire que ces pistes (ex. 01,03)")
    ap.add_argument("--preview", help="écrit aussi une planche de contrôle PNG à ce chemin")
    ap.add_argument("--planches", action="store_true", help="produit aussi les planches de présentation et le PDF")
    args = ap.parse_args()
    jobs, files, all_files = [], [], {}
    for slug, fn in CONCEPTS:
        if args.only and slug[:2] not in args.only.split(","):
            continue
        d = ROOT / "logos" / slug
        d.mkdir(parents=True, exist_ok=True)
        all_files[slug] = {}
        for name, logo in fn().items():
            base = d / f"ksc-{slug[3:]}-{name}"
            base.with_suffix(".svg").write_text(logo.svg())
            files.append(base.with_suffix(".svg"))
            all_files[slug][name] = base.with_suffix(".svg")
            jobs.append(png_job(logo, base.with_suffix(".png"), 1000 if name == "icone" else 700))
    if args.preview:
        jobs.append(preview_job(files, args.preview))
    tmp = None
    if args.planches:
        more, tmp = boards(all_files)
        jobs += more
    render(jobs)
    (ROOT / ".preview.html").unlink(missing_ok=True)
    if tmp:
        for f in tmp.iterdir():
            f.unlink()
        tmp.rmdir()
    print(len(files), "logos écrits dans", ROOT / "logos")


if __name__ == "__main__":
    main()
