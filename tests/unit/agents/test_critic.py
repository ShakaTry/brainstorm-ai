import pytest
from brainstorm_ai.agents.critic import prompt_critique, prompt_replique

def test_prompt_critique():
    """
    Tests that prompt_critique generates a prompt with the correct structure and content.
    """
    texte = "Une proposition à critiquer."
    prompt = prompt_critique(texte)
    
    assert isinstance(prompt, str)
    assert texte in prompt
    assert "Tu es un agent critique." in prompt
    assert "Évalue :" in prompt

def test_prompt_replique():
    """
    Tests that prompt_replique generates a prompt with the correct structure and content.
    """
    defense = "Ceci est ma défense."
    idee = "Ceci est mon idée."
    prompt = prompt_replique(defense, idee)
    
    assert isinstance(prompt, str)
    assert defense in prompt
    assert idee in prompt
    assert "Réagis à cette défense" in prompt 