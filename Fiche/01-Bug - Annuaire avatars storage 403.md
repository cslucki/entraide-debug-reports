---
type: bug
statut: Fait
categorie: FrontEnd
priorite: P1
source: Playwright MCP Windows
url: https://test.laravel/membres
date_creation: 2026-05-24 15:19:19
image: "[[_TODO/captures/01-Bug - Annuaire avatars storage 403.png]]"
---

![[_TODO/captures/01-Bug - Annuaire avatars storage 403.png]]

# 01-Bug - Annuaire avatars storage 403
## Statut

`En cours`

Bug techniquement confirme par Playwright. Le statut est `En cours` car ce bug image est deja en traitement. Pour les nouvelles fiches creees par l'assistant, le statut par defaut doit etre `A faire`.

## Source

- Note Obsidian : navigation demandee depuis la session debug BouclePro.
- Rapport debug lie : `_AUTOMATISATION_DEBUG/rapports/2026-05-24-navigation-test-laravel.md`
- URL : `https://test.laravel/membres`
- Date et heure : `2026-05-24 15:19:19`
- Outil : MCP Playwright lance depuis Windows via OpenCode.

## Symptome

Sur la page annuaire, plusieurs avatars de membres ne se chargent pas. Le navigateur remonte des erreurs `403 Forbidden` sur des fichiers publics situes sous `/storage/avatars/`.

## Resultat Attendu

Les avatars publics des membres doivent etre accessibles par le navigateur et s'afficher dans les cartes de l'annuaire.

## Resultat Actuel

La page `https://test.laravel/membres` se charge, mais plusieurs ressources d'avatars retournent `403 Forbidden`.

Erreurs console observees :

```text
Failed to load resource: the server responded with a status of 403 (Forbidden) @ https://test.laravel/storage/avatars/1778932148_1000081855.jpg
Failed to load resource: the server responded with a status of 403 (Forbidden) @ https://test.laravel/storage/avatars/1778774785_LOGO_PHOENIX_TRANSPARENT.png
Failed to load resource: the server responded with a status of 403 (Forbidden) @ https://test.laravel/storage/avatars/1778485929_PHOTO%20NB.jpg
```

Requetes reseau observees :

```text
GET https://test.laravel/storage/avatars/1778932148_1000081855.jpg => 403 Forbidden
GET https://test.laravel/storage/avatars/1778774785_LOGO_PHOENIX_TRANSPARENT.png => 403 Forbidden
GET https://test.laravel/storage/avatars/1778517410_photo%20et%20logo%20entour%C3%A9s%20avec%20drapeaux.png => 200 OK
GET https://test.laravel/storage/avatars/1778485929_PHOTO%20NB.jpg => 403 Forbidden
```

Le fait qu'un avatar voisin retourne `200 OK` indique que le probleme ne bloque pas tout le dossier `/storage/avatars/`, mais probablement certains fichiers precis.

## Etapes de Reproduction

1. Ouvrir `https://test.laravel/`.
2. Cliquer sur le compteur `24 Membres` ou ouvrir directement `https://test.laravel/membres`.
3. Ouvrir la console navigateur ou l'inspection reseau.
4. Observer les erreurs `403 Forbidden` sur plusieurs URLs `/storage/avatars/...`.

## Preuves

- Capture : `_TODO/captures/01-Bug - Annuaire avatars storage 403.png`
- Snapshot MCP : `.playwright-mcp/page-2026-05-24T13-05-34-331Z.yml`
- Console MCP : erreurs `403 Forbidden` sur trois avatars.
- Reseau MCP : trois avatars en `403`, un avatar comparable en `200 OK`.
- Test recurrent existant : `_AUTOMATISATION_DEBUG/scripts/storage-assets-403.spec.mjs`

## Hypothese Technique

Pistes a verifier cote Laravel/serveur :

- permissions fichiers incorrectes pour certains fichiers dans `storage/app/public/avatars` ou `public/storage/avatars` ;
- fichiers presents mais non lisibles par l'utilisateur du serveur web ;
- lien symbolique `public/storage` partiellement incorrect ou fichiers deployes avec droits differents ;
- regles serveur web qui bloquent certains noms de fichiers, extensions, espaces ou caracteres encodes ;
- metadata ou chemin d'avatar stocke en base vers un fichier non expose correctement.

## Test de Non Regression

Depuis `D:\BouclePro` :

```powershell
npm --prefix _AUTOMATISATION_DEBUG run test:storage
```

Le test doit passer quand aucun asset public sous `/storage/...` ne retourne `403 Forbidden`.

## Handoff GitHub

- Repository : `cslucki/entraide`
- Type : `issue`
- Labels proposes : `bug`, `ui`, `storage`, `playwright`
- Agent Laravel : a traiter cote projet Laravel/WSL.

## Definition of Done

- Les avatars listes ci-dessus retournent `200 OK` ou sont remplaces par une URL valide.
- La page `/membres` ne produit plus d'erreurs console liees aux avatars.
- `npm --prefix _AUTOMATISATION_DEBUG run test:storage` passe depuis Windows.
