#!/usr/bin/env python3
"""Cut the shop's own TikTok thumbnails + avatar out of the profile screenshots.

Usage: python3 -I tools/crop_screens.py <shot1.webp> <shot2.webp>  ->  assets/img/
"""
import os, sys
from PIL import Image, ImageDraw, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "img")
os.makedirs(OUT, exist_ok=True)
COLS = [329, 474, 620, 766, 912, 1057]
W = 135
s1, s2 = (Image.open(p).convert("RGB") for p in sys.argv[1:3])


def save(img, box, name, scale=2.6):
    c = img.crop(box)
    c = c.resize((int(c.width * scale), int(c.height * scale)), Image.LANCZOS)
    c = c.filter(ImageFilter.UnsharpMask(radius=2, percent=60, threshold=2))
    c.save(os.path.join(OUT, name), quality=92)

# rows: (image, top, bottom-without-view-count)
rows = {"a": (s1, 199, 350), "b": (s1, 394, 545), "c": (s2, 214, 365), "d": (s2, 410, 561)}
for r, (img, y0, y1) in rows.items():
    for i, x in enumerate(COLS):
        save(img, (x + 1, y0, x + W, y1), f"t-{r}{i + 1}.jpg")

# round avatar
av = s1.crop((334, 28, 440, 134)).resize((420, 420), Image.LANCZOS)
mask = Image.new("L", av.size, 0)
ImageDraw.Draw(mask).ellipse((14, 14, 406, 406), fill=255)
out = Image.new("RGBA", av.size)
out.paste(av, (0, 0), mask)
out.save(os.path.join(OUT, "avatar.png"))
print(sorted(os.listdir(OUT)))
