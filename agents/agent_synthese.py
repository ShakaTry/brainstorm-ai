from core.gpt import gpt
from typing import List

def prompt_synthese(idees_revisees: List[str]) -> str:
    """Tu es un agent synthétiseur. Voici une série d'idées révisées issues d'un brainstorming :

{joined_idees}

Analyse et sélectionne les 3 idées les plus pertinentes en te basant sur :
- leur faisabilité
- leur originalité
- leur impact potentiel
- leur clarté

Formate ta réponse ainsi :
1. Titre idée 1 : courte explication
2. Titre idée 2 : courte explication
3. Titre idée 3 : courte explication
"""
    joined_idees = "\n\n".join(f"- {idee}" for idee in idees_revisees)
    return gpt(prompt_synthese.__doc__.format(**locals()), role="synthese")