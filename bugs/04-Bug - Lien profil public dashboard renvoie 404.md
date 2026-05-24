| Champ | Valeur |
| --- | --- |
| statut | A faire |
| categorie | FrontEnd |
| priorite | P1 |
| source | Playwright MCP Windows - User 1 |
| url | https://test.laravel/dashboard |
| date_creation | 2026-05-24 17:00:22 |

![Capture du bug](../captures/04-Bug%20-%20Lien%20profil%20public%20dashboard%20renvoie%20404.png)

# 04-Bug - Lien profil public dashboard renvoie 404

## Statut

`A faire`

Bug techniquement confirme par Playwright MCP avec le compte User 1. Le statut reste `A faire` car cette fiche vient d'etre creee et n'est pas encore prise en traitement.

## Verification Prealable

Le site ne semble pas globalement casse par un build manquant au moment du test apres reconstruction WSL :

```text
GET https://test.laravel/build/assets/app-CnTUxgv2.css => 200 OK
GET https://test.laravel/build/assets/app-BE0FrHm7.js => 200 OK
GET https://test.laravel/site.webmanifest => 200 OK
```

## Controle Anti-Doublon

Verification effectuee avant creation :

- `_TODO/Fiche` et `MEMOIRE.md` consultes pour eviter les doublons.
- Le lien `Boucles -> /loops` en 404 est deja documente dans `_TODO/Fiche/Liens cassés sur le frontend et Erreur 404.md`, donc il n'a pas ete duplique.
- Aucun rapport existant trouve sur le lien `Mon profil public` du dashboard User 1 vers `/profile/...`.

## Source

- Compte : User 1 (`TEST_MEMBER1_LOGIN` dans `_AUTOMATISATION_DEBUG/.env`).
- URL de depart : `https://test.laravel/dashboard`.
- URL en erreur : `https://test.laravel/profile/019e59cb-70ee-71ad-801c-85b66d19ea77`.
- Date et heure : `2026-05-24 17:00:22`.
- Outil : MCP Playwright lance depuis Windows via OpenCode.

## Symptome

Depuis le dashboard connecte de User 1, le lien `Mon profil public` renvoie vers une page `404 Not Found`.

## Resultat Attendu

Le lien `Mon profil public` doit ouvrir la page publique du membre connecte, ou ne pas etre affiche si aucun profil public n'est disponible.

## Resultat Actuel

- `https://test.laravel/dashboard` affiche un lien `Mon profil public`.
- Ce lien pointe vers `https://test.laravel/profile/019e59cb-70ee-71ad-801c-85b66d19ea77`.
- L'URL cible retourne `404 Not Found`.

## Etapes De Reproduction

1. Se connecter avec User 1.
2. Ouvrir `https://test.laravel/dashboard`.
3. Cliquer sur `Mon profil public`.
4. Observer la page `404 Not Found`.

## Preuves

- Propriete image : `image: "[[_TODO/captures/04-Bug - Lien profil public dashboard renvoie 404.png]]"`
- Capture principale : `_TODO/captures/04-Bug - Lien profil public dashboard renvoie 404.png`
- Reponse reseau : `GET https://test.laravel/profile/019e59cb-70ee-71ad-801c-85b66d19ea77 => 404 Not Found`

## Hypothese Technique

Pistes a verifier cote Laravel :

- le dashboard genere une URL avec un identifiant qui ne correspond pas a la route publique attendue ;
- la route publique de profil attend un slug, un ID numerique ou un autre parametre que l'UUID affiche ;
- le profil public de l'utilisateur existe mais n'est pas publie ou pas rattache au bon tenant/organisation ;
- la route `profile.show` et le lien dashboard n'utilisent pas le meme scope utilisateur.

## Test De Non Regression

Ajouter un test Playwright connecte qui verifie que le lien `Mon profil public` du dashboard ne renvoie pas une 404.

Commande proposee depuis `D:\BouclePro` :

```powershell
npm --prefix _AUTOMATISATION_DEBUG run test:auth
```

Un test dedie pourra ensuite etre ajoute, par exemple `_AUTOMATISATION_DEBUG/scripts/member-dashboard-links.spec.mjs`.

## Handoff GitHub

- Repository : `cslucki/entraide`
- Type : `issue`
- Labels proposes : `bug`, `ui`, `routing`, `playwright`
- Agent Laravel : a traiter cote projet Laravel/WSL.

## Definition Of Done

- Le lien `Mon profil public` du dashboard User 1 ouvre une page publique valide.
- Si le profil public est indisponible, le lien est masque ou remplace par une action claire de creation/publication.
- Un test de non-regression verifie que le lien ne retourne plus `404`.
