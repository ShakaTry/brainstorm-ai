# Tests - Brainstorm AI

Suite de tests complète pour garantir la qualité du code.

## Structure

```
tests/
├── unit/           # Tests unitaires par module
│   ├── agents/     # Tests des agents IA
│   └── core/       # Tests des composants centraux
├── integration/    # Tests d'intégration
└── conftest.py     # Fixtures pytest partagées
```

## Exécution des tests

### Tous les tests
```bash
pytest
```

### Tests unitaires uniquement
```bash
pytest tests/unit/
```

### Tests d'intégration uniquement
```bash
pytest tests/integration/
```

### Avec couverture
```bash
pytest --cov=src/brainstorm_ai
```

### Mode verbose
```bash
pytest -v
```

## Conventions

- Nom des fichiers : `test_<module>.py`
- Nom des fonctions : `test_<functionality>_<scenario>`
- Utiliser les fixtures de `conftest.py`
- Mocker les appels API externes
- Viser une couverture > 80%

## Ajout de nouveaux tests

1. Créer le fichier dans le bon dossier (unit/ ou integration/)
2. Importer les modules à tester
3. Utiliser les fixtures existantes ou en créer de nouvelles
4. Documenter les cas de test complexes 