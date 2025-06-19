# Tests - Brainstorm AI

Tests essentiels pour valider le bon fonctionnement du système.

## Structure

```
tests/
├── test_config_correlation.py    # Test corrélation config/logs
├── test_export_fix.py           # Test système d'export  
├── conftest.py                  # Fixtures pytest
└── README.md                    # Documentation
```

## Exécution des tests

### Tous les tests
```bash
make test
# ou
pytest
```

### Avec couverture
```bash
pytest --cov=src/brainstorm_ai --cov-report=term-missing
```

### Test spécifique
```bash
pytest tests/test_config_correlation.py -v
```

## Tests disponibles

- **`test_config_correlation.py`** : Valide que la configuration est respectée dans les logs
- **`test_export_fix.py`** : Vérifie le bon fonctionnement des exports
- **Scripts de validation** : Dans le dossier `scripts/` pour tests manuels

## Philosophie

Pour un projet simple, quelques tests ciblés valent mieux qu'une suite complexe. 
Les tests se concentrent sur les fonctionnalités critiques et les bugs connus. 