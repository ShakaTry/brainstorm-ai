# Configuration - Brainstorm AI

Ce dossier centralise toutes les configurations du projet.

## Structure

```
config/
├── config.yaml          # Configuration application
├── env.example          # Template variables d'environnement
├── prompts.yaml         # Templates de prompts IA
└── README.md           # Documentation config
```

## Utilisation

### Fichiers de configuration

- **`config.yaml`** : Paramètres principaux de l'application (cycles, modèles, etc.)
- **`prompts.yaml`** : Templates des prompts pour les agents IA
- **`env.example`** : Template pour créer votre fichier `.env` avec vos clés API

### Commandes utiles

```bash
# Vérifier la configuration
python scripts/check_config.py

# Tests et vérifications  
make test
make check

# Lancer l'application
make run
```

## Note importante

Le fichier `pyproject.toml` à la racine contient toute la configuration du projet Python (dépendances, build, outils de développement). 