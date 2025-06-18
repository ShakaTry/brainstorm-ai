from core.gpt import gpt

def prompt_creatif(objectif: str, contexte: str, contraintes: str, historique: str) -> str:
    """Tu es un agent créatif. Ta mission est de générer des idées innovantes, réalistes et utiles.

Objectif : {objectif}
Contexte : {contexte}
Contraintes : {contraintes}

Idées déjà proposées :
{historique}

Génère 3 nouvelles idées numérotées, originales et non redondantes. Pour la plus prometteuse, fournis un plan de mise en œuvre synthétique."""
    return gpt(prompt_creatif.__doc__.format(**locals()), role="creatif")

def prompt_defense(idee: str, critique: str) -> str:
    """Tu es un agent créatif. Voici une idée qui a été critiquée :

Idée : {idee}
Critique : {critique}

Défends ton idée en expliquant pourquoi elle est valable et comment elle peut être améliorée pour répondre aux critiques."""
    return gpt(prompt_defense.__doc__.format(**locals()), role="creatif")