# -*- coding: utf-8 -*-
"""Les 12 pages prestations (9 façade, 3 toiture).

Champs :
  slug, cat ("facade" ou "toiture"), nav (menu), name, title (balise title), desc (meta description),
  h1, lead, price (clé de PRICES ou ROOF_PRICES), tile (texture de l'illustration), photo (clé photos.json),
  points (3 points clés), sections [(h2, html)], faq [(question, réponse)], related [slugs].
Jetons remplacés par build.py dans les sections : [[prix]], [[prix-toiture]], [[etapes]].
"""

SERVICES = [
    # ------------------------------------------------------------------ RAVALEMENT
    {
        "slug": "ravalement-facade",
        "cat": "facade",
        "nav": "Ravalement complet",
        "name": "Ravalement de façade",
        "title": "Ravalement de façade de maison : étapes, techniques, prix",
        "desc": "Ravalement de façade de maison à Mitry-Mory et 50 km autour : diagnostic gratuit, nettoyage, réparations, enduit ou peinture. Devis détaillé sous 48 h.",
        "h1": "Ravalement de façade de maison, du diagnostic à la finition",
        "lead": "Un ravalement, c'est nettoyer, réparer et protéger les murs extérieurs de votre maison. Nous partons toujours de l'état réel de la façade : certaines ont seulement besoin d'un nettoyage, d'autres d'un enduit neuf.",
        "price": "peinture",
        "tile": "salissures",
        "photo": "ravalement-apres",
        "points": [
            "Diagnostic gratuit sur place, devis poste par poste sous 48 h",
            "Enduits, peintures et revêtements adaptés à chaque support",
            "Toiture et gouttières reprises sur le même échafaudage si besoin",
        ],
        "sections": [
            ("Ce que comprend un ravalement", """
<p>Le mot recouvre plusieurs travaux, qu'on combine selon l'état du mur. Un ravalement complet suit presque toujours le même ordre :</p>
<ul>
<li><strong>Nettoyer</strong> : enlever mousses, algues et pollution, à basse pression ou par hydrogommage selon le support.</li>
<li><strong>Réparer</strong> : piocher l'enduit qui sonne creux, ouvrir et traiter les fissures, reprendre les angles, appuis et encadrements abîmés.</li>
<li><strong>Protéger</strong> : appliquer la finition qui empêche l'eau d'entrer, qu'il s'agisse d'une peinture, d'un revêtement d'imperméabilité, d'un enduit neuf ou d'un hydrofuge incolore.</li>
<li><strong>Embellir</strong> : choisir une teinte et un aspect, en accord avec les règles de la commune.</li>
</ul>
<p>On peut s'arrêter à la première étape si l'enduit est sain. Inversement, une façade très dégradée demande un enduit neuf, et c'est souvent l'occasion de l'isoler par l'extérieur.</p>"""),
            ("Le bon traitement selon votre mur", """
<p>Le support décide de la méthode. Mettre un produit étanche et fermé sur un mur ancien qui a besoin de respirer est l'erreur la plus fréquente, et la plus coûteuse quelques années plus tard.</p>
<table class="tbl">
<thead><tr><th scope="col">Votre façade</th><th scope="col">Ce qu'on fait le plus souvent</th></tr></thead>
<tbody>
<tr><td>Enduit monocouche des années 1980 à 2010, sale mais sain</td><td>Nettoyage, traitement anti-mousse, éventuellement peinture ou hydrofuge</td></tr>
<tr><td>Enduit ciment faïencé</td><td>Revêtement d'imperméabilité souple qui ponte les microfissures</td></tr>
<tr><td>Enduit qui sonne creux ou tombe</td><td>Piochage des zones creuses puis enduit neuf, monocouche ou traditionnel</td></tr>
<tr><td>Meulière, moellons, pierre calcaire</td><td>Nettoyage doux, rejointoiement et enduits à la chaux, jamais de ciment</td></tr>
<tr><td>Brique apparente</td><td>Hydrogommage, remplacement des briques éclatées, joints refaits</td></tr>
<tr><td>Parpaing ou béton nu, murs froids</td><td>Isolation par l'extérieur avec enduit de finition ou bardage</td></tr>
</tbody>
</table>"""),
            ("Comment se déroule votre chantier", "[[etapes]]"),
            ("Ravalement et isolation : la règle à connaître", """
<p>Depuis 2017, quand on refait l'enduit ou le parement de plus de la moitié d'un mur (ouvertures déduites), la réglementation thermique impose en principe d'isoler ce mur en même temps. La règle vise les murs en béton, en parpaing ou en brique industrielle. Les murs anciens en pierre ou en meulière en sont exclus.</p>
<p>Il existe des exceptions : risque technique pour le bâti, contrainte d'urbanisme ou de patrimoine, ou coût disproportionné, quand l'isolation mettrait plus de dix ans à être remboursée par les économies d'énergie. Lors de la visite, nous vous disons si votre projet est concerné et ce que l'isolation changerait au budget.</p>"""),
            ("Un ravalement est-il obligatoire ?", """
<p>Le Code de la construction et de l'habitation demande que les façades soient tenues en bon état de propreté. Dans les communes inscrites sur une liste fixée par le préfet, le maire peut imposer au propriétaire un ravalement au moins tous les dix ans, avec un délai pour s'exécuter.</p>
<p>Ailleurs, aucune fréquence n'est imposée, mais un enduit qui laisse entrer l'eau abîme le mur, puis l'intérieur. Un ravalement fait à temps coûte bien moins qu'une reprise complète d'enduit.</p>"""),
            ("Combien coûte un ravalement de façade ?", "[[prix]]"),
            ("Les démarches avant les travaux", """
<p>Un ravalement à l'identique, sans changer la teinte ni l'aspect, ne demande en général aucune autorisation. Une <a href="/ravalement-facade-declaration-prealable/">déclaration préalable</a> devient obligatoire si vous changez la couleur ou le matériau, si la maison est en secteur protégé ou si la commune a décidé de soumettre tous les ravalements à déclaration. Si l'échafaudage empiète sur le trottoir, il faut aussi une autorisation d'occupation du domaine public, demandée à la mairie.</p>
<p>Nous préparons les pièces techniques : descriptif des travaux, références de teinte, photos et plans de façade.</p>"""),
        ],
        "faq": [
            ("Combien de temps dure un ravalement de pavillon ?",
             "Comptez en général une à trois semaines sur place pour une maison individuelle, selon la surface, l'état de l'enduit et la météo. Les enduits et peintures ne s'appliquent ni sous la pluie, ni par gel, ni en plein soleil sur un mur brûlant."),
            ("Quelle est la meilleure saison pour ravaler ?",
             "Du printemps à l'automne, quand les températures restent entre 5 et 30 °C environ. Nous planifions les finitions en fonction des prévisions et décalons d'un jour ou deux plutôt que de travailler par mauvais temps."),
            ("Faut-il être présent pendant les travaux ?",
             "Non. Nous avons besoin d'un accès au jardin, à un point d'eau et à une prise électrique. Les menuiseries sont protégées : vous pouvez continuer à vivre normalement dans la maison."),
            ("Et si l'échafaudage doit passer chez le voisin ?",
             "Il faut son accord, de préférence écrit, avec les dates et la durée. Nous pouvons vous aider à préparer ce courrier et à organiser le montage pour limiter la gêne."),
            ("Quel taux de TVA pour un ravalement ?",
             "Pour une maison achevée depuis plus de deux ans, la TVA est de 10 % sur les travaux d'entretien et d'amélioration. Elle passe à 5,5 % pour l'isolation par l'extérieur qui respecte les critères de performance fixés par la loi."),
        ],
        "related": ["nettoyage-facade", "enduit-facade", "peinture-facade", "traitement-fissures-facade", "isolation-thermique-exterieure"],
    },
    # ------------------------------------------------------------------ ENDUIT
    {
        "slug": "enduit-facade",
        "cat": "facade",
        "nav": "Enduit de façade",
        "name": "Enduit de façade",
        "title": "Enduit de façade : monocouche, chaux, traditionnel (77)",
        "desc": "Enduit de façade neuf ou en reprise autour de Mitry-Mory : monocouche, traditionnel trois couches ou chaux, finition grattée, talochée ou écrasée. Devis gratuit.",
        "h1": "Enduit de façade : monocouche, traditionnel ou à la chaux",
        "lead": "Quand l'enduit sonne creux, tombe par plaques ou n'arrête plus l'eau, la peinture ne suffit plus. On refait un enduit neuf, choisi selon le mur qui le porte.",
        "price": "enduit",
        "tile": "creux",
        "photo": "carte-enduit",
        "points": [
            "Sondage de l'ancien enduit et piochage des zones creuses",
            "Monocouche, trois couches traditionnelles ou chaux selon le support",
            "Finitions grattée, talochée, écrasée, lissée ou projetée",
        ],
        "sections": [
            ("Trois familles d'enduits, trois usages", """
<h3>L'enduit monocouche</h3>
<p>C'est l'enduit le plus posé sur les maisons récentes. Teinté dans la masse et projeté à la machine, il assure en une seule application, faite en deux passes, l'imperméabilisation et la décoration du mur. Il convient au parpaing, à la brique creuse et au béton, mais pas aux murs anciens.</p>
<h3>L'enduit traditionnel en trois couches</h3>
<p>Un gobetis d'accrochage, un corps d'enduit qui dresse le mur, puis une couche de finition. Plus long à poser, il rattrape les murs irréguliers et permet des finitions plus fines. C'est la technique de référence pour reprendre une façade très abîmée.</p>
<h3>L'enduit à la chaux</h3>
<p>Indispensable sur la meulière, les moellons de calcaire et les maisons anciennes : la chaux laisse passer la vapeur d'eau, ce qui évite d'enfermer l'humidité dans le mur. Elle donne aussi ces teintes douces et légèrement nuancées qu'on ne retrouve pas avec le ciment.</p>"""),
            ("Choisir la finition", """
<ul>
<li><strong>Grattée</strong> : la plus courante. L'enduit est gratté quelques heures après la pose, ce qui donne un aspect mat et régulier qui vieillit bien.</li>
<li><strong>Talochée</strong> : un aspect plus lisse, légèrement ondulé, fréquent sur les maisons de bourg.</li>
<li><strong>Écrasée</strong> : des reliefs aplatis à la lisseuse, pour une façade plus marquée.</li>
<li><strong>Projetée ou rustique</strong> : un relief granuleux qui masque bien les défauts du support.</li>
<li><strong>Lissée</strong> : réservée aux encadrements, bandeaux et soubassements, elle souligne les détails de la façade.</li>
</ul>
<p>Les reliefs prononcés retiennent davantage la poussière. Sur une façade exposée aux arbres ou à une route passante, nous conseillons plutôt une finition grattée ou talochée.</p>"""),
            ("Quand faut-il refaire l'enduit ?", """
<p>Nous sondons l'enduit au marteau sur toute la façade. Il faut le refaire quand :</p>
<ul>
<li>de larges zones sonnent creux, signe que l'enduit n'adhère plus au mur ;</li>
<li>des plaques sont déjà tombées, souvent en bas des murs et aux angles ;</li>
<li>les fissures sont nombreuses et dépassent le simple faïençage ;</li>
<li>le mur est nu ou recouvert de couches successives de peinture qui cloquent.</li>
</ul>
<p>Si l'ancien enduit est sain et bien accroché, un nouvel enduit peut parfois être posé par-dessus, après nettoyage et application d'un primaire d'accrochage. Nous ne le faisons qu'après sondage.</p>"""),
            ("Notre méthode de pose", """
<p>Le support est piqué jusqu'au sain, brossé et humidifié. Aux jonctions de matériaux différents (parpaing et béton, brique et bois), nous posons une armature qui limite les fissures. Les angles reçoivent des baguettes et les ouvertures des joints adaptés.</p>
<p>Chaque couche respecte le temps de séchage prévu par le fabricant. Nous ne posons pas par temps de gel, de forte chaleur ou de pluie, et nous protégeons la façade du soleil direct et du vent pendant la prise.</p>"""),
            ("Prix d'un enduit de façade", "[[prix]]"),
        ],
        "faq": [
            ("Peut-on poser un enduit sur un ancien enduit ?",
             "Oui, si l'ancien enduit est sain, propre et bien accroché, avec un primaire d'accrochage. S'il sonne creux par endroits, ces zones sont piochées et rebouchées avant la pose."),
            ("Monocouche ou chaux, comment choisir ?",
             "Tout dépend du mur. Le monocouche convient au parpaing, à la brique creuse et au béton. La chaux s'impose sur la meulière, les moellons et la pierre, qui doivent pouvoir sécher."),
            ("Faut-il peindre un enduit neuf ?",
             "Non : un enduit monocouche ou à la chaux est déjà teinté dans la masse. Si vous souhaitez une peinture plus tard, il faut attendre que l'enduit ait séché à cœur, soit au moins un mois."),
            ("L'enduit va-t-il changer de couleur ?",
             "Un enduit teinté prend légèrement de l'éclat en séchant et peut présenter de petites nuances, surtout à la chaux. Nous vous montrons des échantillons sur votre mur avant de lancer la façade entière."),
        ],
        "related": ["ravalement-facade", "traitement-fissures-facade", "ravalement-meuliere", "isolation-thermique-exterieure"],
    },
    # ------------------------------------------------------------------ PEINTURE
    {
        "slug": "peinture-facade",
        "cat": "facade",
        "nav": "Peinture de façade",
        "name": "Peinture de façade",
        "title": "Peinture de façade de maison autour de Mitry-Mory (77)",
        "desc": "Peinture de façade sur enduit sain : préparation, fixateur, deux couches de peinture acrylique, siloxane, pliolite ou silicate. Devis gratuit à 50 km de Mitry-Mory.",
        "h1": "Peinture de façade : redonner de la couleur à un enduit sain",
        "lead": "Quand l'enduit adhère encore bien au mur, une peinture de façade suffit pour le protéger et lui redonner de l'éclat. Le résultat dépend surtout de la préparation et du bon choix de peinture.",
        "price": "peinture",
        "tile": "faiencage",
        "photo": "carte-peinture",
        "points": [
            "Nettoyage, rebouchage et fixateur avant toute peinture",
            "Peinture choisie selon le support : acrylique, siloxane, pliolite ou silicate",
            "Deux couches de finition, teinte validée sur échantillon",
        ],
        "sections": [
            ("Quand une peinture suffit", """
<p>La peinture convient à un enduit sain et bien accroché, qui a seulement terni, s'est sali ou présente un léger faïençage. Si l'enduit sonne creux par endroits, si des fissures traversent le mur ou si l'eau entre déjà, il faut passer par une <a href="/traitement-fissures-facade/">réparation des fissures</a>, un <a href="/impermeabilisation-facade/">revêtement d'imperméabilité</a> ou un <a href="/enduit-facade/">enduit neuf</a>.</p>"""),
            ("Les peintures que nous utilisons", """
<ul>
<li><strong>Acrylique en phase aqueuse</strong> : polyvalente, peu odorante, avec un large choix de teintes. C'est le standard pour un enduit ciment ou monocouche.</li>
<li><strong>Siloxane</strong> : elle fait perler l'eau tout en laissant le mur respirer. C'est un bon choix pour une façade exposée à la pluie ou à l'ombre.</li>
<li><strong>Pliolite</strong> : une peinture en phase solvant qui s'applique par temps frais et humide. Elle est utile en début ou en fin de saison.</li>
<li><strong>Silicate</strong> : une peinture minérale qui fait corps avec le support. C'est elle qu'il faut sur un enduit à la chaux ou une façade ancienne.</li>
</ul>
<p>Les peintures de façade sont classées selon leur épaisseur. Une peinture semi-épaisse (classe D3) masque mieux les petits défauts qu'une peinture en film mince (D2).</p>"""),
            ("La préparation, l'essentiel du travail", """
<p>Une peinture sur une façade mal préparée cloque ou s'écaille au bout de deux hivers. Avant de peindre, nous :</p>
<ul>
<li>nettoyons la façade et traitons mousses et algues ;</li>
<li>grattons les anciennes peintures qui n'adhèrent plus ;</li>
<li>ouvrons et rebouchons les fissures, reprenons les éclats d'enduit ;</li>
<li>appliquons un fixateur ou une impression adaptée au support ;</li>
<li>protégeons menuiseries, sols, toitures basses et plantations.</li>
</ul>
<p>Viennent ensuite deux couches de finition, au rouleau ou à la machine, avec les temps de séchage prévus par le fabricant.</p>"""),
            ("Choisir la teinte", """
<p>Le PLU de votre commune ou le règlement de lotissement limite souvent les teintes possibles. Nous vous présentons les nuanciers des fabricants et appliquons des échantillons sur votre façade, car une couleur ne rend pas pareil sur un carton et sur un mur exposé au sud. Notre <a href="/choisir-couleur-facade/">guide pour choisir la couleur de façade</a> détaille les points à vérifier.</p>"""),
            ("Prix d'une peinture de façade", "[[prix]]"),
        ],
        "faq": [
            ("Combien de couches faut-il ?",
             "Une impression ou un fixateur, puis deux couches de finition. Une seule couche ne donne ni la teinte annoncée ni l'épaisseur qui protège le mur."),
            ("Combien de temps tient une peinture de façade ?",
             "Une dizaine d'années en moyenne, davantage sur une façade abritée et bien préparée, moins sur un mur plein ouest ou sous les arbres."),
            ("Peut-on peindre un enduit monocouche ?",
             "Oui, avec une peinture adaptée, après nettoyage et contrôle de l'adhérence. Un monocouche simplement encrassé peut aussi être nettoyé sans être peint : il retrouve sa teinte d'origine."),
            ("Peut-on peindre une façade en meulière ?",
             "Nous le déconseillons : la meulière doit rester apparente et respirer. Une peinture fermée y enferme l'humidité. Nous privilégions le nettoyage et le rejointoiement."),
        ],
        "related": ["nettoyage-facade", "impermeabilisation-facade", "ravalement-facade", "enduit-facade"],
    },
    # ------------------------------------------------------------------ NETTOYAGE
    {
        "slug": "nettoyage-facade",
        "cat": "facade",
        "nav": "Nettoyage de façade",
        "name": "Nettoyage de façade",
        "title": "Nettoyage et démoussage de façade (77, 93, 95)",
        "desc": "Nettoyage de façade à basse pression ou par hydrogommage, traitement anti-mousse et hydrofuge. Mitry-Mory, Seine-et-Marne, Seine-Saint-Denis, Val-d'Oise.",
        "h1": "Nettoyage de façade et traitement anti-mousse",
        "lead": "Traces vertes au nord, coulures noires sous les fenêtres, voile gris de pollution : la plupart des façades sales ont un enduit encore sain. Un nettoyage bien conduit leur rend leur teinte d'origine.",
        "price": "nettoyage",
        "tile": "salissures",
        "photo": "carte-nettoyage",
        "points": [
            "Méthode choisie selon le support : basse pression ou hydrogommage",
            "Traitement anti-mousse et algicide laissé à agir",
            "Hydrofuge incolore en option pour garder la façade propre plus longtemps",
        ],
        "sections": [
            ("Ce qui salit une façade", """
<ul>
<li><strong>Algues et mousses</strong> : taches vertes, puis noires en vieillissant. On les trouve au nord, en bas des murs et près des arbres.</li>
<li><strong>Lichens</strong> : petites plaques grises ou orangées, très accrochées, surtout sur la pierre.</li>
<li><strong>Pollution</strong> : un voile gris uniforme, plus marqué le long des routes passantes.</li>
<li><strong>Coulures</strong> : traînées noires sous les appuis de fenêtre et les gouttières qui débordent.</li>
<li><strong>Efflorescences</strong> : dépôts blancs de sels, signe que l'eau traverse le mur.</li>
</ul>
<p>Les coulures et les efflorescences ont une cause : un appui sans goutte d'eau, une gouttière qui déborde, une remontée d'humidité. Nous la traitons aussi, sinon la trace revient en un hiver.</p>"""),
            ("Nos méthodes de nettoyage", """
<h3>Lavage à basse pression</h3>
<p>De l'eau, parfois chaude, à pression maîtrisée, après application d'un produit nettoyant. C'est la méthode adaptée à la plupart des enduits ciment et monocouches.</p>
<h3>Hydrogommage</h3>
<p>De l'eau et un granulat très fin projetés à basse pression. La méthode décrasse la pierre, la meulière et la brique sans les attaquer ni creuser les joints.</p>
<h3>Traitement anti-mousse et algicide</h3>
<p>Pulvérisé sur la façade et laissé agir plusieurs jours, il détruit les spores jusque dans les pores de l'enduit. Sans lui, les traces vertes reviennent bien plus vite.</p>
<p>Nous n'utilisons jamais de nettoyeur haute pression sur un enduit à la chaux, une pierre tendre ou un vieux joint : il arrache la surface et ouvre la porte à l'eau.</p>"""),
            ("Protéger après le nettoyage", """
<p>Un hydrofuge incolore appliqué sur une façade propre et sèche fait perler la pluie sans changer l'aspect du mur. Il ralentit le retour des mousses et des salissures. Il reste perméable à la vapeur d'eau : le mur continue de sécher normalement.</p>"""),
            ("Quand le nettoyage ne suffit plus", """
<p>Si la façade est faïencée, si l'enduit sonne creux ou si la teinte d'origine est passée, le nettoyage devient la première étape d'un <a href="/ravalement-facade/">ravalement</a> plus complet : <a href="/peinture-facade/">peinture</a>, <a href="/impermeabilisation-facade/">imperméabilisation</a> ou <a href="/enduit-facade/">enduit neuf</a>. Le diagnostic gratuit sert à trancher.</p>"""),
            ("Prix d'un nettoyage de façade", "[[prix]]"),
        ],
        "faq": [
            ("Peut-on nettoyer une façade au nettoyeur haute pression ?",
             "Sur un enduit ciment très dur, à distance et avec une buse adaptée, parfois. Sur un monocouche, un enduit à la chaux, de la pierre ou de vieux joints, c'est à éviter : la surface s'arrache et le mur devient plus poreux qu'avant."),
            ("Combien de temps la façade reste-t-elle propre ?",
             "Cela dépend de l'exposition, des arbres et de la circulation. Avec un traitement anti-mousse puis un hydrofuge, on gagne plusieurs années sur une façade nettoyée simplement à l'eau."),
            ("Faut-il un échafaudage pour un nettoyage ?",
             "Pour le rez-de-chaussée, on peut travailler depuis le sol avec une perche. Pour l'étage et les pignons, il faut un échafaudage ou une nacelle, à la fois pour la sécurité et pour un résultat régulier."),
        ],
        "related": ["peinture-facade", "impermeabilisation-facade", "demoussage-toiture", "ravalement-facade"],
    },
    # ------------------------------------------------------------------ FISSURES
    {
        "slug": "traitement-fissures-facade",
        "cat": "facade",
        "nav": "Traitement des fissures",
        "name": "Traitement des fissures",
        "title": "Traitement des fissures de façade : diagnostic et réparation",
        "desc": "Fissures de façade autour de Mitry-Mory : mesure, diagnostic de la cause, ouverture, pontage armé et revêtement. Microfissures, fissures et lézardes.",
        "h1": "Traitement des fissures de façade",
        "lead": "Toutes les fissures ne se valent pas. Un faïençage léger se traite en même temps que la peinture, alors qu'une lézarde qui s'élargit demande d'abord d'en trouver la cause. Nous commençons toujours par mesurer.",
        "price": "impermeabilisation",
        "tile": "fissure",
        "photo": "carte-fissures",
        "points": [
            "Mesure, relevé et suivi des fissures avant tout chiffrage",
            "Ouverture, traitement et pontage armé des fissures actives",
            "Avis franc quand une fissure relève d'abord d'une étude de structure",
        ],
        "sections": [
            ("Reconnaître le type de fissure", """
<table class="tbl">
<thead><tr><th scope="col">Type</th><th scope="col">Largeur</th><th scope="col">Ce que ça signifie</th></tr></thead>
<tbody>
<tr><td>Microfissure, faïençage</td><td>moins de 0,2 mm</td><td>Vieillissement de l'enduit, en surface. Elle laisse entrer l'eau mais ne menace pas le mur.</td></tr>
<tr><td>Fissure</td><td>de 0,2 à 2 mm</td><td>Retrait, dilatation, jonction de matériaux. À traiter avant qu'elle ne s'ouvre davantage.</td></tr>
<tr><td>Lézarde</td><td>plus de 2 mm</td><td>Elle traverse souvent le mur. Il faut en chercher la cause avant de reboucher.</td></tr>
</tbody>
</table>
<p>La direction compte autant que la largeur. Une fissure horizontale suit souvent un plancher ou un chaînage. Une fissure en biais à l'angle d'une fenêtre signale un linteau. Une fissure en escalier dans les joints peut trahir un mouvement des fondations.</p>"""),
            ("D'où viennent les fissures", """
<ul>
<li><strong>Le retrait</strong> de l'enduit ou du mortier pendant son séchage, surtout s'il a été posé par forte chaleur.</li>
<li><strong>La dilatation</strong> des matériaux entre l'été et l'hiver, plus forte sur une façade sombre exposée au sud.</li>
<li><strong>Les jonctions</strong> entre matériaux qui ne bougent pas de la même façon : parpaing et béton, extension et maison d'origine.</li>
<li><strong>Un linteau ou une armature qui rouille</strong> et fait éclater le béton autour.</li>
<li><strong>Les mouvements du sol</strong>, notamment le retrait et le gonflement des argiles après les étés secs. Une partie de l'est francilien y est exposée. Vous pouvez vérifier votre adresse sur le site Géorisques.</li>
</ul>"""),
            ("Notre traitement", """
<p>Pour une fissure stabilisée de moins de 2 mm, nous :</p>
<ul>
<li>ouvrons la fissure en V pour atteindre le support sain ;</li>
<li>la dépoussiérons et appliquons un primaire ;</li>
<li>la garnissons d'un mastic ou d'un mortier souple adapté ;</li>
<li>posons une bande d'armature qui répartit les mouvements ;</li>
<li>recouvrons d'un revêtement qui ponte les fissures sur toute la façade, pour que la réparation ne reste pas visible.</li>
</ul>
<p>Pour une lézarde active, reboucher ne sert à rien : elle se rouvrira. Nous vous le disons franchement, et nous vous orientons vers une étude de structure avant tout ravalement.</p>"""),
            ("Surveiller une fissure", """
<p>Pour savoir si une fissure bouge, collez un témoin en travers (une jauge de fissure ou une simple bande de plâtre datée) et photographiez-la chaque mois avec une règle à côté. Si le témoin casse ou si la fissure s'élargit, signalez-le-nous avant d'engager les travaux.</p>"""),
            ("Fissures, assurances et catastrophe naturelle", """
<p>Si votre maison a moins de dix ans, une fissure importante peut relever de la garantie décennale du constructeur : contactez-le avant tout. Si votre commune a été reconnue en état de catastrophe naturelle pour la sécheresse, déclarez le sinistre à votre assureur habitation dans les 30 jours qui suivent la publication de l'arrêté au Journal officiel.</p>"""),
            ("Prix d'un traitement de fissures", "[[prix]]"),
        ],
        "faq": [
            ("Une fissure de façade est-elle grave ?",
             "Les microfissures et le faïençage ne mettent pas la maison en danger, mais ils laissent entrer l'eau. Une fissure de plus de 2 mm, traversante ou qui s'élargit, doit être examinée rapidement."),
            ("Peut-on simplement reboucher une fissure ?",
             "Un rebouchage seul se voit et se rouvre souvent. Il faut ouvrir la fissure, la traiter, l'armer puis recouvrir la façade d'un revêtement qui ponte les fissures."),
            ("Combien coûte le traitement d'une fissure ?",
             "Le traitement ponctuel est le plus souvent intégré au ravalement. Seul le diagnostic sur place permet de le chiffrer : longueur, largeur, accès, et revêtement de finition."),
        ],
        "related": ["impermeabilisation-facade", "enduit-facade", "ravalement-facade", "peinture-facade"],
    },
    # ------------------------------------------------------------------ IMPERMÉABILISATION
    {
        "slug": "impermeabilisation-facade",
        "cat": "facade",
        "nav": "Imperméabilisation",
        "name": "Imperméabilisation de façade",
        "title": "Imperméabilisation de façade : revêtements I1 à I4 et hydrofuge",
        "desc": "Imperméabilisation de façade faïencée ou exposée à la pluie : revêtements d'imperméabilité I1 à I4 ou hydrofuge incolore. Devis gratuit autour de Mitry-Mory.",
        "h1": "Imperméabilisation de façade",
        "lead": "Un enduit faïencé ou poreux laisse passer la pluie, et l'humidité finit par se voir à l'intérieur. Un revêtement d'imperméabilité ferme le mur à l'eau tout en le laissant respirer.",
        "price": "impermeabilisation",
        "tile": "faiencage",
        "photo": "carte-impermeabilisation",
        "points": [
            "Revêtements souples qui pontent les microfissures (classes I1 à I4)",
            "Hydrofuge incolore pour garder l'aspect de la pierre ou de l'enduit",
            "Contrôle de l'origine de l'humidité avant de fermer le mur",
        ],
        "sections": [
            ("Deux façons d'imperméabiliser", """
<h3>Le revêtement d'imperméabilité</h3>
<p>Un revêtement à base de résines, plus épais qu'une peinture, qui forme une membrane souple sur la façade. Il est classé de I1 à I4 selon sa capacité à ponter les fissures : les classes I1 et I2 conviennent aux microfissures, les classes I3 et I4, plus épaisses et souvent armées, aux fissures plus larges. Il est teinté et existe en finition lisse ou ribbée.</p>
<h3>L'hydrofuge incolore</h3>
<p>Il pénètre dans le support et fait perler l'eau sans former de film ni changer l'aspect. C'est la solution pour une pierre, une brique ou un enduit sain qu'on veut garder tel quel, mais il ne ponte aucune fissure.</p>"""),
            ("Quand imperméabiliser", """
<ul>
<li>L'enduit est faïencé sur une grande partie de la façade.</li>
<li>La façade est exposée aux pluies dominantes, à l'ouest et au sud-ouest dans notre région.</li>
<li>Des taches d'humidité apparaissent à l'intérieur, sur les murs de la façade exposée.</li>
<li>L'enduit est devenu poreux et noircit très vite après un nettoyage.</li>
</ul>"""),
            ("Notre méthode", """
<p>La façade est nettoyée et traitée contre les mousses, puis les fissures sont ouvertes et pontées. Nous appliquons ensuite un primaire, puis le revêtement en une ou plusieurs couches. Pour les systèmes les plus résistants, une armature est noyée dans la première couche.</p>
<p>L'efficacité dépend de l'épaisseur : nous respectons la consommation au mètre carré indiquée par le fabricant, et c'est elle qui figure sur le devis.</p>"""),
            ("Ne pas fermer un mur qui a besoin de sécher", """
<p>Si l'humidité vient du sol (remontées capillaires en bas des murs, salpêtre), un revêtement étanche l'empêche de s'évacuer et aggrave le problème. Nous vérifions l'origine de l'humidité avant de proposer une imperméabilisation. Sur les murs anciens en meulière ou en pierre, nous restons sur des solutions perméables à la vapeur d'eau.</p>"""),
            ("Prix d'une imperméabilisation", "[[prix]]"),
        ],
        "faq": [
            ("Quelle différence entre imperméabilisation et hydrofuge ?",
             "Le revêtement d'imperméabilité forme une membrane teintée qui ponte les fissures. L'hydrofuge est incolore, ne forme pas de film et sert à protéger un support sain sans changer son aspect."),
            ("Le mur pourra-t-il encore respirer ?",
             "Oui : les revêtements que nous posons sont imperméables à l'eau de pluie mais laissent passer la vapeur d'eau. C'est aussi pour cela qu'ils ne conviennent pas à un mur qui reçoit de l'humidité par le sol."),
            ("Peut-on choisir la couleur ?",
             "Oui, les revêtements d'imperméabilité se teintent dans de nombreuses nuances, en finition lisse ou ribbée, dans les limites fixées par le PLU de votre commune."),
        ],
        "related": ["traitement-fissures-facade", "peinture-facade", "nettoyage-facade", "ravalement-facade"],
    },
    # ------------------------------------------------------------------ MEULIÈRE
    {
        "slug": "ravalement-meuliere",
        "cat": "facade",
        "nav": "Meulière et pierre",
        "name": "Ravalement de meulière et de pierre",
        "title": "Ravalement de meulière et rejointoiement à la chaux (77, 93, 94)",
        "desc": "Rénovation de façade en meulière ou en pierre : nettoyage doux, dégarnissage, rejointoiement à la chaux, joints rocaillés ou beurrés. Est parisien et Seine-et-Marne.",
        "h1": "Ravalement de meulière et de pierre",
        "lead": "La meulière fait le caractère des villas de l'est parisien. Elle vieillit très bien, à une condition : être traitée avec des matériaux qui la laissent respirer. Pas de ciment, pas de peinture, de la chaux.",
        "price": "meuliere",
        "tile": "meuliere",
        "photo": "carte-meuliere",
        "points": [
            "Dégarnissage des joints ciment et rejointoiement à la chaux",
            "Respect de l'aspect d'origine : joints beurrés, en relief ou rocaillés",
            "Nettoyage doux par hydrogommage, décors de brique et céramique préservés",
        ],
        "sections": [
            ("La meulière, pierre de l'Île-de-France", """
<p>La meulière est une roche siliceuse, très dure, criblée de cavités, de couleur miel à rouille. On l'a extraite en abondance dans le Bassin parisien. Les bancs les plus compacts servaient à tailler des meules à grain, d'où son nom ; La Ferté-sous-Jouarre en a fait sa spécialité. Les morceaux plus irréguliers ont bâti des milliers de pavillons et de villas, de la fin du XIXe siècle aux années 1930, du Perreux au Raincy et de Chelles à Villemomble.</p>
<p>Ces murs étaient montés et jointoyés à la chaux. C'est elle qui laisse le mur sécher entre deux pluies.</p>"""),
            ("Pourquoi les joints lâchent", """
<p>Beaucoup de façades en meulière ont été rejointoyées au ciment dans les années 1960 à 1990. Plus dur et moins perméable que la pierre, le ciment se fissure, se décolle et piège l'humidité dans le mur. On le voit aux joints qui sonnent creux ou tombent, aux taches d'humidité à l'intérieur et aux enduits intérieurs qui cloquent.</p>"""),
            ("Notre méthode", """
<ul>
<li><strong>Dégarnissage</strong> des joints abîmés ou en ciment sur 2 à 3 cm de profondeur, à la main ou au petit outillage, sans épaufrer la pierre.</li>
<li><strong>Nettoyage doux</strong> de la pierre par hydrogommage ou lavage à basse pression, et traitement des mousses et lichens.</li>
<li><strong>Remplacement</strong> des pierres éclatées ou gélives par des meulières de récupération.</li>
<li><strong>Rejointoiement</strong> au mortier de chaux naturelle, teinté pour se fondre dans l'ensemble.</li>
<li><strong>Finition des joints</strong> dans l'aspect d'origine : joints beurrés, en relief, tirés au fer ou rocaillés, avec de petits éclats de meulière.</li>
</ul>
<p>Les briques d'encadrement, les frises de céramique et les bandeaux sont nettoyés et réparés à part : ce sont eux qui font le charme de ces façades.</p>"""),
            ("Pierre calcaire et moellons enduits", """
<p>Dans les vieux bourgs de la Goële, du Multien et du Valois, les murs sont souvent en moellons de calcaire, enduits à la chaux ou laissés à pierre vue, avec des chaînes d'angle et des encadrements en pierre de taille. Nous les traitons avec la même logique : nettoyage doux, reprise des pierres au mortier de réparation, rejointoiement et enduits à la chaux, badigeons pour unifier les teintes.</p>"""),
            ("Prix d'un ravalement de meulière", "[[prix]]"),
        ],
        "faq": [
            ("Peut-on peindre une façade en meulière ?",
             "Nous le déconseillons. Une peinture fermée enferme l'humidité dans la pierre et cache ce qui fait la valeur de la maison. Si une teinte uniforme est recherchée, un badigeon de chaux reste perméable."),
            ("Faut-il un hydrofuge sur la meulière ?",
             "Ce n'est pas obligatoire. Sur une façade très exposée, un hydrofuge microporeux appliqué après le rejointoiement limite l'eau qui entre sans empêcher le mur de sécher."),
            ("Combien de temps dure un ravalement de meulière ?",
             "Comptez deux à quatre semaines pour une villa, car le dégarnissage et le rejointoiement se font en grande partie à la main."),
            ("Peut-on isoler une maison en meulière par l'extérieur ?",
             "C'est possible, mais on perd l'aspect de la pierre, et la commune s'y oppose souvent. On isole plutôt par l'intérieur, avec des isolants perméables à la vapeur d'eau, et on soigne les fenêtres et la toiture."),
        ],
        "related": ["nettoyage-facade", "enduit-facade", "ravalement-facade", "choisir-couleur-facade"],
    },
    # ------------------------------------------------------------------ ITE
    {
        "slug": "isolation-thermique-exterieure",
        "cat": "facade",
        "nav": "Isolation par l'extérieur",
        "name": "Isolation thermique par l'extérieur",
        "title": "Isolation thermique par l'extérieur (ITE) en Seine-et-Marne",
        "desc": "Isolation thermique par l'extérieur sous enduit ou bardage autour de Mitry-Mory : PSE, laine de roche, fibre de bois. Ravalement et isolation en un chantier.",
        "h1": "Isolation thermique par l'extérieur",
        "lead": "Isoler les murs par l'extérieur, c'est traiter en un seul chantier la façade et le confort de la maison : un isolant posé sur les murs, puis un enduit ou un bardage par-dessus. Vous ne perdez pas un centimètre à l'intérieur.",
        "price": "ite",
        "tile": "froid",
        "photo": "ravalement-avant",
        "points": [
            "Isolant collé et chevillé, sous-enduit armé, finition enduit ou bardage",
            "Appuis, coffres de volets, descentes et débords de toit traités",
            "Aide pour la déclaration préalable et les règles du PLU",
        ],
        "sections": [
            ("Pourquoi isoler par l'extérieur", """
<ul>
<li><strong>Aucune perte de surface habitable</strong> et pas de travaux dans les pièces : vous restez chez vous.</li>
<li><strong>Les ponts thermiques sont traités</strong> : l'isolant passe devant les planchers et les refends, là où une isolation intérieure s'interrompt.</li>
<li><strong>Les murs restent du côté chaud</strong> : ils gardent la fraîcheur en été et la chaleur en hiver.</li>
<li><strong>La façade est refaite</strong> en même temps, avec un aspect neuf.</li>
</ul>
<p>Dans une maison non isolée, les murs représentent environ un quart des pertes de chaleur. C'est le deuxième poste après la toiture.</p>"""),
            ("Le système que nous posons", """
<p>Les panneaux isolants sont collés et chevillés sur les murs. Selon le projet, nous utilisons du polystyrène expansé (blanc ou graphité), de la laine de roche ou de la fibre de bois. Viennent ensuite un sous-enduit armé d'un treillis en fibre de verre, puis un enduit de finition mince, teinté dans la masse. L'isolant peut aussi être posé entre les montants d'une ossature et recouvert d'un <a href="/bardage/">bardage</a>.</p>
<p>Pour atteindre le niveau de performance demandé par les aides et la TVA réduite (une résistance thermique d'au moins 3,7 m².K/W), il faut en général de 12 à 16 cm d'isolant selon le matériau.</p>"""),
            ("Les points qui font la qualité d'une ITE", """
<ul>
<li><strong>Les appuis de fenêtre</strong> sont prolongés pour garder un débord et une goutte d'eau.</li>
<li><strong>Les coffres de volets roulants</strong>, les gonds de volets battants et les éclairages sont déplacés ou adaptés.</li>
<li><strong>Les descentes d'eau pluviale</strong> sont déposées puis reposées sur des pattes rallongées.</li>
<li><strong>Le soubassement</strong> reçoit un isolant qui résiste à l'humidité du sol et aux chocs.</li>
<li><strong>Le débord de toit</strong> doit protéger le haut de l'isolant. Sinon, nous posons une couvertine.</li>
</ul>
<p>Si votre mur est en limite de propriété, la loi autorise sous conditions un débord d'isolation de 35 cm au plus sur le terrain voisin. La procédure passe par une information préalable du voisin.</p>"""),
            ("Ravalement et isolation : l'obligation de 2017", """
<p>Depuis 2017, un ravalement important (plus de la moitié d'un mur, ouvertures déduites) d'un mur en béton, en parpaing ou en brique industrielle doit en principe s'accompagner d'une isolation. Il existe des dérogations : impossibilité technique, contrainte de patrimoine ou d'urbanisme, ou coût disproportionné par rapport aux économies d'énergie. Nous en parlons dès la visite.</p>"""),
            ("TVA et aides", """
<p>Les travaux d'isolation des murs qui atteignent le niveau de performance réglementaire bénéficient d'une TVA à 5,5 % dans les logements de plus de deux ans. Les aides (MaPrimeRénov', certificats d'économies d'énergie) changent chaque année et exigent une entreprise certifiée RGE : vérifiez les conditions en vigueur sur france-renov.gouv.fr ou auprès d'un conseiller France Rénov' avant de signer un devis.</p>"""),
            ("Prix d'une isolation par l'extérieur", "[[prix]]"),
        ],
        "faq": [
            ("Faut-il une autorisation pour une isolation par l'extérieur ?",
             "Oui : l'isolation change l'aspect de la façade, il faut donc une déclaration préalable. Le PLU peut prévoir des règles particulières, et le code de l'urbanisme permet de déroger à certaines règles d'implantation pour isoler."),
            ("Quelle épaisseur d'isolant faut-il ?",
             "Entre 12 et 16 cm selon le matériau, pour atteindre une résistance thermique d'au moins 3,7 m².K/W. Moins épais, l'isolant reste utile mais n'ouvre pas droit à la TVA à 5,5 %."),
            ("Peut-on isoler une maison en meulière par l'extérieur ?",
             "Techniquement oui, mais on perd la pierre apparente, et beaucoup de communes s'y opposent. Pour ces maisons, on privilégie une isolation intérieure perméable à la vapeur d'eau."),
            ("Combien de temps dure le chantier ?",
             "Comptez en général trois à six semaines pour un pavillon, selon la surface, le nombre d'ouvertures et la finition retenue."),
        ],
        "related": ["bardage", "enduit-facade", "ravalement-facade", "zinguerie-gouttieres"],
    },
    # ------------------------------------------------------------------ BARDAGE
    {
        "slug": "bardage",
        "cat": "facade",
        "nav": "Bardage",
        "name": "Bardage de façade",
        "title": "Bardage de façade bois, composite, fibres-ciment (77, 93)",
        "desc": "Pose de bardage de façade bois, composite, fibres-ciment ou métal, avec ou sans isolation, sur ossature ventilée. Autour de Mitry-Mory, devis gratuit sous 48 h.",
        "h1": "Bardage de façade",
        "lead": "Un bardage habille une façade, un pignon ou une extension de lames posées sur une ossature ventilée. Il protège le mur, peut cacher un isolant et change complètement l'allure d'une maison.",
        "price": None,
        "tile": "froid",
        "photo": "carte-bardage",
        "points": [
            "Bois, composite, fibres-ciment ou métal, à lames horizontales ou verticales",
            "Ossature ventilée avec lame d'air, pare-pluie et grilles anti-rongeurs",
            "Isolation possible entre les montants de l'ossature",
        ],
        "sections": [
            ("Les matériaux", """
<ul>
<li><strong>Le bois</strong> (douglas, mélèze, red cedar, pin traité ou bois thermochauffé) : chaleureux, il grise naturellement ou se protège avec un saturateur.</li>
<li><strong>Le composite</strong> : un aspect bois, une teinte stable et presque pas d'entretien.</li>
<li><strong>Les fibres-ciment</strong> : des lames ou des panneaux très stables, incombustibles, dans de nombreuses teintes.</li>
<li><strong>Le métal</strong> (acier ou aluminium laqué) : des lignes nettes pour une extension contemporaine.</li>
</ul>
<p>Les lames se posent à l'horizontale, à la verticale ou à claire-voie. Le sens de pose change beaucoup la perception d'une façade : des lames verticales élancent une maison basse, des lames horizontales allongent un volume étroit.</p>"""),
            ("Une pose dans les règles", """
<p>Le bardage ne se pose jamais directement contre le mur. Nous fixons une ossature (tasseaux de bois ou profilés en aluminium) sur le mur. Un pare-pluie est tendu si nécessaire, et une lame d'air ventilée d'au moins 2 cm reste entre le mur et les lames. Elle évacue l'humidité. Des grilles ferment le bas et le haut contre les insectes et les rongeurs. Les angles, les tableaux de fenêtre et les jonctions avec l'enduit reçoivent des profils de finition.</p>"""),
            ("Bardage et isolation", """
<p>L'ossature peut accueillir un isolant en laine minérale ou en fibre de bois entre ses montants : c'est une <a href="/isolation-thermique-exterieure/">isolation par l'extérieur</a> sous bardage. La solution est intéressante sur un pignon exposé, une extension en parpaing ou une maison dont l'enduit est trop abîmé pour être repris.</p>"""),
            ("Entretien et durée de vie", """
<p>Un bardage composite, en fibres-ciment ou en métal se nettoie simplement à l'eau. Un bardage bois laissé brut prend une teinte grise argentée sans perdre ses qualités. Si vous voulez garder sa couleur d'origine, il faut renouveler un saturateur tous les deux à cinq ans selon l'exposition.</p>"""),
        ],
        "faq": [
            ("Faut-il une autorisation pour poser un bardage ?",
             "Oui, une déclaration préalable, puisque l'aspect de la façade change. Certains PLU limitent les matériaux ou les teintes autorisés, surtout en centre ancien."),
            ("Peut-on poser un bardage sur une partie seulement de la façade ?",
             "Oui, c'est même fréquent : un pignon, l'étage, une extension ou un soubassement. Le reste de la façade est enduit ou peint dans une teinte qui s'accorde avec le bardage."),
            ("Quel prix pour un bardage ?",
             "Le prix dépend surtout du matériau, de l'ossature et de la présence d'un isolant. Il est établi après visite et métré, poste par poste."),
        ],
        "related": ["isolation-thermique-exterieure", "ravalement-facade", "enduit-facade", "zinguerie-gouttieres"],
    },
    # ------------------------------------------------------------------ COUVERTURE
    {
        "slug": "couverture-toiture",
        "cat": "toiture",
        "nav": "Couverture et toiture",
        "name": "Couverture et toiture",
        "title": "Couvreur à Mitry-Mory : réparation et réfection de toiture",
        "desc": "Couverture et toiture autour de Mitry-Mory : tuiles, ardoise, faîtage, rives, solins, réfection complète et urgences 7 j/7. Profitez de l'échafaudage du ravalement.",
        "h1": "Couverture et toiture",
        "lead": "La toiture est notre seconde activité, et elle se marie bien avec la façade : l'échafaudage monté pour le ravalement donne un accès direct aux rives, au bas de pente et aux gouttières. On en profite pour vérifier, réparer ou refaire.",
        "price": "couverture",
        "tile": "toiture",
        "photo": "couverture-apres",
        "points": [
            "Remplacement de tuiles, faîtage, rives, solins et fenêtres de toit",
            "Réfection complète avec écran sous-toiture et liteaux neufs",
            "Urgences 7 j/7 : fuite, tuiles envolées, bâchage",
        ],
        "sections": [
            ("Profiter de l'échafaudage de la façade", """
<p>Un échafaudage est un poste important d'un chantier de toiture. Quand il est déjà monté pour le ravalement, c'est le bon moment pour faire inspecter la couverture et la zinguerie, remplacer les tuiles de rive, refaire un solin ou changer les gouttières. Faire la toiture avant la façade évite aussi de salir un enduit neuf.</p>"""),
            ("Nos travaux de couverture", """
<h3>Réparations et révision</h3>
<p>Remplacement de tuiles cassées ou glissées, reprise du faîtage (scellé au mortier ou posé à sec et ventilé), des rives et des arêtiers, réfection des solins et des abergements autour des cheminées, recherche de fuite.</p>
<h3>Réfection complète</h3>
<p>Dépose de l'ancienne couverture, contrôle de la charpente, pose d'un écran sous-toiture et de liteaux neufs, puis de tuiles neuves ou de récupération selon l'aspect recherché. Nous intervenons sur tuiles mécaniques, tuiles plates, ardoise et zinc.</p>
<h3>Fenêtres de toit</h3>
<p>Pose ou remplacement de fenêtres de toit avec leur raccord d'étanchéité.</p>"""),
            ("Urgences toiture, 7 jours sur 7", """
<p>Après un coup de vent ou un orage, nous intervenons pour mettre la maison hors d'eau : bâchage, remplacement provisoire des tuiles, dégagement des gouttières. Prenez des photos des dégâts et prévenez votre assureur. Notre devis de réparation sert à constituer le dossier.</p>"""),
            ("Notre site dédié à la toiture", """
<p>Pour un projet uniquement de toiture (charpente, couverture neuve, isolation des combles), retrouvez nos réalisations sur notre site de couvreur, <a href="https://artisandruart.fr/" rel="noopener">artisandruart.fr</a>.</p>"""),
            ("Repères de prix en toiture", "[[prix-toiture]]"),
        ],
        "faq": [
            ("Révision ou réfection : comment savoir ?",
             "Si les tuiles sont saines et que seuls quelques éléments sont abîmés, une révision suffit. Si les tuiles sont poreuses, gélives ou cassent quand on marche dessus, ou si les liteaux ont pourri, il faut une réfection. La visite permet de trancher."),
            ("Faut-il une autorisation pour refaire sa toiture ?",
             "À l'identique, en général non. Changer de matériau ou de teinte, ou poser une fenêtre de toit, demande une déclaration préalable."),
            ("Intervenez-vous le week-end ?",
             "Pour les urgences, oui : nous sommes joignables 7 jours sur 7 pour mettre la maison hors d'eau."),
        ],
        "related": ["demoussage-toiture", "zinguerie-gouttieres", "ravalement-facade"],
    },
    # ------------------------------------------------------------------ DÉMOUSSAGE
    {
        "slug": "demoussage-toiture",
        "cat": "toiture",
        "nav": "Démoussage de toiture",
        "name": "Démoussage de toiture",
        "title": "Démoussage et traitement de toiture autour de Mitry-Mory",
        "desc": "Démoussage de toiture sans haute pression : brossage, traitement anti-mousse, hydrofuge en option et nettoyage des gouttières. Seine-et-Marne, 93, 95, 94, 60.",
        "h1": "Démoussage et traitement de toiture",
        "lead": "Les mousses retiennent l'eau, soulèvent les tuiles et bouchent les gouttières. Un démoussage régulier, fait sans abîmer les tuiles, prolonge de beaucoup la vie d'une couverture.",
        "price": "demoussage",
        "tile": "toiture",
        "photo": "carte-demoussage",
        "points": [
            "Brossage et nettoyage maîtrisé, sans haute pression qui use les tuiles",
            "Traitement anti-mousse laissé à agir, hydrofuge en option",
            "Tuiles cassées remplacées et gouttières vidées dans la foulée",
        ],
        "sections": [
            ("Pourquoi démousser", """
<p>La mousse agit comme une éponge. Elle garde les tuiles humides, et quand il gèle, l'eau qu'elles contiennent les fait éclater. Elle soulève aussi les tuiles et ouvre des passages au vent et à la pluie. Enfin, elle finit dans les gouttières, qui débordent et salissent la façade.</p>"""),
            ("Notre méthode", """
<ul>
<li><strong>Brossage</strong> à la main des mousses épaisses, tuile par tuile.</li>
<li><strong>Nettoyage</strong> à pression maîtrisée, jamais à haute pression : elle décape la surface des tuiles en terre cuite et les rend plus poreuses.</li>
<li><strong>Traitement anti-mousse</strong> pulvérisé et laissé agir. La pluie et le temps achèvent le travail dans les semaines qui suivent.</li>
<li><strong>Hydrofuge</strong> en option, sur tuiles sèches, pour ralentir le retour des mousses.</li>
<li><strong>Remplacement</strong> des tuiles cassées et <strong>nettoyage des gouttières</strong> en fin de chantier.</li>
</ul>"""),
            ("Quand le faire", """
<p>Au printemps ou à l'automne, par temps sec et hors gel. Une toiture se démousse en général tous les cinq ans environ, plus souvent sous les arbres ou sur un versant nord.</p>"""),
            ("Travailler en sécurité", """
<p>Une toiture en tuiles mouillées est glissante et fragile. Nous travaillons avec harnais et points d'ancrage, ou depuis un échafaudage. Évitez de monter vous-même sur le toit : une tuile cassée en marchant suffit à provoquer une fuite.</p>"""),
            ("Repères de prix", "[[prix-toiture]]"),
        ],
        "faq": [
            ("L'hydrofuge de toiture est-il utile ?",
             "Sur des tuiles saines mais poreuses, oui : il limite l'absorption d'eau et ralentit le retour des mousses. Sur des tuiles en fin de vie, il ne fait que retarder une réfection."),
            ("Le démoussage abîme-t-il les tuiles ?",
             "Pas avec un brossage et un nettoyage à pression maîtrisée. C'est la haute pression qui les use, en arrachant leur surface."),
            ("Peut-on démousser soi-même ?",
             "Le traitement peut se pulvériser depuis une échelle sur un petit appentis. Pour une maison, le risque de chute et de casse justifie un professionnel équipé."),
        ],
        "related": ["couverture-toiture", "zinguerie-gouttieres", "nettoyage-facade"],
    },
    # ------------------------------------------------------------------ ZINGUERIE
    {
        "slug": "zinguerie-gouttieres",
        "cat": "toiture",
        "nav": "Zinguerie et gouttières",
        "name": "Zinguerie et gouttières",
        "title": "Gouttières et zinguerie : pose, réparation (77, 93, 95)",
        "desc": "Pose et réparation de gouttières zinc ou alu, descentes, chéneaux, solins et noues autour de Mitry-Mory. À faire avant le ravalement pour éviter les coulures.",
        "h1": "Zinguerie et gouttières",
        "lead": "Une gouttière qui déborde laisse des coulures noires sur la façade et mouille le pied des murs. Changer la zinguerie avant le ravalement, c'est protéger le travail neuf dès le premier orage.",
        "price": "gouttiere",
        "tile": "toiture",
        "photo": "carte-zinguerie",
        "points": [
            "Gouttières pendantes ou chéneaux, en zinc, aluminium ou cuivre",
            "Descentes, naissances, crochets, solins, noues et abergements",
            "Dépose et repose des descentes lors d'un ravalement ou d'une ITE",
        ],
        "sections": [
            ("Ce que recouvre la zinguerie", """
<ul>
<li><strong>Les gouttières</strong> pendantes (demi-rondes ou carrées) et les chéneaux, qui recueillent l'eau en bas de pente.</li>
<li><strong>Les descentes d'eaux pluviales</strong>, avec leurs naissances, coudes et colliers.</li>
<li><strong>Les solins</strong>, qui assurent l'étanchéité entre la toiture et un mur ou une cheminée.</li>
<li><strong>Les noues</strong>, à la rencontre de deux versants.</li>
<li><strong>Les abergements</strong> autour des cheminées et des fenêtres de toit.</li>
</ul>"""),
            ("Zinc, aluminium ou cuivre", """
<p>Le zinc reste la référence : durable, réparable, en finition naturelle ou prépatinée. L'aluminium laqué est façonné en continu sur place, sans raccord, dans la teinte de votre choix. Le cuivre, plus cher, convient aux maisons de caractère. Le PVC est économique mais vieillit mal au soleil, et nous le réservons aux annexes.</p>"""),
            ("Les signes qu'il faut intervenir", """
<ul>
<li>L'eau déborde par fortes pluies ou coule le long de la façade.</li>
<li>Des traînées noires ou des mousses apparaissent sous la gouttière.</li>
<li>Les joints fuient, les crochets sont tordus ou la pente est devenue insuffisante.</li>
<li>Le zinc est percé ou le chéneau retient l'eau.</li>
</ul>"""),
            ("Zinguerie et ravalement", """
<p>Lors d'un ravalement, les descentes sont déposées pour traiter le mur derrière, puis reposées. Pour une isolation par l'extérieur, elles sont reposées sur des colliers rallongés. Si la gouttière est en fin de vie, mieux vaut la changer à ce moment-là : l'échafaudage est déjà en place et la nouvelle façade reste propre.</p>"""),
            ("Repères de prix", "[[prix-toiture]]"),
        ],
        "faq": [
            ("Combien de temps dure une gouttière en zinc ?",
             "Plusieurs décennies si elle est bien posée, avec une pente régulière et des dilatations prévues, et vidée régulièrement des feuilles et des mousses."),
            ("Faut-il nettoyer ses gouttières ?",
             "Oui, au moins une fois par an, idéalement à la fin de l'automne. Nous le faisons à chaque démoussage de toiture."),
            ("Peut-on changer seulement une partie de la gouttière ?",
             "Oui, une longueur ou une descente peut être remplacée. Si plusieurs fuites apparaissent, le remplacement complet revient souvent moins cher à terme."),
        ],
        "related": ["couverture-toiture", "demoussage-toiture", "ravalement-facade", "isolation-thermique-exterieure"],
    },
]

BY_SLUG = {s["slug"]: s for s in SERVICES}
FACADE = [s for s in SERVICES if s["cat"] == "facade"]
TOITURE = [s for s in SERVICES if s["cat"] == "toiture"]
