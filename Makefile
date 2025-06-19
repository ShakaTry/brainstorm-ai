.PHONY: help install install-dev test check clean run bump-patch bump-minor bump-major

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
	$(PIP) install -e ".[dev]"

test: ## Lance les tests avec coverage
	pytest -v --cov=$(PROJECT_NAME) --cov-report=term-missing

check: ## Vérifie et formate le code avec ruff
	@echo "$(BLUE)Vérification du code avec ruff...$(NC)"
	ruff check src tests main.py scripts
	@echo "$(BLUE)Formatage du code avec ruff...$(NC)"
	ruff format src tests main.py scripts

clean: ## Nettoie les fichiers temporaires
	@echo "$(BLUE)Nettoyage des fichiers temporaires...$(NC)"
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	@echo "$(GREEN)Nettoyage terminé!$(NC)"

run: ## Lance l'application principale
	$(PYTHON) main.py

bump-patch: ## Incrémente la version patch (2.1.0 -> 2.1.1)
	@echo "$(BLUE)Bump version patch...$(NC)"
	bump2version patch

bump-minor: ## Incrémente la version minor (2.1.0 -> 2.2.0)
	@echo "$(BLUE)Bump version minor...$(NC)"
	bump2version minor

bump-major: ## Incrémente la version major (2.1.0 -> 3.0.0)
	@echo "$(BLUE)Bump version major...$(NC)"
	bump2version major
 