# -*- coding: utf-8 -*-
"""Guides et pages éditoriales : prix, déclaration préalable, couleur, sommaire des conseils, zones."""

GUIDES = [
    {
        "slug": "prix-ravalement-facade",
        "nav": "Prix d'un ravalement",
        "name": "Prix d'un ravalement de façade",
        "title": "Prix d'un ravalement de façade au m² en 2026 (77, 93, 95)",
        "desc": "Prix d'un ravalement de façade au m² : nettoyage, peinture, imperméabilisation, enduit, meulière, isolation. Estimez votre budget et ce qui le fait varier.",
        "h1": "Prix d'un ravalement de façade",
        "lead": "Le prix d'un ravalement dépend de trois choses : la surface de façade, l'état du support et la finition. Voici nos fourchettes au mètre carré, un calculateur pour estimer votre budget et ce qui fait varier la facture.",
        "kicker": "Guide des prix",
        "tile": "creux",
        "sections": [
            ("Estimez votre budget", "[[estimateur]]"),
            ("Les prix au mètre carré", "[[prix]]"),
            ("Ce qui fait varier le prix", """
<ul>
<li><strong>La surface réelle de façade.</strong> On mesure les murs, pignons compris, et on déduit les grandes ouvertures. Un pavillon de 100 m² habitables sur deux niveaux compte souvent 150 à 220 m² de façade.</li>
<li><strong>L'état du support.</strong> Plus il y a d'enduit à piocher, de fissures à traiter ou de joints à refaire, plus la préparation pèse dans le devis.</li>
<li><strong>La hauteur et l'accès.</strong> Un échafaudage sur trois niveaux, un passage étroit ou un trottoir à occuper demandent plus de temps et de matériel.</li>
<li><strong>Les détails.</strong> Encadrements, bandeaux, corniches, soubassements, appuis, garde-corps : chaque détail se traite à la main.</li>
<li><strong>La finition.</strong> Une peinture coûte moins cher qu'un revêtement d'imperméabilité, lui-même moins cher qu'un enduit neuf ou une isolation.</li>
</ul>"""),
            ("Trois exemples de budget", """
<table class="tbl">
<thead><tr><th scope="col">Projet</th><th scope="col">Surface</th><th scope="col">Budget indicatif</th></tr></thead>
<tbody>
<tr><td>Pavillon des années 1990, monocouche sale mais sain : nettoyage, traitement et hydrofuge</td><td>160 m²</td><td>1 600 à 4 000 €</td></tr>
<tr><td>Maison des années 1970, enduit ciment faïencé : traitement des fissures et revêtement d'imperméabilité</td><td>180 m²</td><td>5 400 à 10 800 €</td></tr>
<tr><td>Villa en meulière : dégarnissage et rejointoiement à la chaux</td><td>140 m²</td><td>8 400 à 16 800 €</td></tr>
</tbody>
</table>
<p>Ces montants sont calculés à partir de nos fourchettes au mètre carré. Ils ne remplacent pas le devis établi après visite.</p>"""),
            ("Ce que doit contenir un devis de ravalement", """
<p>Un devis sérieux détaille chaque poste. Vous devez y trouver :</p>
<ul>
<li>la surface mesurée de chaque façade, ouvertures déduites ;</li>
<li>l'installation et la location de l'échafaudage, avec les protections ;</li>
<li>la préparation : nettoyage, piochage, traitement des fissures, avec les surfaces ou les longueurs ;</li>
<li>la finition : produit, marque, classe, nombre de couches ou épaisseur, teinte ;</li>
<li>les travaux annexes : zinguerie, appuis, descentes, traitement des boiseries ;</li>
<li>le taux de TVA, le délai, les conditions de paiement, et l'attestation d'assurance décennale.</li>
</ul>
<p>Pour comparer deux devis, comparez ces lignes une à une, pas seulement le total. Un devis plus bas omet souvent la préparation.</p>"""),
            ("TVA et aides", """
<p>Pour une maison achevée depuis plus de deux ans, la TVA est de 10 % sur les travaux de ravalement. Elle passe à 5,5 % pour une isolation des murs qui atteint le niveau de performance réglementaire. Les aides à la rénovation énergétique concernent l'isolation, pas le ravalement seul. Elles évoluent chaque année et exigent une entreprise certifiée RGE : renseignez-vous sur france-renov.gouv.fr avant de signer.</p>"""),
        ],
        "faq": [
            ("Quel est le prix moyen d'un ravalement de façade ?",
             "Pour une maison individuelle, comptez de 10 à 25 €/m² pour un nettoyage avec traitement, de 25 à 50 €/m² pour une peinture, de 30 à 60 €/m² pour une imperméabilisation et de 40 à 100 €/m² pour un enduit neuf. Le prix ferme est fixé après visite."),
            ("L'échafaudage est-il compris ?",
             "Il figure sur le devis comme un poste à part entière, chiffré selon la hauteur, la longueur de façade et la durée du chantier."),
            ("Peut-on étaler le ravalement sur plusieurs années ?",
             "Oui, façade par façade, en commençant par la plus exposée. Mais chaque tranche demande de remonter l'échafaudage : un chantier unique revient en général moins cher."),
        ],
    },
    {
        "slug": "ravalement-facade-declaration-prealable",
        "nav": "Déclaration préalable",
        "name": "Ravalement et déclaration préalable",
        "title": "Ravalement de façade : faut-il une déclaration préalable ?",
        "desc": "Quand un ravalement de façade demande une déclaration préalable, quelles pièces fournir, quels délais, et l'autorisation pour l'échafaudage sur le trottoir.",
        "h1": "Ravalement de façade : faut-il une déclaration préalable ?",
        "lead": "Pas toujours. Un ravalement à l'identique se fait le plus souvent sans formalité, mais dès que l'aspect change ou que la maison est en secteur protégé, il faut déposer une déclaration préalable en mairie avant de commencer.",
        "kicker": "Démarches",
        "tile": "fissure",
        "sections": [
            ("Les cas où la déclaration est obligatoire", """
<ul>
<li><strong>Vous changez l'aspect de la façade</strong> : nouvelle teinte, nouveau matériau, enduit sur une pierre apparente, bardage, isolation par l'extérieur.</li>
<li><strong>La maison est en secteur protégé</strong> : abords d'un monument historique, site patrimonial remarquable, site classé ou inscrit. Dans ce cas, même un ravalement à l'identique doit être déclaré.</li>
<li><strong>La commune a soumis tous les ravalements à déclaration</strong> par une délibération du conseil municipal. Beaucoup de communes d'Île-de-France l'ont fait.</li>
</ul>
<p>Pour savoir si votre adresse est concernée, interrogez le service urbanisme de votre mairie, ou consultez le Géoportail de l'urbanisme et l'Atlas des patrimoines, qui affichent le PLU et les périmètres protégés.</p>"""),
            ("Constituer le dossier", """
<p>La déclaration se fait sur le formulaire Cerfa n° 13703 (maison individuelle et ses annexes), en mairie ou en ligne sur le guichet numérique de la commune. Pour un ravalement, on joint en général :</p>
<ul>
<li>un plan de situation du terrain dans la commune ;</li>
<li>les plans ou élévations des façades, avant et après travaux ;</li>
<li>des photos de la façade, de près et dans son environnement ;</li>
<li>une notice ou un document qui précise les matériaux, les teintes et leurs références.</li>
</ul>
<p>Nous fournissons les pièces techniques de notre ressort : descriptif des travaux, références de produits et de teintes, élévations cotées et photos.</p>"""),
            ("Les délais", """
<p>Le délai d'instruction est d'un mois à compter du dépôt d'un dossier complet. Il passe à deux mois quand l'architecte des Bâtiments de France doit donner son avis, aux abords d'un monument historique ou en site patrimonial remarquable. Sans réponse dans ce délai, la déclaration vaut en principe accord : vous pouvez demander à la mairie un certificat de non-opposition.</p>
<p>Une fois l'accord obtenu, affichez-le sur un panneau visible depuis la rue pendant toute la durée des travaux. Les voisins disposent de deux mois à compter de cet affichage pour contester. L'autorisation est valable trois ans.</p>"""),
            ("L'échafaudage sur le trottoir", """
<p>Si l'échafaudage ou une benne occupe le trottoir ou la chaussée, il faut une autorisation d'occupation du domaine public (souvent appelée permis de stationnement), demandée à la mairie ou au gestionnaire de la voirie plusieurs semaines avant le chantier. Elle est en général payante, à la journée ou au mètre carré. Nous préparons la demande avec vous.</p>"""),
            ("Ravaler sans autorisation : les risques", """
<p>Des travaux réalisés sans la déclaration requise constituent une infraction au code de l'urbanisme. La commune peut demander une remise en état ou une régularisation, et l'absence d'autorisation peut bloquer une vente ou compliquer un sinistre avec votre assurance. Le dossier prend quelques heures à préparer, c'est un bon investissement.</p>"""),
        ],
        "faq": [
            ("Faut-il une déclaration pour repeindre sa façade de la même couleur ?",
             "En général non, sauf si la maison est en secteur protégé ou si la commune impose une déclaration pour tout ravalement. Le service urbanisme de la mairie vous le confirme en quelques minutes."),
            ("Qui dépose la déclaration préalable ?",
             "Le propriétaire, ou une personne qu'il mandate. Nous préparons les pièces techniques et vous aidons à remplir le formulaire."),
            ("Peut-on commencer les travaux pendant l'instruction ?",
             "Non. Attendez la décision de non-opposition, ou la fin du délai d'instruction, puis affichez l'autorisation sur le terrain."),
        ],
    },
    {
        "slug": "choisir-couleur-facade",
        "nav": "Choisir la couleur",
        "name": "Choisir la couleur de sa façade",
        "title": "Choisir la couleur de sa façade : règles, nuanciers, conseils",
        "desc": "Choisir la couleur de façade de sa maison : règles du PLU et du lotissement, teintes claires ou foncées, échantillons, accord avec la toiture et les volets.",
        "h1": "Choisir la couleur de sa façade",
        "lead": "Une teinte de façade se choisit pour de longues années, dans les limites fixées par la commune. Ce guide vous aide à vérifier les règles, à tester les couleurs sur votre mur et à éviter les pièges des teintes trop sombres.",
        "kicker": "Couleurs et teintes",
        "tile": "salissures",
        "sections": [
            ("Essayez quelques teintes courantes", "[[nuancier]]"),
            ("D'abord, les règles de la commune", """
<p>Le règlement du PLU, dans son chapitre sur l'aspect extérieur des constructions, encadre souvent les couleurs : teintes interdites, nuancier communal, couleurs imposées pour les menuiseries. Dans un lotissement, le règlement ou le cahier des charges peut aller plus loin. En secteur protégé, l'architecte des Bâtiments de France donne son avis sur la teinte.</p>
<p>Un changement de couleur demande une <a href="/ravalement-facade-declaration-prealable/">déclaration préalable</a>. Indiquez-y la référence exacte du fabricant : c'est elle qui sera contrôlée.</p>"""),
            ("Teintes claires, teintes foncées", """
<p>Une façade foncée absorbe beaucoup plus la chaleur du soleil. Sur un enduit, et plus encore sur une isolation par l'extérieur, elle subit des écarts de température qui favorisent les fissures. Les fabricants fixent donc un niveau de clarté minimal pour leurs teintes sur isolant, et certains déconseillent les teintes très sombres sur les façades exposées au sud et à l'ouest.</p>
<p>Si vous aimez les teintes soutenues, réservez-les aux soubassements, aux encadrements ou à une partie de façade à l'ombre.</p>"""),
            ("Tester sur le mur, pas sur un écran", """
<p>Une couleur paraît toujours plus claire et plus vive sur une grande surface que sur un échantillon de quelques centimètres. Nous appliquons des échantillons d'un mètre carré environ sur deux façades d'orientation différente. Regardez-les le matin, à midi et en fin de journée, par temps clair et par temps gris, avant de décider.</p>
<p>La finition change aussi la perception : un enduit gratté paraît plus mat et plus clair qu'un enduit taloché de même teinte.</p>"""),
            ("Composer avec la maison", """
<ul>
<li><strong>La toiture</strong> : une tuile rouge s'accorde avec les tons pierre, sable et ocre clair. Une tuile brune ou une ardoise appelle des gris chauds et des beiges.</li>
<li><strong>Les menuiseries et les volets</strong> : choisissez-les en même temps que la façade, en contraste doux ou franc, mais rarement dans la même teinte.</li>
<li><strong>Les détails</strong> : encadrements, bandeaux et soubassements dans une teinte voisine plus soutenue ou plus claire structurent la façade.</li>
<li><strong>La rue</strong> : regardez les maisons voisines. Une façade qui s'accorde avec la rue vieillit mieux, et passe plus facilement en mairie.</li>
</ul>
<p>Trois teintes suffisent presque toujours : le fond, les détails, les menuiseries.</p>"""),
            ("Le cas de la meulière et de la pierre", """
<p>Une façade en meulière ou en pierre apparente ne se peint pas. On joue sur la teinte des joints à la chaux, plus ou moins claire, et sur celle des enduits des pignons. Notre page <a href="/ravalement-meuliere/">ravalement de meulière</a> détaille la méthode.</p>"""),
        ],
        "faq": [
            ("Peut-on choisir n'importe quelle couleur de façade ?",
             "Non. Le PLU, le règlement de lotissement ou l'architecte des Bâtiments de France peuvent limiter les teintes. Vérifiez auprès de la mairie avant de choisir, et déclarez tout changement de couleur."),
            ("Quelle couleur de façade vieillit le mieux ?",
             "Les teintes moyennes, ni très claires ni très foncées (tons pierre, sable, gris chauds), marquent moins les salissures que le blanc pur et se décolorent moins que les teintes sombres."),
            ("Peut-on garder la couleur d'origine d'un enduit monocouche ?",
             "Oui : un nettoyage suivi d'un traitement suffit souvent à lui rendre sa teinte. Sinon, une peinture adaptée peut reprendre une teinte proche."),
        ],
    },
]

GUIDE_BY_SLUG = {g["slug"]: g for g in GUIDES}

# Teintes de démonstration (noms génériques, pas des références de fabricant)
SWATCHES = [
    ("Blanc cassé", "#ece7dd"),
    ("Ton pierre", "#d8cbb3"),
    ("Sable", "#d4bf98"),
    ("Beige rosé", "#d8bfab"),
    ("Ocre clair", "#d6b27a"),
    ("Gris perle", "#cfcdc6"),
    ("Gris chaud", "#b4aa9e"),
    ("Taupe", "#9a8778"),
]

CONSEILS_INTRO = "Prix, démarches, couleurs, choix des matériaux : nos guides pour préparer votre ravalement et comparer les devis en connaissance de cause."

ZONES_INTRO = "Nous intervenons dans un rayon de 50 km autour de Mitry-Mory, sur le nord et l'ouest de la Seine-et-Marne, l'est de la Seine-Saint-Denis, l'est du Val-d'Oise, les bords de Marne du Val-de-Marne et le sud de l'Oise. Chaque commune a sa page, avec les façades qu'on y rencontre et les démarches à prévoir."
