from core.gpt import gpt

def prompt_score(texte: str) -> str:
    """Tu es un évaluateur. Voici une idée à noter :

\"\"\"{texte}\"\"\"

Attribue une note sur 10 à chacun des critères suivants :
1. Impact
2. Faisabilité
3. Originalité
4. Clarté

Réponds au format JSON strict :
{{
  "impact": <int>,
  "faisabilite": <int>,
  "originalite": <int>,
  "clarte": <int>,
  "total": <somme>
}}"""
    return gpt(prompt_score.__doc__.format(**locals()), role="score")  # La température est définie dans la configuration
