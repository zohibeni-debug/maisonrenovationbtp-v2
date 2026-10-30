# -*- coding: utf-8 -*-
"""Générateur du site maisonrenovationbtp.fr (Artisan Druart, Maison Rénovation).

Usage : python3 site/build.py
Produit le dossier public/ : pages HTML complètes, plan du site, robots, redirections, en-têtes.
"""
import base64
import hashlib
import html
import json
import os
import re
import shutil
import zlib
from datetime import date

import art
import communes as CM
import logo as LG
import content as C
import guides as G
import services as SV

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")
PUBLIC = os.path.join(ROOT, "public")
TODAY = date.today().isoformat()
URL = C.SITE_URL
B = C.BUSINESS
PHOTOS_FILE = os.path.join(SITE, "photos.json")
PHOTOS = json.load(open(PHOTOS_FILE, encoding="utf-8")) if os.path.exists(PHOTOS_FILE) else {}
PAGES = []  # (chemin, priorité, indexable)

# ---------------------------------------------------------------------------
# Outils
# ---------------------------------------------------------------------------

def nw(s):
    """Empêche la coupure d'un nom composé (Mitry-Mory, Claye-Souilly…) en fin de ligne (texte hors balises)."""
    parts = re.split(r"(<[^>]+>)", s)
    return "".join(p if p.startswith("<") else re.sub(r"([^\s<>]+-[^\s<>]+)", r'<span class="nw">\1</span>', p) for p in parts)


def esc(s):
    return html.escape(str(s), quote=True)


def fr(text):
    """Typographie française hors balises : espaces insécables avant ; : ! ? et dans les nombres."""
    parts = re.split(r"(<[^>]+>)", text)
    out = []
    for p in parts:
        if p.startswith("<"):
            out.append(p)
            continue
        p = re.sub(r" ([?!;])", "\u00a0\\1", p)
        p = re.sub(r" :(?=\s|$)", "\u00a0:", p)
        p = p.replace("« ", "«\u00a0").replace(" »", "\u00a0»")
        p = re.sub(r"(\d) (km|m²|m|cm|mm|h|%|€|°C|ans|semaines|jours|heures|habitants|€/m²|€/ml)(?=[\s.,;)]|$)", "\\1\u00a0\\2", p)
        p = re.sub(r"(\d) (\d{3})\b", "\\1\u00a0\\2", p)
        p = re.sub(r"\b(n°) ", "\\1\u00a0", p)
        out.append(p)
    return "".join(out)


def money(v):
    v = int(round(v / 50.0) * 50)
    return f"{v:,}".replace(",", "\u00a0") + "\u00a0€"


def jsonld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/") + "</script>"


def write(rel, data, binary=False):
    path = os.path.join(PUBLIC, rel.lstrip("/"))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb" if binary else "w", **({} if binary else {"encoding": "utf-8"})) as f:
        f.write(data)


def h(s):
    return hashlib.sha1(s.encode()).hexdigest()


def pick(slug, n):
    return int(h(slug)[:8], 16) % n


EARLY_JS = "document.documentElement.classList.add('js')"
EARLY_JS_HASH = "sha256-" + base64.b64encode(hashlib.sha256(EARLY_JS.encode()).digest()).decode()

ICONS = {
    "tel": '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M6.6 3.5h2.8l1.4 4.2-2 1.5a12 12 0 0 0 6 6l1.5-2 4.2 1.4v2.8a2 2 0 0 1-2.2 2A17 17 0 0 1 4.6 5.7a2 2 0 0 1 2-2.2z" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linejoin="round"/></svg>',
    "check": '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12.5l4.2 4.2L19 7" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "pin": '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 21s-6.5-6.2-6.5-11a6.5 6.5 0 0 1 13 0c0 4.8-6.5 11-6.5 11z" fill="none" stroke="currentColor" stroke-width="1.9"/><circle cx="12" cy="10" r="2.4" fill="none" stroke="currentColor" stroke-width="1.9"/></svg>',
    "mail": '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><rect x="3.5" y="5.5" width="17" height="13" rx="2" fill="none" stroke="currentColor" stroke-width="1.9"/><path d="M4 7l8 6 8-6" fill="none" stroke="currentColor" stroke-width="1.9"/></svg>',
    "menu": '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>',
    "close": '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>',
    "chev": '<svg class="ico chev" viewBox="0 0 24 24" aria-hidden="true"><path d="M7 10l5 5 5-5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
}
MARK = ('<svg class="mark" viewBox="0 0 40 40" aria-hidden="true"><rect width="40" height="40" rx="6" fill="#806d61"/>'
        '<path d="M8 19L20 9l12 10v14H8z" fill="#eeece8"/><path d="M8 25h24" stroke="#806d61" stroke-width="1.6"/>'
        '<rect x="16.5" y="25" width="7" height="8" fill="#806d61"/></svg>')

SHORT = {
    "ravalement-facade": "Diagnostic, nettoyage, réparations et finition, en un seul chantier",
    "enduit-facade": "Monocouche, traditionnel ou à la chaux, finition grattée, talochée ou écrasée",
    "peinture-facade": "Sur enduit sain : acrylique, siloxane, pliolite ou silicate",
    "nettoyage-facade": "Basse pression ou hydrogommage, anti-mousse et hydrofuge",
    "traitement-fissures-facade": "Mesure, ouverture, pontage armé et revêtement",
    "impermeabilisation-facade": "Revêtements souples I1 à I4 ou hydrofuge incolore",
    "ravalement-meuliere": "Dégarnissage et rejointoiement à la chaux, pierre préservée",
    "isolation-thermique-exterieure": "Isolant sous enduit ou sous bardage, ponts thermiques traités",
    "bardage": "Bois, composite, fibres-ciment ou métal, sur ossature ventilée",
    "couverture-toiture": "Tuiles, ardoise, faîtage, rives, solins, réfection complète",
    "demoussage-toiture": "Brossage, traitement anti-mousse, hydrofuge en option",
    "zinguerie-gouttieres": "Gouttières, descentes, chéneaux, solins et noues",
}
LIST_PRICE = {
    "ravalement-facade": "10 à 100 €/m²",
    "traitement-fissures-facade": "sur diagnostic",
    "bardage": "sur devis",
}


def price_label(slug):
    if slug in LIST_PRICE:
        return LIST_PRICE[slug]
    s = SV.BY_SLUG[slug]
    k = s["price"]
    p = C.PRICES.get(k) or C.ROOF_PRICES.get(k)
    return f"{p[0]} à {p[1]} {p[2]}"


# ---------------------------------------------------------------------------
# Photos (facultatives : sans photo, l'illustration dessinée prend le relais)
# ---------------------------------------------------------------------------

def has_photo(key):
    return key in PHOTOS


DIAG_POS = {"salissures": "50% 72%", "faiencage": "50% 50%", "fissure": "50% 30%", "creux": "50% 50%", "meuliere": "50% 50%", "froid": "40% 55%"}


def img(key, alt=None, sizes="100vw", cls="", eager=False, pos=None):
    m = PHOTOS[key]
    widths = m["sizes"]
    w = widths[-1]
    hh = round(m["h"] * w / m["w"])
    srcset = ", ".join(f"/assets/img/{key}-{x}.webp {x}w" for x in widths)
    src = f"/assets/img/{key}-{widths[min(1, len(widths) - 1)]}.webp"
    a = [f'src="{src}"', f'srcset="{srcset}"', f'sizes="{sizes}"', f'width="{w}"', f'height="{hh}"', f'alt="{esc(alt if alt is not None else m.get("alt", ""))}"']
    a.append('fetchpriority="high"' if eager else 'loading="lazy"')
    a.append('decoding="async"')
    if cls:
        a.append(f'class="{cls}"')
    if pos:
        a.append(f'style="object-position:{pos}"')
    return "<img " + " ".join(a) + ">"


def tile_or_photo(tile_key, uid, alt=None, sizes="(min-width: 960px) 40vw, 100vw", eager=False, cls="tile"):
    """Photo du diagnostic correspondant à la texture si elle existe, sinon l'illustration dessinée."""
    if has_photo("diag-" + tile_key):
        return img("diag-" + tile_key, alt, sizes, cls=cls, eager=eager, pos=DIAG_POS.get(tile_key))
    return art.tile(tile_key, uid, cls=cls, label=alt)


def visual(photo_key, tile_key, uid, alt, sizes="(min-width: 960px) 40vw, 100vw", eager=False):
    if photo_key and has_photo(photo_key):
        return f'<figure class="visual">{img(photo_key, alt, sizes, eager=eager)}</figure>'
    if has_photo("diag-" + tile_key):
        return f'<figure class="visual">{tile_or_photo(tile_key, uid, PHOTOS["diag-" + tile_key]["alt"], sizes, eager)}</figure>'
    return f'<figure class="visual visual-art">{art.tile(tile_key, uid, label=alt)}</figure>'


# ---------------------------------------------------------------------------
# Données structurées
# ---------------------------------------------------------------------------
ORG_ID = URL + "/#entreprise"


def org_schema():
    o = {
        "@context": "https://schema.org",
        "@type": ["GeneralContractor", "RoofingContractor"],
        "@id": ORG_ID,
        "name": B["name"],
        "alternateName": [B["gbp"], B["short"]],
        "url": URL + "/",
        "image": URL + "/assets/og-image.jpg",
        "logo": URL + "/assets/logo.png",
        "telephone": B["phone_e164"],
        "email": B["email"],
        "priceRange": "€€",
        "address": {"@type": "PostalAddress", "streetAddress": B["street"], "postalCode": B["postcode"],
                    "addressLocality": B["city"], "addressRegion": "Île-de-France", "addressCountry": "FR"},
        "areaServed": [{"@type": "GeoCircle", "geoMidpoint": {"@type": "GeoCoordinates", "latitude": CM.MITRY[0], "longitude": CM.MITRY[1]}, "geoRadius": 50000}]
        + [{"@type": "City", "name": c["name"]} for c in CM.COMMUNES],
        "contactPoint": [{"@type": "ContactPoint", "telephone": B["phone_e164"], "contactType": "customer service", "areaServed": "FR", "availableLanguage": "fr"},
                         {"@type": "ContactPoint", "telephone": B["phone2_e164"], "contactType": "customer service", "areaServed": "FR", "availableLanguage": "fr"}],
        "sameAs": [B["sister_url"]],
        "knowsAbout": [s["name"] for s in SV.SERVICES],
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Travaux de façade et de toiture",
                            "itemListElement": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["name"], "url": f"{URL}/{s['slug']}/"}} for s in SV.SERVICES]},
    }
    if C.A_CONFIRMER["siret"]:
        o["identifier"] = {"@type": "PropertyValue", "propertyID": "SIRET", "value": C.A_CONFIRMER["siret"]}
    return o


def website_schema():
    return {"@context": "https://schema.org", "@type": "WebSite", "@id": URL + "/#site", "url": URL + "/",
            "name": B["name"], "inLanguage": "fr-FR", "publisher": {"@id": ORG_ID}}


def crumbs_schema(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": URL + p} for i, (n, p) in enumerate(items)]}


def faq_schema(faq):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}


def service_schema(s, area=None):
    o = {"@context": "https://schema.org", "@type": "Service", "name": s["name"], "serviceType": s["name"],
         "url": f"{URL}/{s['slug']}/", "description": s["desc"], "provider": {"@id": ORG_ID},
         "areaServed": area or {"@type": "GeoCircle", "geoMidpoint": {"@type": "GeoCoordinates", "latitude": CM.MITRY[0], "longitude": CM.MITRY[1]}, "geoRadius": 50000}}
    k = s.get("price")
    p = C.PRICES.get(k) or C.ROOF_PRICES.get(k) if k else None
    if p and s["slug"] not in LIST_PRICE:
        o["offers"] = {"@type": "Offer", "priceCurrency": "EUR", "priceSpecification": {
            "@type": "UnitPriceSpecification", "minPrice": p[0], "maxPrice": p[1], "priceCurrency": "EUR",
            "unitText": "m²" if "m²" in p[2] else "mètre linéaire"}}
    return o


def article_schema(g, path):
    return {"@context": "https://schema.org", "@type": "Article", "headline": g["h1"], "description": g["desc"],
            "url": URL + path, "inLanguage": "fr-FR", "dateModified": TODAY, "datePublished": "2026-10-01",
            "author": {"@id": ORG_ID}, "publisher": {"@id": ORG_ID}, "image": URL + "/assets/og-image.jpg",
            "mainEntityOfPage": URL + path}


# ---------------------------------------------------------------------------
# Gabarit commun
# ---------------------------------------------------------------------------
ASSETS = {}


def tel_btn(cls="btn btn-primary", label=None, num="phone"):
    label = label or f"Appeler le {B[num]}"
    return f'<a class="{cls}" href="tel:{B[num + "_e164"]}">{ICONS["tel"]}<span>{esc(label)}</span></a>'


def devis_btn(cls="btn btn-ghost", label="Demander un devis gratuit", href="#devis"):
    return f'<a class="{cls}" href="{href}"><span>{esc(label)}</span></a>'


def brand_html():
    return ('<img class="lg-full lg-dark" src="/assets/logo-h.svg" width="300" height="46" alt="Artisan Druart, couverture et ravalement">'
            '<img class="lg-full lg-light" src="/assets/logo-h-light.svg" width="300" height="46" alt="Artisan Druart, couverture et ravalement">'
            '<img class="lg-mark lg-dark" src="/assets/logo-mark.svg" width="101" height="44" alt="Artisan Druart">'
            '<img class="lg-mark lg-light" src="/assets/logo-mark-light.svg" width="101" height="44" alt="Artisan Druart">')


def brand_html_old():
    if has_photo("logo"):
        m = PHOTOS["logo"]
        ss = ", ".join(f"/assets/img/logo-{w}.webp {w}w" for w in m["sizes"])
        return f'<img class="logo" src="/assets/img/logo-{m["sizes"][0]}.webp" srcset="{ss}" sizes="240px" width="{m["w"]}" height="{m["h"]}" alt="Artisan Druart, ravalement et couverture">'
    return f'{MARK}<span class="wm"><span class="wm-a">Artisan Druart</span><span class="wm-b">Maison Rénovation</span></span>'


def header(current):
    def sub(label, items, key):
        lis = "".join(
            f'<li><a href="/{s["slug"]}/"{" aria-current=page" if current == s["slug"] else ""}><span>{esc(s["nav"])}</span><small>{esc(price_label(s["slug"]))}</small></a></li>'
            for s in items)
        on = " is-current" if current in [s["slug"] for s in items] else ""
        return (f'<li class="has-sub{on}"><details class="sub"><summary>{label}{ICONS["chev"]}</summary>'
                f'<ul class="sub-list sub-{key}">{lis}</ul></details></li>')

    def link(slug, label):
        here = ' aria-current="page"' if current == slug else ""
        return f'<li><a href="/{slug}/"{here}>{label}</a></li>'

    return f"""<a class="skip" href="#contenu">Aller au contenu</a>
<header class="hd" data-header>
  <div class="wrap hd-in">
    <a class="brand" href="/" aria-label="{esc(B['name'])}, accueil">{brand_html()}</a>
    <nav class="nav" id="nav" aria-label="Navigation principale">
      <ul class="nav-list">
        {sub('Façade', SV.FACADE, 'facade')}
        {sub('Toiture', SV.TOITURE, 'toiture')}
        {link('prix-ravalement-facade', 'Prix')}
        {link('conseils', 'Conseils')}
        {link('zones-intervention', 'Zones')}
        {link('contact', 'Contact')}
      </ul>
      <div class="nav-foot">{tel_btn('btn btn-primary', B['phone'])}<a class="btn btn-ghost" href="tel:{B['phone2_e164']}">{ICONS['tel']}<span>{B['phone2']}</span></a></div>
    </nav>
    {tel_btn('btn btn-primary hd-tel', B['phone'])}
    <button class="menu-btn" type="button" aria-controls="nav" aria-expanded="false" aria-label="Ouvrir le menu">{ICONS['menu']}{ICONS['close']}</button>
  </div>
</header>"""


def footer(cls=""):
    fac = "".join(f'<li><a href="/{s["slug"]}/">{esc(s["nav"])}</a></li>' for s in SV.FACADE)
    toi = "".join(f'<li><a href="/{s["slug"]}/">{esc(s["nav"])}</a></li>' for s in SV.TOITURE)
    gui = "".join(f'<li><a href="/{g["slug"]}/">{esc(g["nav"])}</a></li>' for g in G.GUIDES)
    big = sorted([c for c in CM.COMMUNES if c["pop"] and c["pop"] > 40000], key=lambda c: c["dist"])[:10]
    zon = "".join(f'<li><a href="/ravalement-facade-{c["slug"]}/">{esc(c["name"])}</a></li>' for c in big)
    return f"""<footer class="ft">
  <div class="wrap ft-grid">
    <div class="ft-id">
      <a href="/" aria-label="{esc(B['name'])}, accueil"><img class="ft-logo" src="/assets/logo-light.svg" width="220" height="135" alt="Artisan Druart, couverture et ravalement"></a>
      <p>Façadier et couvreur à Mitry-Mory. Ravalement, enduit, peinture, meulière, isolation par l'extérieur et toiture, dans un rayon de 50 km.</p>
      <address>
        <p>{ICONS['pin']}<span>{esc(B['street'])}<br>{B['postcode']} {B['city']}</span></p>
        <p>{ICONS['tel']}<span><a href="tel:{B['phone_e164']}">{B['phone']}</a> ou <a href="tel:{B['phone2_e164']}">{B['phone2']}</a>, 7 j/7</span></p>
        <p>{ICONS['mail']}<span><a href="mailto:{B['email']}">{B['email']}</a></span></p>
      </address>
    </div>
    <nav class="ft-nav" aria-label="Façade"><h2>Façade</h2><ul>{fac}</ul></nav>
    <nav class="ft-nav" aria-label="Toiture et conseils"><h2>Toiture</h2><ul>{toi}</ul><h2>Conseils</h2><ul>{gui}<li><a href="/conseils/">Tous les conseils</a></li></ul></nav>
    <nav class="ft-nav" aria-label="Zones d'intervention"><h2>Zones</h2><ul>{zon}<li><a href="/zones-intervention/">Toutes les communes</a></li></ul></nav>
  </div>
  <div class="wrap ft-legal">
    <p>© {date.today().year} {esc(B['name'])}</p>
    <p><a href="/mentions-legales/">Mentions légales</a> <a href="/contact/">Contact</a> <a href="{B['sister_url']}" rel="noopener">Notre site toiture</a> <a href="https://allositeweb.com/" rel="noopener">Site réalisé par ALLOSITEWEB</a></p>
  </div>
</footer>
<div class="callbar" data-callbar>{tel_btn('btn btn-primary', 'Appeler')}<a class="btn btn-ghost" href="{'/contact/#devis' if cls in ('p-legal', 'p-404') else '#devis'}"><span>Devis gratuit</span></a></div>"""


def page(path, title, desc, body, crumbs=None, schema=None, current=None, robots="index,follow", priority="0.6", cls="", og_title=None, extra_head=""):
    canonical = URL + (path if path != "/404.html" else "/")
    crumbs_html = ""
    schemas = [website_schema(), org_schema()] if path == "/" else []
    if crumbs:
        items = [("Accueil", "/")] + crumbs
        lis = []
        for i, (n, p) in enumerate(items):
            if i == len(items) - 1:
                lis.append(f'<li aria-current="page">{esc(n)}</li>')
            else:
                lis.append(f'<li><a href="{p}">{esc(n)}</a></li>')
        crumbs_html = f'<nav class="crumbs wrap" aria-label="Fil d\'Ariane"><ol>{"".join(lis)}</ol></nav>'
        schemas.append(crumbs_schema(items))
    schemas += schema or []
    ld = "".join(jsonld(s) for s in schemas)
    t = esc(title)
    doc = f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t}</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:locale" content="fr_FR">
<meta property="og:site_name" content="{esc(B['name'])}">
<meta property="og:title" content="{esc(og_title or title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{URL}/assets/og-image.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#806d61">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preload" href="{ASSETS['font']}" as="font" type="font/woff2" crossorigin>{extra_head}
<link rel="stylesheet" href="{ASSETS['css']}">
<script>{EARLY_JS}</script>
<script src="{ASSETS['js']}" defer></script>
{ld}
</head>
<body class="{cls}">
{header(current)}
<main id="contenu">
{crumbs_html}
{re.sub(r"<h1>(.*?)</h1>", lambda m: "<h1>" + nw(m.group(1)) + "</h1>", fr(body), flags=re.S)}
</main>
{fr(footer(cls))}
</body>
</html>
"""
    rel = path if path.endswith(".html") else path.rstrip("/") + "/index.html"
    write(rel, doc)
    if robots.startswith("index"):
        PAGES.append((path, priority))


# ---------------------------------------------------------------------------
# Composants
# ---------------------------------------------------------------------------

def prices_table(highlight=None, roof=False, self_guide=False):
    guide_link = "" if self_guide else ' Voir aussi notre <a href="/prix-ravalement-facade/">guide des prix</a>.'
    src = C.ROOF_PRICES if roof else C.PRICES
    rows = []
    for k, (a, b, u, label) in src.items():
        on = ' class="is-on"' if k == highlight else ""
        rows.append(f'<tr{on}><th scope="row">{esc(label)}</th><td>{a} à {b} {u}</td></tr>')
    if roof:
        note = "Repères constatés en Île-de-France, fourniture et pose. Le prix ferme est fixé après visite, selon la pente, l'accès et l'état de la couverture."
    else:
        note = "Fourchettes indicatives au mètre carré de façade, fourniture et pose. Le prix ferme est fixé après visite, selon la surface, l'état du support, la hauteur et la finition. L'échafaudage figure sur le devis comme un poste à part."
    return (f'<div class="tbl-wrap"><table class="tbl tbl-prix"><thead><tr><th scope="col">Travaux</th><th scope="col">Prix indicatif</th></tr></thead>'
            f'<tbody>{"".join(rows)}</tbody></table></div><p class="note">{note}{guide_link}</p>')


def steps_html():
    lis = "".join(f'<li><h3>{esc(t)}</h3><p>{esc(d)}</p></li>' for t, d in C.STEPS)
    return f'<ol class="steps">{lis}</ol>'


def faq_html(faq, title="Questions fréquentes", hid="faq"):
    items = "".join(f'<details class="qa"><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in faq)
    return f'<section class="sec sec-faq" aria-labelledby="{hid}"><div class="wrap narrow"><h2 id="{hid}">{title}</h2>{items}</div></section>'


def devis_list(slugs, cls=""):
    rows = []
    for slug in slugs:
        s = SV.BY_SLUG[slug]
        rows.append(f'<li><a href="/{slug}/"><span class="dv-n">{esc(s["name"])}</span><span class="dv-d">{esc(SHORT[slug])}</span>'
                    f'<span class="dv-p">{esc(price_label(slug))}</span></a></li>')
    return f'<ol class="devis {cls}">{"".join(rows)}</ol>'


def estimator():
    checks = []
    for k, (a, b, u, label) in C.PRICES.items():
        on = " checked" if k == "nettoyage" else ""
        checks.append(f'<label class="chk"><input type="checkbox" name="t" value="{k}" data-min="{a}" data-max="{b}"{on}><span>{esc(label)}</span><small>{a} à {b} {u}</small></label>')
    a, b = C.PRICES["nettoyage"][:2]
    return f"""<form class="estim" data-estim onsubmit="return false">
<div class="estim-in">
<label class="range"><span>Surface de façade</span><output data-surf>160 m²</output>
<input type="range" name="surface" min="40" max="400" step="10" value="160" aria-describedby="surf-aide"></label>
<p class="hint" id="surf-aide">Pas de mesure ? Multipliez le tour de la maison par la hauteur des murs, puis retirez les grandes ouvertures.</p>
<fieldset><legend>Travaux envisagés</legend>{''.join(checks)}</fieldset>
</div>
<div class="estim-out" aria-live="polite"><p>Budget indicatif</p><p class="estim-val" data-out>{money(160 * a)} à {money(160 * b)}</p>
<p class="small">Fourniture et pose, avant visite. Le devis ferme suit le diagnostic sur place.</p>
<a class="btn btn-primary" href="/contact/#devis"><span>Faire chiffrer ma façade</span></a></div>
</form>"""


def nuancier():
    sw = "".join(f'<li><button type="button" class="sw" data-sw="{c}" style="--c:{c}" aria-pressed="{"true" if i == 1 else "false"}"><span>{esc(n)}</span></button></li>'
                 for i, (n, c) in enumerate(G.SWATCHES))
    house = """<svg class="house" viewBox="0 0 480 300" role="img" aria-label="Maison d'exemple dont la teinte de façade change">
<path d="M40 128L240 30l200 98z" fill="#9c4a33"/><path d="M40 128L240 30l200 98" fill="none" stroke="#7d3a28" stroke-width="6"/>
<rect x="60" y="128" width="360" height="160" class="house-wall"/>
<rect x="60" y="270" width="360" height="18" fill="#000" opacity=".12"/>
<g fill="#3a3835"><rect x="96" y="156" width="56" height="70"/><rect x="328" y="156" width="56" height="70"/><rect x="214" y="190" width="52" height="98"/></g>
<g fill="#eeece8"><rect x="88" y="226" width="72" height="8"/><rect x="320" y="226" width="72" height="8"/></g>
<g fill="#5f6b5a"><rect x="76" y="156" width="18" height="70"/><rect x="154" y="156" width="18" height="70"/><rect x="308" y="156" width="18" height="70"/><rect x="386" y="156" width="18" height="70"/></g>
<rect x="214" y="190" width="52" height="98" fill="none" stroke="#eeece8" stroke-width="6"/></svg>"""
    return f'<div class="nuancier" data-nuancier style="--wall:{G.SWATCHES[1][1]}">{house}<ul class="sw-list">{sw}</ul><p class="small">Teintes indicatives : à l\'écran, une couleur paraît toujours plus foncée que sur un mur au soleil.</p></div>'


def before_after(before, after, cap_before, cap_after, label):
    if not (has_photo(before) and has_photo(after)):
        return ""
    return f"""<figure class="ba" data-ba style="--pos:50%">
<div class="ba-img ba-after">{img(after, cap_after, "(min-width: 960px) 60vw, 100vw")}</div>
<div class="ba-img ba-before" aria-hidden="true">{img(before, cap_before, "(min-width: 960px) 60vw, 100vw")}</div>
<span class="ba-tag ba-tag-b">Avant</span><span class="ba-tag ba-tag-a">Après</span>
<input type="range" min="0" max="100" value="50" aria-label="{esc(label)} : faites glisser pour comparer avant et après">
<figcaption>{esc(label)}</figcaption></figure>"""


def form_html(commune=None, type_default=None, compact=False):
    opts = "".join(f'<option{" selected" if t == type_default else ""}>{esc(t)}</option>' for t in C.WORK_TYPES)
    dl = "".join(f'<option value="{esc(c["name"])}">' for c in sorted(CM.COMMUNES, key=lambda c: c["name"])) + '<option value="Mitry-Mory">'
    val = f' value="{esc(commune)}"' if commune else ""
    mail = "" if compact else '''<div class="f-row"><label for="f-mail">Email <small>(facultatif)</small></label><input id="f-mail" name="email" type="email" autocomplete="email" maxlength="120"></div>'''
    tel_mail = (f'''<div class="f-two"><div class="f-row"><label for="f-tel">Téléphone</label><input id="f-tel" name="telephone" type="tel" autocomplete="tel" required pattern="[+0-9 .()\\-]{{8,20}}" maxlength="20"></div>{mail}</div>'''
                if not compact else
                '''<div class="f-row"><label for="f-tel">Téléphone</label><input id="f-tel" name="telephone" type="tel" autocomplete="tel" required pattern="[+0-9 .()\\-]{8,20}" maxlength="20"></div>''')
    nom_tel = (f'''<div class="f-two"><div class="f-row"><label for="f-nom">Nom</label><input id="f-nom" name="nom" autocomplete="name" required maxlength="80"></div>
<div class="f-row"><label for="f-tel">Téléphone</label><input id="f-tel" name="telephone" type="tel" autocomplete="tel" required pattern="[+0-9 .()\\-]{{8,20}}" maxlength="20"></div></div>'''
               if compact else
               f'''<div class="f-row"><label for="f-nom">Nom</label><input id="f-nom" name="nom" autocomplete="name" required maxlength="80"></div>{tel_mail}''')
    rappel = "" if compact else '''<fieldset class="f-row f-radio"><legend>Rappel de préférence</legend>
<label><input type="radio" name="rappel" value="Matin"> Matin</label><label><input type="radio" name="rappel" value="Après-midi"> Après-midi</label><label><input type="radio" name="rappel" value="Indifférent" checked> Indifférent</label></fieldset>'''
    msg_req = "" if compact else " required"
    msg_lab = "Votre projet <small>(facultatif)</small>" if compact else "Votre projet"
    rows = 2 if compact else 4
    return f"""<form class="form" id="devis-form" novalidate>
{nom_tel}
<div class="f-two">
<div class="f-row"><label for="f-commune">Commune des travaux</label><input id="f-commune" name="commune" list="communes-l" required maxlength="80" autocomplete="address-level2"{val}><datalist id="communes-l">{dl}</datalist></div>
<div class="f-row"><label for="f-type">Travaux</label><select id="f-type" name="type" required><option value="">Choisir…</option>{opts}</select></div>
</div>
<div class="f-row"><label for="f-msg">{msg_lab}</label><textarea id="f-msg" name="message" rows="{rows}" maxlength="3000"{msg_req} placeholder="Type de maison, état de la façade, surface approximative…"></textarea></div>
{rappel}
<div class="f-hp" aria-hidden="true"><label for="f-site">Site web</label><input id="f-site" name="site_web" tabindex="-1" autocomplete="off"></div>
<label class="f-ok"><input type="checkbox" name="consentement" required> <span>J'accepte que mes coordonnées servent uniquement à traiter ma demande de devis.</span></label>
<button class="btn btn-primary btn-big" type="submit"><span>Recevoir mon devis gratuit</span></button>
<div class="form-status" id="form-status" role="status"></div>
</form>"""


def form_section(commune=None, title="Demandez votre devis gratuit", type_default=None):
    return f"""<section class="sec sec-devis" id="devis" aria-labelledby="devis-t">
<div class="wrap devis-grid">
<div class="devis-txt">
<h2 id="devis-t">{title}</h2>
<p>Décrivez votre façade en quelques mots. Nous vous rappelons pour convenir d'une visite, gratuite, puis vous recevez un devis détaillé sous 48 heures.</p>
<ul class="ticks">
<li>{ICONS['check']}<span>Visite et devis gratuits, sans engagement</span></li>
<li>{ICONS['check']}<span>Chaque poste chiffré : échafaudage, préparation, finition</span></li>
<li>{ICONS['check']}<span>Attestation d'assurance décennale jointe au devis</span></li>
</ul>
<p class="devis-tel">Vous préférez appeler ? {tel_btn('btn btn-primary', B['phone'])}</p>
<p class="small">Ou au <a href="tel:{B['phone2_e164']}">{B['phone2']}</a>, 7 jours sur 7.</p>
</div>
{form_html(commune, type_default)}
</div></section>"""


def aside_card(price=None, label="Votre devis", head=None):
    p = f'<p class="ac-price"><small>Prix indicatif</small><strong>{esc(price)}</strong></p>' if price else ""
    if head:
        p = f'<p class="ac-price"><strong>{esc(head)}</strong></p>'

    return f"""<aside class="aside-card" aria-label="{esc(label)}">{p}
<ul class="ticks">
<li>{ICONS['check']}<span>Visite et devis gratuits</span></li>
<li>{ICONS['check']}<span>Devis détaillé sous 48 h</span></li>
<li>{ICONS['check']}<span>Garantie décennale</span></li>
</ul>
{tel_btn('btn btn-primary', B['phone'])}
<a class="btn btn-ghost" href="#devis"><span>Demander un devis</span></a>
<p class="ac-rate"><strong>{B['google_rating']}/5</strong> sur Google, {B['google_count']} avis</p>
</aside>"""


def sections_html(sections, price_key=None, self_guide=False):
    out = []
    for i, (t, body) in enumerate(sections):
        b = body.strip()
        b = b.replace("[[prix]]", prices_table(price_key, self_guide=self_guide)).replace("[[prix-toiture]]", prices_table(price_key, roof=True))
        b = b.replace("[[etapes]]", steps_html()).replace("[[estimateur]]", estimator()).replace("[[nuancier]]", nuancier())
        sid = re.sub(r"[^a-z0-9]+", "-", t.lower().encode("ascii", "ignore").decode())[:40].strip("-") or f"s{i}"
        out.append(f'<section class="art-sec" aria-labelledby="{sid}"><h2 id="{sid}">{esc(t)}</h2>{b}</section>')
    return "".join(out)


def near_communes(n=12):
    return sorted(CM.COMMUNES, key=lambda c: c["dist"])[:n]


def commune_chips(communes, prefix="Ravalement"):
    return '<ul class="chips">' + "".join(
        f'<li><a href="/ravalement-facade-{c["slug"]}/">{esc(c["name"])} <small>{c["dist_site"]} km</small></a></li>' for c in communes) + "</ul>"


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------

def diag_module():
    tabs, stage, panels = [], [], []
    for i, d in enumerate(C.DIAG):
        sel = "true" if i == 0 else "false"
        hid = "" if i == 0 else " hidden"
        tabs.append(f'<li role="presentation"><button type="button" role="tab" id="dt-{d["key"]}" aria-controls="dp-{d["key"]}" aria-selected="{sel}" tabindex="{0 if i == 0 else -1}" data-key="{d["key"]}"><span class="dt-dot"></span>{esc(d["label"])}</button></li>')
        alt = PHOTOS["diag-" + d["key"]]["alt"] if has_photo("diag-" + d["key"]) else d["title"]
        stage.append(f'<div class="ds" data-tile="{d["key"]}"{hid}>{tile_or_photo(d["key"], "h" + str(i), alt, "(min-width: 900px) 55vw, 100vw")}</div>')
        if d["price"]:
            a, b, u, _ = C.PRICES[d["price"]]
            price = f'<p class="dp-price"><small>Budget indicatif</small><strong>{a} à {b} {u}</strong></p>'
        else:
            price = '<p class="dp-price"><small>Budget</small><strong>sur diagnostic</strong></p>'
        s = SV.BY_SLUG[d["page"]]
        panels.append(f'<div class="dp" role="tabpanel" id="dp-{d["key"]}" aria-labelledby="dt-{d["key"]}" data-panel="{d["key"]}"{hid}>'
                      f'<h3>{esc(d["title"])}</h3><p><strong>Ce que c\'est.</strong> {esc(d["what"])}</p><p><strong>Ce qu\'on fait.</strong> {esc(d["do"])}</p>'
                      f'<div class="dp-foot">{price}<a class="dp-link" href="/{d["page"]}/">{esc(s["name"])}</a></div></div>')
    return f"""<section class="diag" data-diag aria-labelledby="diag-t">
<div class="diag-stage">{''.join(stage)}</div>
<div class="diag-side">
<h2 id="diag-t">Que montre votre façade ?</h2>
<p class="diag-sub">Choisissez ce que vous voyez sur vos murs : on vous dit ce que c'est, comment on le traite et ce que ça coûte.</p>
<ul class="diag-tabs" role="tablist" aria-label="Symptômes de façade">{''.join(tabs)}</ul>
<div class="diag-panels">{''.join(panels)}</div>
</div>
</section>"""


def zones_block(full=False):
    groups = []
    for g in C.GROUPS:
        cs = sorted([c for c in CM.COMMUNES if c["group"] == g], key=lambda c: c["dist"])
        lis = "".join(f'<li><a href="/ravalement-facade-{c["slug"]}/">{esc(c["name"])}</a> <small>{c["dist_site"]} km</small></li>' for c in cs)
        if full:
            prof = CM.GROUP_PROFILES[g]["habitat"][0]
            groups.append(f'<section class="zg" aria-labelledby="zg-{h(g)[:6]}"><h2 id="zg-{h(g)[:6]}">{esc(g)}</h2><p>{esc(prof)}</p><ul class="zg-list">{lis}</ul></section>')
        else:
            groups.append(f'<details class="zg-d"><summary>{esc(g)} <small>{len(cs)} communes</small></summary><ul class="zg-list">{lis}</ul></details>')
    return "".join(groups)


TICKER = ["Ravalement de façade", "Enduit", "Peinture de façade", "Nettoyage", "Traitement des fissures", "Imperméabilisation",
          "Meulière et pierre", "Isolation par l'extérieur", "Bardage", "Couverture", "Démoussage", "Zinguerie"]


def build_home():
    ba = before_after("ravalement-avant", "ravalement-apres", "Façade avant ravalement", "Façade après ravalement", "Ravalement d'un pavillon : avant et après")
    ba2 = before_after("couverture-avant", "couverture-apres", "Toiture avant réfection", "Toiture après réfection", "Réfection d'une couverture en tuiles : avant et après")
    ba_sec = ""
    if ba:
        ba_sec = f"""<section class="sec sec-sable" aria-labelledby="ba-t"><div class="wrap ba-grid">
<div><h2 id="ba-t">Avant, après</h2><p>Échafaudage monté, isolant posé, puis enduit de finition clair : la même façade, à quelques semaines d'écart.</p></div>{ba}</div></section>"""
    roof_vis = ba2 or visual("couverture-apres", "toiture", "rf", "Toiture en tuiles mécaniques en partie couverte de mousses")
    toit = "".join(f'<li><a href="/{s["slug"]}/"><span>{esc(s["name"])}</span><small>{esc(SHORT[s["slug"]])}</small></a></li>' for s in SV.TOITURE)
    brands = "".join(f"<li>{esc(b)}</li>" for b in C.BRANDS)
    tick = "".join(f"<li>{esc(t)}</li>" for t in TICKER)
    video = ""
    if os.path.exists(os.path.join(SITE, "video", "hero.mp4")):
        video = ('<video class="hero-vid" muted loop playsinline preload="none" poster="/assets/video/hero-poster.jpg" data-hero-video>'
                 '<source data-src="/assets/video/hero.webm" type="video/webm"><source data-src="/assets/video/hero.mp4" type="video/mp4"></video>')
    body = f"""
<section class="hero-video" aria-labelledby="hero-t">
<div class="hero-media" aria-hidden="true">{video}</div>
<div class="wrap hero-grid">
<div class="hero-brand">
{LG.svg("stacked", "light", animated=True, cls="hero-logo", title="Artisan Druart, couverture et ravalement", uid="hl")}
<h1 id="hero-t">Ravalement de façade à Mitry-Mory et dans un rayon de 50 km</h1>
<p class="lead">Nettoyage, enduit, peinture, fissures, meulière et isolation par l'extérieur. La toiture et les gouttières reprises sur le même échafaudage.</p>
<div class="cta-row">{tel_btn()}<span class="rate"><strong>{B['google_rating']}</strong><span><span class="stars" aria-hidden="true">★★★★★</span> {B['google_count']} avis Google</span></span></div>
</div>
<div class="hero-card" id="devis">
<h2>Votre devis gratuit</h2>
<p class="hc-sub">Visite offerte, devis détaillé sous 48 heures. Réponse rapide, 7 jours sur 7.</p>
{form_html(compact=True)}
</div>
</div>
</section>
<div class="ticker" aria-hidden="true"><div class="ticker-in"><ul>{tick}</ul><ul>{tick}</ul></div></div>

<div class="sec">
<div class="wrap">
{diag_module()}
</div>
</div>

<section class="sec sec-sable" aria-labelledby="postes-t">
<div class="wrap split">
<div class="split-h">
<h2 id="postes-t">Nos travaux de façade, poste par poste</h2>
<p>Comme sur nos devis : chaque travail a sa ligne et son prix au mètre carré. Les fourchettes sont indicatives, le prix ferme est fixé après la visite.</p>
<p><a class="more" href="/prix-ravalement-facade/">Estimer le budget de ma façade</a></p>
</div>
{devis_list([s['slug'] for s in SV.FACADE])}
</div>
</section>
{ba_sec}
<section class="sec" aria-labelledby="etapes-t">
<div class="wrap">
<div class="sec-head"><h2 id="etapes-t">Comment se passe un ravalement avec nous</h2><p>Six étapes, du premier coup de fil à la réception de la façade. Vous savez toujours ce qui se passe et ce que ça coûte.</p></div>
{steps_html()}
</div>
</section>

<section class="sec sec-roof" aria-labelledby="toit-t">
<div class="wrap roof-grid">
<div class="roof-txt">
<h2 id="toit-t">La toiture, pendant que l'échafaudage est en place</h2>
<p>La couverture est notre seconde activité. L'échafaudage monté pour la façade donne accès aux gouttières, aux rives et au bas de pente : on change une descente, on refait un solin ou on démousse le toit sans remonter de matériel. Urgences fuite ou tuiles envolées : 7 jours sur 7.</p>
<ul class="roof-list">{toit}</ul>
<p class="small">Projet de toiture seule ? Voir notre site de couvreur, <a href="{B['sister_url']}" rel="noopener">artisandruart.fr</a>.</p>
</div>
<div class="roof-vis">{roof_vis}</div>
</div>
</section>

<section class="sec" aria-labelledby="conf-t">
<div class="wrap">
<div class="sec-head"><h2 id="conf-t">Ce sur quoi vous pouvez compter</h2><p>Une entreprise locale, joignable, assurée, et des devis que l'on peut comparer ligne par ligne.</p></div>
<dl class="stats">
<div><dt>{B['google_rating']}/5</dt><dd><strong>Note Google</strong>{B['google_count']} avis clients, et {B['mappy_rating']} sur Mappy</dd></div>
<div><dt>48 h</dt><dd><strong>Devis détaillé</strong>après une visite gratuite, chaque poste chiffré</dd></div>
<div><dt>10 ans</dt><dd><strong>Garantie décennale</strong>attestation jointe à chaque devis</dd></div>
<div><dt>7 j/7</dt><dd><strong>Joignables</strong>au {B['phone']}, y compris pour une urgence toiture</dd></div>
</dl>
<div class="brands"><p>Nous travaillons avec les produits de</p><ul>{brands}</ul></div>
</div>
</section>

<section class="sec sec-sable" aria-labelledby="zones-t">
<div class="wrap zones-grid">
<div class="zones-txt">
<h2 id="zones-t">73 communes à moins de 50 km</h2>
<p>De Compans, à 3,5 km, à Coulommiers, à 40 km : nous intervenons en Seine-et-Marne, en Seine-Saint-Denis, dans le Val-d'Oise, sur les bords de Marne du Val-de-Marne et dans le sud de l'Oise.</p>
{zones_block()}
<p><a class="more" href="/zones-intervention/">Toutes les zones d'intervention</a></p>
</div>
<div class="zones-map">{art.zone_map(cls="map", links=True, title="Carte des communes où nous intervenons autour de Mitry-Mory")}</div>
</div>
</section>
{faq_html(C.HOME_FAQ)}
<section class="sec sec-tight" aria-labelledby="cta-t"><div class="wrap">
<div class="cta-band"><div><h2 id="cta-t">Votre façade mérite mieux qu'un coup de peinture</h2><p>Visite gratuite, diagnostic franc, devis détaillé sous 48 heures.</p></div>
<div class="cta-row">{tel_btn()}<a class="btn btn-ghost" href="#devis"><span>Demander un devis</span></a></div></div>
</div></section>
"""
    page("/", "Ravalement de façade Mitry-Mory (77) | Artisan Druart",
         "Ravalement de façade à Mitry-Mory et 50 km autour : nettoyage, enduit, peinture, fissures, meulière, isolation par l'extérieur, toiture. Devis gratuit sous 48 h.",
         body, schema=[faq_schema(C.HOME_FAQ)], priority="1.0", cls="p-home",
         extra_head='\n<link rel="preload" href="/assets/video/hero-poster.jpg" as="image">')


def build_service(s):
    path = f"/{s['slug']}/"
    cat = ("Façade", "/ravalement-facade/") if s["cat"] == "facade" else ("Toiture", "/couverture-toiture/")
    crumbs = [(s["name"], path)] if s["slug"] in ("ravalement-facade", "couverture-toiture") else [cat, (s["name"], path)]
    points = "".join(f'<li>{ICONS["check"]}<span>{esc(p)}</span></li>' for p in s["points"])
    related = []
    for r in s["related"]:
        if r in SV.BY_SLUG:
            x = SV.BY_SLUG[r]
            related.append(f'<li><a href="/{r}/"><span>{esc(x["name"])}</span><small>{esc(SHORT[r])}</small></a></li>')
        elif r in G.GUIDE_BY_SLUG:
            x = G.GUIDE_BY_SLUG[r]
            related.append(f'<li><a href="/{r}/"><span>{esc(x["name"])}</span><small>Guide</small></a></li>')
    roof = s["cat"] == "toiture"
    body = f"""
<section class="ph{' ph-roof' if roof else ''}">
<div class="wrap ph-grid">
<div class="ph-txt">
<h1>{esc(s['h1'])}</h1>
<p class="lead">{esc(s['lead'])}</p>
<ul class="ticks">{points}</ul>
<div class="cta-row">{tel_btn()}{devis_btn()}</div>
</div>
{visual(s.get('photo'), s['tile'], 'v', s['name'], eager=True)}
</div>
</section>
<div class="wrap body-grid">
<article class="art">{sections_html(s['sections'], None if s['slug'] == 'ravalement-facade' else s.get('price'))}</article>
<div class="aside-col">{aside_card(price_label(s['slug']))}
<nav class="related" aria-label="Prestations liées"><h2>À voir aussi</h2><ul>{''.join(related)}</ul></nav></div>
</div>
{faq_html(s['faq'])}
<section class="sec sec-near" aria-labelledby="near-t"><div class="wrap">
<h2 id="near-t">{esc(s['name'])} autour de Mitry-Mory</h2>
<p>Nous intervenons dans 73 communes à moins de 50 km. Les plus proches :</p>
{commune_chips(near_communes(16))}
<p><a class="more" href="/zones-intervention/">Toutes les communes</a></p>
</div></section>
{form_section(type_default=_type_for(s['slug']))}
"""
    sch = [service_schema(s)]
    if s["faq"]:
        sch.append(faq_schema(s["faq"]))
    page(path, s["title"], s["desc"], body, crumbs=crumbs, schema=sch, current=s["slug"], priority="0.9", cls="p-service")


def _type_for(slug):
    return {"ravalement-facade": "Ravalement complet", "enduit-facade": "Enduit de façade", "peinture-facade": "Peinture de façade",
            "nettoyage-facade": "Nettoyage / démoussage de façade", "traitement-fissures-facade": "Fissures",
            "impermeabilisation-facade": "Imperméabilisation", "ravalement-meuliere": "Meulière / pierre",
            "isolation-thermique-exterieure": "Isolation par l'extérieur", "bardage": "Bardage",
            "couverture-toiture": "Toiture / couverture", "demoussage-toiture": "Toiture / couverture",
            "zinguerie-gouttieres": "Gouttières / zinguerie"}.get(slug)


def build_guide(g):
    path = f"/{g['slug']}/"
    others = "".join(f'<li><a href="/{o["slug"]}/"><span>{esc(o["name"])}</span><small>Guide</small></a></li>' for o in G.GUIDES if o["slug"] != g["slug"])
    svc = "".join(f'<li><a href="/{s}/"><span>{esc(SV.BY_SLUG[s]["name"])}</span><small>{esc(price_label(s))}</small></a></li>' for s in ["ravalement-facade", "enduit-facade", "peinture-facade", "isolation-thermique-exterieure"])
    body = f"""
<section class="ph ph-guide">
<div class="wrap ph-grid">
<div class="ph-txt">
<h1>{esc(g['h1'])}</h1>
<p class="lead">{esc(g['lead'])}</p>
<p class="meta">Mis à jour le {date.today().strftime('%d/%m/%Y')} par {esc(B['short'])}, façadier à Mitry-Mory</p>
</div>
{visual(None, g['tile'], 'v', g['name'], eager=True)}
</div>
</section>
<div class="wrap body-grid">
<article class="art">{sections_html(g['sections'], None, self_guide=g['slug'] == 'prix-ravalement-facade')}</article>
<div class="aside-col">{aside_card()}
<nav class="related" aria-label="Autres guides"><h2>Autres guides</h2><ul>{others}</ul><h2>Prestations</h2><ul>{svc}</ul></nav></div>
</div>
{faq_html(g['faq'])}
{form_section()}
"""
    page(path, g["title"], g["desc"], body, crumbs=[("Conseils", "/conseils/"), (g["name"], path)],
         schema=[article_schema(g, path), faq_schema(g["faq"])], current=g["slug"], priority="0.8", cls="p-guide")


def build_conseils():
    cards = []
    for i, g in enumerate(G.GUIDES):
        cards.append(f'<li class="gc"><a href="/{g["slug"]}/">{tile_or_photo(g["tile"], "c" + str(i), "", "(min-width: 900px) 30vw, 100vw")}<span class="gc-t">{esc(g["name"])}</span><span class="gc-d">{esc(g["desc"])}</span></a></li>')
    svc = "".join(f'<li><a href="/{s["slug"]}/"><span>{esc(s["name"])}</span><small>{esc(SHORT[s["slug"]])}</small></a></li>' for s in SV.SERVICES)
    body = f"""
<section class="ph ph-plain"><div class="wrap narrow"><h1>Conseils pour votre ravalement</h1><p class="lead">{esc(G.CONSEILS_INTRO)}</p></div></section>
<section class="sec sec-tight"><div class="wrap"><ul class="guide-cards">{''.join(cards)}</ul></div></section>
<section class="sec" aria-labelledby="fiches-t"><div class="wrap split">
<div class="split-h"><h2 id="fiches-t">Nos fiches travaux</h2><p>Chaque prestation a sa page : quand la choisir, comment on la réalise, ce qu'elle coûte et les questions qu'on nous pose le plus souvent.</p></div>
<ul class="link-list">{svc}</ul></div></section>
{faq_html(C.HOME_FAQ[2:5], "Questions courantes")}
{form_section()}
"""
    page("/conseils/", "Conseils ravalement de façade : prix, démarches, couleurs",
         "Guides pour préparer un ravalement de façade : prix au m², déclaration préalable, choix de la couleur, et fiches de chaque travail de façade et de toiture.",
         body, crumbs=[("Conseils", "/conseils/")], current="conseils", priority="0.7", cls="p-hub")


def build_zones():
    body = f"""
<section class="ph ph-plain"><div class="wrap ph-grid ph-zones">
<div class="ph-txt"><h1>Zones d'intervention : 50 km autour de Mitry-Mory</h1><p class="lead">{esc(G.ZONES_INTRO)}</p>
<div class="cta-row">{tel_btn()}{devis_btn()}</div></div>
<div class="zones-map">{art.zone_map(cls="map map-big", links=True, title="Carte des 73 communes où nous intervenons")}</div>
</div></section>
<section class="sec sec-tight"><div class="wrap zg-grid">{zones_block(full=True)}</div></section>
{form_section()}
"""
    page("/zones-intervention/", "Zones d'intervention : ravalement autour de Mitry-Mory",
         "Les 73 communes où Artisan Druart réalise ravalements de façade et travaux de toiture, à moins de 50 km de Mitry-Mory : 77, 93, 95, 94 et sud de l'Oise.",
         body, crumbs=[("Zones d'intervention", "/zones-intervention/")], current="zones-intervention", priority="0.8", cls="p-zones")


def dir_phrase(bearing):
    d = CM.direction(bearing)
    return ("à l'" + d) if d in ("est", "ouest") else ("au " + d)


def build_commune(c):
    name = c["name"]
    a, de = CM.a_(name), CM.de_(name)
    cp = c["cp"][0]
    prof = CM.GROUP_PROFILES[c["group"]]
    habitat = prof["habitat"][pick(c["slug"], len(prof["habitat"]))]
    note = CM.NOTES.get(c["slug"], "")
    dist = c["dist_site"]
    dirp = dir_phrase(c["bearing"])
    path = f"/ravalement-facade-{c['slug']}/"
    S0, keys, ex_desc = prof["example"]
    surf = S0 + (pick(c["slug"] + "s", 5) - 2) * 10
    lo = sum(C.PRICES[k][0] for k in keys) * surf
    hi = sum(C.PRICES[k][1] for k in keys) * surf
    budget = f"{money(lo)} à {money(hi)}"
    protected = c["slug"] in CM.PROTECTED
    neigh = CM.neighbours(c, 6)
    dept = f"{c['dept_name']} ({c['dept']})"
    facts = [("Département", dept), ("Code postal", ", ".join(c["cp"])), ("Population", CM.pop_label(c["pop"]).replace("environ ", "")),
             ("Intercommunalité", c["epci"] or ""), ("Depuis Mitry-Mory", f"{dist} km {dirp.replace('à l', 'l').replace('au ', '')}")]
    facts_html = "".join(f"<div><dt>{esc(k)}</dt><dd>{esc(v)}</dd></div>" for k, v in facts if v)
    lotiss = c["group"] in ("Goële et Plaine de France", "Vallée de la Marne et Marne-la-Vallée", "Plateau de Brie")
    demarches = [f"<p>Un ravalement à l'identique ne demande en général aucune autorisation, sauf si la commune a soumis les ravalements à déclaration préalable ou si la maison se trouve en secteur protégé. Le service urbanisme de la mairie {esc(de)} vous le confirme, et le Géoportail de l'urbanisme permet de consulter le PLU applicable.</p>"]
    if protected:
        demarches.append(f"<p>Une partie {'du centre ' if c['slug'] not in ('noisiel', 'champs-sur-marne') else ''}{esc(de)} se trouve en secteur protégé. Dans ce cas, même un ravalement à l'identique se déclare, l'architecte des Bâtiments de France donne son avis, et le délai d'instruction passe à deux mois.</p>")
    if lotiss:
        demarches.append("<p>Dans les lotissements et les quartiers récents, le règlement de lotissement ou le PLU fixe souvent les teintes et les finitions autorisées : vérifiez-les avant de changer de couleur.</p>")
    demarches.append(f"<p>Si l'échafaudage doit occuper le trottoir, demandez une autorisation d'occupation du domaine public à la mairie quelques semaines avant le chantier. Notre guide de la <a href=\"/ravalement-facade-declaration-prealable/\">déclaration préalable</a> détaille les pièces à fournir.</p>")
    faq = [
        (f"Intervenez-vous {a} ?",
         f"Oui. {name} se trouve à {dist} km {dirp} de Mitry-Mory, dans notre secteur « {c['group']} ». La visite et le devis sont gratuits, et le devis détaillé vous parvient sous 48 heures."),
        (f"Faut-il une déclaration préalable pour un ravalement {a} ?",
         ("Oui, très probablement si votre maison est dans le secteur protégé : l'architecte des Bâtiments de France donne son avis. Ailleurs dans la commune, une déclaration est nécessaire si vous changez la teinte ou l'aspect, ou si la commune l'impose pour tout ravalement."
          if protected else
          "Elle est nécessaire si vous changez la teinte ou l'aspect de la façade, si la maison est en secteur protégé, ou si la commune impose une déclaration pour tout ravalement. Le service urbanisme de la mairie vous le confirme.")),
        (f"Combien coûte un ravalement {a} ?",
         f"Les prix ne dépendent pas de la commune mais de la façade. Pour {ex_desc} d'environ {surf} m², comptez {budget.replace(chr(8239), ' ').replace(chr(160), ' ')}. Le prix ferme est fixé après visite."),
    ]
    neigh_html = commune_chips(neigh)
    V = lambda key, opts: opts[pick(c["slug"] + key, len(opts))]
    E = esc
    lead = V("lead", [
        f"Artisan Druart rénove les façades des maisons {E(de)} ({cp}) : nettoyage, enduit, peinture, fissures, meulière et isolation par l'extérieur. {E(name)} se trouve à {dist} km {dirp} de Mitry-Mory, où nous sommes installés.",
        f"Façadier installé à Mitry-Mory, à {dist} km {dirp}, nous réalisons {E(a)} ({cp}) le nettoyage, la réparation et le ravalement complet des façades de maisons, de la visite gratuite à la réception du chantier.",
        f"Nettoyage, enduit, peinture, traitement des fissures, meulière, isolation : nous intervenons {E(a)} ({cp}), à {dist} km de notre base de Mitry-Mory, avec un devis détaillé sous 48 heures.",
    ])
    tr_intro = V("tr", [
        "Les demandes qui reviennent le plus souvent dans ce secteur, avec nos prix indicatifs :",
        f"Ce que l'on nous demande le plus souvent {E(a)} et alentour, avec les fourchettes de prix au mètre carré :",
        "Les travaux les plus fréquents sur ce type de bâti, du plus courant au plus spécifique :",
    ])
    budget_p = V("bu", [
        f"Pour {E(ex_desc)}, sur environ {surf} m² de façade, le budget se situe entre <strong>{budget}</strong>, fourniture et pose. Il varie avec l'état du support, la hauteur, les détails de façade et l'accès. Le devis ferme est établi après une visite gratuite.",
        f"Prenons {E(ex_desc)} : environ {surf} m² de façade. Avec nos prix indicatifs, le budget va de <strong>{budget}</strong>, fourniture et pose. L'état réel du support, la hauteur et l'accès font varier ce montant : seul le devis établi après visite fait foi.",
    ])
    toit_p = V("to", [
        f"L'échafaudage monté pour la façade donne accès au bas de la toiture. C'est le bon moment pour <a href=\"/zinguerie-gouttieres/\">changer une gouttière</a>, <a href=\"/demoussage-toiture/\">démousser le toit</a> ou faire vérifier la <a href=\"/couverture-toiture/\">couverture</a>. Nous intervenons aussi en urgence {E(a)}, 7 jours sur 7.",
        f"Une gouttière qui déborde salit une façade neuve en un hiver. Pendant le ravalement, nous pouvons <a href=\"/zinguerie-gouttieres/\">reprendre la zinguerie</a>, <a href=\"/demoussage-toiture/\">démousser la toiture</a> ou réviser la <a href=\"/couverture-toiture/\">couverture</a> depuis le même échafaudage. En cas de fuite {E(a)}, nous sommes joignables 7 jours sur 7.",
        f"La toiture est notre seconde activité. Depuis l'échafaudage de la façade, nous vérifions rives, solins et gouttières, et nous pouvons <a href=\"/demoussage-toiture/\">démousser le toit</a>, <a href=\"/zinguerie-gouttieres/\">changer les descentes</a> ou réparer la <a href=\"/couverture-toiture/\">couverture</a>. Urgences {E(a)} : 7 jours sur 7.",
    ])
    nn = [n["name"] for n in neigh[:3]]
    near_p = f"Autour {E(de)}, nous réalisons aussi des ravalements {E(CM.a_(nn[0]))}, {E(CM.a_(nn[1]))} et {E(CM.a_(nn[2]))}. Les communes les plus proches :"
    body = f"""
<section class="ph ph-commune">
<div class="wrap ph-grid">
<div class="ph-txt">
<h1>Ravalement de façade {esc(a)}</h1>
<p class="lead">{lead}</p>
<div class="cta-row">{tel_btn()}{devis_btn()}</div>
<dl class="facts">{facts_html}</dl>
</div>
<figure class="visual visual-map">{art.zone_map(current=c, cls="map map-mini", links=False, title=f"Position {de} par rapport à Mitry-Mory")}<figcaption>{esc(name)} et Mitry-Mory, cercles tous les 10 km</figcaption></figure>
</div>
</section>
<div class="wrap body-grid">
<article class="art">
<section class="art-sec" aria-labelledby="bati"><h2 id="bati">Les façades {esc(de)}</h2>{f'<p>{esc(note)}</p>' if note else ''}<p>{esc(habitat)}</p></section>
<section class="art-sec" aria-labelledby="travaux"><h2 id="travaux">Nos travaux de façade {esc(a)}</h2>
<p>{tr_intro}</p>{devis_list(prof['works'], 'devis-compact')}</section>
<section class="art-sec" aria-labelledby="budget"><h2 id="budget">Exemple de budget {esc(a)}</h2>
<p>{budget_p}</p>
<p><a class="more" href="/prix-ravalement-facade/">Estimer le budget de votre façade</a></p></section>
<section class="art-sec" aria-labelledby="demarches"><h2 id="demarches">Démarches avant un ravalement {esc(a)}</h2>{''.join(demarches)}</section>
<section class="art-sec" aria-labelledby="toit"><h2 id="toit">Et la toiture ?</h2>
<p>{toit_p}</p></section>
</article>
<div class="aside-col">{aside_card(head=f"Devis gratuit {a}")}</div>
</div>
{faq_html(faq)}
<section class="sec sec-near" aria-labelledby="near-t"><div class="wrap">
<h2 id="near-t">Nous intervenons aussi près {esc(de)}</h2>
<p>{near_p}</p>
{neigh_html}
<p><a class="more" href="/zones-intervention/">Les 73 communes de notre zone</a></p>
</div></section>
{form_section(commune=name)}
"""
    title = f"Ravalement de façade {a} ({cp}) | Artisan Druart"
    if len(title) > 62:
        title = f"Ravalement de façade {a} ({cp})"
    desc = f"Ravalement de façade {a} ({cp}) : nettoyage, enduit, peinture, fissures, meulière, isolation. Artisan à {dist} km, devis gratuit sous 48 h."
    area = {"@type": "City", "name": name, "address": {"@type": "PostalAddress", "postalCode": cp, "addressLocality": name, "addressCountry": "FR"}}
    sch = [service_schema(SV.BY_SLUG["ravalement-facade"] | {"desc": desc, "name": f"Ravalement de façade {a}"}, area=area), faq_schema(faq)]
    page(path, title, desc, body, crumbs=[("Zones d'intervention", "/zones-intervention/"), (name, path)], schema=sch, priority="0.7", cls="p-commune")


def build_contact():
    maps = "https://www.google.com/maps/search/?api=1&query=" + "Artisan+Druart+Maison+Renovation+13+rue+Paul+Vaillant+Couturier+77290+Mitry-Mory"
    body = f"""
<section class="ph ph-plain"><div class="wrap ph-grid">
<div class="ph-txt"><h1>Contact et devis gratuit</h1>
<p class="lead">Appelez-nous ou décrivez votre projet dans le formulaire : nous vous rappelons pour convenir d'une visite, puis vous recevez un devis détaillé sous 48 heures.</p></div>
<div class="contact-card">
<p class="cc-l">Téléphone, 7 j/7</p>
<p class="cc-tel"><a href="tel:{B['phone_e164']}">{B['phone']}</a><br><a href="tel:{B['phone2_e164']}">{B['phone2']}</a></p>
<p class="cc-l">Email</p><p><a href="mailto:{B['email']}">{B['email']}</a></p>
<p class="cc-l">Adresse</p><p>{esc(B['name'])}<br>{esc(B['street'])}<br>{B['postcode']} {B['city']}</p>
<p><a class="more" href="{maps}" rel="noopener">Itinéraire sur Google Maps</a></p>
</div>
</div></section>
{form_section(title="Votre demande de devis")}
"""
    page("/contact/", "Contact et devis gratuit | Artisan Druart, Mitry-Mory",
         "Contactez Artisan Druart, façadier et couvreur à Mitry-Mory : 06 20 14 69 91 ou 06 51 28 34 89, 7 j/7. Demande de devis gratuit en ligne, réponse sous 48 h.",
         body, crumbs=[("Contact", "/contact/")], current="contact", priority="0.7", cls="p-contact",
         schema=[{"@context": "https://schema.org", "@type": "ContactPage", "url": URL + "/contact/", "about": {"@id": ORG_ID}}])


def build_legal():
    A = C.A_CONFIRMER
    ident = [f"<strong>{esc(B['name'])}</strong>"]
    if A["forme"]:
        ident.append(esc(A["forme"]))
    ident.append(f"{esc(B['street'])}, {B['postcode']} {B['city']}")
    if A["siret"]:
        ident.append(f"SIRET : {esc(A['siret'])}")
    ident.append(f"Téléphone : {B['phone']}, email : <a href=\"mailto:{B['email']}\">{B['email']}</a>")
    if A["dirigeant"]:
        ident.append(f"Directeur de la publication : {esc(A['dirigeant'])}")
    extra = ""
    if A["assureur"]:
        extra += f"<h2>Assurance décennale</h2><p>{esc(A['assureur'])}</p>"
    if A["mediateur"]:
        extra += f"<h2>Médiation de la consommation</h2><p>En cas de litige, vous pouvez recourir gratuitement au médiateur de la consommation : {esc(A['mediateur'])}.</p>"
    body = f"""
<section class="ph ph-plain"><div class="wrap narrow"><h1>Mentions légales</h1></div></section>
<section class="sec sec-tight"><div class="wrap narrow art legal">
<h2>Éditeur du site</h2><p>{'<br>'.join(ident)}</p>
{extra}
<h2>Hébergement</h2><p>Cloudflare, Inc., 101 Townsend St, San Francisco, CA 94107, États-Unis.</p>
<h2>Conception</h2><p>ALLOSITEWEB, Montreuil (<a href="https://allositeweb.com/" rel="noopener">allositeweb.com</a>).</p>
<h2>Données personnelles</h2>
<p>Les informations envoyées par le formulaire de devis (nom, téléphone, email, commune, description du projet) servent uniquement à répondre à votre demande et à établir un devis. Elles sont transmises par email à {esc(B['short'])} et ne sont ni revendues ni utilisées à des fins publicitaires. Elles sont conservées le temps nécessaire au suivi de votre demande, puis, si un contrat est conclu, pendant la durée des obligations légales.</p>
<p>Conformément au règlement général sur la protection des données, vous disposez d'un droit d'accès, de rectification, d'effacement et d'opposition, en écrivant à <a href="mailto:{B['email']}">{B['email']}</a>. Vous pouvez aussi adresser une réclamation à la CNIL.</p>
<h2>Cookies</h2><p>Ce site ne dépose aucun cookie de mesure d'audience ni de publicité. Les polices de caractères sont hébergées sur le site lui-même.</p>
<h2>Crédits</h2><p>Polices Big Shoulders Display et Hanken Grotesk (licence SIL Open Font License). Illustrations et cartes : ALLOSITEWEB. Données communales : INSEE et Etalab (découpage administratif), GeoNames.</p>
</div></section>"""
    page("/mentions-legales/", "Mentions légales | Artisan Druart", "Mentions légales et données personnelles du site maisonrenovationbtp.fr.",
         body, crumbs=[("Mentions légales", "/mentions-legales/")], robots="noindex,follow", cls="p-legal")


def build_404():
    body = f"""<section class="ph ph-plain"><div class="wrap narrow"><h1>Cette page n'existe pas</h1>
<p class="lead">L'adresse a peut-être changé. Voici les pages les plus consultées :</p>
<ul class="link-list">
<li><a href="/"><span>Accueil</span></a></li><li><a href="/ravalement-facade/"><span>Ravalement de façade</span></a></li>
<li><a href="/prix-ravalement-facade/"><span>Prix d'un ravalement</span></a></li><li><a href="/couverture-toiture/"><span>Toiture</span></a></li>
<li><a href="/zones-intervention/"><span>Zones d'intervention</span></a></li><li><a href="/contact/"><span>Contact</span></a></li></ul>
<div class="cta-row">{tel_btn()}</div></div></section>"""
    page("/404.html", "Page introuvable | Artisan Druart", "Cette page n'existe pas.", body, robots="noindex,follow", cls="p-404")


# ---------------------------------------------------------------------------
# Fichiers techniques
# ---------------------------------------------------------------------------

def copy_assets():
    if os.path.exists(PUBLIC):
        shutil.rmtree(PUBLIC)
    os.makedirs(os.path.join(PUBLIC, "assets", "fonts"))
    for name, key in (("archivo.woff2", "font"),):
        data = open(os.path.join(SITE, "fonts", name), "rb").read()
        fn = name.replace(".woff2", f".{hashlib.sha1(data).hexdigest()[:8]}.woff2")
        write(f"/assets/fonts/{fn}", data, binary=True)
        ASSETS[key] = f"/assets/fonts/{fn}"
    css = open(os.path.join(SITE, "site.css"), encoding="utf-8").read()
    css = css.replace("__FONT__", ASSETS["font"])
    js = open(os.path.join(SITE, "site.js"), encoding="utf-8").read()
    js = js.replace("__PHONE__", B["phone_e164"]).replace("__WHATSAPP__", B["whatsapp"])
    pr = {k: [v[0], v[1]] for k, v in C.PRICES.items()}
    js = js.replace("__PRICES__", json.dumps(pr))
    for kind, data in (("css", css), ("js", js)):
        fn = f"/assets/site.{h(data)[:10]}.{kind}"
        write(fn, data)
        ASSETS[kind] = fn
    # logos SVG et vidéo
    write("/assets/logo-h.svg", LG.svg("horizontal", "color"))
    write("/assets/logo-h-light.svg", LG.svg("horizontal", "light"))
    write("/assets/logo-mark.svg", LG.svg("mark", "color"))
    write("/assets/logo-mark-light.svg", LG.svg("mark", "light"))
    write("/assets/logo-light.svg", LG.svg("stacked", "light"))
    write("/assets/logo.svg", LG.svg("stacked", "color"))
    write("/favicon.svg", LG.favicon())
    vid = os.path.join(SITE, "video")
    if os.path.isdir(vid):
        for f in os.listdir(vid):
            write(f"/assets/video/{f}", open(os.path.join(vid, f), "rb").read(), binary=True)
    img_src = os.path.join(SITE, "img-out")
    if os.path.isdir(img_src):
        shutil.copytree(img_src, os.path.join(PUBLIC, "assets", "img"), dirs_exist_ok=True)
    legacy = os.path.join(SITE, "legacy-out")
    if os.path.isdir(legacy):
        shutil.copytree(legacy, PUBLIC, dirs_exist_ok=True)
    for f in ("og-image.jpg", "icon-512.png", "icon-192.png", "apple-touch-icon.png", "favicon.ico", "logo.png", "logo-artisan-druart-2ea109d7.png"):
        p = os.path.join(SITE, "brand", f)
        if os.path.exists(p):
            dest = f"/assets/{f}" if f.startswith(("og-", "icon-", "logo")) else f"/{f}"
            write(dest, open(p, "rb").read(), binary=True)


def tech_files():
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for p, prio in PAGES:
        sm.append(f"<url><loc>{URL}{p}</loc><lastmod>{TODAY}</lastmod><priority>{prio}</priority></url>")
    sm.append("</urlset>")
    write("/sitemap.xml", "\n".join(sm) + "\n")
    write("/robots.txt", f"User-agent: *\nAllow: /\nDisallow: /api/\n\nSitemap: {URL}/sitemap.xml\n")
    red = ["# Anciennes adresses → nouvelles (301)"]
    for a, b in C.REDIRECTS:
        red.append(f"{a} {b} 301")
        red.append(f"{a}/ {b} 301")
    red.append("/index.html / 301")
    write("/_redirects", "\n".join(red) + "\n")
    csp = ("default-src 'self'; script-src 'self' '" + EARLY_JS_HASH + "'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; "
           "font-src 'self'; connect-src 'self'; form-action 'self'; frame-ancestors 'self'; base-uri 'self'; object-src 'none'")
    hd = f"""/*
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  X-Frame-Options: SAMEORIGIN
  Permissions-Policy: camera=(), microphone=(), geolocation=(), interest-cohort=()
  Content-Security-Policy: {csp}

/assets/*
  Cache-Control: public, max-age=31536000, immutable

/assets/img/*
  Cache-Control: public, max-age=2592000

/assets/og-image.jpg
  Cache-Control: public, max-age=86400

/assets/icon-*
  Cache-Control: public, max-age=86400

https://:project.:subdomain.workers.dev/*
  X-Robots-Tag: noindex

https://:version.:project.:subdomain.workers.dev/*
  X-Robots-Tag: noindex
"""
    write("/_headers", hd)
    man = {"name": B["name"], "short_name": "Artisan Druart", "start_url": "/", "display": "browser", "background_color": "#eeece8",
           "theme_color": "#806d61", "icons": [{"src": "/assets/icon-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "/assets/icon-512.png", "sizes": "512x512", "type": "image/png"}]}
    write("/site.webmanifest", json.dumps(man, ensure_ascii=False, indent=1))
    ll = [f"# {B['name']}", "",
          f"> Façadier et couvreur à {B['city']} ({B['postcode']}, {B['dept']}). Ravalement de façade (activité principale) et couverture (activité secondaire) dans un rayon de 50 km : Seine-et-Marne, Seine-Saint-Denis, Val-d'Oise, Val-de-Marne, sud de l'Oise. Téléphone {B['phone']} ou {B['phone2']}, 7 j/7. Email {B['email']}.",
          "", "## Prestations"]
    ll += [f"- [{s['name']}]({URL}/{s['slug']}/): {SHORT[s['slug']]} ({price_label(s['slug'])})" for s in SV.SERVICES]
    ll += ["", "## Guides"] + [f"- [{g['name']}]({URL}/{g['slug']}/): {g['desc']}" for g in G.GUIDES]
    ll += ["", "## Zones d'intervention", f"- [Toutes les communes]({URL}/zones-intervention/)"]
    ll += [f"- [Ravalement de façade {CM.a_(c['name'])}]({URL}/ravalement-facade-{c['slug']}/) ({c['dist_site']} km)" for c in sorted(CM.COMMUNES, key=lambda c: c["dist"])]
    ll += ["", "## Contact", f"- [Contact et devis]({URL}/contact/)"]
    write("/llms.txt", "\n".join(ll) + "\n")


def main():
    copy_assets()
    build_home()
    for s in SV.SERVICES:
        build_service(s)
    for g in G.GUIDES:
        build_guide(g)
    build_conseils()
    build_zones()
    for c in CM.COMMUNES:
        build_commune(c)
    build_contact()
    build_legal()
    build_404()
    tech_files()
    n = len([p for p in PAGES])
    print(f"{n} pages indexables générées dans public/ ({len(CM.COMMUNES)} communes), photos : {len(PHOTOS)}")


if __name__ == "__main__":
    main()
