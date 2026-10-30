# -*- coding: utf-8 -*-
"""Génère l'image de partage (og-image.jpg), les icônes et le favicon dans site/brand/."""
import io, os
from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "site", "brand")
os.makedirs(OUT, exist_ok=True)

def ttf(name):
    f = TTFont(os.path.join(ROOT, "site", "fonts", name)); f.flavor = None
    b = io.BytesIO(); f.save(b); b.seek(0); return b.getvalue()

DISP, TEXT = ttf("big-shoulders.woff2"), ttf("hanken-grotesk.woff2")
def font(data, size, wght):
    f = ImageFont.truetype(io.BytesIO(data), size)
    try: f.set_variation_by_axes([wght])
    except Exception: pass
    return f

TAUPE, CHAUX, CHARBON, TAUPE_L = (128, 109, 97), (238, 236, 232), (38, 34, 31), (201, 188, 177)

# Image de partage 1200 x 630
W, H = 1200, 630
im = Image.new("RGB", (W, H), CHAUX)
rng = random.Random(4)
px = im.load()
for _ in range(90000):
    x, y = rng.randrange(W), rng.randrange(H); d = rng.randint(-14, 6)
    r, g, b = px[x, y]; px[x, y] = (r + d, g + d, b + d)
d = ImageDraw.Draw(im)
d.rectangle([0, 0, 380, H], fill=TAUPE)
# maison stylisée
d.polygon([(90, 300), (190, 215), (290, 300), (290, 430), (90, 430)], fill=CHAUX)
d.rectangle([168, 360, 212, 430], fill=TAUPE)
d.line([(90, 360), (290, 360)], fill=TAUPE, width=6)
d.text((90, 470), "Artisan Druart", font=font(DISP, 54, 800), fill=CHAUX)
d.text((92, 530), "Maison Rénovation", font=font(TEXT, 26, 600), fill=TAUPE_L)
d.text((440, 120), "Ravalement de façade", font=font(DISP, 92, 800), fill=CHARBON)
d.text((440, 230), "à Mitry-Mory et 50 km autour", font=font(DISP, 64, 700), fill=CHARBON)
d.text((442, 340), "Nettoyage, enduit, peinture, fissures, meulière,", font=font(TEXT, 30, 500), fill=(91, 84, 78))
d.text((442, 382), "isolation par l'extérieur et toiture.", font=font(TEXT, 30, 500), fill=(91, 84, 78))
d.rounded_rectangle([440, 470, 860, 540], radius=8, fill=TAUPE)
d.text((468, 482), "06 20 14 69 91", font=font(DISP, 48, 800), fill=(255, 255, 255))
d.text((884, 488), "Devis gratuit\nsous 48 h", font=font(TEXT, 22, 600), fill=CHARBON, spacing=4)
im.save(os.path.join(OUT, "og-image.jpg"), quality=86, optimize=True, progressive=True)

# Icônes
def icon(size, radius_ratio=0.15):
    s = 512
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, s - 1, s - 1], radius=int(s * radius_ratio), fill=TAUPE)
    k = s / 40
    d.polygon([(8 * k, 19 * k), (20 * k, 9 * k), (32 * k, 19 * k), (32 * k, 33 * k), (8 * k, 33 * k)], fill=CHAUX)
    d.line([(8 * k, 25 * k), (32 * k, 25 * k)], fill=TAUPE, width=int(1.6 * k))
    d.rectangle([16.5 * k, 25 * k, 23.5 * k, 33 * k], fill=TAUPE)
    return im.resize((size, size), Image.LANCZOS)
icon(512).save(os.path.join(OUT, "icon-512.png"))
icon(192).save(os.path.join(OUT, "icon-192.png"))
icon(180, 0).convert("RGB").save(os.path.join(OUT, "apple-touch-icon.png"))
icon(64).save(os.path.join(OUT, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)])
open(os.path.join(OUT, "favicon.svg"), "w").write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 40"><rect width="40" height="40" rx="6" fill="#806d61"/><path d="M8 19L20 9l12 10v14H8z" fill="#eeece8"/><path d="M8 25h24" stroke="#806d61" stroke-width="1.6"/><rect x="16.5" y="25" width="7" height="8" fill="#806d61"/></svg>\n')
print("ok", os.listdir(OUT))
