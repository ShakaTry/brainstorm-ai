# Dossier Data - Brainstorm AI

Ce dossier contient toutes les données générées par l'application.

## Structure

```
data/
├── logs/       # Journaux d'exécution
├── exports/    # Résultats exportés des brainstorms
└── cache/      # Cache temporaire (ignoré par Git)
```

## Description

### logs/
Contient les journaux détaillés de chaque session de brainstorming :
- Format : `brainstorm_YYYY-MM-DD_HH-MM-SS.yaml`
- Historique complet des interactions entre agents
- Métriques de performance et coûts

### exports/
Stocke les idées exportées en format texte :
- Fichiers `.txt` avec les idées générées
- Nommage basé sur le contenu de l'idée

### cache/
Dossier temporaire pour :
- Fichiers de travail temporaires
- Cache des réponses API (si activé)
- **Note** : Ce dossier est ignoré par Git

## Maintenance

- Les logs peuvent être supprimés périodiquement pour économiser l'espace
- Les exports doivent être sauvegardés si nécessaires
- Le cache peut être vidé à tout moment sans impact 