# -*- coding: utf-8 -*-
"""Prépare les photos du site à partir de site/photos-src/.

Déposer dans site/photos-src/ les images de l'ancien site, avec leur nom d'origine
(ex. ravalement-avant-1400.jpg, carte-enduit-8d38b9a8.jpg, logo-artisan-druart-2ea109d7.png).
Le script :
  - reconnaît chaque image d'après son nom (voir ALTS) et garde la plus grande version ;
  - produit site/img-out/<clé>-<largeur>.webp en 480, 960 et 1440 px (sans agrandir) ;
  - recopie chaque fichier d'origine à son ancienne adresse (site/legacy-out/assets/...),
    pour que les liens vers les anciennes images restent valides ;
  - écrit site/photos.json, lu par build.py.
Usage : python3 site/photos.py, puis python3 site/build.py
"""
import json
import os
import re
import shutil

from PIL import Image, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "photos-src")
OUT = os.path.join(HERE, "img-out")
LEGACY = os.path.join(HERE, "legacy-out")
WIDTHS = [480, 960, 1440]

# Textes alternatifs (repris de l'ancien site et précisés)
ALTS = {
    "logo": "Artisan Druart, ravalement et couverture",
    "logo-blanc": "Artisan Druart",
    "hero-blanc-casse": "Pavillon contemporain à l'enduit blanc cassé",
    "ravalement-avant": "Façade en travaux : panneaux d'isolation posés avant l'enduit",
    "ravalement-apres": "Maison après ravalement : façade enduite, finition claire",
    "carte-enduit": "Façade préparée avant enduit, menuiseries et gouttière protégées",
    "carte-peinture": "Application d'une peinture de façade au rouleau",
    "carte-nettoyage": "Nettoyage de façade au jet d'eau à basse pression",
    "carte-fissures": "Réparation d'une fissure de façade au mortier",
    "carte-impermeabilisation": "Application d'un hydrofuge incolore sur une façade",
    "carte-meuliere": "Maison en meulière rejointoyée, enduit clair et toiture en tuiles",
    "carte-bardage": "Façade habillée d'un bardage à lames horizontales gris anthracite",
    "couverture-avant": "Toiture ancienne aux tuiles usées avant réfection",
    "couverture-apres": "Toiture après réfection : tuiles neuves sur le versant",
    "carte-demoussage": "Démoussage d'une toiture en tuiles",
    "carte-zinguerie": "Pose d'une gouttière et d'une descente en acier laqué",
    # photos du diagnostic de façade (accueil)
    "diag-salissures": "Façade enduite avec coulures noires sous l'appui de fenêtre et algues vertes en pied de mur",
    "diag-faiencage": "Enduit de façade faïencé : réseau de fines craquelures près d'une fenêtre",
    "diag-fissure": "Fissure en escalier partant de l'angle d'une fenêtre jusque sous la toiture",
    "diag-creux": "Enduit décollé et tombé par plaque sous une fenêtre, maçonnerie apparente",
    "diag-meuliere": "Mur en pierre meulière aux joints creusés et décollés",
    "diag-froid": "Caméra thermique montrant les pertes de chaleur autour d'une fenêtre",
}


def key_of(filename):
    base = os.path.splitext(os.path.basename(filename))[0].lower()
    base = re.sub(r"-(\d{3,4})$", "", base)          # suffixe de largeur : -800, -1400
    base = re.sub(r"-[0-9a-f]{8}$", "", base)         # empreinte : -2ea109d7
    if base.startswith("logo-artisan-druart-blanc"):
        return "logo-blanc"
    if base.startswith("logo-artisan-druart"):
        return "logo"
    return base


def main():
    if not os.path.isdir(SRC):
        print("Aucun dossier site/photos-src : rien à faire.")
        return
    for d in (OUT, LEGACY):
        if os.path.exists(d):
            shutil.rmtree(d)
        os.makedirs(d)
    best = {}
    for dp, _, files in os.walk(SRC):
        for f in files:
            if not f.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                continue
            path = os.path.join(dp, f)
            rel = os.path.relpath(path, SRC)
            # copie à l'ancienne adresse, seulement pour les images de l'ancien site (dossier assets/)
            if rel.startswith("assets"):
                dest = os.path.join(LEGACY, rel)
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                shutil.copy2(path, dest)
            k = key_of(f)
            with Image.open(path) as im:
                w = im.size[0]
            if k not in best or w > best[k][1]:
                best[k] = (path, w)
    meta = {}
    for k, (path, _) in sorted(best.items()):
        im = ImageOps.exif_transpose(Image.open(path))
        logo = k.startswith("logo")
        if logo:
            im = im.convert("RGBA")
            widths = [w for w in (240, 480) if w <= im.size[0]] or [im.size[0]]
        else:
            im = im.convert("RGB")
            W = im.size[0]
            widths = [w for w in WIDTHS if w < W] + [min(W, WIDTHS[-1])]
        for w in widths:
            h = round(im.size[1] * w / im.size[0])
            im.resize((w, h), Image.LANCZOS).save(os.path.join(OUT, f"{k}-{w}.webp"), "WEBP", quality=80, method=6)
        if k == "logo":
            im.save(os.path.join(OUT, "logo.png"))
        meta[k] = {"w": im.size[0], "h": im.size[1], "sizes": widths, "alt": ALTS.get(k, "")}
        print(f"{k:28} {im.size[0]}x{im.size[1]} -> {widths}")
    json.dump(meta, open(os.path.join(HERE, "photos.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    unknown = [k for k in meta if k not in ALTS]
    if unknown:
        print("Images sans texte alternatif (à compléter dans ALTS) :", unknown)


if __name__ == "__main__":
    main()
