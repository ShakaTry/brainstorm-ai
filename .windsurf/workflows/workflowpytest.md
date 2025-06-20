---
description: workflow_test
---

Copiez-collez dans `.windsurf/workflows/test_and_lint.yaml` :

```yaml
name: Test-Lint-CI
on:
  manual: true      # /test-and-lint
  push: true
  pull_request: true
  save: true        # exécution rapide à chaque sauvegarde locale

jobs:
  setup:
    steps:
      - name: Create venv
        run: |
          python -m venv .venv
          source .venv/bin/activate
      - name: Install deps (Poetry)
        run: |
          pip install poetry
          poetry install --no-root --no-ansi
          poetry run pip install black flake8 mypy pytest pytest-cov detect-secrets safety

  lint:
    needs: setup
    steps:
      - run: poetry run black . --check
      - run: poetry run flake8 .
      - run: poetry run mypy --strict src/

  test:
    needs: lint
    steps:
      - run: poetry run pytest --cov=src --cov-fail-under=90 -q

  security:
    needs: test
    steps:
      - run: poetry run detect-secrets scan --all-files
      - run: poetry run safety check --fail-on 0

  summary:
    needs: security
    steps:
      - run: echo "Pipeline conforme aux rules : qualité, tests, sécurité, couverture ≥90 %."
```
