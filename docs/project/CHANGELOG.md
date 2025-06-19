# Changelog

Tous les changements notables de ce projet seront documentés dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### 🚀 Ajouté
- Configuration complète pour le développement professionnel
  - `requirements.txt` avec toutes les dépendances
  - `pyproject.toml` pour l'installation du package
  - `pyproject.toml` pour la configuration des outils
  - `Makefile` pour automatiser les tâches courantes
  - `ruff` pour standardiser le formatage
  - `.pre-commit-config.yaml` pour les hooks de pré-commit
  - GitHub Actions CI/CD pipeline
  - Guide de contribution (`CONTRIBUTING.md`)

- Architecture améliorée
  - Classe de base `BaseAgent` pour tous les agents
  - Registre centralisé des prompts `PromptRegistry`
  - Module `core/types.py` avec TypedDict et dataclasses
  - Exports propres dans `__init__.py`

- Gestion des erreurs et logging
  - Logging structuré dans tous les modules
  - Gestion d'erreur robuste avec retry automatique
  - Client OpenAI singleton thread-safe
  - Calcul des coûts API en temps réel

### 🔧 Modifié
- Refactoring complet de tous les agents pour utiliser `BaseAgent`
- `core/config.py` : Singleton thread-safe avec double-checked locking
- `core/gpt.py` : Client singleton avec statistiques et retry robuste
- `core/loop_manager.py` : Suppression des variables globales et code dupliqué
- `main.py` : Ajout de logging et gestion d'erreur améliorée

### 🐛 Corrigé
- Variables globales supprimées
- Gestion d'erreur manquante
- Code massivement dupliqué
- Client OpenAI recréé à chaque appel
- Singleton Config non thread-safe

### 📚 Documentation
- Docstrings complètes avec types
- Guide de contribution détaillé
- Changelog pour suivre les modifications

## [1.0.0] - 2025-01-18

### 🎉 Version Initiale
- Système multi-agents pour le brainstorming créatif
- 6 agents spécialisés : Créatif, Critique, Révision, Score, Synthèse, Application
- Configuration YAML flexible
- Export multi-format (YAML, JSON, Markdown)
- Système de progression en temps réel
- Optimisations pour réduire les coûts API

[Unreleased]: https://github.com/brainstorm-ai/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/brainstorm-ai/releases/tag/v1.0.0 