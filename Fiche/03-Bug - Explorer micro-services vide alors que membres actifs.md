---
type: bug
statut: En cours
categorie: FrontEnd
priorite: P1
source: Playwright MCP Windows
url: https://test.laravel/explorer
date_creation: 2026-05-24 15:45:09
image: "[[_TODO/captures/03-Bug - Explorer micro-services vide alors que membres actifs.png]]"
---

![[_TODO/captures/03-Bug - Explorer micro-services vide alors que membres actifs.png]]

# 03-Bug - Explorer micro-services vide alors que membres actifs

## Statut

`En cours`

Bug techniquement confirme par Playwright MCP. Le statut est `En cours` car cette fiche est deja prise en traitement.

## Verification Prealable

Le site ne semble pas globalement casse par un build manquant au moment du test :

```text
GET https://test.laravel/build/assets/app-CnTUxgv2.css => 200 OK
GET https://test.laravel/build/assets/app-BE0FrHm7.js => 200 OK
GET https://test.laravel/site.webmanifest => 200 OK
```

Le debug fonctionnel est donc exploitable.

## Controle Anti-Doublon

Verification effectuee avant creation :

- `_TODO/TODO.base` consulte pour confirmer l'usage de `_TODO/Fiche` et `imageProperty: note.image`.
- Recherche Obsidian dans `_TODO/Fiche` : seules les fiches bug `01` et `02` existaient.
- Sujet different des bugs deja crees : pas un bug d'avatars `/storage` et pas le compteur global accueil/annuaire.

## Source

- Note Obsidian : session debug BouclePro.
- Rapport debug lie : `_AUTOMATISATION_DEBUG/rapports/2026-05-24-navigation-test-laravel.md`
- URL explorer : `https://test.laravel/explorer`
- URL annuaire : `https://test.laravel/membres`
- Date et heure : `2026-05-24 15:45:09`
- Outil : MCP Playwright lance depuis Windows via OpenCode.

## Symptome

L'onglet `Micro-services` de la page `Échanges` affiche `Aucun service trouvé`, alors que l'annuaire liste des membres avec des micro-services actifs.

## Resultat Attendu

Si des membres ont des micro-services actifs, l'onglet `Micro-services` de `/explorer` doit afficher ces services ou expliquer clairement pourquoi ils sont exclus.

## Resultat Actuel

- Page `/explorer`, onglet `Micro-services` : `Aucun service trouvé`.
- Page `/membres` : plusieurs cartes membres annoncent des micro-services actifs.
- Exemple observe : `Yves AHODONOU` affiche `4 micro-services · 2 demandes`.
- Exemple observe : `Jean-Michel HOUSSAY` affiche `1 micro-services · 0 demande` avec les libelles `Réécriture`, `Rédaction courte`, `Correction texte`.

## Etapes De Reproduction

1. Ouvrir `https://test.laravel/explorer`.
2. Cliquer sur l'onglet `Micro-services`.
3. Observer le message `Aucun service trouvé`.
4. Ouvrir `https://test.laravel/membres`.
5. Observer que certains membres affichent pourtant des micro-services actifs.

## Preuves

- Capture principale : `_TODO/captures/03-Bug - Explorer micro-services vide alors que membres actifs.png`
- Propriete image : `image: "[[_TODO/captures/03-Bug - Explorer micro-services vide alors que membres actifs.png]]"`
- Snapshot MCP explorer : `.playwright-mcp/page-2026-05-24T13-44-47-491Z.yml`
- Snapshot MCP annuaire : `.playwright-mcp/page-2026-05-24T13-45-13-962Z.yml`

Extraits observes par Playwright :

```text
Explorer / Micro-services: Aucun service trouvé.
Annuaire / Yves AHODONOU: 4 micro-services · 2 demandes
Annuaire / Jean-Michel HOUSSAY: 1 micro-services · 0 demande Réécriture Rédaction courte Correction texte
```

## Hypothese Technique

Pistes a verifier cote Laravel :

- l'onglet `Micro-services` filtre uniquement un statut publie/actif different de celui affiche dans l'annuaire ;
- les compteurs de l'annuaire et la liste explorer n'utilisent pas les memes scopes Eloquent ;
- les micro-services sont attaches aux profils mais ne sont pas publies dans la table ou route consommee par `/explorer` ;
- le filtre front-end de l'onglet reste sur un etat vide apres changement d'onglet ;
- une pagination, un cache ou un scope organisationnel masque les services dans `/explorer`.

## Test De Non Regression

Creer ou adapter un test Playwright qui verifie que l'onglet `Micro-services` affiche au moins un service quand l'annuaire indique des membres avec micro-services actifs.

Commande proposee depuis `D:\BouclePro` :

```powershell
npm --prefix _AUTOMATISATION_DEBUG run test:navigation
```

Un test dedie pourra ensuite etre ajoute, par exemple `_AUTOMATISATION_DEBUG/scripts/explorer-microservices-consistency.spec.mjs`.

## Handoff GitHub

- Repository : `cslucki/entraide`
- Type : `issue`
- Labels proposes : `bug`, `ui`, `data-consistency`, `playwright`
- Agent Laravel : a traiter cote projet Laravel/WSL.

## Definition Of Done

- L'onglet `Micro-services` affiche les services actifs visibles/coherents avec l'annuaire.
- Si certains micro-services sont volontairement exclus, l'interface ou les libelles expliquent le perimetre.
- Un test de non-regression couvre la coherence entre annuaire et explorer.
