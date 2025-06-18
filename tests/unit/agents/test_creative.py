import pytest
from brainstorm_ai.agents.creative import prompt_creatif, prompt_defense

def test_prompt_creatif():
    """
    Tests that prompt_creatif generates a prompt with the correct structure and content.
    """
    objectif = "Test Objectif"
    contexte = "Test Contexte"
    contraintes = "Test Contraintes"
    historique = "Ancienne idée 1\nAncienne idée 2"
    
    prompt = prompt_creatif(objectif, contexte, contraintes, historique)
    
    assert isinstance(prompt, str)
    assert objectif in prompt
    assert contexte in prompt
    assert contraintes in prompt
    assert historique in prompt
    assert "Tu es un agent créatif." in prompt

def test_prompt_defense():
    """
    Tests that prompt_defense generates a prompt with the correct structure and content.
    """
    idee = "Mon idée test"
    critique = "Ma critique test"
    
    prompt = prompt_defense(idee, critique)
    
    assert isinstance(prompt, str)
    assert idee in prompt
    assert critique in prompt
    assert "Défends ton idée" in prompt 