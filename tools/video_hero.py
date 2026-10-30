# -*- coding: utf-8 -*-
"""Génère la vidéo de fond de l'accueil : un ravalement en cours, en boucle parfaite.

Un mur enduit défile lentement ; à gauche du rouleau, la façade est propre et fraîchement peinte,
à droite, elle est encrassée (salissures, coulures sous l'appui, algues en pied de mur).
Au premier plan, des tubes d'échafaudage et un plancher défilent plus vite (parallaxe).
Sortie : site/video/ (hero.mp4, hero.webm, hero-poster.jpg)
"""
import math, os, shutil, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "site", "video")
TMP = "/tmp/hero_frames"
W, H = 1280, 720
FPS, SECONDS = 24, 10
N = FPS * SECONDS
P = 640            # période horizontale du mur (px)
PF = 1024          # période du premier plan (parallaxe 1,6)
XB = int(W * 0.60) # front de peinture, fixe à l'écran
rng = np.random.default_rng(7)


def fnoise(h, w, beta, seed):
    """Bruit fractal périodique (filtrage FFT), normalisé 0..1."""
    r = np.random.default_rng(seed)
    f = np.fft.fft2(r.standard_normal((h, w)))
    fy = np.fft.fftfreq(h)[:, None]; fx = np.fft.fftfreq(w)[None, :]
    k = np.sqrt(fx * fx + fy * fy); k[0, 0] = 1
    n = np.real(np.fft.ifft2(f / k ** beta))
    n -= n.min(); n /= n.max()
    return n


def smooth(x, a, b):
    t = np.clip((x - a) / (b - a), 0, 1)
    return t * t * (3 - 2 * t)


# ---------------------------------------------------------------- mur (une période)
yy, xx = np.mgrid[0:H, 0:P].astype(np.float32)
low = fnoise(H, P, 1.6, 1)
mid = fnoise(H, P, 1.1, 2)
grain = fnoise(H, P, 0.15, 3)
pits = (fnoise(H, P, 0.05, 4) > 0.83).astype(np.float32)
pits = np.asarray(Image.fromarray((pits * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.7)), np.float32) / 255

clean_rgb = np.array([236, 229, 217], np.float32)
clean = clean_rgb[None, None, :] * (0.93 + 0.08 * low[..., None]) * (0.96 + 0.06 * grain[..., None])
clean *= (1 - 0.22 * pits[..., None])

dirty = np.array([196, 188, 172], np.float32)[None, None, :] * (0.82 + 0.22 * low[..., None]) * (0.93 + 0.1 * grain[..., None])
dirty *= (1 - 0.3 * pits[..., None])
grime = smooth(mid, 0.35, 0.9)[..., None]
dirty = dirty * (1 - 0.18 * grime) + np.array([92, 88, 80], np.float32) * 0.18 * grime
# fenêtre au centre de la période
wx0, wx1, wy0, wy1 = 230, 410, 150, 400
sill_y = wy1 + 14
# coulures sous l'appui
streak = np.zeros((H, P), np.float32)
for i in range(26):
    x = rng.uniform(wx0 - 10, wx1 + 10); w = rng.uniform(2, 9); L = rng.uniform(60, 230); a = rng.uniform(.35, .9)
    m = np.exp(-((xx - x) / w) ** 2) * smooth(yy, sill_y + 8, sill_y + 20) * (1 - smooth(yy, sill_y + 10, sill_y + L))
    streak = np.maximum(streak, a * m)
dirty *= (1 - 0.42 * streak[..., None])
# algues en pied de mur
alg = smooth(yy, H * 0.62, H * 0.98) * smooth(fnoise(H, P, 1.3, 5), 0.3, 0.75)
green = np.array([88, 104, 56], np.float32)
dirty = dirty * (1 - 0.62 * alg[..., None]) + green * 0.62 * alg[..., None]
dark_alg = smooth(yy, H * 0.82, H) * smooth(fnoise(H, P, 1.0, 6), 0.45, 0.8)
dirty = dirty * (1 - 0.5 * dark_alg[..., None]) + np.array([42, 48, 30], np.float32) * 0.5 * dark_alg[..., None]


def draw_window(arr):
    img = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)); d = ImageDraw.Draw(img)
    # volets battants couleur taupe
    for vx in (wx0 - 78, wx1 + 14):
        d.rectangle([vx, wy0 - 6, vx + 64, wy1 + 6], fill=(128, 109, 97))
        for k in range(wy0, wy1, 14):
            d.line([vx + 4, k, vx + 60, k + 4], fill=(108, 91, 80), width=3)
    d.rectangle([wx0 - 12, wy0 - 12, wx1 + 12, wy1 + 12], fill=(246, 244, 240))
    d.rectangle([wx0, wy0, wx1, wy1], fill=(46, 52, 58))
    mx = (wx0 + wx1) // 2
    d.rectangle([mx - 5, wy0, mx + 5, wy1], fill=(246, 244, 240))
    d.rectangle([wx0, (wy0 + wy1) // 2 - 4, wx1, (wy0 + wy1) // 2 + 4], fill=(246, 244, 240))
    d.polygon([(wx0 + 14, wy1 - 20), (wx0 + 70, wy0 + 12), (wx0 + 110, wy0 + 12), (wx0 + 54, wy1 - 20)], fill=(70, 78, 86))
    d.rectangle([wx0 - 26, sill_y - 6, wx1 + 26, sill_y + 8], fill=(232, 228, 220))
    d.rectangle([wx0 - 26, sill_y + 8, wx1 + 26, sill_y + 12], fill=(150, 146, 140))
    return np.asarray(img, np.float32)

clean = draw_window(clean)
dirty = draw_window(dirty)

# ---------------------------------------------------------------- premier plan (une période PF), RGBA
fg = Image.new("RGBA", (PF, H), (0, 0, 0, 0)); d = ImageDraw.Draw(fg)
def tube_v(x, wdt=34):
    for i in range(wdt):
        t = i / (wdt - 1); s = 0.35 + 0.65 * math.sin(math.pi * t) ** 0.6
        c = int(70 + 150 * s * (1 - 0.35 * t))
        d.line([x + i, 0, x + i, H], fill=(c, c + 2, c + 6, 255))
def tube_h(y, hgt=28):
    for i in range(hgt):
        t = i / (hgt - 1); s = 0.35 + 0.65 * math.sin(math.pi * t) ** 0.6
        c = int(70 + 150 * s * (1 - 0.35 * t))
        d.line([0, y + i, PF, y + i], fill=(c, c + 2, c + 6, 255))
tube_h(70)
for x in (180, 180 + PF // 2):
    tube_v(x)
    d.rounded_rectangle([x - 10, 58, x + 44, 110], radius=6, fill=(96, 98, 104, 255))
    d.rounded_rectangle([x - 6, 62, x + 40, 106], radius=5, fill=(140, 142, 148, 255))
# plancher en bois
for i in range(0, PF, 256):
    for j in range(64):
        c = 118 + int(22 * math.sin(j / 5.0 + i)) + (j % 7) * 2
        d.line([i, H - 64 + j, i + 252, H - 64 + j], fill=(c, int(c * 0.8), int(c * 0.6), 255))
    d.rectangle([i + 252, H - 64, i + 255, H], fill=(60, 44, 32, 255))
d.rectangle([0, H - 68, PF, H - 64], fill=(70, 52, 38, 255))
fg = fg.filter(ImageFilter.GaussianBlur(3.2))
fg_arr = np.asarray(fg, np.float32)

# ---------------------------------------------------------------- rouleau (sprite)
def roller_sprite():
    s = 2
    rw, rh = 240 * s, 74 * s
    im = Image.new("RGBA", (rw + 140 * s, rh + 160 * s), (0, 0, 0, 0)); dd = ImageDraw.Draw(im)
    for i in range(rh):
        t = i / (rh - 1); sh = 0.55 + 0.45 * math.sin(math.pi * t)
        c = (int(236 * sh), int(229 * sh), int(217 * sh), 255)
        dd.line([0, i, rw, i], fill=c)
    for k in range(0, rw, 3 * s):
        dd.line([k, 0, k + 2 * s, rh], fill=(255, 255, 255, 40))
    dd.rectangle([rw, rh // 2 - 6 * s, rw + 26 * s, rh // 2 + 6 * s], fill=(52, 52, 56, 255))
    dd.line([rw + 22 * s, rh // 2, rw + 22 * s, rh + 70 * s], fill=(52, 52, 56, 255), width=11 * s)
    dd.rounded_rectangle([rw + 8 * s, rh + 60 * s, rw + 38 * s, rh + 160 * s], radius=10 * s, fill=(40, 40, 42, 255))
    return im.resize((im.width // s, im.height // s), Image.LANCZOS)
ROLL = roller_sprite()

# ---------------------------------------------------------------- lumière
ly, lx = np.mgrid[0:H, 0:W].astype(np.float32)
light = 0.86 + 0.24 * np.exp(-(((lx - W * 0.25) / (W * 0.7)) ** 2 + ((ly - H * 0.05) / (H * 0.9)) ** 2))
vign = 1 - 0.32 * (((lx - W / 2) / (W * 0.75)) ** 2 + ((ly - H / 2) / (H * 0.8)) ** 2)
grade = (light * vign)[..., None]
edge_noise = fnoise(H, 64, 1.2, 9)[:, 0]

if os.path.exists(TMP): shutil.rmtree(TMP)
os.makedirs(TMP)
for f in range(N):
    o = P * f / N
    idx = (np.arange(W) + o).astype(np.int64) % P
    frac = (np.arange(W) + o) % 1.0
    idx2 = (idx + 1) % P
    c = clean[:, idx] * (1 - frac[None, :, None]) + clean[:, idx2] * frac[None, :, None]
    dt = dirty[:, idx] * (1 - frac[None, :, None]) + dirty[:, idx2] * frac[None, :, None]
    ph = 2 * math.pi * 4 * f / N
    ry = H * 0.47 + H * 0.26 * math.sin(ph)
    xe = XB + 14 * np.sin(ly[:, :1] / 41 + 1.3) + 22 * (edge_noise[:, None] - 0.5)
    near = np.exp(-((ly[:, :1] - ry) / 60) ** 2)
    xe = xe + 26 * near
    m = 1 - smooth(lx, xe - 3, xe + 3)
    wet = np.exp(-np.clip(xe - lx, 0, None) / 55) * m
    painted = c * (1 - 0.06 * wet[..., None]) + 255 * 0.05 * wet[..., None]
    img = painted * m[..., None] + dt * (1 - m[..., None])
    img = img * grade
    frame = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
    # ombre et rouleau
    shadow = Image.new("L", (W, H), 0); sd = ImageDraw.Draw(shadow)
    rx = XB - 170; rtop = int(ry - 37)
    sd.ellipse([rx + 18, rtop + 30, rx + 270, rtop + 100], fill=120)
    shadow = shadow.filter(ImageFilter.GaussianBlur(14))
    frame = Image.composite(Image.new("RGB", (W, H), (40, 34, 28)), frame, shadow.point(lambda v: int(v * 0.55)))
    frame.paste(ROLL, (rx, rtop), ROLL)
    pd = ImageDraw.Draw(frame)
    hx, hy = rx + 240 + 23, rtop + 74 + 160
    pd.line([hx, hy - 4, hx + 150, H + 40], fill=(58, 60, 66), width=14)
    pd.line([hx - 3, hy - 4, hx + 147, H + 40], fill=(110, 112, 120), width=3)
    # premier plan
    of = PF * f / N
    fidx = (np.arange(W) + of).astype(np.int64) % PF
    fga = fg_arr[:, fidx]
    a = fga[..., 3:4] / 255
    arr = np.asarray(frame, np.float32) * (1 - a) + fga[..., :3] * a
    Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).save(f"{TMP}/f{f:04d}.png")
    if f % 48 == 0: print("image", f, file=sys.stderr)

os.makedirs(OUT, exist_ok=True)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", f"{TMP}/f%04d.png", "-c:v", "libx264", "-preset", "veryfast",
                "-crf", "27", "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-an", os.path.join(OUT, "hero.mp4")], check=True)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", f"{TMP}/f%04d.png", "-c:v", "libvpx-vp9", "-b:v", "0", "-crf", "40",
                "-row-mt", "1", "-deadline", "good", "-cpu-used", "4", "-pix_fmt", "yuv420p", "-an", os.path.join(OUT, "hero.webm")], check=True)
Image.open(f"{TMP}/f0000.png").convert("RGB").save(os.path.join(OUT, "hero-poster.jpg"), quality=78, optimize=True, progressive=True)
for fn in os.listdir(OUT): print(fn, os.path.getsize(os.path.join(OUT, fn)) // 1024, "Ko")
