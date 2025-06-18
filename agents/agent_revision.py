from core.gpt import gpt

def prompt_revision(idee: str, critique: str) -> str:
    """Tu es un agent de révision. Améliore ou reformule une idée sur base de la critique reçue.

Idée initiale :
{idee}

Critique reçue :
{critique}

Corrige les faiblesses, clarifie l'idée, ou propose une variante plus robuste, sans trahir l'intention initiale."""
    return gpt(prompt_revision.__doc__.format(**locals()), role="revision")