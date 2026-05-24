Dossier qui contient la gestion des tâches du projet Laravel 

## Fiches Bug Et Captures

Les fiches exploitables par les agents sont dans `_TODO/Fiche`.

Les captures principales des fiches bug sont dans `_TODO/captures` pour que le futur depot GitHub limite a `_TODO` soit autonome.

Convention pour une fiche bug :

- frontmatter `image: "[[_TODO/captures/NN-Bug - Titre court.png]]"` ;
- premiere ligne de contenu avant le titre : `![[_TODO/captures/NN-Bug - Titre court.png]]` ;
- capture principale nommee comme la fiche, avec extension `.png`.



# Low Task 
Rappel : les Low Task sont des tâches rapides à effectuer en parallèle des TASK qui sont dans TODO.
On créé un fichier de type LT-01 avec le minimum pour que l'agent puisse inscrire sa compréhension de la tâche, les choses à faire puis indiquer qu'il a fini. 
On n'utilise pas le workflow conçu pour les TASK (avec verrou du workflow pour le multi-agent).
Les LT sont déployés sur la branche "main" car considérée comme prioritaire.
Sauf cas exceptionnel, elles ne doivent pas concerner des modifications importantes et rentrer en conflit avec les TASKS en cours. 
