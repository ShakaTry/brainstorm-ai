.PHONY: help install install-dev test format lint type-check clean run docs

# Variables
PYTHON := python
PIP := pip
PROJECT_NAME := brainstorm_ai

# Couleurs pour l'affichage
BLUE := \033[0;34m
GREEN := \033[0;32m
RED := \033[0;31m
NC := \033[0m # No Color

help: ## Affiche cette aide
	@echo "$(BLUE)Commands disponibles:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-15s$(NC) %s\n", $$1, $$2}'

install: ## Installe les dépendances de production
	$(PIP) install -r requirements.txt

install-dev: install ## Installe toutes les dépendances (dev inclus)
	$(PIP) install -e ".[dev,docs]"
	pre-commit install

test: ## Lance les tests avec coverage
	pytest -v --cov=$(PROJECT_NAME) --cov-report=term-missing --cov-report=html

format: ## Formate le code avec Black et isort
	@echo "$(BLUE)Formatage avec Black...$(NC)"
	black src tests main.py setup.py scripts
	@echo "$(BLUE)Tri des imports avec isort...$(NC)"
	isort src tests main.py setup.py scripts

lint: ## Vérifie le code avec flake8 et mypy
	@echo "$(BLUE)Vérification avec flake8...$(NC)"
	flake8 src tests main.py scripts
	@echo "$(BLUE)Vérification des types avec mypy...$(NC)"
	mypy src main.py

type-check: ## Vérifie les types avec mypy (alias)
	mypy src main.py

clean: ## Nettoie les fichiers temporaires
	@echo "$(BLUE)Nettoyage des fichiers temporaires...$(NC)"
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	@echo "$(GREEN)Nettoyage terminé!$(NC)"

run: ## Lance l'application principale
	$(PYTHON) main.py

docs: ## Génère la documentation
	mkdocs build

docs-serve: ## Lance le serveur de documentation
	mkdocs serve

check: format lint test ## Lance toutes les vérifications

setup: install-dev ## Configure l'environnement de développement complet
	@echo "$(GREEN)Environnement de développement configuré!$(NC)"

# Commandes pour les releases
release-patch: ## Crée une release patch (0.0.X)
	bumpversion patch

release-minor: ## Crée une release mineure (0.X.0)
	bumpversion minor

release-major: ## Crée une release majeure (X.0.0)
	bumpversion major 