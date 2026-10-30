# -*- coding: utf-8 -*-
"""Contenus communs du site maisonrenovationbtp.fr (Artisan Druart, Maison Rénovation).

Les textes des prestations sont dans services.py, les guides dans guides.py,
les pages communes dans communes.py.
"""

SITE_URL = "https://maisonrenovationbtp.fr"

BUSINESS = {
    "name": "Artisan Druart – Maison Rénovation",
    "short": "Artisan Druart",
    "gbp": "Artisan Druart - Maison Renovation",
    "phone": "06 20 14 69 91",
    "phone_e164": "+33620146991",
    "phone2": "06 51 28 34 89",
    "phone2_e164": "+33651283489",
    "whatsapp": "33620146991",
    "email": "maison.renovationbtp@gmail.com",
    "street": "13 rue Paul Vaillant Couturier",
    "postcode": "77290",
    "city": "Mitry-Mory",
    "dept": "Seine-et-Marne",
    "sister_url": "https://artisandruart.fr/",
    "google_rating": "5,0",
    "google_count": 73,
    "mappy_rating": "5/5",
}

# À confirmer avec le client avant la bascule du domaine (laisser vide = non affiché)
A_CONFIRMER = {
    "siret": "",
    "forme": "",            # ex. « Entreprise individuelle »
    "dirigeant": "",        # directeur de la publication
    "assureur": "",         # assureur décennale et zone couverte
    "mediateur": "",        # médiateur de la consommation (nom + site)
}

# Prix indicatifs au m² repris du site actuel (validés par le client)
PRICES = {
    "nettoyage": (10, 25, "€/m²", "Nettoyage et traitement"),
    "peinture": (25, 50, "€/m²", "Peinture de façade"),
    "impermeabilisation": (30, 60, "€/m²", "Revêtement d'imperméabilité"),
    "enduit": (40, 100, "€/m²", "Enduit neuf"),
    "meuliere": (60, 120, "€/m²", "Rejointoiement de meulière"),
    "ite": (120, 220, "€/m²", "Isolation par l'extérieur"),
}

# Repères de prix toiture : fourchettes de marché, à faire valider par le client
ROOF_PRICES = {
    "demoussage": (15, 35, "€/m²", "Démoussage et traitement de toiture"),
    "hydrofuge": (10, 20, "€/m²", "Hydrofuge de toiture (en plus)"),
    "gouttiere": (40, 90, "€/ml", "Gouttière zinc posée"),
    "descente": (30, 60, "€/ml", "Descente d'eaux pluviales"),
    "couverture": (120, 250, "€/m²", "Réfection de couverture en tuiles"),
}

BRANDS = ["Weber", "Le Comptoir Seigneurie Gauthier", "Zolpan", "Tollens", "Unikalo", "Parexlanko", "PRB"]

# Diagnostic interactif de l'accueil : symptôme → explication, traitement, budget, page
DIAG = [
    {
        "key": "salissures",
        "label": "Traces vertes ou noires",
        "title": "Salissures, mousses et algues",
        "what": "Des algues, des mousses ou de la pollution se fixent sur l'enduit, surtout en bas des murs, au nord et sous les appuis de fenêtre. Le support est en général sain.",
        "do": "Nettoyage à basse pression, traitement anti-mousse laissé à agir, puis hydrofuge incolore si vous voulez garder l'aspect actuel plus longtemps.",
        "price": "nettoyage",
        "page": "nettoyage-facade",
    },
    {
        "key": "faiencage",
        "label": "Fines craquelures en réseau",
        "title": "Faïençage de l'enduit",
        "what": "Un réseau de microfissures de moins de 0,2 mm, comme une toile d'araignée. C'est le vieillissement normal d'un enduit : il laisse entrer l'eau mais ne met pas le mur en danger.",
        "do": "Un revêtement souple qui ponte les microfissures et rend le mur étanche à la pluie, tout en le laissant respirer.",
        "price": "impermeabilisation",
        "page": "impermeabilisation-facade",
    },
    {
        "key": "fissure",
        "label": "Fissure en escalier ou au-dessus d'une fenêtre",
        "title": "Fissure à surveiller",
        "what": "Une fissure nette, souvent en biais depuis l'angle d'une fenêtre ou en escalier dans les joints. Elle peut venir d'un linteau, d'un retrait du mortier ou d'un léger mouvement du sol.",
        "do": "On mesure la largeur, on vérifie si elle bouge, puis on ouvre, on traite et on ponte avec une armature. Au-delà de 2 mm, on cherche d'abord la cause.",
        "price": None,
        "page": "traitement-fissures-facade",
    },
    {
        "key": "creux",
        "label": "L'enduit sonne creux ou tombe",
        "title": "Enduit décollé",
        "what": "Quand on tape, ça sonne creux : l'enduit n'adhère plus au mur, souvent à cause de l'eau. Les plaques finissent par tomber, en commençant par le bas et les angles.",
        "do": "On pioche les zones creuses jusqu'au support sain, puis on refait l'enduit en deux ou trois passes, avec la finition de votre choix.",
        "price": "enduit",
        "page": "enduit-facade",
    },
    {
        "key": "meuliere",
        "label": "Joints de meulière qui se détachent",
        "title": "Joints de meulière fatigués",
        "what": "Les joints se creusent ou se décollent, souvent parce qu'ils ont été refaits au ciment, trop dur pour la pierre. L'humidité reste alors piégée dans le mur.",
        "do": "Dégarnissage des joints, brossage de la pierre, puis rejointoiement à la chaux dans l'aspect d'origine : joints beurrés, en relief ou rocaillés.",
        "price": "meuliere",
        "page": "ravalement-meuliere",
    },
    {
        "key": "froid",
        "label": "Murs froids, chauffage qui peine",
        "title": "Murs qui laissent fuir la chaleur",
        "what": "Des murs froids au toucher, de la condensation dans les angles, des factures qui montent : les murs ne sont pas ou peu isolés. Un ravalement est le bon moment pour y remédier.",
        "do": "Isolation par l'extérieur : un isolant collé et chevillé, puis un enduit ou un bardage par-dessus. La maison garde sa surface habitable.",
        "price": "ite",
        "page": "isolation-thermique-exterieure",
    },
]

STEPS = [
    ("Visite et diagnostic", "On mesure les façades, on sonde l'enduit, on relève les fissures et les traces d'humidité. La visite est gratuite."),
    ("Devis détaillé", "Chaque poste est chiffré : échafaudage, préparation, traitement, finition. Vous le recevez sous 48 heures."),
    ("Démarches", "On prépare les pièces techniques de la déclaration préalable et, si besoin, la demande d'occupation du trottoir."),
    ("Installation", "Montage de l'échafaudage, bâches, protection des menuiseries, des sols et des plantations."),
    ("Préparation et finition", "Nettoyage et réparations d'abord, finition ensuite, par temps sec et hors gel, comme le prévoient les fabricants."),
    ("Réception", "Démontage, nettoyage du chantier et tour de la façade ensemble avant la facture."),
]

HOME_FAQ = [
    ("Quels travaux de façade réalisez-vous ?",
     "Le ravalement complet et chacune de ses étapes : nettoyage et démoussage, traitement des fissures, enduit neuf (monocouche, traditionnel ou à la chaux), peinture, revêtements d'imperméabilité, rejointoiement de meulière et de pierre, isolation par l'extérieur et bardage."),
    ("Dans quelles communes intervenez-vous ?",
     "Dans un rayon de 50 km autour de Mitry-Mory : nord et ouest de la Seine-et-Marne, est de la Seine-Saint-Denis, est du Val-d'Oise, bords de Marne dans le Val-de-Marne et sud de l'Oise. La liste complète est sur la page des zones d'intervention."),
    ("Le devis est-il gratuit ?",
     "Oui. La visite pour mesurer et diagnostiquer la façade est gratuite, et le devis détaillé poste par poste vous parvient sous 48 heures."),
    ("Faut-il une autorisation pour ravaler sa façade ?",
     "Pas toujours. Une déclaration préalable est nécessaire si la teinte ou l'aspect change, si la maison est en secteur protégé (abords d'un monument historique, site patrimonial remarquable) ou si la commune l'impose pour tout ravalement. Nous préparons les pièces techniques du dossier."),
    ("Faites-vous aussi la toiture ?",
     "Oui, c'est notre seconde activité : réparation et réfection de couverture, démoussage, gouttières et zinguerie. L'échafaudage monté pour la façade donne un accès direct au bas de la toiture."),
    ("Êtes-vous assurés ?",
     "Oui, en responsabilité civile professionnelle et en garantie décennale. L'attestation d'assurance décennale est jointe au devis."),
]

# Secteurs de la zone d'intervention (même ordre que sur le site actuel)
GROUPS = [
    "Goële et Plaine de France",
    "Est de la Seine-Saint-Denis",
    "Vallée de la Marne et Marne-la-Vallée",
    "Pays de Meaux et Brie des rivières",
    "Plateau de Brie",
    "Est du Val-d'Oise",
    "Sud de l'Oise",
    "Bords de Marne (Val-de-Marne)",
]

WORK_TYPES = [
    "Ravalement complet",
    "Nettoyage / démoussage de façade",
    "Enduit de façade",
    "Peinture de façade",
    "Fissures",
    "Imperméabilisation",
    "Meulière / pierre",
    "Isolation par l'extérieur",
    "Bardage",
    "Toiture / couverture",
    "Gouttières / zinguerie",
    "Autre",
]

# Anciennes adresses (ancien site) → nouvelles, en 301
REDIRECTS = [
    ("/-ravalement-de-facade-mitry-mory", "/ravalement-facade/"),
    ("/couvreur-77-charpentier-77", "/couverture-toiture/"),
    ("/bardage-aulnay-sous-bois", "/bardage/"),
    ("/travaux-renovation-maison-77", "/"),
    ("/renovation-salle-de-bain-77-", "/"),
    ("/-blog-conseils", "/conseils/"),
    ("/devis", "/contact/"),
    ("/prix", "/prix-ravalement-facade/"),
    ("/zones", "/zones-intervention/"),
]
