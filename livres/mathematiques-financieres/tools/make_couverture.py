#!/usr/bin/env python3
"""Couverture du livre « Mathématiques Financières » (Professeur Raoul, Édition Moderna, 2026).

Couverture à plat pour l'imprimeur (4e de couverture, dos, 1re de couverture), en CMJN, texte vectorisé :
l'imprimeur n'a aucune police à installer. Fichiers produits :

    couverture/Mathematiques-Financieres_couverture_imprimeur.pdf        fond perdu 3 mm, sans repères
    couverture/Mathematiques-Financieres_couverture_traits-de-coupe.pdf  avec traits de coupe et repères du dos
    couverture/Mathematiques-Financieres_face-avant.png / .jpg           1re de couverture (300 dpi / web)
    couverture/Mathematiques-Financieres_4e-de-couverture.png            4e de couverture (300 dpi)
    planches/couverture-controle.png     couverture à plat : coupe, fond perdu, zone de sécurité, dos
    planches/couverture-maquette.png     le livre en volume
    planches/couverture-palettes.png     les palettes de couleurs côte à côte
    Mathematiques-Financieres_couverture.zip   tout le dossier à envoyer, avec un LISEZ-MOI

    python3 -I livres/mathematiques-financieres/tools/make_couverture.py                  # palette PALETTE
    python3 -I livres/mathematiques-financieres/tools/make_couverture.py --palette bordeaux

Le format, le nombre de pages (qui donne l'épaisseur du dos), la palette et les données à compléter
(A_COMPLETER) se règlent ci-dessous. Tant qu'une donnée manque, un texte d'attente est imprimé à sa place.
"""

import json
import os
import subprocess
import tempfile
import zipfile
from dataclasses import dataclass
from pathlib import Path

import pyphen
import uharfbuzz as hb
from fontTools.pens.basePen import BasePen
from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont
from reportlab.graphics import renderPDF
from reportlab.graphics.barcode.eanbc import ISBNBarcodeWidget
from reportlab.graphics.shapes import Drawing
from reportlab.lib.colors import CMYKColor
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont as RLTTFont
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parent.parent
FONTS = ROOT / "fonts"
OUT = ROOT / "couverture"
PLANCHES = ROOT / "planches"
NOM = "Mathematiques-Financieres"
RENDER = ROOT.parent.parent / "brand" / "ksc-studio" / "tools" / "render.cjs"  # Chromium de Playwright

# ------------------------------------------------------------------ réglages d'impression
FORMAT = (170.0, 240.0)  # couverture finie, largeur × hauteur en mm (17 × 24 cm)
FOND_PERDU = 3.0  # mm tout autour
SECURITE = 6.0  # mm : aucun texte plus près de la coupe (1re et 4e de couverture)
PAGES = 240  # pages intérieures (estimation) : l'épaisseur du dos en dépend
EPAISSEUR_PAGE = 0.056  # mm par page (offset 80 à 90 g) : l'imprimeur donne la valeur exacte
DOS = round(PAGES * EPAISSEUR_PAGE, 1)  # largeur du dos en mm
CADRE = 9.0  # filet or, en mm du bord fini
AUTEUR_Y = 175.0  # 4e de couverture : haut du bloc auteur, en mm sous le haut fini

# ------------------------------------------------------------------ couleurs CMJN (0 à 1)
@dataclass(frozen=True)
class Palette:
    nom: str
    resume: str
    fond_haut: CMYKColor  # le fond s'assombrit doucement vers le bas
    fond_bas: CMYKColor
    accent: CMYKColor  # cadre, filets, numéros, petites capitales
    texte: CMYKColor  # titre et textes principaux
    texte2: CMYKColor  # textes secondaires
    attente: CMYKColor  # textes d'attente, à remplacer avant impression
    clair: bool = False  # fond clair : le cadre blanc du code-barres reçoit un filet


OR = CMYKColor(0.05, 0.20, 0.72, 0.0)
PAPIER = CMYKColor(0, 0, 0, 0)  # blanc : pas d'encre
GRIS = CMYKColor(0, 0, 0, 0.55)
REPERE = CMYKColor(1, 1, 1, 1)  # traits de coupe : couleur de repérage
PALETTES = {
    "emeraude": Palette("Émeraude et or", "Le vert de la finance et de la croissance, l’or du haut de gamme.",
                        CMYKColor(0.90, 0.30, 0.75, 0.35), CMYKColor(0.95, 0.40, 0.80, 0.56), OR, PAPIER,
                        CMYKColor(0.14, 0.02, 0.12, 0.0), CMYKColor(0.45, 0.15, 0.40, 0.10)),
    "bordeaux": Palette("Bordeaux et or", "Classique et prestigieux, l’allure d’un grand manuel universitaire.",
                        CMYKColor(0.28, 0.97, 0.72, 0.38), CMYKColor(0.40, 0.95, 0.75, 0.60), OR, PAPIER,
                        CMYKColor(0.02, 0.12, 0.08, 0.0), CMYKColor(0.25, 0.45, 0.35, 0.15)),
    "anthracite": Palette("Anthracite et turquoise", "Moderne et sobre, dans l’esprit de la finance numérique.",
                          CMYKColor(0.70, 0.57, 0.52, 0.55), CMYKColor(0.75, 0.65, 0.57, 0.80),
                          CMYKColor(0.75, 0.05, 0.40, 0.0), PAPIER, CMYKColor(0.10, 0.06, 0.06, 0.0),
                          CMYKColor(0.45, 0.35, 0.32, 0.15)),
    "ivoire": Palette("Ivoire et vert", "Une couverture claire, qui se remarque parmi les manuels sombres.",
                      CMYKColor(0.02, 0.03, 0.09, 0.0), CMYKColor(0.04, 0.07, 0.18, 0.02),
                      CMYKColor(0.22, 0.45, 1.0, 0.12), CMYKColor(0.92, 0.35, 0.78, 0.50),
                      CMYKColor(0.70, 0.35, 0.60, 0.30), CMYKColor(0.15, 0.15, 0.25, 0.25), clair=True),
}
PALETTE = "emeraude"  # palette des fichiers pour l'imprimeur (l'option --palette la remplace)

# ------------------------------------------------------------------ textes
AUTEUR = "Professeur Raoul"
TITRE = ("Mathématiques", "Financières")
SOUS_TITRE = "Cours complet et exercices corrigés"
NIVEAU = "Niveau Licence • Sciences Économiques et Gestion"
CHAPITRES = ["Suites numériques", "Intérêt simple", "Intérêt composé", "Annuités", "Emprunts indivis",
             "Emprunts obligataires", "Décisions d’investissement"]
DESCRIPTION = ["Manuel de cours, méthodes de calcul et applications corrigées",
               "à l’usage des étudiants et professionnels de la finance"]
EDITEUR, ANNEE = "Moderna", "2026"

ACCROCHE = ["De l’intérêt simple", "aux décisions d’investissement :", "toute la méthode pour réussir"]
PRESENTATION = ("Pensé pour les étudiants de Licence en Sciences économiques et de gestion, ce manuel réunit en un "
                "seul volume le cours complet de mathématiques financières et des exercices corrigés. Chaque notion "
                "est expliquée simplement, suivie de sa méthode de calcul pas à pas, puis mise en application.")
OBJECTIFS_TITRE = "Au fil des sept chapitres, vous apprendrez à :"
OBJECTIFS = [
    "utiliser les suites numériques, base de tout calcul financier ;",
    "calculer intérêts simples et composés, valeurs acquises et valeurs actuelles ;",
    "évaluer des annuités et établir le remboursement d’un emprunt indivis ;",
    "analyser les emprunts obligataires ;",
    "comparer des projets pour prendre les bonnes décisions d’investissement.",
]
POINTS_FORTS = ["Cours complet", "Méthodes pas à pas", "Exercices corrigés"]
PROS = "Un outil précieux aussi pour les professionnels de la finance qui veulent revoir les fondamentaux."

# à compléter : tant qu'une valeur vaut None, un texte d'attente est imprimé à sa place
A_COMPLETER = {
    "bio": None,  # 2 ou 3 phrases sur l'auteur
    "isbn": None,  # 13 chiffres, ex. "9782123456786" : le code-barres est alors dessiné
    "prix": None,  # ex. "15 000 FCFA" ou "29 €"
}
ATTENTES = {
    "bio": "[Présentation de l’auteur à compléter : parcours, université, années d’enseignement.]",
    "isbn": "Code-barres ISBN",
    "prix": "Prix : à compléter",
}


# ------------------------------------------------------------------ texte vectorisé (HarfBuzz + contours)
class Face:
    _cache = {}

    def __init__(self, name):
        path = FONTS / f"{name}.ttf"
        tt = TTFont(path)
        self.upem = tt["head"].unitsPerEm
        self.glyphs = tt.getGlyphSet()
        self.names = tt.getGlyphOrder()
        self.cap = tt["OS/2"].sCapHeight / self.upem
        self.hb = hb.Font(hb.Face(hb.Blob.from_file_path(str(path))))

    @classmethod
    def get(cls, name):
        if name not in cls._cache:
            cls._cache[name] = cls(name)
        return cls._cache[name]

    def shape(self, s):
        buf = hb.Buffer()
        buf.add_str(s)
        buf.guess_segment_properties()
        hb.shape(self.hb, buf, {"kern": True, "liga": True})
        return [(self.names[i.codepoint], p.x_advance, p.x_offset, p.y_offset)
                for i, p in zip(buf.glyph_infos, buf.glyph_positions)]


@dataclass(frozen=True)
class St:
    face: str
    size: float  # corps en points
    color: CMYKColor
    track: float = 0.0  # interlettrage, en fraction du corps

    @property
    def f(self):
        return Face.get(self.face)

    def but(self, **kw):
        return St(**{**self.__dict__, **kw})


class PathPen(BasePen):
    """Dessine un glyphe dans un chemin ReportLab (contours TrueType convertis en courbes de Bézier)."""

    def __init__(self, glyphset, path, x, y, k):
        super().__init__(glyphset)
        self.p, self.x, self.y, self.k = path, x, y, k

    def _xy(self, pt):
        return self.x + pt[0] * self.k, self.y + pt[1] * self.k

    def _moveTo(self, pt):
        self.p.moveTo(*self._xy(pt))

    def _lineTo(self, pt):
        self.p.lineTo(*self._xy(pt))

    def _curveToOne(self, p1, p2, p3):
        self.p.curveTo(*self._xy(p1), *self._xy(p2), *self._xy(p3))

    def _qCurveToOne(self, p1, p2):
        p0 = self._getCurrentPoint()
        self._curveToOne((p0[0] + 2 / 3 * (p1[0] - p0[0]), p0[1] + 2 / 3 * (p1[1] - p0[1])),
                         (p2[0] + 2 / 3 * (p1[0] - p2[0]), p2[1] + 2 / 3 * (p1[1] - p2[1])), p2)

    def _closePath(self):
        self.p.close()


def width(s, st):
    run = st.f.shape(s)
    return sum(g[1] for g in run) * st.size / st.f.upem + st.track * st.size * max(0, len(run) - 1)


def text(c, s, st, x, y, align="left"):
    """Une ligne de texte, ligne de base en y ; renvoie sa largeur (points)."""
    w = width(s, st)
    x0 = x - {"left": 0, "center": w / 2, "right": w}[align]
    f, k = st.f, st.size / st.f.upem
    path = c.beginPath()
    for name, adv, xo, yo in f.shape(s):
        f.glyphs[name].draw(PathPen(f.glyphs, path, x0 + xo * k, y + yo * k, k))
        x0 += adv * k + st.track * st.size
    if s.strip():
        c.setFillColor(st.color)
        c.drawPath(path, stroke=0, fill=1, fillMode=canvas.FILL_NON_ZERO)
    return w


HYPH = pyphen.Pyphen(lang="fr_FR", left=3, right=3)


def lines_of(s, st, w, hyphenate=True):
    """Coupe `s` en lignes d'au plus `w` points, avec césure française quand un mot déborde."""
    words, lines, cur = s.split(" "), [], []
    while words:
        word = words.pop(0)
        if width(" ".join(cur + [word]), st) <= w:
            cur.append(word)
            continue
        for head, tail in (HYPH.iterate(word) if hyphenate else ()):
            if "’" not in head[-2:] and width(" ".join(cur + [head + "-"]), st) <= w:
                cur.append(head + "-")
                words.insert(0, tail)
                break
        else:
            words.insert(0, word)
        if not cur:  # mot plus long que la ligne : on le pose tel quel
            cur.append(words.pop(0))
        lines.append(cur)
        cur = []
    if cur:
        lines.append(cur)
    return lines


def para(c, s, st, x, y, w, lead, align="justify", hyphenate=None):
    """Paragraphe ; y est la première ligne de base. Renvoie la ligne de base qui suivrait.
    Césure seulement en texte justifié, sauf demande contraire."""
    lines = lines_of(s, st, w, align == "justify" if hyphenate is None else hyphenate)
    sp = width(" ", st)
    for i, ws in enumerate(lines):
        last = i == len(lines) - 1
        if align == "justify" and not last and len(ws) > 1:
            gap = (w - sum(width(t, st) for t in ws)) / (len(ws) - 1)
            xx = x
            for t in ws:
                xx += text(c, t, st, xx, y) + gap
        else:
            line = " ".join(ws)
            ax = {"justify": x, "left": x, "center": x + w / 2, "right": x + w}[align]
            text(c, line, st, ax, y, "left" if align == "justify" else align)
        y -= lead
    return y


# ------------------------------------------------------------------ la couverture
class Couverture:
    def __init__(self, c, palette, ox=0.0, oy=0.0):
        self.c, self.p = c, palette
        self.W, self.H, self.B, self.D = FORMAT[0] * mm, FORMAT[1] * mm, FOND_PERDU * mm, DOS * mm
        self.ox, self.oy = ox, oy
        self.back_x = ox + self.B
        self.spine_x = self.back_x + self.W
        self.front_x = self.spine_x + self.D
        self.bottom = oy + self.B
        self.top = self.bottom + self.H

    def at(self, x0, x_mm, y_mm):
        """Point à x_mm du bord gauche du panneau et y_mm sous le haut fini."""
        return x0 + x_mm * mm, self.top - y_mm * mm

    def T(self, x0, s, st, x_mm, y_mm, align="center"):
        return text(self.c, s, st, *self.at(x0, x_mm, y_mm), align)

    def draw(self):
        self.background()
        self.back()
        self.spine()
        self.front()

    def background(self):
        c = self.c
        x0, y0 = self.ox, self.oy
        w, h = 2 * self.B + 2 * self.W + self.D, 2 * self.B + self.H
        c.saveState()
        p = c.beginPath()
        p.rect(x0, y0, w, h)
        c.clipPath(p, stroke=0, fill=0)
        c.linearGradient(x0, y0 + h, x0, y0, [self.p.fond_haut, self.p.fond_bas], extend=True)
        c.restoreState()

    def frame(self, x0):
        c = self.c
        c.setStrokeColor(self.p.accent)
        c.setLineWidth(0.8)
        c.rect(x0 + CADRE * mm, self.bottom + CADRE * mm, self.W - 2 * CADRE * mm, self.H - 2 * CADRE * mm,
               stroke=1, fill=0)

    def rule(self, x0, cx_mm, y_mm, length_mm, weight=0.6):
        c = self.c
        x, y = self.at(x0, cx_mm, y_mm)
        c.setStrokeColor(self.p.accent)
        c.setLineWidth(weight)
        c.line(x - length_mm / 2 * mm, y, x + length_mm / 2 * mm, y)

    # ---------------------------------------------------------- 1re de couverture
    def front(self):
        x0, cx = self.front_x, FORMAT[0] / 2
        self.frame(x0)
        self.T(x0, AUTEUR.upper(), St("noto-sans-600", 10.5, self.p.accent, 0.14), cx, 27)
        title = St("noto-serif-cond-700", 1, self.p.texte)
        title = title.but(size=0.72 * self.W / width(TITRE[0], title))
        y1 = 27 + 11 + title.size * title.f.cap / mm
        lead = 1.0 * title.size / mm
        self.T(x0, TITRE[0], title, cx, y1)
        self.T(x0, TITRE[1], title, cx, y1 + lead)
        y = y1 + lead + 13.5
        self.T(x0, SOUS_TITRE, St("noto-serif-semicond-400i", 17, self.p.texte), cx, y)
        y += 9.5
        self.T(x0, NIVEAU, St("noto-sans-semicond-500", 10.5, self.p.accent, 0.01), cx, y)

        y += 19.5
        self.T(x0, "SOMMAIRE DES CHAPITRES", St("noto-sans-600", 11, self.p.accent, 0.06), cx, y)
        num, name = St("noto-sans-semicond-700", 12.5, self.p.accent), St("noto-sans-semicond-500", 12.5, self.p.texte)
        col = width("00", num) + 5 * mm
        block = col + max(width(ch, name) for ch in CHAPITRES)
        left = cx - block / 2 / mm
        y += 12
        for i, ch in enumerate(CHAPITRES):
            self.T(x0, f"{i + 1:02d}", num, left, y, "left")
            self.T(x0, ch, name, left + col / mm, y, "left")
            y += 8.4
        self.rule(x0, cx, y + 4.5, 22)
        y += 15
        desc = St("noto-sans-semicond-400", 9.5, self.p.texte)
        for line in DESCRIPTION:
            self.T(x0, line, desc, cx, y)
            y += 5.2
        self.edition(x0, cx, FORMAT[1] - 19.5)

    def edition(self, x0, cx, y):
        """« Édition MODERNA » et l'année entre deux filets, comme sur la bannière."""
        a, b = St("noto-sans-semicond-400", 10.5, self.p.texte), St("noto-sans-600", 10.5, self.p.texte, 0.04)
        wa, wb = width("Édition ", a), width(EDITEUR.upper(), b)
        x, yy = self.at(x0, cx, y - 6)
        text(self.c, "Édition ", a, x - (wa + wb) / 2, yy)
        text(self.c, EDITEUR.upper(), b, x - (wa + wb) / 2 + wa, yy)
        yr = St("noto-sans-600", 10.5, self.p.accent, 0.08)
        self.T(x0, ANNEE, yr, cx, y)
        half = width(ANNEE, yr) / 2 / mm
        for side in (-1, 1):
            self.rule(x0, cx + side * (half + 3 + 5), y - 1.3, 10, 0.6)

    # ---------------------------------------------------------- dos
    def spine(self):
        c, D = self.c, DOS
        if D < 6:  # trop fin pour du texte
            return
        xc = self.spine_x + self.D / 2
        c.setStrokeColor(self.p.accent)
        c.setLineWidth(0.6)
        for y in (self.top - 11 * mm, self.bottom + 11 * mm):
            c.line(self.spine_x + 1.8 * mm, y, self.spine_x + self.D - 1.8 * mm, y)
        tsize = min(16.0, 0.30 * D * mm / Face.get("noto-serif-cond-700").cap)
        items = [  # (texte, style, position le long du dos, alignement)
            (f"{TITRE[0]} {TITRE[1]}", St("noto-serif-cond-700", tsize, self.p.texte), self.bottom + self.H / 2, "center"),
            (AUTEUR.upper(), St("noto-sans-600", min(7.5, tsize * 0.5), self.p.accent, 0.14), self.top - 17 * mm, "right"),
            (f"ÉDITION {EDITEUR.upper()}", St("noto-sans-600", min(6.5, tsize * 0.43), self.p.accent, 0.14),
             self.bottom + 17 * mm, "left"),
        ]
        for s, st, y, align in items:  # lecture de bas en haut, à la française
            c.saveState()
            c.translate(xc + st.size * st.f.cap / 2, y)
            c.rotate(90)
            text(c, s, st, 0, 0, align)
            c.restoreState()

    # ---------------------------------------------------------- 4e de couverture
    def back(self):
        c, x0, cx = self.c, self.back_x, FORMAT[0] / 2
        self.frame(x0)
        left, colw = 20.0, FORMAT[0] - 40.0
        self.T(x0, f"{TITRE[0]} {TITRE[1]}".upper(), St("noto-sans-600", 8.5, self.p.accent, 0.16), cx, 25)
        head = St("noto-serif-cond-700", 19.5, self.p.texte)
        y = 36
        for line in ACCROCHE:
            self.T(x0, line, head, cx, y)
            y += 8.0
        self.rule(x0, cx, y - 2.5, 22)
        y += 5.5
        body = St("noto-serif-semicond-400", 10.2, self.p.texte)
        lead = 14.2
        yy = para(c, PRESENTATION, body, *self.at(x0, left, y), colw * mm, lead)
        y = (self.top - yy) / mm + 3.2
        self.T(x0, OBJECTIFS_TITRE, St("noto-sans-semicond-700", 10.2, self.p.accent, 0.01), left, y, "left")
        y += 6.6
        bullet = St("noto-serif-semicond-400", 10.2, self.p.texte)
        for item in OBJECTIFS:
            bx, by = self.at(x0, left + 1.2, y - 1.25)
            c.setFillColor(self.p.accent)
            p = c.beginPath()
            r = 0.95 * mm
            p.moveTo(bx, by + r)
            p.lineTo(bx + r, by)
            p.lineTo(bx, by - r)
            p.lineTo(bx - r, by)
            p.close()
            c.drawPath(p, stroke=0, fill=1)
            yy = para(c, item, bullet, *self.at(x0, left + 5, y), (colw - 5) * mm, lead, align="left")
            y = (self.top - yy) / mm + 1.2
        y += 6
        self.badges(x0, cx, y)
        y += 27.5
        yy = para(c, PROS, St("noto-serif-semicond-400i", 9.6, self.p.texte2), *self.at(x0, left + 6, y),
                  (colw - 12) * mm, 12.6, align="center")
        end = (self.top - yy) / mm - 4.4  # dernière ligne de base
        assert end < AUTEUR_Y - 8, f"le texte de la 4e déborde sur le bloc auteur ({end:.1f} mm)"
        self.author_and_codes(x0, AUTEUR_Y)

    def badges(self, x0, cx, y):
        """Trois points forts : pictogramme or dans un cercle, libellé en dessous."""
        c = self.c
        step = 44.0
        lab = St("noto-sans-600", 7.6, self.p.texte, 0.1)
        for i, label in enumerate(POINTS_FORTS):
            bx_mm = cx + (i - 1) * step
            x, yc = self.at(x0, bx_mm, y + 6)
            c.setStrokeColor(self.p.accent)
            c.setLineWidth(0.8)
            c.circle(x, yc, 6.2 * mm, stroke=1, fill=0)
            c.setLineWidth(0.9)
            c.setLineJoin(1)
            c.setLineCap(1)
            u = mm
            if i == 0:  # livre ouvert
                p = c.beginPath()
                p.moveTo(x, yc - 2.4 * u)
                p.curveTo(x - 1.2 * u, yc - 1.6 * u, x - 2.6 * u, yc - 1.7 * u, x - 3.6 * u, yc - 2.1 * u)
                p.lineTo(x - 3.6 * u, yc + 2.3 * u)
                p.curveTo(x - 2.6 * u, yc + 2.7 * u, x - 1.2 * u, yc + 2.6 * u, x, yc + 1.8 * u)
                p.curveTo(x + 1.2 * u, yc + 2.6 * u, x + 2.6 * u, yc + 2.7 * u, x + 3.6 * u, yc + 2.3 * u)
                p.lineTo(x + 3.6 * u, yc - 2.1 * u)
                p.curveTo(x + 2.6 * u, yc - 1.7 * u, x + 1.2 * u, yc - 1.6 * u, x, yc - 2.4 * u)
                p.moveTo(x, yc - 2.4 * u)
                p.lineTo(x, yc + 1.8 * u)
                c.drawPath(p, stroke=1, fill=0)
            elif i == 1:  # escalier : pas à pas
                p = c.beginPath()
                pts = [(-3.4, -2.6), (-3.4, -1.0), (-1.1, -1.0), (-1.1, 0.6), (1.2, 0.6), (1.2, 2.2), (3.5, 2.2)]
                p.moveTo(x + pts[0][0] * u, yc + pts[0][1] * u)
                for px, py in pts[1:]:
                    p.lineTo(x + px * u, yc + py * u)
                p.moveTo(x - 3.4 * u, yc - 2.6 * u)
                p.lineTo(x + 3.5 * u, yc - 2.6 * u)
                c.drawPath(p, stroke=1, fill=0)
            else:  # coche : corrigé
                p = c.beginPath()
                p.moveTo(x - 2.9 * u, yc - 0.1 * u)
                p.lineTo(x - 0.8 * u, yc - 2.2 * u)
                p.lineTo(x + 3.1 * u, yc + 2.2 * u)
                c.drawPath(p, stroke=1, fill=0)
            self.T(x0, label.upper(), lab, bx_mm, y + 17.5)

    def author_and_codes(self, x0, y):
        c = self.c
        left = 20.0
        self.T(x0, "L’AUTEUR", St("noto-sans-600", 7.8, self.p.accent, 0.16), left, y, "left")
        self.T(x0, AUTEUR, St("noto-serif-cond-700", 13.5, self.p.texte), left, y + 6.2, "left")
        bio = A_COMPLETER["bio"]
        st = St("noto-serif-semicond-400" if bio else "noto-serif-semicond-400i", 8.8, self.p.texte if bio else self.p.attente)
        para(c, bio or ATTENTES["bio"], st, *self.at(x0, left, y + 11.6), 80 * mm, 11.6, align="left")
        self.edition(x0, left + 37, FORMAT[1] - 19.5)
        # code-barres et prix, en bas à droite
        bw, bh = 46.0, 27.0
        bx, by = FORMAT[0] - 20.0 - bw, FORMAT[1] - 15.0 - bh
        x, ytop = self.at(x0, bx, by)
        c.setFillColor(PAPIER)
        c.setStrokeColor(GRIS)
        c.setLineWidth(0.3)
        c.roundRect(x, ytop - bh * mm, bw * mm, bh * mm, 1.2 * mm, stroke=int(self.p.clair), fill=1)
        isbn = A_COMPLETER["isbn"]
        if isbn:
            digits = "".join(ch for ch in isbn if ch.isdigit())
            bc = ISBNBarcodeWidget(value=digits[:12], barHeight=15 * mm, barWidth=0.33 * mm, fontSize=8,
                                   barFillColor=CMYKColor(0, 0, 0, 1), textColor=CMYKColor(0, 0, 0, 1))
            x1, y1, x2, y2 = bc.getBounds()
            d = Drawing(x2 - x1, y2 - y1)
            d.add(bc)
            renderPDF.draw(d, c, x + (bw * mm - (x2 - x1)) / 2 - x1, ytop - bh * mm + 3 * mm - y1)
        else:
            self.T(x0, ATTENTES["isbn"], St("noto-sans-600", 8.2, GRIS, 0.02), bx + bw / 2, by + bh / 2 - 0.5)
            self.T(x0, "à placer ici", St("noto-sans-semicond-400", 7.6, GRIS), bx + bw / 2, by + bh / 2 + 4.2)
        prix = A_COMPLETER["prix"]
        self.T(x0, f"Prix : {prix}" if prix else ATTENTES["prix"],
               St("noto-sans-600", 8.6, self.p.texte if prix else self.p.attente, 0.02), bx + bw, by - 3.2, "right")


# ------------------------------------------------------------------ fichiers
def new_canvas(path, w, h):
    pdfmetrics.registerFont(RLTTFont("NotoSans", str(FONTS / "noto-sans-semicond-400.ttf")))
    c = canvas.Canvas(str(path), pagesize=(w, h), invariant=1, enforceColorSpace="cmyk",
                      initialFontName="NotoSans", initialFontSize=8, initialLeading=9.6)
    c.setTitle("Mathématiques Financières — couverture")
    c.setAuthor(AUTEUR)
    c.setSubject(f"Couverture {FORMAT[0]:g} × {FORMAT[1]:g} mm, dos {DOS:g} mm ({PAGES} pages), "
                 f"fond perdu {FOND_PERDU:g} mm, CMJN")
    return c


def spread_size():
    return (2 * FOND_PERDU + 2 * FORMAT[0] + DOS) * mm, (2 * FOND_PERDU + FORMAT[1]) * mm


def pdf_imprimeur(path, palette):
    w, h = spread_size()
    c = new_canvas(path, w, h)
    B = FOND_PERDU * mm
    c.setTrimBox((B, B, w - B, h - B))
    c.setBleedBox((0, 0, w, h))
    Couverture(c, palette).draw()
    c.showPage()
    c.save()


def pdf_traits(path, palette, slug=13.0):
    w, h = spread_size()
    S = slug * mm
    c = new_canvas(path, w + 2 * S, h + 2 * S)
    B = FOND_PERDU * mm
    c.setTrimBox((S + B, S + B, S + w - B, S + h - B))
    c.setBleedBox((S, S, S + w, S + h))
    cov = Couverture(c, palette, S, S)
    cov.draw()
    c.setStrokeColor(REPERE)
    c.setLineWidth(0.25)
    gap, length = B + 1.5 * mm, 6 * mm
    xs = [cov.back_x, cov.front_x + cov.W]
    ys = [cov.bottom, cov.top]
    for x in xs:
        for y, sgn in ((cov.bottom, -1), (cov.top, 1)):
            c.line(x, y + sgn * gap, x, y + sgn * (gap + length))
    for y in ys:
        for x, sgn in ((cov.back_x, -1), (cov.front_x + cov.W, 1)):
            c.line(x + sgn * gap, y, x + sgn * (gap + length), y)
    for x in (cov.spine_x, cov.front_x):  # pliures du dos
        for y, sgn in ((cov.bottom, -1), (cov.top, 1)):
            c.setDash(1.5, 1.5)
            c.line(x, y + sgn * gap, x, y + sgn * (gap + length))
            c.setDash()
    info = (f"Mathématiques Financières — couverture {FORMAT[0]:g} × {FORMAT[1]:g} mm — dos {DOS:g} mm "
            f"({PAGES} pages) — fond perdu {FOND_PERDU:g} mm — CMJN").replace(".", ",")
    text(c, info, St("noto-sans-semicond-400", 6.5, REPERE), S + B, 4.5 * mm)
    c.showPage()
    c.save()


def raster(pdf, dpi, out_png):
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(["pdftoppm", "-r", str(dpi), "-png", "-singlefile", str(pdf), f"{tmp}/p"], check=True)
        Image.open(f"{tmp}/p.png").convert("RGB").save(out_png)
    return Image.open(out_png)


def panels(img, dpi):
    """Découpe 4e, dos et 1re (format fini, sans fond perdu) dans l'image de la couverture à plat."""
    k = dpi / 25.4
    B, W, H, D = FOND_PERDU * k, FORMAT[0] * k, FORMAT[1] * k, DOS * k
    box = lambda x0, w: tuple(round(v) for v in (x0, B, x0 + w, B + H))  # noqa: E731
    return img.crop(box(B, W)), img.crop(box(B + W, D)), img.crop(box(B + W + D, W))


def control_sheet(spread, dpi, out):
    """Couverture à plat avec repères : coupe, fond perdu, zone de sécurité, plis du dos, cotes."""
    k = dpi / 25.4
    B, W, H, D, M = FOND_PERDU * k, FORMAT[0] * k, FORMAT[1] * k, DOS * k, 90
    sheet = Image.new("RGB", (spread.width + 2 * M, spread.height + 2 * M + 70), "white")
    sheet.paste(spread, (M, M))
    d = ImageDraw.Draw(sheet)
    font = ImageFont.truetype(str(FONTS / "noto-sans-semicond-500.ttf"), 22)
    small = ImageFont.truetype(str(FONTS / "noto-sans-semicond-400.ttf"), 19)
    X = lambda v: M + v  # noqa: E731
    d.rectangle((X(0), X(0), X(spread.width) - 1, X(spread.height) - 1), outline=(220, 30, 30), width=2)
    d.rectangle((X(B), X(B), X(spread.width - B), X(spread.height - B)), outline=(0, 190, 230), width=2)
    for x in (B + W, B + W + D):
        d.line((X(x), X(0) - 30, X(x), X(spread.height) + 30), fill=(0, 190, 230), width=2)
    s = SECURITE * k
    for x0, w in ((B, W), (B + W + D, W)):
        box = (X(x0 + s), X(B + s), X(x0 + w - s), X(B + H - s))
        for i in range(int(box[0]), int(box[2]), 16):
            d.line((i, box[1], min(i + 8, box[2]), box[1]), fill=(230, 0, 160), width=2)
            d.line((i, box[3], min(i + 8, box[2]), box[3]), fill=(230, 0, 160), width=2)
        for j in range(int(box[1]), int(box[3]), 16):
            d.line((box[0], j, box[0], min(j + 8, box[3])), fill=(230, 0, 160), width=2)
            d.line((box[2], j, box[2], min(j + 8, box[3])), fill=(230, 0, 160), width=2)
    labels = [(B + W / 2, "4e de couverture"), (B + W + D / 2, "dos"), (B + W + D + W / 2, "1re de couverture")]
    for x, lab in labels:
        tw = d.textlength(lab, font=font)
        d.text((X(x) - tw / 2, 28), lab, font=font, fill=(40, 40, 40))
    legend = (f"Format fini {FORMAT[0]:g} × {FORMAT[1]:g} mm · dos {DOS:g} mm ({PAGES} pages) · "
              f"à plat avec fond perdu {2 * FORMAT[0] + DOS + 2 * FOND_PERDU:g} × {FORMAT[1] + 2 * FOND_PERDU:g} mm"
              ).replace(".", ",")
    d.text((M, sheet.height - 120), legend, font=font, fill=(40, 40, 40))
    keys = [((220, 30, 30), "fond perdu (3 mm, coupé)"), ((0, 190, 230), "coupe et plis du dos"),
            ((230, 0, 160), f"zone de sécurité ({SECURITE:g} mm)")]
    xx = M
    for col, lab in keys:
        d.rectangle((xx, sheet.height - 72, xx + 26, sheet.height - 58), fill=col)
        d.text((xx + 36, sheet.height - 78), lab.replace(".", ","), font=small, fill=(40, 40, 40))
        xx += 60 + d.textlength(lab, font=small)
    sheet.save(out)


MOCKUP_HTML = """<!doctype html><html><head><meta charset="utf-8"><style>
html,body{margin:0;width:1600px;height:1100px;overflow:hidden;
  background:radial-gradient(ellipse 70% 60% at 50% 42%,#2b3442 0%,#151a22 70%,#0d1016 100%)}
.scene{position:absolute;left:0;top:0;width:1600px;height:1100px;perspective:2600px}
.book{position:absolute;left:__LEFT__px;top:120px;width:__W__px;height:__H__px;transform-style:preserve-3d;
  transform:rotateY(30deg)}
.face{position:absolute;inset:0;background:url('__FRONT__') center/100% 100%}
.face:after{content:"";position:absolute;inset:0;
  background:linear-gradient(100deg,rgba(0,0,0,.28) 0%,rgba(0,0,0,0) 4%,rgba(255,255,255,.07) 30%,
  rgba(255,255,255,0) 60%,rgba(0,0,0,.10) 100%)}
.spine{position:absolute;left:-__D__px;top:0;width:__D__px;height:__H__px;
  background:url('__SPINE__') center/100% 100%;transform-origin:right center;transform:rotateY(-90deg)}
.spine:after{content:"";position:absolute;inset:0;
  background:linear-gradient(90deg,rgba(0,0,0,.45),rgba(0,0,0,.18) 45%,rgba(255,255,255,.06) 80%,rgba(0,0,0,.2))}
.shadow{position:absolute;left:__SL__px;top:__ST__px;width:__SW__px;height:70px;border-radius:50%;
  background:radial-gradient(closest-side,rgba(0,0,0,.6),rgba(0,0,0,0));filter:blur(6px)}
</style></head><body><div class="scene"><div class="shadow"></div><div class="book">
<div class="spine"></div><div class="face"></div></div></div></body></html>"""


def mockup(front_png, spine_png, out):
    """Le livre en volume (aperçu), rendu par le Chromium de Playwright."""
    H = 860
    W = round(H * FORMAT[0] / FORMAT[1])
    D = max(8, round(H * DOS / FORMAT[1]))
    html = MOCKUP_HTML
    for key, val in {"__LEFT__": 800 - W // 2 + 30, "__W__": W, "__H__": H, "__D__": D,
                     "__FRONT__": Path(front_png).as_uri(), "__SPINE__": Path(spine_png).as_uri(),
                     "__SL__": 800 - W // 2 - 20, "__ST__": 120 + H - 40, "__SW__": W + 120}.items():
        html = html.replace(key, str(val))
    with tempfile.TemporaryDirectory() as tmp:
        page = Path(tmp) / "maquette.html"
        page.write_text(html)
        jobs = Path(tmp) / "jobs.json"
        jobs.write_text(json.dumps([{"file": str(page), "out": str(out), "width": 1600, "height": 1100}]))
        env = dict(os.environ)
        env["NODE_PATH"] = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()
        subprocess.run(["node", str(RENDER), str(jobs)], check=True, env=env)


def palettes_board(out, dpi=84):
    """Les palettes côte à côte, sur la même 1re de couverture, pour choisir."""
    cw, gap, m, top = round(FORMAT[0] * dpi / 25.4), 44, 64, 150
    ch = round(FORMAT[1] * dpi / 25.4)
    board = Image.new("RGB", (2 * m + len(PALETTES) * cw + (len(PALETTES) - 1) * gap, top + ch + 150), (244, 242, 238))
    d = ImageDraw.Draw(board)
    big = ImageFont.truetype(str(FONTS / "noto-sans-600.ttf"), 40)
    lab = ImageFont.truetype(str(FONTS / "noto-sans-600.ttf"), 27)
    small = ImageFont.truetype(str(FONTS / "noto-sans-semicond-400.ttf"), 21)
    d.text((m, 46), "Mathématiques Financières · couleurs de couverture au choix", font=big, fill=(30, 30, 30))
    with tempfile.TemporaryDirectory() as tmp:
        for i, (key, pal) in enumerate(PALETTES.items()):
            pdf = Path(tmp) / f"{key}.pdf"
            pdf_imprimeur(pdf, pal)
            front = panels(raster(pdf, dpi, Path(tmp) / f"{key}.png"), dpi)[2].resize((cw, ch), Image.LANCZOS)
            x = m + i * (cw + gap)
            board.paste(front, (x, top))
            name = f"{chr(65 + i)} · {pal.nom}" + ("  (mon conseil)" if key == "emeraude" else "")
            d.text((x, top + ch + 26), name, font=lab, fill=(30, 30, 30))
            words, line, yy = pal.resume.split(), "", top + ch + 72
            for w in words:  # résumé sur deux lignes au plus
                if d.textlength(f"{line} {w}".strip(), font=small) > cw:
                    d.text((x, yy), line, font=small, fill=(90, 90, 90))
                    line, yy = w, yy + 30
                else:
                    line = f"{line} {w}".strip()
            d.text((x, yy), line, font=small, fill=(90, 90, 90))
    board.save(out)


LISEZ_MOI = """MATHÉMATIQUES FINANCIÈRES · couverture du livre
Professeur Raoul · Édition Moderna · {annee}
==============================================

POUR L'IMPRIMEUR
- {nom}_couverture_imprimeur.pdf
  Couverture à plat : 4e de couverture + dos + 1re de couverture, en CMJN, texte vectorisé
  (aucune police à installer).
  Format fini de chaque face : {fw} x {fh} mm. Dos : {dos} mm. Fond perdu : {fp} mm tout autour.
  Taille du fichier à plat : {lw} x {lh} mm.
- {nom}_couverture_traits-de-coupe.pdf
  La même couverture avec les traits de coupe et les repères de pliure du dos.

À FAIRE AVANT L'IMPRESSION
- Le dos ({dos} mm) est calculé pour {pages} pages à {ep} mm par page : donnez à l'imprimeur le
  nombre de pages exact et le papier choisi, il vous dira l'épaisseur réelle du dos.
- Les textes entre crochets ou en couleur pâle sont des textes d'attente : présentation de
  l'auteur, prix et code-barres ISBN. Ils seront remplacés par les vraies informations.

POUR LE WEB ET LES RÉSEAUX
- {nom}_face-avant.png (300 dpi) et {nom}_face-avant.jpg (1200 px de large) :
  boutique en ligne, WhatsApp, Facebook, Instagram.
- {nom}_4e-de-couverture.png
- couverture-maquette.png : le livre en volume, pour la promotion.
- couverture-controle.png : la couverture à plat avec les repères de coupe et de sécurité.

Couleurs : {palette}.
Polices : Noto Serif et Noto Sans (licence libre SIL OFL 1.1, usage commercial autorisé).
"""


def cmjn(col):
    return "C{:.0f} M{:.0f} J{:.0f} N{:.0f}".format(*(100 * v for v in (col.cyan, col.magenta, col.yellow, col.black)))


def package(palette):
    """LISEZ-MOI et archive à envoyer (dates fixes dans le ZIP : même contenu, même fichier)."""
    fr = lambda v: f"{v:g}".replace(".", ",")  # noqa: E731
    txt = LISEZ_MOI.format(
        nom=NOM, annee=ANNEE, fw=fr(FORMAT[0]), fh=fr(FORMAT[1]), dos=fr(DOS), fp=fr(FOND_PERDU),
        lw=fr(round(2 * FORMAT[0] + DOS + 2 * FOND_PERDU, 1)), lh=fr(FORMAT[1] + 2 * FOND_PERDU), pages=PAGES,
        ep=fr(EPAISSEUR_PAGE),
        palette=f"{palette.nom.lower()} : fond {cmjn(palette.fond_haut)} en haut, {cmjn(palette.fond_bas)} en bas, "
                f"accent {cmjn(palette.accent)}")
    (OUT / "LISEZ-MOI.txt").write_text(txt, encoding="utf-8")
    files = sorted(OUT.iterdir()) + [PLANCHES / "couverture-maquette.png", PLANCHES / "couverture-controle.png"]
    archive = ROOT / f"{NOM}_couverture.zip"
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as z:
        for f in files:
            info = zipfile.ZipInfo(f"{NOM}_couverture/{f.name}", date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, f.read_bytes())
    return archive


def main():
    import sys
    key = sys.argv[sys.argv.index("--palette") + 1] if "--palette" in sys.argv else PALETTE
    palette = PALETTES[key]
    OUT.mkdir(exist_ok=True)
    PLANCHES.mkdir(exist_ok=True)
    pdf = OUT / f"{NOM}_couverture_imprimeur.pdf"
    pdf_imprimeur(pdf, palette)
    pdf_traits(OUT / f"{NOM}_couverture_traits-de-coupe.pdf", palette)
    with tempfile.TemporaryDirectory() as tmp:
        hi = raster(pdf, 300, Path(tmp) / "hi.png")
        back, spine, front = panels(hi, 300)
        front.save(OUT / f"{NOM}_face-avant.png", dpi=(300, 300))
        back.save(OUT / f"{NOM}_4e-de-couverture.png", dpi=(300, 300))
        front.resize((1200, round(1200 * front.height / front.width)), Image.LANCZOS).save(
            OUT / f"{NOM}_face-avant.jpg", quality=90)
        spine.save(Path(tmp) / "dos.png")
        mockup(OUT / f"{NOM}_face-avant.png", Path(tmp) / "dos.png", PLANCHES / "couverture-maquette.png")
        lo = raster(pdf, 110, Path(tmp) / "lo.png")
        control_sheet(lo, 110, PLANCHES / "couverture-controle.png")
    palettes_board(PLANCHES / "couverture-palettes.png")
    archive = package(palette)
    print(f"palette {palette.nom} ; dos {DOS:g} mm pour {PAGES} pages ; fichiers dans {OUT} et {PLANCHES} ; "
          f"archive {archive.name} ({archive.stat().st_size / 1e6:.1f} Mo)")


if __name__ == "__main__":
    main()
