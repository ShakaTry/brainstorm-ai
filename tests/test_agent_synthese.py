import pytest
from agents.agent_synthese import prompt_synthese

def test_prompt_synthese():
    """
    Tests that prompt_synthese correctly processes a list of logs
    and generates the synthesis prompt.
    """
    logs = [
        {"revision": "Idée révisée 1"},
        {"revision": "Idée révisée 2"},
        {"some_other_key": "valeur"}, # Should be ignored
        {"revision": "Idée révisée 3"}
    ]
    
    prompt = prompt_synthese(logs)
    
    assert isinstance(prompt, str)
    assert "Tu es un agent synthétiseur." in prompt
    assert "- Idée révisée 1" in prompt
    assert "- Idée révisée 2" in prompt
    assert "- Idée révisée 3" in prompt
    assert "valeur" not in prompt # Make sure other data is ignored
    assert "Analyse et sélectionne les 3 idées les plus pertinentes" in prompt

def test_prompt_synthese_empty_logs():
    """
    Tests prompt_synthese with an empty list of logs.
    """
    prompt = prompt_synthese([])
    
    assert isinstance(prompt, str)
    # The main prompt text should still be there
    assert "Tu es un agent synthétiseur." in prompt
    # But the placeholder for ideas will be empty
    assert "Voici une série d'idées révisées issues d'un brainstorming :\n\n\n\nAnalyse et sélectionne" in prompt 