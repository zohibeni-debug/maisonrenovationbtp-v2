# -*- coding: utf-8 -*-
"""Logo Artisan Druart en SVG, reconstruit à partir du tracé vectoriel (logo_parts.json).

Variantes :
  - stacked    : logo complet (pictogramme, nom, « Couverture - Ravalement »)
  - horizontal : pictogramme + nom sur une ligne (en-tête)
  - mark       : pictogramme seul (mobile, favicon)
Couleurs : "color" (noir + taupe du logo) ou "light" (blanc + taupe clair, sur fond sombre).
La version animée (accueil) découpe le logo en calques animés par CSS (classes lg-*).
"""
import json
import math
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
P = json.load(open(os.path.join(HERE, "logo_parts.json"), encoding="utf-8"))
COLORS = {"color": {"dark": "#1d1c1a", "taupe": "#9d7d68"}, "light": {"dark": "#ffffff", "taupe": "#c3a28b"}}
MARK = ["roof", "base", "arc", "window", "roller_d", "roller_t"]
NAME = ["artisan", "druart"]
TAG = ["tagline_t", "tagline_d", "lines"]
# Boîtes (en pixels de l'image d'origine)
MARK_BOX = (49, 338, 1113, 801)
NAME_BOX = (63, 825, 1126, 923)
# Centre du « D » (estimé sur le tracé) pour le masque de peinture de l'arc
DC, DR = (881, 570), 178


def _path(g, colors, cls=None, extra=""):
    c = colors[P[g]["color"]]
    k = f' class="{cls}"' if cls else ""
    return f'<path{k} fill="{c}" fill-rule="evenodd" d="{P[g]["d"]}"{extra}/>'


def _subpaths(d):
    return [m + "Z" for m in re.split(r"Z", d) if m.strip()]


def svg(layout="stacked", mode="color", animated=False, title="Artisan Druart, couverture et ravalement", cls="logo-svg", uid="lg"):
    col = COLORS[mode]
    if layout == "stacked":
        vb = "40 328 1100 674"
        groups = MARK + NAME + TAG
        name_tr = ""
    elif layout == "mark":
        vb = "40 328 1086 482"
        groups = MARK
        name_tr = ""
    else:  # horizontal
        k = 1.8
        x0 = MARK_BOX[2] + 80
        yc = (MARK_BOX[1] + MARK_BOX[3]) / 2
        ny = (NAME_BOX[1] + NAME_BOX[3]) / 2
        tx, ty = x0 - NAME_BOX[0] * k, yc - ny * k
        w = x0 + (NAME_BOX[2] - NAME_BOX[0]) * k - 40 + 12
        vb = f"40 328 {w:.0f} 482"
        groups = MARK + NAME
        name_tr = f' transform="translate({tx:.1f} {ty:.1f}) scale({k})"'
    parts = []
    if animated:
        a0 = math.radians(-112)
        a1 = math.radians(12)
        x0, y0 = DC[0] + DR * math.cos(a0), DC[1] + DR * math.sin(a0)
        x1, y1 = DC[0] + DR * math.cos(a1), DC[1] + DR * math.sin(a1)
        parts.append(f'<defs><mask id="{uid}-m" maskUnits="userSpaceOnUse" x="700" y="300" width="500" height="320">'
                     f'<path class="lg-paint" d="M{x0:.0f} {y0:.0f} A{DR} {DR} 0 0 1 {x1:.0f} {y1:.0f}" fill="none" stroke="#fff" stroke-width="230" pathLength="1"/></mask></defs>')
        parts.append(f'<g class="lg-roof">{_path("roof", col)}</g>')
        parts.append(f'<g class="lg-base">{_path("base", col)}</g>')
        wins = "".join(f'<path class="lg-w" fill="{col["taupe"]}" d="{d}"/>' for d in _subpaths(P["window"]["d"]))
        parts.append(f'<g class="lg-win">{wins}</g>')
        parts.append(f'<g mask="url(#{uid}-m)">{_path("arc", col)}</g>')
        parts.append(f'<g class="lg-roller">{_path("roller_d", col)}{_path("roller_t", col)}</g>')
        if layout != "mark":
            parts.append(f'<g{name_tr}><g class="lg-artisan">{_path("artisan", col)}</g><g class="lg-druart">{_path("druart", col)}</g>')
            if layout == "stacked":
                parts.append(f'<g class="lg-lines">{_path("lines", col)}</g><g class="lg-tag">{_path("tagline_t", col)}{_path("tagline_d", col)}</g>')
            parts.append("</g>")
    else:
        parts += [_path(g, col) for g in MARK]
        if layout != "mark":
            parts.append(f"<g{name_tr}>" + "".join(_path(g, col) for g in (NAME + (TAG if layout == "stacked" else []))) + "</g>")
    a = " aria-hidden=\"true\"" if not title else f' role="img" aria-label="{title}"'
    t = f"<title>{title}</title>" if title else ""
    return f'<svg class="{cls}{" logo-anim" if animated else ""}" xmlns="http://www.w3.org/2000/svg" viewBox="{vb}"{a}>{t}{"".join(parts)}</svg>'


def favicon():
    """Pictogramme centré dans un carré blanc arrondi (favicon SVG)."""
    col = COLORS["color"]
    inner = "".join(_path(g, col) for g in MARK)
    s = 1000 / 1150
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000"><rect width="1000" height="1000" rx="180" fill="#fff"/>'
            f'<g transform="translate({500 - 581 * s:.1f} {500 - 570 * s:.1f}) scale({s:.3f})">{inner}</g></svg>')
