from core.gpt import gpt

def prompt_critique(texte: str) -> str:
    """Tu es un agent critique. Analyse objectivement la proposition suivante :

"{texte}"

Évalue :
1. Clarté
2. Faisabilité
3. Coût estimé (faible/moyen/élevé)
4. Points faibles
5. Suggestions d'amélioration

Réponds de manière structurée, concise et actionable."""
    return gpt(prompt_critique.__doc__.format(**locals()), role="critique")

def prompt_replique(defense: str, idee: str) -> str:
    """Tu es un agent critique. Voici une défense d'une idée :

Idée : {idee}
Défense : {defense}

Réagis à cette défense en indiquant si tu es d'accord, si tu as des nuances à apporter, ou si tu souhaites contre-argumenter."""
    return gpt(prompt_replique.__doc__.format(**locals()), role="critique")