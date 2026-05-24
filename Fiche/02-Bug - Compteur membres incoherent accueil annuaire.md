---
type: bug
statut: A faire
categorie: FrontEnd
priorite: P1
source: Playwright MCP Windows
url: https://test.laravel/
date_creation: 2026-05-24 15:23:40
image: "[[_TODO/captures/02-Bug - Compteur membres incoherent accueil annuaire.png]]"
---

![[_TODO/captures/02-Bug - Compteur membres incoherent accueil annuaire.png]]

# 02-Bug - Compteur membres incoherent accueil annuaire

## Statut

`A faire`

Bug techniquement confirme par Playwright MCP. Le statut reste `A faire` car cette fiche vient d'etre creee et n'est pas encore prise en traitement.

## Source

- Note Obsidian : session debug BouclePro.
- Rapport debug lie : `_AUTOMATISATION_DEBUG/rapports/2026-05-24-navigation-test-laravel.md`
- URL accueil : `https://test.laravel/`
- URL annuaire : `https://test.laravel/membres`
- Date et heure : `2026-05-24 15:23:40`
- Outil : MCP Playwright lance depuis Windows via OpenCode.

## Symptome

Le compteur de membres affiche deux valeurs differentes selon la page consultee.

## Resultat Attendu

Le nombre de membres affiche sur l'accueil doit etre coherent avec le total annonce dans l'annuaire public.

Si les deux chiffres correspondent volontairement a des perimetres differents, l'interface doit l'indiquer clairement pour eviter une contradiction apparente.

## Resultat Actuel

- Accueil `https://test.laravel/` : le bloc statistique affiche `24 Membres`.
- Annuaire `https://test.laravel/membres` : l'en-tete affiche `19 membres inscrits`.
- Pagination annuaire : `Showing 1 to 16 of 19 results`.

L'ecart visible est de `5` membres.

## Etapes De Reproduction

1. Ouvrir `https://test.laravel/`.
2. Observer le compteur `24 Membres` dans les statistiques de la page d'accueil.
3. Cliquer sur ce compteur ou ouvrir directement `https://test.laravel/membres`.
4. Observer l'en-tete `19 membres inscrits` et la pagination `Showing 1 to 16 of 19 results`.

## Preuves

- Capture principale : `_TODO/captures/02-Bug - Compteur membres incoherent accueil annuaire.png`
- Capture annuaire : `_TODO/captures/02-Bug - Compteur membres incoherent accueil annuaire - annuaire.png`
- Snapshot MCP accueil : `.playwright-mcp/page-2026-05-24T13-21-38-124Z.yml`
- Snapshot MCP annuaire : `.playwright-mcp/page-2026-05-24T13-21-59-273Z.yml`

Extraits observes par Playwright :

```text
Accueil: 24 Membres
Annuaire: 19 membres inscrits
Pagination: Showing 1 to 16 of 19 results
```

## Hypothese Technique

Pistes a verifier cote Laravel :

- l'accueil compte tous les utilisateurs, tandis que l'annuaire filtre seulement les profils publics ou actifs ;
- l'accueil utilise une valeur cachee ou une agregation non mise a jour ;
- l'annuaire exclut certains comptes incomplets, inactifs, non verifies ou hors organisation ;
- les deux pages utilisent deux requetes ou scopes Eloquent differents pour definir un "membre".

## Test De Non Regression

Creer ou adapter un test Playwright qui compare le compteur d'accueil avec le total annonce par l'annuaire.

Commande proposee depuis `D:\BouclePro` :

```powershell
npm --prefix _AUTOMATISATION_DEBUG run test:navigation
```

Un test dedie pourra ensuite etre ajoute, par exemple `_AUTOMATISATION_DEBUG/scripts/member-count-consistency.spec.mjs`.

## Handoff GitHub

- Repository : `cslucki/entraide`
- Type : `issue`
- Labels proposes : `bug`, `ui`, `data-consistency`, `playwright`
- Agent Laravel : a traiter cote projet Laravel/WSL.

## Definition Of Done

- L'accueil et l'annuaire affichent le meme total pour le meme perimetre de membres.
- Si les perimetres sont differents, les libelles sont explicites et ne pretent plus a confusion.
- Un test de non-regression verifie la coherence du compteur membres.
