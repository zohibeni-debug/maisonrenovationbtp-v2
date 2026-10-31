# -*- coding: utf-8 -*-
"""Contrôles du site généré : liens internes, balises, données structurées, adresses de l'ancien site."""
import json, os, re, sys
from html.parser import HTMLParser
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUB = os.path.join(ROOT, "public")
OLD = ["/", "/ravalement-facade/", "/enduit-facade/", "/peinture-facade/", "/nettoyage-facade/", "/traitement-fissures-facade/",
       "/impermeabilisation-facade/", "/ravalement-meuliere/", "/isolation-thermique-exterieure/", "/bardage/", "/couverture-toiture/",
       "/demoussage-toiture/", "/zinguerie-gouttieres/", "/prix-ravalement-facade/", "/conseils/", "/zones-intervention/", "/contact/",
       "/mentions-legales/", "/qui-sommes-nous/", "/ravalement-facade-declaration-prealable/", "/choisir-couleur-facade/"]
OLD += ["/ravalement-facade-%s/" % s for s in """villeparisis claye-souilly compans dammartin-en-goele othis saint-mard juilly moussy-le-neuf le-pin villevaude annet-sur-marne le-mesnil-amelot tremblay-en-france villepinte sevran aulnay-sous-bois livry-gargan vaujours coubron clichy-sous-bois montfermeil les-pavillons-sous-bois le-raincy villemomble gagny le-blanc-mesnil bondy neuilly-sur-marne noisy-le-grand rosny-sous-bois drancy chelles courtry brou-sur-chantereine vaires-sur-marne thorigny-sur-marne pomponne lagny-sur-marne torcy champs-sur-marne noisiel bussy-saint-georges montevrain serris magny-le-hongre meaux trilport esbly coulommiers la-ferte-sous-jouarre pontault-combault roissy-en-brie ozoir-la-ferriere tournan-en-brie gonesse goussainville louvres fosses arnouville garges-les-gonesse sarcelles villiers-le-bel roissy-en-france senlis chantilly crepy-en-valois nanteuil-le-haudouin le-perreux-sur-marne nogent-sur-marne bry-sur-marne champigny-sur-marne villiers-sur-marne fontenay-sous-bois""".split()]

class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.links=[]; s.ids=[]; s.h1=0; s.title=""; s.desc=None; s.canon=None; s.imgs_noalt=0; s.ld=[]; s._t=False; s._ld=False; s.text=[]; s._main=0; s._skip=0; s.robots=""
    def handle_starttag(s, t, a):
        a = dict(a)
        if "id" in a: s.ids.append(a["id"])
        if t == "a" and a.get("href"): s.links.append(a["href"])
        if t == "h1": s.h1 += 1
        if t == "title" and not s._skip and not s.title: s._t = True
        if t == "meta" and a.get("name") == "description": s.desc = a.get("content")
        if t == "meta" and a.get("name") == "robots": s.robots = a.get("content")
        if t == "link" and a.get("rel") == "canonical": s.canon = a.get("href")
        if t == "img" and "alt" not in a: s.imgs_noalt += 1
        if t == "img":
            s.links.append(a.get("src", ""))
            for part in (a.get("srcset") or "").split(","):
                if part.strip(): s.links.append(part.strip().split(" ")[0])
        if t == "link" and a.get("href", "").startswith("/"): s.links.append(a["href"])
        if t == "script" and a.get("src"): s.links.append(a["src"])
        if t == "script" and a.get("type") == "application/ld+json": s._ld = True; s.ld.append("")
        if t == "main": s._main += 1
        if t in ("script", "style", "svg"): s._skip += 1
    def handle_endtag(s, t):
        if t == "title": s._t = False
        if t == "script": s._ld = False
        if t in ("script", "style", "svg"): s._skip = max(0, s._skip - 1)
    def handle_data(s, d):
        if s._t: s.title += d
        if s._ld: s.ld[-1] += d
        elif s._main and not s._skip: s.text.append(d)

pages = {}
for dp, dn, fn in os.walk(PUB):
    for f in fn:
        if f.endswith(".html"):
            rel = "/" + os.path.relpath(os.path.join(dp, f), PUB).replace("index.html", "")
            p = P(); p.feed(open(os.path.join(dp, f), encoding="utf-8").read()); pages[rel] = p

def exists(path):
    path = path.split("#")[0].split("?")[0]
    if not path: return True
    full = os.path.join(PUB, path.lstrip("/"))
    if path.endswith("/"): return os.path.exists(os.path.join(full, "index.html"))
    return os.path.exists(full)

errors = []
titles, descs = Counter(), Counter()
inbound = defaultdict(int)
words = {}
for rel, p in sorted(pages.items()):
    if p.h1 != 1: errors.append(f"{rel}: {p.h1} h1")
    dup = [i for i, n in Counter(p.ids).items() if n > 1]
    if dup: errors.append(f"{rel}: ids en double {dup}")
    if p.imgs_noalt: errors.append(f"{rel}: {p.imgs_noalt} images sans alt")
    for l in p.links:
        if l.startswith("/") and not l.startswith("//"):
            if not exists(l): errors.append(f"{rel}: lien cassé {l}")
            else: inbound[l.split("#")[0]] += 1
    for j in p.ld:
        try: json.loads(j)
        except Exception as e: errors.append(f"{rel}: JSON-LD invalide {e}")
    if rel != "/404.html":
        titles[p.title] += 1; descs[p.desc] += 1
        if len(p.title) > 65: errors.append(f"{rel}: titre long ({len(p.title)}) {p.title}")
        if not p.desc or len(p.desc) > 165: errors.append(f"{rel}: description {len(p.desc or '')} car.")
        if not p.canon or not p.canon.endswith(rel): errors.append(f"{rel}: canonical {p.canon}")
    words[rel] = len(re.findall(r"\w+", " ".join(p.text)))
for t, n in titles.items():
    if n > 1: errors.append(f"titre en double x{n}: {t}")
for d, n in descs.items():
    if n > 1: errors.append(f"description en double x{n}: {d}")
for u in OLD:
    if not exists(u): errors.append(f"ancienne adresse absente : {u}")
orph = [r for r in pages if r not in ("/404.html",) and inbound.get(r, 0) == 0 and r != "/"]
sm = open(os.path.join(PUB, "sitemap.xml")).read()
print(f"{len(pages)} fichiers HTML, {len(OLD)} adresses de l'ancien site contrôlées, {sm.count('<loc>')} URL dans le sitemap")
print("pages sans lien entrant :", orph)
w = sorted(words.items(), key=lambda x: x[1])
print("mots (contenu principal) min :", w[:3], "max :", w[-3:])
groups = defaultdict(list)
for r, n in words.items():
    k = "commune" if r.startswith("/ravalement-facade-") and r.count("-") > 2 and "declaration" not in r else r
    groups[k if k == "commune" else "autres"].append(n)
for k, v in groups.items(): print(k, "moyenne", sum(v) // len(v), "min", min(v))
print("ERREURS :", len(errors))
for e in errors[:60]: print(" -", e)
sys.exit(1 if errors else 0)
