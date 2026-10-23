"""Photos d'ambiance générées (aucune photo réelle) pour les mises en situation des logos.

Chaque fonction renvoie une image PIL RGB déterministe : coucher de soleil, portrait studio en contre-jour,
montagnes à l'aube, filés de lumière en ville, plage, objet sur fond pastel, bokeh de soirée.
"""

import numpy as np
from PIL import Image, ImageFilter


def _grid(W, H):
    y, x = np.mgrid[0:H, 0:W].astype(float)
    return x / W, y / H


def _lerp(stops, t):
    """Dégradé : `stops` = [(position, (r, g, b)), …], t tableau entre 0 et 1."""
    pos = np.array([s[0] for s in stops])
    cols = np.array([s[1] for s in stops], float)
    out = np.empty(t.shape + (3,))
    for c in range(3):
        out[..., c] = np.interp(t, pos, cols[:, c])
    return out


def _finish(img, seed, grain=3.0, blur=0.6):
    rng = np.random.default_rng(seed)
    img = img + rng.normal(0, grain, img.shape)
    im = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
    return im.filter(ImageFilter.GaussianBlur(blur)) if blur else im


def sunset(W=1080, H=1080, seed=1, warm=1.0):
    x, y = _grid(W, H)
    hz = 0.6
    sky = _lerp([(0, (24, 30, 78)), (0.35, (122, 66, 120)), (0.5, (236, 112, 78)), (hz, (255, 196, 128))], y)
    sea = _lerp([(hz, (150, 86, 92)), (1, (22, 24, 52))], y)
    img = np.where((y < hz)[..., None], sky, sea)
    sx, sy, r = 0.58, hz - 0.055, 0.06
    d = np.hypot((x - sx) * W / H, y - sy)
    img += (np.clip(1 - d / r, 0, 1) ** 0.25)[..., None] * np.array([40, 30, 10]) * 3
    img += (np.exp(-d / 0.18) * 0.6)[..., None] * np.array([255, 150, 80]) * warm * (y < hz)[..., None]
    rng = np.random.default_rng(seed)
    waves = np.sin(y * 900 + rng.uniform(0, 6) + np.sin(x * 40) * 2) * 0.5 + 0.5
    streak = np.exp(-((x - sx) / (0.04 + (y - hz) * 0.35)) ** 2) * (y > hz) * waves
    img += streak[..., None] * np.array([255, 170, 100]) * 0.8
    return _finish(img, seed)


def portrait(W=1080, H=1080, seed=2, back=((70, 62, 58), (24, 22, 24)), rim=(255, 150, 80)):
    x, y = _grid(W, H)
    d = np.hypot((x - 0.62) * W / H, y - 0.32)
    img = _lerp([(0, back[0]), (0.9, back[1])], np.clip(d, 0, 1))
    head = ((x - 0.48) / 0.115) ** 2 + ((y - 0.37) / 0.145) ** 2 < 1
    neck = (np.abs(x - 0.48) < 0.07) & (y > 0.45) & (y < 0.62)
    shoulders = (y > 0.6 + 0.5 * ((x - 0.48) / 0.46) ** 2) & (np.abs(x - 0.48) < 0.46)  # épaules en pente
    mask = Image.fromarray(((head | neck | shoulders) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(W / 300))
    m = np.asarray(mask, float) / 255
    edge = np.clip(m - np.asarray(mask.filter(ImageFilter.GaussianBlur(W / 60)), float) / 255, 0, 1)
    side = np.clip((x - 0.4) * 4, 0, 1)  # lumière de contre-jour venant de la droite
    body = np.array([22, 20, 24]) * np.ones_like(img)
    img = img * (1 - m[..., None]) + body * m[..., None]
    img += (edge * side * 3.2)[..., None] * np.array(rim)
    return _finish(img, seed, blur=0.8)


def mountains(W=1080, H=1080, seed=3):
    x, y = _grid(W, H)
    img = _lerp([(0, (88, 120, 170)), (0.45, (240, 170, 160)), (0.62, (255, 222, 170))], y)
    d = np.hypot((x - 0.32) * W / H, y - 0.5)
    img += (np.exp(-d / 0.12))[..., None] * np.array([255, 220, 160]) * 0.7
    rng = np.random.default_rng(seed)
    cols = [(176, 150, 170), (128, 104, 132), (84, 70, 98), (46, 40, 60), (20, 18, 28)]
    for i, c in enumerate(cols):
        base = 0.5 + 0.1 * i
        ridge = base + sum(rng.uniform(0.01, 0.05) / (k + 1) * np.sin(x[0] * rng.uniform(4, 9) * (k + 1) + rng.uniform(0, 6))
                           for k in range(5))
        img = np.where((y > ridge[None, :])[..., None], np.array(c, float), img)
    return _finish(img, seed)


def trails(W=1080, H=1080, seed=4):
    x, y = _grid(W, H)
    img = _lerp([(0, (10, 14, 34)), (1, (30, 22, 40))], y)
    rng = np.random.default_rng(seed)
    layer = np.zeros((H, W, 3))
    for i in range(14):
        a, b = rng.uniform(0.55, 0.9), rng.uniform(-0.25, 0.25)
        yy = a + b * (x - 0.5) + 0.06 * np.sin(x * 3 + i)
        w = rng.uniform(0.002, 0.006)
        col = np.array([[255, 120, 50], [255, 60, 50], [255, 236, 210], [255, 180, 90]][i % 4], float)
        layer += (np.exp(-((y - yy) / w) ** 2) * rng.uniform(0.5, 1.0))[..., None] * col
    for _ in range(40):
        cx, cy, r = rng.uniform(0, 1), rng.uniform(0, 0.55), rng.uniform(0.01, 0.04)
        d = np.hypot((x - cx) * W / H, y - cy)
        layer += (np.clip((r - d) / 0.003, 0, 1) * rng.uniform(0.1, 0.35))[..., None] * np.array([255, 200, 130])
    im = Image.fromarray(np.clip(img + layer, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.5))
    return _finish(np.asarray(im, float), seed, blur=0)


def beach(W=1080, H=1080, seed=5):
    x, y = _grid(W, H)
    img = _lerp([(0, (70, 150, 220)), (0.45, (170, 215, 240)), (0.5, (40, 170, 190)), (0.66, (110, 210, 205)),
                 (0.7, (240, 226, 196)), (1, (222, 196, 158))], y)
    rng = np.random.default_rng(seed)
    for k in range(4):
        yy = 0.665 + 0.012 * k + 0.008 * np.sin(x * 14 + rng.uniform(0, 6))
        img += (np.exp(-((y - yy) / 0.003) ** 2) * 0.8)[..., None] * np.array([255, 255, 255]) * 0.5
    return _finish(img, seed)


def product(W=1080, H=1080, seed=6, back=((255, 214, 190), (246, 170, 140))):
    x, y = _grid(W, H)
    img = _lerp([(0, back[0]), (0.62, back[1]), (0.63, (250, 200, 176)), (1, (236, 176, 150))], y)
    cx, cy, r = 0.5, 0.5, 0.2
    d = np.hypot((x - 0.5) / 0.26, (y - 0.71) / 0.04)
    img *= (1 - 0.35 * np.exp(-d ** 2))[..., None]
    dx, dy = (x - cx) / r, (y - cy) / r
    inside = dx ** 2 + dy ** 2 < 1
    nz = np.sqrt(np.clip(1 - dx ** 2 - dy ** 2, 0, 1))
    lam = np.clip(-0.5 * dx - 0.6 * dy + 0.62 * nz, 0, 1)
    spec = np.clip(-0.5 * dx - 0.6 * dy + 0.62 * nz, 0, 1) ** 40
    sphere = np.array([255, 116, 31]) * (0.35 + 0.75 * lam)[..., None] + 255 * spec[..., None]
    img = np.where(inside[..., None], sphere, img)
    return _finish(img, seed, grain=2)


def bokeh(W=1400, H=900, seed=11):
    x, y = _grid(W, H)
    t = y[..., None]
    img = np.array([22, 26, 40]) * (1 - t) + np.array([70, 40, 30]) * t
    X, Y = x * W, y * H
    light = np.zeros((H, W, 3))
    rng = np.random.default_rng(seed)
    palette = np.array([[255, 168, 88], [255, 214, 160], [255, 122, 52], [255, 236, 214], [255, 190, 120]])
    for _ in range(85):
        cx, cy, r = rng.uniform(0, W), rng.uniform(-0.05 * H, 0.9 * H), rng.uniform(16, 95)
        d = np.hypot(X - cx, Y - cy)
        disc = np.clip((r - d) / 2.5, 0, 1) * (0.75 + 0.25 * np.clip(d / r, 0, 1))
        rim = np.clip(1 - np.abs(d - r + 3) / 3, 0, 1) * 0.3
        light += (disc + rim)[..., None] * palette[rng.integers(len(palette))] * rng.uniform(0.06, 0.3)
    img = img + light
    vig = 1 - 0.55 * np.clip(np.hypot((X - W / 2) / (W / 2), (Y - H / 2) / (H / 2)) - 0.35, 0, 1) ** 1.4
    return _finish(img * vig[..., None], seed, grain=0, blur=1.2)
