import pytest
from brainstorm_ai.agents.score import prompt_score

def test_prompt_score():
    """
    Tests that prompt_score generates a prompt requesting a JSON structure.
    """
    texte_idee = "Une idée brillante à évaluer."
    prompt = prompt_score(texte_idee)
    
    assert isinstance(prompt, str)
    assert texte_idee in prompt
    assert "Tu es un évaluateur." in prompt
    assert "Réponds au format JSON strict :" in prompt
    assert '"impact": <int>' in prompt
    assert '"faisabilite": <int>' in prompt
    assert '"originalite": <int>' in prompt
    assert '"clarte": <int>' in prompt
    assert '"total": <somme>' in prompt 