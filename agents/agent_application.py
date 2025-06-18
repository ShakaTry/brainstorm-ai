from core.gpt import gpt

def prompt_plan(idee: str) -> str:
    """Tu es un agent d'application. Voici une idée à mettre en œuvre :

{idee}

Propose un plan d'action structuré pour l'appliquer concrètement. Inclue :
- Étapes clés
- Ressources ou outils nécessaires
- Éventuelles difficultés ou risques
- Estimation du temps requis si possible

Sois clair, structuré, orienté efficacité réelle.
"""
    return gpt(prompt_plan.__doc__.format(**locals()), role="application")

def prompt_critique_plan(plan: str) -> str:
    """Tu es un agent critique. Voici un plan d'action proposé :

{plan}

Analyse ce plan selon les critères suivants :
1. Réalisme des étapes
2. Risques ou imprécisions potentielles
3. Coûts cachés ou non anticipés
4. Suggestions concrètes d'amélioration

Sois direct, structuré, et constructif.
"""
    return gpt(prompt_critique_plan.__doc__.format(**locals()), role="critique")

def prompt_defense_plan(plan: str, critique: str) -> str:
    """Tu es l'auteur du plan suivant :

{plan}

Voici la critique que tu as reçue :
{critique}

Réponds à cette critique. Défends ton approche, ajuste les points faibles, ou propose une alternative cohérente. Reste clair, structuré, et objectif.
"""
    return gpt(prompt_defense_plan.__doc__.format(**locals()), role="application")

def prompt_revision_plan(plan: str, critique: str) -> str:
    """Tu es un agent de révision. Tu dois améliorer ce plan en tenant compte de la critique suivante.

Plan :
{plan}

Critique :
{critique}

Réécris un plan plus robuste, corrigé, tout en respectant l'intention de départ. Structure les étapes, les ressources, et améliore la lisibilité.
"""
    return gpt(prompt_revision_plan.__doc__.format(**locals()), role="revision")
