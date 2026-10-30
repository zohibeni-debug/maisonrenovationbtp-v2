# -*- coding: utf-8 -*-
"""Illustrations dessinées en SVG : textures de façade (diagnostic) et cartes de la zone d'intervention."""
import html
import math
import random

import communes as CM

W, H = 480, 360


def _grain(uid, freq=0.9, opacity=0.5, seed=4):
    return (f'<filter id="gr{uid}" x="0" y="0" width="100%" height="100%" color-interpolation-filters="sRGB">'
            f'<feTurbulence type="fractalNoise" baseFrequency="{freq}" numOctaves="2" seed="{seed}"/>'
            '<feColorMatrix values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  -0.7 -0.7 -0.7 0 1.25"/></filter>'
            f'<filter id="mo{uid}" x="0" y="0" width="100%" height="100%" color-interpolation-filters="sRGB">'
            f'<feTurbulence type="fractalNoise" baseFrequency="0.012 0.02" numOctaves="3" seed="{seed + 7}"/>'
            '<feColorMatrix values="0 0 0 0 0.35  0 0 0 0 0.3  0 0 0 0 0.25  0 0 0 0.9 -0.32"/></filter>'), \
        (f'<rect width="{W}" height="{H}" filter="url(#mo{uid})" opacity="0.55"/>'
         f'<rect width="{W}" height="{H}" filter="url(#gr{uid})" opacity="{opacity}"/>')


def _wobble(rng, x1, y1, x2, y2, steps=3, amp=4):
    pts = [(x1, y1)]
    for i in range(1, steps):
        t = i / steps
        pts.append((x1 + (x2 - x1) * t + rng.uniform(-amp, amp), y1 + (y2 - y1) * t + rng.uniform(-amp, amp)))
    pts.append((x2, y2))
    return "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)


def _window(x, y, w, h, frame="#efe9df", glass="#3a3835"):
    return (f'<rect x="{x - 9}" y="{y - 9}" width="{w + 18}" height="{h + 18}" fill="{frame}"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{glass}"/>'
            f'<rect x="{x + w / 2 - 3}" y="{y}" width="6" height="{h}" fill="{frame}" opacity=".9"/>'
            f'<rect x="{x - 16}" y="{y + h + 9}" width="{w + 32}" height="13" fill="#e8e2d7"/>'
            f'<rect x="{x - 16}" y="{y + h + 22}" width="{w + 32}" height="3" fill="#000" opacity=".12"/>')


def tile(key, uid, cls="tile", label=None):
    rng = random.Random(key)
    defs, body = [], []
    if key == "salissures":
        g_defs, g_body = _grain(uid, seed=3)
        defs.append(g_defs)
        defs.append(f'<linearGradient id="st{uid}" gradientUnits="userSpaceOnUse" x1="0" y1="205" x2="0" y2="320"><stop offset="0" stop-color="#3a3530" stop-opacity=".5"/><stop offset="1" stop-color="#3a3530" stop-opacity="0"/></linearGradient>')
        defs.append(f'<linearGradient id="al{uid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5d6a37" stop-opacity="0"/><stop offset=".45" stop-color="#5d6a37" stop-opacity=".55"/><stop offset="1" stop-color="#2f3a1e" stop-opacity=".9"/></linearGradient>')
        defs.append(f'<filter id="pa{uid}" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="0.035 0.09" numOctaves="3" seed="9" result="n"/><feColorMatrix in="n" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 2.4 -0.9" result="m"/><feComposite in="SourceGraphic" in2="m" operator="in"/></filter>')
        body.append(f'<rect width="{W}" height="{H}" fill="#d6cec1"/>')
        body.append(g_body)
        body.append(_window(170, 34, 140, 140))
        for i in range(14):
            x = 160 + i * 11.5 + rng.uniform(-5, 5)
            w = rng.uniform(2, 9)
            body.append(f'<path d="M{x:.1f} 205 q{rng.uniform(-3, 3):.1f} 40 {rng.uniform(-4, 4):.1f} {rng.uniform(30, 110):.1f}" stroke="url(#st{uid})" stroke-width="{w:.1f}" stroke-linecap="round" fill="none" opacity="{rng.uniform(.35, .8):.2f}"/>')
        body.append(f'<rect y="210" width="{W}" height="150" fill="url(#al{uid})" filter="url(#pa{uid})"/>')
        body.append(f'<rect y="300" width="{W}" height="60" fill="#2f3a1e" opacity=".35" filter="url(#pa{uid})"/>')
    elif key == "faiencage":
        g_defs, g_body = _grain(uid, seed=5)
        defs.append(g_defs)
        body.append(f'<rect width="{W}" height="{H}" fill="#dcd4c8"/>')
        body.append(g_body)
        step = 34
        pts = {}
        for i in range(-1, W // step + 2):
            for j in range(-1, H // step + 2):
                pts[(i, j)] = (i * step + rng.uniform(-13, 13), j * step + rng.uniform(-13, 13))
        paths = []
        for (i, j), (x, y) in pts.items():
            for di, dj in ((1, 0), (0, 1)):
                if (i + di, j + dj) in pts and rng.random() > 0.12:
                    x2, y2 = pts[(i + di, j + dj)]
                    paths.append(_wobble(rng, x, y, x2, y2, steps=3, amp=3.5))
        body.append(f'<path d="{" ".join(paths)}" fill="none" stroke="#fff" stroke-opacity=".35" stroke-width="1.6" transform="translate(.8 .8)"/>')
        body.append(f'<path d="{" ".join(paths)}" fill="none" stroke="#5f564d" stroke-opacity=".62" stroke-width=".85"/>')
    elif key == "fissure":
        g_defs, g_body = _grain(uid, seed=6)
        defs.append(g_defs)
        body.append(f'<rect width="{W}" height="{H}" fill="#ddd5ca"/>')
        body.append(g_body)
        body.append(_window(262, 34, 140, 130))
        pts = [(254, 186)]
        x, y = 254, 186
        while y < H + 10:
            x -= rng.uniform(10, 24)
            y += rng.uniform(14, 26)
            pts.append((x, y))
        d = "M" + " L".join(f"{a:.1f} {b:.1f}" for a, b in pts)
        body.append(f'<path d="{d}" fill="none" stroke="#000" stroke-opacity=".12" stroke-width="7" stroke-linejoin="round"/>')
        body.append(f'<path d="{d}" fill="none" stroke="#2c2620" stroke-width="2.6" stroke-linejoin="round"/>')
        for k in (2, 4, 6):
            if k < len(pts):
                a, b = pts[k]
                body.append(f'<path d="{_wobble(rng, a, b, a - rng.uniform(20, 40), b + rng.uniform(-5, 20), 3, 3)}" fill="none" stroke="#2c2620" stroke-width="1" stroke-opacity=".7"/>')
        a, b = pts[3]
        body.append(f'<g transform="translate({a:.1f} {b:.1f}) rotate(-38)"><rect x="-34" y="-11" width="68" height="22" rx="3" fill="#f1ede6" stroke="#8b8177"/>'
                    '<path d="M-26 -11v7M-18 -11v5M-10 -11v7M-2 -11v5M6 -11v7M14 -11v5M22 -11v7" stroke="#8b8177" stroke-width="1"/>'
                    '<path d="M0 -11V11" stroke="#c0392b" stroke-width="1.4"/></g>')
    elif key == "creux":
        g_defs, g_body = _grain(uid, seed=8)
        defs.append(g_defs)
        defs.append(f'<clipPath id="cp{uid}"><path d="M70 110 C120 70 210 80 250 120 C300 160 290 230 240 262 C190 296 110 290 80 250 C50 210 40 140 70 110Z"/></clipPath>')
        body.append(f'<rect width="{W}" height="{H}" fill="#dad2c6"/>')
        blocks = []
        for r in range(0, 9):
            off = 0 if r % 2 == 0 else -40
            for c in range(-1, 7):
                blocks.append(f'<rect x="{c * 80 + off + 2}" y="{r * 40 + 2}" width="76" height="36" fill="#a7a197"/>')
        body.append(f'<g clip-path="url(#cp{uid})"><rect width="{W}" height="{H}" fill="#86817a"/>{"".join(blocks)}<rect width="{W}" height="{H}" fill="#000" opacity=".08"/></g>')
        body.append(g_body)
        body.append('<path d="M70 110 C120 70 210 80 250 120 C300 160 290 230 240 262 C190 296 110 290 80 250 C50 210 40 140 70 110Z" fill="none" stroke="#efe9df" stroke-width="5"/>')
        body.append('<path d="M70 110 C120 70 210 80 250 120 C300 160 290 230 240 262 C190 296 110 290 80 250 C50 210 40 140 70 110Z" fill="none" stroke="#000" stroke-opacity=".25" stroke-width="2" transform="translate(3 4)"/>')
        for _ in range(6):
            a = rng.uniform(0, math.tau)
            x1, y1 = 165 + math.cos(a) * 125, 185 + math.sin(a) * 100
            body.append(f'<path d="{_wobble(rng, x1, y1, x1 + math.cos(a) * rng.uniform(40, 90), y1 + math.sin(a) * rng.uniform(30, 70), 4, 5)}" fill="none" stroke="#4f4740" stroke-width="1.2" stroke-opacity=".7"/>')
    elif key == "meuliere":
        g_defs, g_body = _grain(uid, freq=1.1, opacity=.45, seed=2)
        defs.append(g_defs)
        body.append(f'<rect width="{W}" height="{H}" fill="#e2d6c2"/>')
        tones = ["#b98b54", "#a9783f", "#c69c65", "#9d6c3b", "#b48049", "#c2915a", "#a37a4c"]
        cw, ch = 64, 46
        for r in range(-1, H // ch + 2):
            off = rng.uniform(-30, 30)
            x = -cw + off
            while x < W + cw:
                w = cw * rng.uniform(.75, 1.3)
                cx, cy = x + w / 2, r * ch + ch / 2 + rng.uniform(-4, 4)
                n = rng.randint(7, 11)
                sx, sy = w / 2 + 1, ch / 2 + 1
                pts = []
                for k in range(n):
                    a = k / n * math.tau + rng.uniform(-.18, .18)
                    f = rng.uniform(.86, 1.08)
                    pts.append((cx + math.cos(a) * sx * f, cy + math.sin(a) * sy * f))
                d = "M" + " L".join(f"{px:.1f} {py:.1f}" for px, py in pts) + "Z"
                body.append(f'<path d="{d}" fill="{rng.choice(tones)}" stroke="#e2d6c2" stroke-width="5" stroke-linejoin="round" paint-order="stroke"/>')
                body.append(f'<path d="{d}" fill="none" stroke="#5c3d1f" stroke-opacity=".35" stroke-width="1" transform="translate(1 1.5)"/>')
                for _ in range(rng.randint(5, 10)):
                    body.append(f'<ellipse cx="{cx + rng.uniform(-w * .32, w * .32):.1f}" cy="{cy + rng.uniform(-12, 12):.1f}" rx="{rng.uniform(1, 3.4):.1f}" ry="{rng.uniform(.8, 2.2):.1f}" fill="#4f341a" opacity=".5"/>')
                x += w
        for x, y, w in ((300, 120, 130), (40, 250, 150), (330, 290, 110)):
            body.append(f'<path d="M{x} {y} q{w / 3} -8 {w} 4" stroke="#9a958c" stroke-width="11" fill="none" stroke-linecap="round" opacity=".95"/>')
            body.append(f'<path d="M{x + 10} {y - 1} l{w / 4} 3 l{w / 5} -4" stroke="#4a443d" stroke-width="1.3" fill="none"/>')
        body.append(g_body)
    elif key == "froid":
        defs.append(f'<linearGradient id="tb{uid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffe066"/><stop offset=".25" stop-color="#ff8c1a"/><stop offset=".5" stop-color="#d6246e"/><stop offset=".75" stop-color="#5a2a9c"/><stop offset="1" stop-color="#1b2266"/></linearGradient>')
        defs.append(f'<radialGradient id="tw{uid}" cx=".5" cy=".55" r=".75"><stop offset="0" stop-color="#3a2b8c"/><stop offset="1" stop-color="#161c58"/></radialGradient>')
        defs.append(f'<filter id="bl{uid}" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="9"/></filter>')
        body.append(f'<rect width="{W}" height="{H}" fill="url(#tw{uid})"/>')
        body.append(f'<g filter="url(#bl{uid})"><rect x="-20" y="150" width="{W + 40}" height="26" fill="#c2266e"/>'
                    '<rect x="128" y="44" width="170" height="164" fill="none" stroke="#ff7a1a" stroke-width="22"/>'
                    '<rect x="150" y="66" width="126" height="120" fill="#e0306a"/>'
                    '<rect x="-20" y="330" width="520" height="40" fill="#7a2c9a"/><rect x="0" y="0" width="30" height="360" fill="#4a2a90"/></g>')
        body.append('<rect x="150" y="66" width="126" height="120" fill="#ffb02e" opacity=".55"/>')
        body.append('<g fill="none" stroke="#fff" stroke-width="1.6"><circle cx="213" cy="163" r="14"/><path d="M213 141v10M213 175v10M191 163h10M225 163h10"/></g>')
        body.append('<text x="234" y="140" fill="#fff" font-size="15" font-weight="600">6,2 °C</text>')
        body.append(f'<rect x="436" y="34" width="16" height="292" rx="3" fill="url(#tb{uid})"/>')
        body.append('<g fill="#fff" font-size="12" text-anchor="end"><text x="428" y="44">19 °C</text><text x="428" y="326">3 °C</text></g>')
    elif key == "toiture":
        g_defs, g_body = _grain(uid, seed=11, opacity=.35)
        defs.append(g_defs)
        defs.append(f'<filter id="ms{uid}" x="-10%" y="-10%" width="120%" height="120%"><feTurbulence type="fractalNoise" baseFrequency="0.08" numOctaves="3" seed="2" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="14"/></filter>')
        body.append(f'<rect width="{W}" height="{H}" fill="#7b3a26"/>')
        tones = ["#b5583a", "#a84f33", "#bf6342", "#ad5536", "#9e4a30"]
        for r in range(0, 12):
            y = r * 32 - 10
            off = 0 if r % 2 == 0 else -27
            for c in range(-1, 10):
                x = c * 54 + off
                body.append(f'<path d="M{x} {y} h50 v26 q-25 10 -50 0z" fill="{rng.choice(tones)}"/>'
                            f'<path d="M{x + 25} {y + 3} v24" stroke="#000" stroke-opacity=".12" stroke-width="3"/>'
                            f'<path d="M{x} {y + 26} q25 10 50 0" stroke="#000" stroke-opacity=".28" stroke-width="2" fill="none"/>')
        moss = []
        for _ in range(26):
            moss.append(f'<ellipse cx="{rng.uniform(0, 300):.0f}" cy="{rng.uniform(150, 360):.0f}" rx="{rng.uniform(10, 34):.0f}" ry="{rng.uniform(5, 13):.0f}" fill="{rng.choice(["#6b7a35", "#56652a", "#7f8c45"])}"/>')
        body.append(f'<g filter="url(#ms{uid})" opacity=".92">{"".join(moss)}</g>')
        body.append(g_body)
    else:
        raise KeyError(key)
    lab = f' role="img" aria-label="{html.escape(label)}"' if label else ' aria-hidden="true"'
    return (f'<svg class="{cls}" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice" focusable="false"{lab}>'
            f'<defs>{"".join(defs)}</defs>{"".join(body)}</svg>')


# ---------------------------------------------------------------------------
# Cartes
# ---------------------------------------------------------------------------
S = 10  # unités SVG par km
VB = (-240, -320, 660, 630)
PARIS = CM.project(48.8566, 2.3522)
CDG = CM.project(49.0097, 2.5479)


def _base_map():
    out = []
    for r in (10, 20, 30, 40):
        out.append(f'<circle cx="0" cy="0" r="{r * S}" class="ring"/>')
        out.append(f'<text x="{r * S * 0.7071 + 6:.0f}" y="{-r * S * 0.7071 - 4:.0f}" class="ring-l">{r} km</text>')
    px, py = PARIS[0] * S, PARIS[1] * S
    out.append(f'<circle cx="{px:.0f}" cy="{py:.0f}" r="44" class="paris"/><text x="{px:.0f}" y="{py + 5:.0f}" class="paris-l" text-anchor="middle">Paris</text>')
    cx, cy = CDG[0] * S, CDG[1] * S
    out.append(f'<path d="M{cx - 7:.0f} {cy:.0f}h14M{cx:.0f} {cy - 7:.0f}v14" class="cdg"/><text x="{cx - 10:.0f}" y="{cy - 10:.0f}" class="cdg-l" text-anchor="end">Aéroport CDG</text>')
    return out


def _home():
    return ('<g class="home-mark"><circle r="16" class="home-halo"/>'
            '<path d="M-9 4v-8l9-7 9 7v8z" class="home-ico"/><text y="34" text-anchor="middle" class="home-l">Mitry-Mory</text></g>')


def zone_map(current=None, cls="map", links=True, title=None):
    out = _base_map()
    for c in CM.COMMUNES:
        x, y = (v * S for v in CM.project(c["lat"], c["lon"]))
        here = current and c["slug"] == current["slug"]
        r = 9 if here else (6 if c["pop"] and c["pop"] > 30000 else 4.5)
        dot = f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" class="dot{" dot-here" if here else ""}"/>'
        name = html.escape(c["name"])
        if links and not here:
            out.append(f'<a href="/ravalement-facade-{c["slug"]}/" class="pt" aria-label="Ravalement de façade {html.escape(CM.a_(c["name"]))}"><title>{name}</title>{dot}'
                       f'<text x="{x + 9:.0f}" y="{y + 4:.0f}" class="pt-l">{name}</text></a>')
        else:
            out.append(dot)
            if here:
                anchor = "end" if x > 250 else "start"
                dx = -14 if anchor == "end" else 14
                out.append(f'<text x="{x + dx:.0f}" y="{y + 6:.0f}" class="here-l" text-anchor="{anchor}">{name}</text>')
                out.append(f'<path d="M0 0L{x:.0f} {y:.0f}" class="here-line"/>')
    out.append(_home())
    t = f'<title>{html.escape(title)}</title>' if title else ""
    role = 'role="img" ' if not links else ""
    return f'<svg class="{cls}" viewBox="{" ".join(map(str, VB))}" {role}aria-label="{html.escape(title or "Carte de la zone d intervention")}">{t}{"".join(out)}</svg>'
