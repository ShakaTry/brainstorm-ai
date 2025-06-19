# Guide de Contribution

Merci de votre intérêt pour contribuer à Brainstorm AI ! Ce guide vous aidera à démarrer.

## 🚀 Démarrage Rapide

1. **Fork** le projet
2. **Clone** votre fork :
   ```bash
   git clone https://github.com/votre-username/brainstorm-ai.git
   cd brainstorm-ai
   ```

3. **Installez** l'environnement de développement :
   ```bash
   make setup
   # ou manuellement :
   pip install -e ".[dev]"
   pre-commit install
   ```

4. **Créez** une branche pour votre fonctionnalité :
   ```bash
   git checkout -b feature/ma-nouvelle-fonctionnalite
   ```

## 📋 Standards de Code

### Style de Code
- Nous utilisons **Black** pour le formatage (ligne de 100 caractères)
- **isort** pour l'organisation des imports
- **flake8** pour la validation du style
- **mypy** pour la vérification des types

Exécutez tous les checks avec :
```bash
make check
```

### Structure du Code
```
brainstorm_ai/
├── agents/          # Agents spécialisés
├── core/            # Logique métier principale
├── tests/           # Tests unitaires et d'intégration
└── docs/            # Documentation
```

### Conventions de Nommage
- **Classes** : PascalCase (`AgentCreatif`)
- **Fonctions/variables** : snake_case (`prompt_creatif`)
- **Constantes** : UPPER_SNAKE_CASE (`MAX_RETRIES`)
- **Fichiers** : snake_case (`agent_creatif.py`)

## ✅ Checklist de Contribution

Avant de soumettre votre PR, assurez-vous que :

- [ ] Le code suit les standards du projet (`make lint`)
- [ ] Les tests passent (`make test`)
- [ ] Vous avez ajouté des tests pour les nouvelles fonctionnalités
- [ ] La documentation est à jour
- [ ] Les messages de commit sont clairs et descriptifs
- [ ] Votre branche est à jour avec `main`

## 🧪 Tests

### Exécuter les Tests
```bash
# Tous les tests
make test

# Un test spécifique
pytest tests/test_agent_creatif.py -v

# Avec coverage
pytest --cov=agents --cov=core --cov-report=html
```

### Écrire des Tests
- Utilisez `pytest` et ses fixtures
- Mockez les appels API avec `pytest-mock`
- Visez une couverture > 80%
- Tests unitaires dans `tests/`
- Tests d'intégration dans `tests/integration/`

## 📝 Documentation

- Docstrings pour toutes les fonctions publiques
- Type hints pour tous les paramètres
- Exemples d'utilisation dans les docstrings
- README.md à jour pour les nouvelles fonctionnalités

### Format des Docstrings
```python
def ma_fonction(param1: str, param2: int) -> bool:
    """
    Description courte de la fonction.
    
    Description plus détaillée si nécessaire.
    
    Args:
        param1: Description du paramètre 1
        param2: Description du paramètre 2
        
    Returns:
        Description de la valeur retournée
        
    Raises:
        ValueError: Si param2 est négatif
        
    Example:
        >>> ma_fonction("test", 42)
        True
    """
```

## 🔄 Processus de Pull Request

1. **Créez** votre PR avec un titre descriptif
2. **Remplissez** le template de PR
3. **Liez** l'issue correspondante (#123)
4. **Attendez** la revue de code
5. **Répondez** aux commentaires
6. **Mergez** après approbation

### Format des Commits
```
type(scope): description courte

Description détaillée si nécessaire

Fixes #123
```

Types : `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

## 🐛 Signaler un Bug

1. Vérifiez que le bug n'est pas déjà signalé
2. Créez une issue avec :
   - Version de Python
   - Description du bug
   - Étapes pour reproduire
   - Comportement attendu vs actuel
   - Logs/erreurs

## 💡 Proposer une Fonctionnalité

1. Ouvrez une issue pour discuter
2. Décrivez :
   - Le problème résolu
   - La solution proposée
   - Les alternatives considérées
   - L'impact sur l'existant

## 🤝 Code de Conduite

- Soyez respectueux et inclusif
- Acceptez les critiques constructives
- Focalisez sur ce qui est meilleur pour la communauté
- Montrez de l'empathie envers les autres

## 📞 Besoin d'Aide ?

- 📖 Consultez la [documentation](docs/)
- 💬 Ouvrez une [discussion](https://github.com/brainstorm-ai/discussions)
- 🐛 Créez une [issue](https://github.com/brainstorm-ai/issues)

Merci de contribuer à Brainstorm AI ! 🎉 