# -*- coding: utf-8 -*-
"""Pages « Ravalement de façade à <commune> » : données et textes propres à chaque secteur et commune.

Les données chiffrées (code INSEE, codes postaux, population, intercommunalité) viennent du jeu
« découpage administratif » d'Etalab ; les coordonnées, de GeoNames. Voir communes_data.json.
"""
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
COMMUNES = json.load(open(os.path.join(HERE, "communes_data.json"), encoding="utf-8"))
BY_SLUG = {c["slug"]: c for c in COMMUNES}
MITRY = (48.98333, 2.61667)

# ---------------------------------------------------------------------------
# Profils par secteur : bâti courant, travaux typiques, exemple de budget
# ---------------------------------------------------------------------------
GROUP_PROFILES = {
    "Goële et Plaine de France": {
        "habitat": [
            "Autour de Mitry-Mory, les vieux centres de village ont des murs de moellons calcaires enduits à la chaux, des corps de ferme et des maisons de bourg à la façade sobre. Autour, des lotissements des années 1970 à 2010, en parpaing et enduit monocouche, ont fait grandir les communes.",
            "Le bâti mêle deux époques : les maisons anciennes du bourg, en pierre enduite à la chaux, et les pavillons construits depuis les années 1970, presque tous en enduit monocouche gratté. Ces derniers arrivent aujourd'hui à l'âge du premier vrai ravalement.",
        ],
        "works": ["nettoyage-facade", "peinture-facade", "enduit-facade", "traitement-fissures-facade", "isolation-thermique-exterieure"],
        "example": (170, ["nettoyage", "peinture"], "un pavillon des années 1980 en monocouche, nettoyé puis repeint"),
    },
    "Est de la Seine-Saint-Denis": {
        "habitat": [
            "Les rues pavillonnaires sont nées des lotissements de l'entre-deux-guerres : maisons en meulière, en brique ou en parpaing enduit au ciment, souvent agrandies depuis. On y trouve aussi des villas plus anciennes et des maisons des années 1950 à 1970.",
            "Une grande partie des maisons date des années 1920 à 1960 : pavillons en meulière aux joints décorés, maisons de brique, façades enduites au ciment qui faïencent avec le temps. Beaucoup ont reçu des extensions dont les jonctions fissurent.",
        ],
        "works": ["ravalement-meuliere", "traitement-fissures-facade", "impermeabilisation-facade", "enduit-facade", "peinture-facade"],
        "example": (150, ["impermeabilisation"], "un pavillon des années 1950 à l'enduit ciment faïencé, traité et imperméabilisé"),
    },
    "Vallée de la Marne et Marne-la-Vallée": {
        "habitat": [
            "Deux paysages se côtoient : les anciens bourgs des bords de Marne, avec leurs maisons en meulière et leurs villas du début du XXe siècle, et les quartiers de Marne-la-Vallée construits à partir des années 1970, en enduit monocouche et souvent soumis à des règles de teintes précises.",
            "Sur les coteaux et en bord de Marne, la meulière et la brique dominent. Dans les quartiers de la ville nouvelle, les maisons de 20 à 40 ans ont des enduits monocouches qui se salissent, se décolorent et faïencent par endroits.",
        ],
        "works": ["nettoyage-facade", "peinture-facade", "ravalement-meuliere", "impermeabilisation-facade", "isolation-thermique-exterieure"],
        "example": (170, ["nettoyage", "peinture"], "une maison des années 1990 en monocouche, nettoyée puis repeinte"),
    },
    "Pays de Meaux et Brie des rivières": {
        "habitat": [
            "Dans la vallée de la Marne et sur les plateaux briards, les centres anciens ont des maisons de pierre et de moellons enduits, et la meulière est partout. Les faubourgs et les villages alentour comptent de nombreux pavillons des années 1960 à 2000.",
            "Le bâti ancien est fait de moellons de calcaire et de meulière, enduits à la chaux, avec des encadrements de brique ou de pierre. Les maisons plus récentes, en parpaing et enduit ciment, demandent surtout nettoyage et imperméabilisation.",
        ],
        "works": ["ravalement-meuliere", "enduit-facade", "nettoyage-facade", "impermeabilisation-facade", "traitement-fissures-facade"],
        "example": (190, ["enduit"], "une maison de bourg dont l'enduit sonne creux, piochée et réenduite"),
    },
    "Plateau de Brie": {
        "habitat": [
            "Les villes du plateau ont grandi avec de grands quartiers pavillonnaires des années 1960 à 2000. Les enduits ciment et monocouche y dominent, autour de quelques noyaux anciens en pierre et en meulière.",
            "Le parc de maisons est récent pour l'essentiel : pavillons des années 1970 et 1980, souvent avec un sous-sol semi-enterré et des pignons très exposés au vent d'ouest. C'est là que le faïençage et les salissures apparaissent en premier.",
        ],
        "works": ["nettoyage-facade", "impermeabilisation-facade", "peinture-facade", "isolation-thermique-exterieure", "traitement-fissures-facade"],
        "example": (180, ["nettoyage", "impermeabilisation"], "un pavillon des années 1970 nettoyé et imperméabilisé"),
    },
    "Est du Val-d'Oise": {
        "habitat": [
            "Autour des vieux villages de la Plaine de France, aux maisons rurales de pierre enduite, se sont construits des quartiers pavillonnaires de toutes les époques, de l'entre-deux-guerres aux années 2000, et de grands ensembles.",
            "Les maisons anciennes des centres, en moellons enduits, voisinent avec des pavillons en brique, en meulière ou en parpaing enduit au ciment. Près de l'aéroport, beaucoup ont reçu des fenêtres isolantes, mais rarement une isolation des murs.",
        ],
        "works": ["enduit-facade", "traitement-fissures-facade", "impermeabilisation-facade", "isolation-thermique-exterieure", "peinture-facade"],
        "example": (150, ["impermeabilisation"], "un pavillon à l'enduit ciment faïencé, traité et imperméabilisé"),
    },
    "Sud de l'Oise": {
        "habitat": [
            "Le sud de l'Oise est un pays de pierre calcaire : maisons de bourg en moellons, chaînes d'angle et encadrements en pierre de taille, murs enduits à la chaux. Les centres historiques sont souvent protégés, et l'avis de l'architecte des Bâtiments de France y est fréquent.",
            "Pierre de taille, moellons de calcaire et enduits à la chaux font le caractère des centres anciens du Valois et des bords de la Nonette. Les quartiers récents, plus en périphérie, sont en enduit monocouche.",
        ],
        "works": ["ravalement-meuliere", "enduit-facade", "nettoyage-facade", "traitement-fissures-facade", "peinture-facade"],
        "example": (200, ["enduit"], "une maison de bourg en moellons, réenduite à la chaux"),
    },
    "Bords de Marne (Val-de-Marne)": {
        "habitat": [
            "Les bords de Marne sont le pays de la villa en meulière : maisons de 1890 à 1930 aux joints décorés, encadrements de brique, frises de céramique et marquises. On y trouve aussi des maisons bourgeoises enduites et des pavillons plus récents.",
            "Les coteaux de la Marne ont été lotis entre la fin du XIXe siècle et les années 1930. La meulière y règne, souvent associée à la brique et à des décors de céramique, et les enduits des pignons sont à reprendre à la chaux.",
        ],
        "works": ["ravalement-meuliere", "nettoyage-facade", "enduit-facade", "traitement-fissures-facade", "peinture-facade"],
        "example": (160, ["meuliere"], "une villa en meulière dégarnie et rejointoyée à la chaux"),
    },
}

# ---------------------------------------------------------------------------
# Notes propres à certaines communes (faits vérifiables, sans approximations)
# ---------------------------------------------------------------------------
NOTES = {
    "compans": "Compans est un petit village de la Plaine de France, entre la plateforme aéroportuaire et la zone d'activités de Mitry-Compans, à quelques minutes de notre dépôt.",
    "villeparisis": "Ville très pavillonnaire, Villeparisis réunit des pavillons de l'entre-deux-guerres, des maisons des années 1960 et 1970 et des lotissements récents : on y rencontre à peu près tous les types d'enduits.",
    "le-mesnil-amelot": "Au bord de l'aéroport Paris-Charles-de-Gaulle, Le Mesnil-Amelot garde un bourg ancien en moellons enduits, entouré de maisons plus récentes.",
    "claye-souilly": "Claye-Souilly associe un bourg ancien, le long de la Beuvronne, et de vastes quartiers pavillonnaires construits depuis les années 1960.",
    "villevaude": "Villevaudé est faite de plusieurs hameaux, dont Montjay-la-Tour, aux maisons anciennes en pierre, et de quartiers pavillonnaires plus récents.",
    "juilly": "Juilly, connue pour son ancien collège des oratoriens, a un bourg aux murs de pierre et des maisons récentes en périphérie.",
    "annet-sur-marne": "Village des bords de Marne, Annet-sur-Marne compte des maisons anciennes en pierre et en meulière et des pavillons plus récents.",
    "dammartin-en-goele": "Perchée sur sa butte, Dammartin-en-Goële a un centre ancien aux maisons de pierre et de nombreux quartiers pavillonnaires sur les pentes. Une partie du centre se trouve aux abords de monuments historiques.",
    "tremblay-en-france": "Tremblay-en-France associe le Vieux-Pays, au bâti rural ancien, et de grands quartiers pavillonnaires comme le Vert-Galant.",
    "coubron": "Coubron est une commune résidentielle en lisière de la forêt régionale de Bondy, aux maisons individuelles avec jardin. La végétation proche favorise les mousses sur les façades nord.",
    "livry-gargan": "Livry-Gargan est l'une des communes les plus pavillonnaires de la Seine-Saint-Denis, avec beaucoup de maisons en meulière et de pavillons de l'entre-deux-guerres.",
    "aulnay-sous-bois": "Au sud de la ville, Aulnay-sous-Bois a de grands quartiers pavillonnaires aux maisons de meulière, de brique et d'enduit ciment.",
    "les-pavillons-sous-bois": "La commune porte bien son nom : créée en 1905, elle s'est construite autour de lotissements de pavillons, dont beaucoup en meulière.",
    "le-raincy": "Le Raincy s'est bâti sur le domaine de l'ancien château, loti au XIXe siècle : villas, maisons de maître et meulière dominent. L'église Notre-Dame du Raincy, d'Auguste Perret, est classée monument historique : les maisons de ses abords demandent l'avis de l'architecte des Bâtiments de France.",
    "gagny": "Gagny, sur les coteaux, compte de nombreux pavillons en meulière et des maisons de l'entre-deux-guerres.",
    "villemomble": "Villemomble a conservé beaucoup de villas et de maisons en meulière du début du XXe siècle, aux joints souvent refaits au ciment.",
    "drancy": "Drancy est une ville de pavillons de l'entre-deux-guerres, en brique, en meulière ou en enduit ciment, souvent agrandis.",
    "neuilly-sur-marne": "Entre la Marne et les coteaux, Neuilly-sur-Marne compte de nombreux pavillons, dont une partie en meulière près de la rivière.",
    "chelles": "Chelles, la plus grande ville du secteur, compte un très grand nombre de pavillons, avec beaucoup de meulière sur les coteaux et en bord de Marne.",
    "lagny-sur-marne": "Lagny-sur-Marne a un centre ancien serré autour de l'église Notre-Dame-des-Ardents, et des faubourgs en meulière. Une partie du centre se trouve aux abords de monuments historiques.",
    "torcy": "Torcy fait partie de la ville nouvelle de Marne-la-Vallée : la plupart des maisons datent des années 1970 à 1990, en enduit monocouche.",
    "champs-sur-marne": "Champs-sur-Marne associe le domaine du château, classé monument historique, des quartiers de la ville nouvelle et des pavillons plus anciens près de la Marne.",
    "noisiel": "Noisiel est marquée par l'ancienne chocolaterie Menier, classée monument historique, et par sa cité ouvrière en brique. Les quartiers plus récents relèvent de la ville nouvelle de Marne-la-Vallée.",
    "bussy-saint-georges": "Bussy-Saint-Georges s'est surtout construite à partir des années 1990 : les maisons en enduit monocouche y arrivent à l'âge du premier ravalement.",
    "magny-le-hongre": "Les quartiers récents de Magny-le-Hongre suivent souvent des règles précises de teintes et de matériaux : vérifiez-les avant de changer une couleur.",
    "serris": "Les quartiers du Val d'Europe à Serris suivent des prescriptions architecturales précises sur les teintes et les matériaux : renseignez-vous avant de changer une couleur.",
    "meaux": "Meaux a un centre ancien autour de la cathédrale Saint-Étienne et de la cité épiscopale, protégé au titre des monuments historiques, et de nombreux faubourgs pavillonnaires.",
    "la-ferte-sous-jouarre": "La Ferté-sous-Jouarre a été la capitale de la pierre meulière : on y taillait des meules exportées dans le monde entier. La meulière est partout dans le bâti de la ville.",
    "coulommiers": "Coulommiers a un centre ancien de maisons briardes en moellons enduits, et des quartiers pavillonnaires plus récents en périphérie.",
    "ozoir-la-ferriere": "En lisière de la forêt d'Armainvilliers, Ozoir-la-Ferrière est très pavillonnaire. Sous les arbres, les façades se couvrent vite de mousses.",
    "tournan-en-brie": "Tournan-en-Brie garde un bourg ancien briard, entouré de lotissements des années 1970 à 2000.",
    "goussainville": "Goussainville est une ville pavillonnaire ; au nord, le Vieux-Pays a été en grande partie abandonné à cause du bruit de l'aéroport.",
    "sarcelles": "Sarcelles associe le grand ensemble des Lochères, le vieux village de Sarcelles et des quartiers pavillonnaires.",
    "chantilly": "Chantilly, ville du château et du cheval, a un centre en pierre calcaire et en brique, et de nombreuses villas. Une bonne partie de la ville est concernée par des protections patrimoniales.",
    "senlis": "Senlis possède l'un des premiers secteurs sauvegardés de France, aujourd'hui site patrimonial remarquable : dans le centre historique, tout ravalement passe par l'architecte des Bâtiments de France.",
    "crepy-en-valois": "Ancienne capitale du Valois, Crépy-en-Valois a un centre ancien en pierre calcaire, dont une partie se trouve aux abords de monuments historiques.",
    "le-perreux-sur-marne": "Le Perreux-sur-Marne est l'une des villes de la villa en meulière, avec ses maisons du début du XXe siècle aux décors de brique et de céramique.",
    "nogent-sur-marne": "Nogent-sur-Marne compte de nombreuses villas en meulière et maisons bourgeoises sur les coteaux qui descendent vers la Marne.",
    "bry-sur-marne": "Bry-sur-Marne a un bâti de bord de Marne fait de villas, de maisons en meulière et de pavillons plus récents sur le plateau.",
    "champigny-sur-marne": "Champigny-sur-Marne, grande ville des bords de Marne, compte de très nombreux pavillons en meulière et en brique.",
    "fontenay-sous-bois": "Fontenay-sous-Bois associe un centre ancien, des maisons de ville et des pavillons en meulière sur les hauteurs.",
}

# Communes où une partie du bâti est en secteur protégé (centre ancien, abords de monument)
PROTECTED = {"dammartin-en-goele", "le-raincy", "lagny-sur-marne", "champs-sur-marne", "noisiel", "meaux",
             "chantilly", "senlis", "crepy-en-valois", "coulommiers"}


NOTES.update({
    "le-pin": "Petite commune résidentielle entre Courtry et Villevaudé, Le Pin compte surtout des maisons individuelles avec jardin, anciennes dans le bourg, plus récentes en périphérie.",
    "saint-mard": "Voisine de Dammartin-en-Goële, Saint-Mard associe un bourg ancien et des lotissements pavillonnaires construits depuis les années 1970.",
    "moussy-le-neuf": "Moussy-le-Neuf, au nord de Mitry-Mory, est un village de la Goële qui s'est étendu avec des lotissements de maisons individuelles.",
    "othis": "Othis, au nord de Dammartin-en-Goële, s'est beaucoup développée avec des quartiers pavillonnaires à partir des années 1970.",
    "vaujours": "Vaujours, à la limite de la Seine-et-Marne, compte surtout des maisons individuelles, des pavillons anciens aux constructions récentes.",
    "villepinte": "Villepinte associe un vieux village, des quartiers pavillonnaires de l'entre-deux-guerres aux années 1970, et des ensembles d'habitat collectif.",
    "sevran": "Sevran alterne quartiers d'habitat collectif et rues pavillonnaires, avec de nombreux pavillons de l'entre-deux-guerres de part et d'autre du canal de l'Ourcq.",
    "clichy-sous-bois": "Clichy-sous-Bois, sur le plateau, mêle grands ensembles et quartiers pavillonnaires en lisière de la forêt de Bondy.",
    "montfermeil": "Montfermeil, sur le plateau, compte un vieux centre et de nombreuses maisons individuelles. La forêt de Bondy toute proche favorise les mousses sur les murs exposés au nord.",
    "le-blanc-mesnil": "Le Blanc-Mesnil a de grands quartiers pavillonnaires de l'entre-deux-guerres, en brique, en meulière ou en enduit ciment, à côté des ensembles d'habitat collectif.",
    "bondy": "Bondy compte de nombreux pavillons de l'entre-deux-guerres, de part et d'autre du canal de l'Ourcq, souvent agrandis au fil du temps.",
    "rosny-sous-bois": "Rosny-sous-Bois, au pied du plateau d'Avron, compte beaucoup de pavillons et de maisons en meulière sur ses coteaux.",
    "noisy-le-grand": "Noisy-le-Grand associe les quartiers modernes du Mont d'Est et de nombreux pavillons, dont des maisons en meulière vers les bords de Marne.",
    "courtry": "Courtry, entre Chelles et Le Pin, est une commune résidentielle faite surtout de maisons individuelles, des années 1960 à aujourd'hui.",
    "brou-sur-chantereine": "Brou-sur-Chantereine, voisine de Chelles et de Vaires-sur-Marne, compte un vieux bourg et des rues pavillonnaires.",
    "pomponne": "Pomponne, en bord de Marne, garde un bourg ancien et des maisons de caractère, entourés de quartiers pavillonnaires.",
    "thorigny-sur-marne": "Thorigny-sur-Marne s'étage sur le coteau qui domine la Marne, face à Lagny-sur-Marne : maisons de bourg, meulière et pavillons.",
    "vaires-sur-marne": "Vaires-sur-Marne est une ville très pavillonnaire, avec beaucoup de maisons en meulière et de pavillons de l'entre-deux-guerres.",
    "montevrain": "Montévrain associe un vieux village et des quartiers récents de Marne-la-Vallée, construits pour l'essentiel depuis les années 2000.",
    "esbly": "Esbly, en bord de Marne, compte un bourg ancien et de nombreux pavillons, des années 1930 à aujourd'hui.",
    "trilport": "Trilport, en bord de Marne à l'est de Meaux, a un bourg ancien et des quartiers pavillonnaires.",
    "roissy-en-brie": "Roissy-en-Brie s'est fortement développée à partir des années 1970 : la plupart des maisons y sont des pavillons en enduit ciment ou monocouche.",
    "pontault-combault": "Pontault-Combault, l'une des plus grandes villes de Seine-et-Marne, est très pavillonnaire, avec des maisons des années 1960 à 2000.",
    "roissy-en-france": "Roissy-en-France est un village ancien tout proche des pistes de l'aéroport, aux maisons de pierre enduite et aux lotissements plus récents.",
    "louvres": "Louvres garde un centre ancien et s'est agrandie avec de nombreux quartiers récents.",
    "gonesse": "Gonesse a un vieux centre autour de son église Saint-Pierre-Saint-Paul, monument historique, et de vastes quartiers pavillonnaires.",
    "arnouville": "Arnouville est une ville surtout pavillonnaire, organisée autour du château d'Arnouville et de son parc.",
    "garges-les-gonesse": "Garges-lès-Gonesse associe de grands ensembles et des quartiers pavillonnaires, avec de nombreuses maisons de l'entre-deux-guerres.",
    "villiers-le-bel": "Villiers-le-Bel a un vieux village sur le coteau, et des quartiers pavillonnaires et d'habitat collectif en contrebas.",
    "fosses": "Fosses, à la limite de l'Oise, a un bourg ancien et des quartiers construits depuis les années 1970.",
    "nanteuil-le-haudouin": "Nanteuil-le-Haudouin, bourg du Valois, compte de nombreuses maisons en pierre calcaire et des lotissements récents en périphérie.",
    "villiers-sur-marne": "Villiers-sur-Marne compte beaucoup de pavillons, en meulière sur les coteaux et plus récents vers le plateau.",
})
PROTECTED.add("gonesse")

# ---------------------------------------------------------------------------
# Outils de langue et de géographie
# ---------------------------------------------------------------------------

def a_(name):
    """« à Meaux », « au Raincy », « aux Pavillons-sous-Bois », « à La Ferté-sous-Jouarre »."""
    if name.startswith("Le "):
        return "au " + name[3:]
    if name.startswith("Les "):
        return "aux " + name[4:]
    return "à " + name


def de_(name):
    """« de Meaux », « du Raincy », « des Pavillons-sous-Bois », « d'Esbly »."""
    if name.startswith("Le "):
        return "du " + name[3:]
    if name.startswith("Les "):
        return "des " + name[4:]
    if name[0] in "AEIOUÉÈYaeiouéy":
        return "d'" + name
    return "de " + name


DIRS = ["nord", "nord-est", "est", "sud-est", "sud", "sud-ouest", "ouest", "nord-ouest"]


def direction(bearing):
    return DIRS[int(((bearing + 22.5) % 360) // 45)]


def km(a, b):
    R = 6371.0
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    d = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 2 * R * math.asin(math.sqrt(d))


def neighbours(c, n=6):
    others = [o for o in COMMUNES if o["slug"] != c["slug"]]
    others.sort(key=lambda o: km((c["lat"], c["lon"]), (o["lat"], o["lon"])))
    return others[:n]


def project(lat, lon):
    """Projection locale en km autour de Mitry-Mory (x vers l'est, y vers le sud)."""
    x = (lon - MITRY[1]) * 111.32 * math.cos(math.radians(MITRY[0]))
    y = (MITRY[0] - lat) * 110.57
    return x, y


def dist_label(c):
    return c["dist_site"]


def pop_label(p):
    if not p:
        return ""
    if p < 1000:
        return f"{p} habitants"
    r = int(round(p / 100.0) * 100)
    return f"environ {r:,} habitants".replace(",", " ")
