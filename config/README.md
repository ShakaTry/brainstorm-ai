# Configuration - Brainstorm AI

Ce dossier centralise toutes les configurations du projet.

## Structure

```
config/
├── python/              # Configurations Python/outils
│   ├── .bumpversion.cfg # Version bumping
│   ├── .editorconfig    # Config éditeurs
│   ├── .pre-commit-config.yaml # Pre-commit hooks
│   ├── pytest.ini       # Configuration pytest
│   ├── pyproject.toml   # Config Python projet
│   └── tox.ini          # Configuration tox
├── config.yaml          # Configuration application
├── env.example          # Template variables d'environnement
└── mkdocs.yml           # Configuration documentation
```

## Utilisation

### Configuration de l'application
- `config.yaml` : Paramètres principaux de l'application
- `env.example` : Template pour créer votre fichier `.env`

### Outils Python
Les configurations Python sont dans le sous-dossier `python/`. 
Le Makefile est configuré pour les utiliser automatiquement.

Pour utiliser manuellement :
```bash
# Tests
pytest -c config/python/pytest.ini

# Documentation
mkdocs serve -f config/mkdocs.yml

# Pre-commit
pre-commit run -c config/python/.pre-commit-config.yaml --all-files

# Tox
tox -c config/python/tox.ini

# Bumpversion
bumpversion --config-file config/python/.bumpversion.cfg patch
```

## Note importante

Un fichier `pyproject.toml` minimal est maintenu à la racine pour la compatibilité avec certains outils qui s'attendent à le trouver là. 