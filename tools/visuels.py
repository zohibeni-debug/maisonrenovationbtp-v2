# -*- coding: utf-8 -*-
"""Image de partage, icônes et logo PNG à partir du logo du client (site/brand-src/logo-artisan-druart.png)."""
import io, os
from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "site", "brand")
os.makedirs(OUT, exist_ok=True)
src = Image.open(os.path.join(ROOT, "site", "brand-src", "logo-artisan-druart.png")).convert("RGBA")
logo = src.crop(src.getbbox())                       # logo complet détouré
mark = src.crop((40, 330, 1130, 812))                # pictogramme seul
src.save(os.path.join(OUT, "logo-artisan-druart-2ea109d7.png"))   # ancienne adresse du logo
l2 = logo.copy(); l2.thumbnail((600, 600), Image.LANCZOS); l2.save(os.path.join(OUT, "logo.png"), optimize=True)

def ttf(name):
    f = TTFont(os.path.join(ROOT, "site", "fonts", name)); f.flavor = None
    b = io.BytesIO(); f.save(b); b.seek(0); return b.getvalue()
FONT = ttf("archivo.woff2")
def font(size, wght, wdth=112):
    f = ImageFont.truetype(io.BytesIO(FONT), size)
    try:
        axes = f.get_variation_axes()
        f.set_variation_by_axes([wght if a["name"] in (b"Weight", "Weight") else wdth for a in axes])
    except Exception:
        pass
    return f

INK, TAUPE = (23, 21, 19), (128, 109, 97)
W, H = 1200, 630
im = Image.new("RGB", (W, H), (255, 255, 255))
d = ImageDraw.Draw(im)
d.rectangle([0, 0, 470, H], fill=(245, 242, 238))
l3 = logo.copy(); l3.thumbnail((380, 380), Image.LANCZOS)
im.paste(l3, ((470 - l3.width) // 2, (H - l3.height) // 2), l3)
d.text((520, 150), "Ravalement", font=font(82, 800), fill=INK)
d.text((520, 240), "de façade", font=font(82, 800), fill=INK)
d.text((522, 345), "Mitry-Mory et 50 km autour", font=font(36, 600, 100), fill=TAUPE)
d.rounded_rectangle([520, 430, 880, 500], radius=35, fill=TAUPE)
d.text((548, 446), "06 20 14 69 91", font=font(34, 800), fill=(255, 255, 255))
d.text((900, 440), "Devis gratuit\nsous 48 h", font=font(22, 600, 100), fill=INK, spacing=4)
im.save(os.path.join(OUT, "og-image.jpg"), quality=86, optimize=True, progressive=True)

def icon(size, pad=0.1, bg=(255, 255, 255, 255), radius=0.18):
    S = 1024
    can = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    ImageDraw.Draw(can).rounded_rectangle([0, 0, S - 1, S - 1], radius=int(S * radius), fill=bg)
    m = mark.copy(); m.thumbnail((int(S * (1 - 2 * pad)), int(S * (1 - 2 * pad))), Image.LANCZOS)
    can.paste(m, ((S - m.width) // 2, (S - m.height) // 2), m)
    return can.resize((size, size), Image.LANCZOS)
icon(512).save(os.path.join(OUT, "icon-512.png"))
icon(192).save(os.path.join(OUT, "icon-192.png"))
icon(180, radius=0).convert("RGB").save(os.path.join(OUT, "apple-touch-icon.png"))
icon(64, pad=0.04).save(os.path.join(OUT, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)])
for f in ("favicon.svg",):
    p = os.path.join(OUT, f)
    if os.path.exists(p): os.remove(p)
print(sorted(os.listdir(OUT)))
