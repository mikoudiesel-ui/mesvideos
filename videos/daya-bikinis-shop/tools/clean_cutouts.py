#!/usr/bin/env python3
"""Keep the largest opaque blob of each mannequin cut-out, crop to it, soften the edge.
Usage: python3 -I tools/clean_cutouts.py <src.png> <dst.png> [bottom_crop_px]"""
import sys
import numpy as np
from PIL import Image, ImageFilter

src, dst = sys.argv[1], sys.argv[2]
bottom = int(sys.argv[3]) if len(sys.argv) > 3 else 0
im = Image.open(src).convert("RGBA")
if bottom:
    im = im.crop((0, 0, im.width, im.height - bottom))
a = np.array(im)
alpha = a[:, :, 3].astype(float)
alpha[alpha < 40] = 0
# connected components on the solid mask (4-neighbour flood fill)
mask = alpha > 128
lab = np.zeros(mask.shape, int)
cur = 0
sizes = {}
for y, x in zip(*np.nonzero(mask)):
    if lab[y, x]:
        continue
    cur += 1
    stack = [(y, x)]
    lab[y, x] = cur
    n = 0
    while stack:
        cy, cx = stack.pop()
        n += 1
        for ny, nx in ((cy + 1, cx), (cy - 1, cx), (cy, cx + 1), (cy, cx - 1)):
            if 0 <= ny < mask.shape[0] and 0 <= nx < mask.shape[1] and mask[ny, nx] and not lab[ny, nx]:
                lab[ny, nx] = cur
                stack.append((ny, nx))
    sizes[cur] = n
keep = max(sizes, key=sizes.get)
body = Image.fromarray(((lab == keep) * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(2))
alpha = np.minimum(alpha, np.array(body, float))
a[:, :, 3] = alpha.astype(np.uint8)
out = Image.fromarray(a)
out = out.crop(out.getbbox())
out.save(dst)
print(dst, out.size)
