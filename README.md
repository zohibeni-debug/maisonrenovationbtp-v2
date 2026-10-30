# maisonrenovationbtp.fr : site d'Artisan Druart, Maison Rénovation

Site du façadier et couvreur Artisan Druart, à Mitry-Mory (77). Ses pages sont en HTML complet, lisibles par Google sans JavaScript. Il est hébergé sur Cloudflare : un Worker sert les fichiers statiques et traite le formulaire de devis.

Il compte 93 pages, toutes aux mêmes adresses que sur l'ancien site :
- l'accueil ;
- 9 pages façade et 3 pages toiture ;
- la page prix, 2 guides et le sommaire des conseils ;
- la page zones et les 73 pages « Ravalement de façade à … » ;
- contact et mentions légales.

## Ce que contient ce dépôt

| Dossier / fichier | Rôle |
|---|---|
| `public/` | Le site tel qu'il est mis en ligne : pages, images, plan du site, redirections, en-têtes |
| `src/worker.js` | Le formulaire de devis (`POST /api/devis`) |
| `site/content.py` | Coordonnées, prix, diagnostic de l'accueil, FAQ, anciennes adresses à rediriger |
| `site/services.py` | Les 12 pages prestations |
| `site/guides.py` | Prix, déclaration préalable, couleur, textes des pages conseils et zones |
| `site/communes.py`, `site/communes_data.json` | Les 73 communes : données INSEE, coordonnées, textes par secteur et par commune |
| `site/art.py` | Illustrations dessinées (textures de façade) et cartes |
| `site/build.py` | Le générateur : produit `public/` |
| `site/photos.py` | Prépare les photos déposées dans `site/photos-src/` |
| `site/site.css`, `site/site.js` | Styles et scripts |
| `tools/verifier.py` | Contrôles : liens, balises, données structurées, anciennes adresses |
| `tools/visuels.py` | Image de partage et icônes |
| `wrangler.jsonc` | Configuration Cloudflare |

## Modifier le site

```bash
python3 site/photos.py      # seulement si des photos ont été ajoutées dans site/photos-src/
python3 site/build.py       # régénère public/
python3 tools/verifier.py   # doit afficher « ERREURS : 0 »
git add -A && git commit -m "…" && git push   # Cloudflare redéploie tout seul
```

Ne renommez pas les adresses des pages : ce sont celles que Google connaît déjà.

## Brancher Cloudflare (une seule fois)

Dans Cloudflare : **Compute**, puis **Workers & Pages**, puis **Create application**. Choisissez **Import a repository** (GitHub) et sélectionnez `zohibeni-debug/maisonrenovationbtp-v2`. Ne passez pas par l'onglet Pages.

Réglez ensuite :
- **Project name** : `maisonrenovationbtp-v2`, exactement comme le `name` de `wrangler.jsonc` ;
- **Build command** : laisser vide ;
- **Deploy command** : `npx wrangler deploy`.

Le site apparaît d'abord sur une adresse provisoire en `.workers.dev`. Celle-ci n'est pas indexée par Google, grâce à l'en-tête `X-Robots-Tag: noindex` défini dans `public/_headers`.

## Formulaire de devis

Les demandes partent par email à `maison.renovationbtp@gmail.com` (valeur par défaut). Deux modes d'envoi sont prévus :

1. **Cloudflare Email Service** (binding `EMAIL`) : ajoutez le domaine dans **Compute > Email Service > Email Sending > Onboard Domain**, une fois `maisonrenovationbtp.fr` géré par Cloudflare.
2. **Resend**, en secours : ajoutez le secret `RESEND_API_KEY`.

Réglages facultatifs (**Settings > Variables and Secrets**) :

| Nom | Type | Rôle |
|---|---|---|
| `DEVIS_TO` | Text | Destinataires, séparés par des virgules (ex. l'artisan et ALLOSITEWEB en copie) |
| `DEVIS_FROM` | Text | Expéditeur, ex. `Site Maison Rénovation <devis@maisonrenovationbtp.fr>` |
| `RESEND_API_KEY` | Secret | Clé API Resend (envoi de secours) |

Tant qu'aucun envoi ne fonctionne, le formulaire propose au visiteur d'envoyer sa demande par WhatsApp ou par SMS au 06 20 14 69 91. Aucune demande n'est perdue.

## Bascule du nom de domaine

1. Ajoutez `maisonrenovationbtp.fr` dans Cloudflare (formule Free). Vérifiez que les enregistrements email (MX, SPF, DKIM) ont bien été repris.
2. Chez le registrar, remplacez les serveurs DNS par ceux indiqués par Cloudflare.
3. Supprimez les enregistrements A, AAAA ou CNAME qui pointent vers l'ancien hébergement.
4. Dans **Workers & Pages > maisonrenovationbtp-v2 > Settings > Domains & Routes**, cliquez sur **Add**, puis **Custom domain**, et entrez `maisonrenovationbtp.fr`.
5. Pour le `www`, ajoutez un enregistrement A `www` → `192.0.2.0` (nuage orange), puis la règle **Redirect from WWW to root** dans **Rules > Redirect Rules**. Le site est déclaré sans `www`.
6. Dans la Search Console, soumettez `https://maisonrenovationbtp.fr/sitemap.xml`.

## À confirmer avec le client

Ces points sont dans `site/content.py`. Les champs vides ne s'affichent pas.

- `A_CONFIRMER` : SIRET, forme juridique, directeur de la publication, assureur décennale, médiateur de la consommation. Ils sont obligatoires dans les mentions légales d'un artisan.
- `ROOF_PRICES` : les repères de prix toiture. Ce sont des fourchettes de marché, à faire valider.
- `BUSINESS` : la note et le nombre d'avis Google, à mettre à jour de temps en temps.

## Photos

Sans photo, le site utilise ses illustrations dessinées. Pour ajouter les photos de l'ancien site, déposez-les dans `site/photos-src/` en gardant leur nom d'origine. Par exemple :
- `assets/img/ravalement-avant-1400.jpg` ;
- `assets/img/carte-enduit-8d38b9a8.jpg` ;
- `assets/logo-artisan-druart-2ea109d7.png`.

Lancez ensuite `site/photos.py` puis `site/build.py`. Les photos sont alors converties en WebP et placées dans les pages. Le logo remplace le pictogramme, et les blocs avant/après de l'accueil apparaissent. Chaque fichier d'origine est aussi recopié à son ancienne adresse.
