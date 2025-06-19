# Code Source - Brainstorm AI

Ce dossier contient le code source principal de l'application Brainstorm AI.

## Structure

```
brainstorm_ai/
├── agents/      # Agents IA pour le processus de brainstorming
├── cli/         # Interface en ligne de commande
└── core/        # Composants centraux (config, GPT, loop manager)
```

## Modules

### agents/
Contient tous les agents spécialisés :
- `creative.py` : Agent créatif pour générer des idées
- `critic.py` : Agent critique pour évaluer les idées
- `revision.py` : Agent de révision pour améliorer les idées
- `score.py` : Agent de notation
- `synthesis.py` : Agent de synthèse
- `application.py` : Agent d'application pratique
- `base.py` : Classe de base pour tous les agents

### cli/
Interface en ligne de commande pour exécuter le brainstorming.

### core/
Composants centraux :
- `config.py` : Gestion de la configuration
- `gpt.py` : Interface avec l'API OpenAI
- `loop_manager.py` : Gestionnaire du cycle de brainstorming
- `progress_tracker.py` : Suivi de la progression
- `types.py` : Types et structures de données
- `exporter.py` : Export des résultats
- `utils.py` : Utilitaires divers 