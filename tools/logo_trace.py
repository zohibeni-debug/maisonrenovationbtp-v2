# -*- coding: utf-8 -*-
"""Vectorise le logo Artisan Druart (site/brand-src/logo-artisan-druart.png) en groupes SVG animables.

Sortie : site/logo_parts.json  { groupe: {"color": "dark"|"taupe", "d": "<path data>"} }
Groupes : roof, base, arc, window, roller, artisan, druart, tagline_t (taupe), tagline_d (sombre), lines.
"""
import json, os
import numpy as np
import potrace
from PIL import Image
from scipy import ndimage

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
a = np.asarray(Image.open(os.path.join(ROOT, "site", "brand-src", "logo-artisan-druart.png")).convert("RGBA")).astype(int)
rgb, al = a[..., :3], a[..., 3]
lum = rgb.mean(2)
vis = al > 100
dark = vis & (lum < 85)
taupe = vis & (lum >= 85)
dl, _ = ndimage.label(dark)
tl, _ = ndimage.label(taupe)

def comps(lab, mask):
    out = []
    for i, sl in enumerate(ndimage.find_objects(lab)):
        sz = int((lab[sl] == i + 1).sum())
        if sz > 150:
            out.append((i + 1, sl[1].start, sl[1].stop, sl[0].start, sl[0].stop, sz))
    return out

D, T = comps(dl, dark), comps(tl, taupe)

def pick(cs, cond):
    return [c[0] for c in cs if cond(*c[1:5])]

groups = {
    "roof": ("dark", pick(D, lambda x0, x1, y0, y1: x0 < 100 and y1 < 820)),
    "base": ("dark", pick(D, lambda x0, x1, y0, y1: 150 < x0 < 260 and y0 > 500 and y1 < 820)),
    "roller_d": ("dark", pick(D, lambda x0, x1, y0, y1: 560 < x0 < 900 and y1 < 760)),
    "artisan": ("dark", pick(D, lambda x0, x1, y0, y1: 815 < y0 < 840)),
    "tagline_d": ("dark", pick(D, lambda x0, x1, y0, y1: y0 > 930)),
    "arc": ("taupe", pick(T, lambda x0, x1, y0, y1: x0 > 880 and y1 < 540)),
    "roller_t": ("taupe", pick(T, lambda x0, x1, y0, y1: 600 < x0 < 880 and y1 < 440)),
    "window": ("taupe", pick(T, lambda x0, x1, y0, y1: 340 < x0 < 490 and 600 < y0 < 740)),
    "druart": ("taupe", pick(T, lambda x0, x1, y0, y1: 815 < y0 < 840)),
    "tagline_t": ("taupe", pick(T, lambda x0, x1, y0, y1: y0 > 930 and (x1 - x0) > 20 and not (y1 - y0 < 20))),
    "lines": ("taupe", pick(T, lambda x0, x1, y0, y1: y0 > 950 and (y1 - y0) < 20)),
}

def trace(mask):
    bm = potrace.Bitmap(~mask)
    plist = bm.trace(turdsize=4, turnpolicy=potrace.POTRACE_TURNPOLICY_MINORITY, alphamax=1.0, opticurve=True, opttolerance=0.25)
    parts = []
    for curve in plist:
        sp = curve.start_point
        s = [f"M{sp.x:.1f} {sp.y:.1f}"]
        for seg in curve.segments:
            if seg.is_corner:
                s.append(f"L{seg.c.x:.1f} {seg.c.y:.1f}L{seg.end_point.x:.1f} {seg.end_point.y:.1f}")
            else:
                s.append(f"C{seg.c1.x:.1f} {seg.c1.y:.1f} {seg.c2.x:.1f} {seg.c2.y:.1f} {seg.end_point.x:.1f} {seg.end_point.y:.1f}")
        s.append("Z")
        parts.append("".join(s))
    return "".join(parts)

out, used = {}, set()
for g, (col, ids) in groups.items():
    lab = dl if col == "dark" else tl
    m = np.isin(lab, ids)
    out[g] = {"color": col, "d": trace(m), "n": len(ids)}
    used |= {(col, i) for i in ids}
    print(f"{g:10} {col:5} composantes {len(ids):2}  {len(out[g]['d'])} car.")
left = [(c, i) for c, cs in (("dark", D), ("taupe", T)) for i, *_ in cs if (c, i) not in used]
print("non classées :", left)
cols = {"dark": rgb[dark].mean(0), "taupe": rgb[taupe].mean(0)}
out["_colors"] = {k: "#%02x%02x%02x" % tuple(int(v) for v in c) for k, c in cols.items()}
print(out["_colors"])
json.dump(out, open(os.path.join(ROOT, "site", "logo_parts.json"), "w"), indent=0)
