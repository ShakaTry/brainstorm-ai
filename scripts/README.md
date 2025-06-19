# Scripts Utilitaires - Brainstorm AI

Ce dossier contient des scripts utilitaires pour le développement et la maintenance.

## Scripts disponibles

### 📊 benchmark_optimizations.py
Script de benchmark pour mesurer les performances et optimisations.
- Analyse la configuration optimisée
- Compare avec une configuration de base
- Estime les gains de performance
```bash
python scripts/benchmark_optimizations.py
```

### 🔍 check_config.py
Vérifie et valide la configuration complète du projet.
- Teste le chargement de la configuration
- Valide la structure et les sections requises
- Affiche les erreurs et avertissements
```bash
python scripts/check_config.py
```

### 🧹 cleanup.py
Nettoie les fichiers temporaires et caches du projet.
- Supprime les __pycache__, .pyc, .pyo
- Nettoie .mypy_cache, .pytest_cache
- Option pour vider le cache de données
```bash
python scripts/cleanup.py
```

### 🐛 debug_config.py
Outil de débogage pour afficher la configuration détaillée.
- Affiche la configuration complète
- Teste les fonctions de configuration
- Aide au diagnostic des problèmes
```bash
python scripts/debug_config.py
```

### 📈 demo_progression.py
Démonstration du système de progression visuelle.
- Simule un brainstorm complet
- Montre les barres de progression
- Affiche le suivi des coûts en temps réel
```bash
python scripts/demo_progression.py
```

### 📦 generate_requirements.py
Génère les fichiers requirements.txt depuis pyproject.toml.
- Extrait les dépendances principales
- Crée requirements-dev.txt pour le développement
```bash
python scripts/generate_requirements.py
```

### 📤 test_export_fix.py
Test et validation du système d'export.
- Vérifie l'export des idées individuelles
- Teste la création des fichiers markdown
- Valide le contenu des exports
```bash
python scripts/test_export_fix.py
```

## Utilisation

Ces scripts peuvent être exécutés directement depuis la racine du projet :
```bash
python scripts/<nom_du_script>.py
```

## Développement

Pour ajouter un nouveau script utilitaire :
1. Créer le fichier dans ce dossier
2. Documenter son utilisation ici
3. S'assurer qu'il peut être exécuté depuis la racine du projet 