---
trigger: manual
---

Attention: Ne jamais lancer main.py/run_quick_start.py en mode normal car dirrectement connecté via clé API

<quality>
1. Tout le code doit passer Black --check (line-length = 88).
2. Flake8 ne doit produire aucun avertissement (--max-line-length = 88).
3. Mypy strict = 0 erreurs.
</quality>

<testing>
4. Couverture minimale : 90 % via pytest --cov.
5. Les tests <30 s ; marquer les lents @pytest.mark.slow.
</testing>

<commits>
6. Messages : Conventional Commits `type(scope): summary` (≤72 car.).
7. Branches : feature/* | fix/* | chore/* | release/*.
</commits>

<security>
8. Détecter et bloquer tout secret (detect-secrets).
9. `safety check` = 0 vulnérabilités avant merge.
</security>

<ci>
10. Workflow Windsurf `test_and_lint` doit passer avant push.
11. GitHub Actions doit répliquer exactement ces étapes.
</ci>

<documentation>
12. Docstrings Google style pour chaque API publique.
13. Changelog généré par cz changelog avant release.
</documentation>

<automation>
14. Script ou workflow obligatoire pour toute tâche répétée >1 fois.
15. pre-commit : black, flake8, mypy, pytest -q.
</automation>

<files>
16. Ne pas modifier /migrations/ hors révisions Alembic.
17. Ignorer .pyc, build/, dist/, __pypackages__/ via .gitignore.
</files>

<dependencies>
18. Gestion Poetry ; `pyproject.toml` + `poetry.lock` versionnés.
</dependencies>

<optimization>
19. Les assistants IA doivent signaler code smells, dead code et proposer des optimisations.
</optimization>