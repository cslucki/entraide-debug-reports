---
statut: En cours
type: low task
categorie: DashBoard User
priorite: P1
Niveau: facile
created_at: 2026-05-24
updated_at: 2026-05-24
---
## Arbitrage T138

Oui, on attaque les bugs, mais **pas tous dans la même tâche fonctionnelle**.

Je recommande :

```text
TASK-138 — Broken frontend/admin links after Organization scope hardening
```

**Objectif T138 :** corriger les liens cassés, les pages vides et les 404 liés au passage `Community → Organization`, aux routes françaises, au scope tenant/default Organization.

**À exclure de T138 :**

- tri avancé du tableau `/admin/users` ;
    
- amélioration UX admin globale ;
    
- renommage massif “Communautés” ;
    
- migration DB ou déplacement massif de données.
    

Ces points doivent aller en backlog ou tâche suivante, sinon T138 devient trop large.

---

## Classement de vos bugs

|Sujet|Gravité|À faire dans T138 ?|Commentaire|
|---|--:|--:|---|
|Header “Boucles” pointe vers `/loops` au lieu `/boucles`|P1|Oui|Correction ciblée de route/UI publique française.|
|`/services/{uuid}` depuis Explorer renvoie 404|P0/P1|Oui|Probable souci scope tenant / route model binding / default Organization.|
|Micro-services / demandes d’aide depuis Explorer n’affichent rien|P0/P1|Oui|À reproduire avec données PostgreSQL locales.|
|`/requests/{uuid}` renvoie 404|P0/P1|Oui|Même famille que services.|
|`/admin/services` vide|P1|Oui|Admin global ne doit pas être bloqué par tenant scope.|
|`/admin/requests` vide|P1|Oui|Idem.|
|`/admin/messages` vide|P1|Oui|Idem, à auditer avant patch.|
|Vérifier toutes les pages Admin|P1|Oui, audit ciblé|Corriger seulement les cassures évidentes liées au scope.|
|Tri `/admin/users` par login/date/email|P2|Non|Tâche suivante UX/admin table.|
|Users rattachés à Organization “Test”|P1/P2 audit|Audit seulement|Ne pas renommer/déplacer sans comprendre la source.|

---

## Point important : Organization “Test”

Ne pas corriger ça à l’aveugle.

Après TASK-122, il est possible que les données legacy importées avec `community_id/organization_id NULL` aient été rattachées à une **Default Organization**. Si cette Organization s’appelle “Test”, l’affichage peut être techniquement cohérent mais produit/confus.

Donc dans T138 :

```text
auditer pourquoi “Test” apparaît comme Organization
```

mais **ne pas déplacer les users**, **ne pas renommer la Default Organization**, **ne pas modifier la DB** sans tâche dédiée.

---

## Prompt T138 prêt à coller

```text
Qui je suis / à qui je m’adresse :
Tu es CODEX-COCKPIT WSL / OpenCode sur le repo Laravel BouclePro/Cyberworkers. Tu dois ouvrir et traiter TASK-138.

Tâche :
TASK-138 — Broken frontend/admin links after Organization scope hardening

Contexte :
Après les tâches de durcissement Organization/default tenant, plusieurs liens frontend et pages admin sont cassés ou vides en local PostgreSQL.

Important :
Utiliser PostgreSQL local + comptes QA. Ne pas utiliser SQLite pour reproduire ces bugs runtime.
Ne pas toucher main/PROD.
Ne pas lancer de migration.
Ne pas modifier la DB sauf validation explicite.
Ne pas faire de refactor large.
Ne pas lancer de sync prod/local.
Garder le scope strict.

Bugs signalés :

Frontend :
1. Header frontend : lien “Boucles” pointe vers /loops au lieu de /boucles.
   Attendu : https://test.laravel/boucles
2. Depuis /explorer, les liens détail micro-services 404.
   Exemple : /services/019e30e1-27f0-73d1-a731-651fe0e1093a
3. Depuis /explorer, cliquer sur les micro-services ou demandes d’aide n’affiche rien.
4. Depuis l’annuaire, lien demande d’aide 404.
   Exemple : /requests/019e3125-078a-718d-a31c-78414f8c996f

Admin :
5. /admin/services n’affiche plus rien.
6. /admin/requests n’affiche plus rien.
7. /admin/messages n’affiche plus rien.
8. Vérifier rapidement l’ensemble des pages du dashboard admin pour repérer les pages vides/404 liées au même problème.
9. /admin/users affiche des utilisateurs rattachés à une Organization nommée “Test”.
   Auditer pourquoi, mais ne pas renommer ou déplacer les données dans cette tâche.

Hors scope T138 :
- Ajouter les tris sur /admin/users par login/date/email.
- Refonte dashboard admin.
- Renommage global “Communautés”.
- Migration Community → Organization.
- Déplacement massif de données.
- Modification DB.
- Refonte Explorer.
- Nouveau système de routes.

Plan :
1. Depuis develop propre, créer la tâche avec ai/scripts/create-task.sh.
2. Vérifier branche et git status.
3. Reproduire chaque bug avec PostgreSQL local.
4. Identifier les routes, controllers, policies, scopes et vues concernés.
5. Distinguer :
   - mauvais lien public français (/loops vs /boucles) ;
   - route model binding cassé ;
   - BelongsToTenantScope qui filtre trop ;
   - default Organization absente ou mauvaise ;
   - admin global qui devrait bypasser le scope ;
   - données réellement absentes.
6. Corriger uniquement les causes prouvées.
7. Pour les pages admin :
   - préserver l’accès admin plateforme global ;
   - documenter tout withoutGlobalScope si nouveau bypass nécessaire ;
   - préférer un bypass ciblé avec justification + test si nécessaire.
8. Pour /services/{uuid} et /requests/{uuid} :
   - ne pas contourner le tenant de manière globale ;
   - vérifier que le contexte Organization est résolu ;
   - vérifier que les ressources appartiennent bien à l’Organization attendue ;
   - corriger la route ou le query scope de façon minimale.
9. Pour “Test” Organization :
   - identifier l’Organization ID/slug/name ;
   - expliquer si c’est la Default Organization ;
   - expliquer pourquoi les users y sont rattachés ;
   - documenter une recommandation séparée si besoin.
10. Ajouter/adapter des tests ciblés si possible :
   - header Boucles -> /boucles ;
   - service detail accessible depuis Explorer si même Organization ;
   - request detail accessible si même Organization ;
   - admin services/requests/messages visibles pour admin plateforme.
11. Mettre à jour le TASK file avec :
   - bugs reproduits ;
   - causes ;
   - fichiers modifiés ;
   - validations ;
   - bugs reportés hors scope.
12. Quand DONE + UNLOCKED :
   - ai/scripts/check-task.sh
   - ai/scripts/finalize-task.sh
13. Commit/push.
14. Ne pas merger sans instruction explicite.

Contraintes architecture :
- Organization = Tenant.
- Loop ≠ Tenant.
- Partner ≠ Tenant.
- Public ≠ Global.
- Community/community_id/current_community = legacy technique temporaire uniquement.
- Ne pas introduire de nouveau vocabulaire Community dans les nouveaux concepts, docs ou UI.
- Les routes publiques visibles doivent rester françaises : /boucles, /partenaires, /partenaires/demande.
```

---

## Tâche suivante recommandée après T138

Les tris admin doivent être une tâche séparée :

```text
TASK-139 — Admin users table sorting and filtering
```

Scope probable :

- tri par nom/login ;
    
- tri par email ;
    
- tri par date création ;
    
- éventuellement filtre Organization ;
    
- éventuellement filtre statut disponible/admin.
    

C’est utile, mais **moins prioritaire que les 404 et pages vides**.

---

## Priorité immédiate

1. **T137 merge si pas déjà fait.**
    
2. **T138 : routes cassées / pages vides.**
    
3. **T139 : confort admin users.**
    

T138 doit rester une tâche de **stabilisation runtime**, pas une refonte admin.