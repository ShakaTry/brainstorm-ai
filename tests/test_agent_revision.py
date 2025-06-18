import pytest
from agents.agent_revision import prompt_revision

def test_prompt_revision():
    """
    Tests that prompt_revision generates a prompt with the correct structure and content.
    """
    idee = "Mon idée à améliorer."
    critique = "Une critique constructive."
    
    prompt = prompt_revision(idee, critique)
    
    assert isinstance(prompt, str)
    assert idee in prompt
    assert critique in prompt
    assert "Tu es un agent de révision." in prompt
    assert "Corrige les faiblesses" in prompt