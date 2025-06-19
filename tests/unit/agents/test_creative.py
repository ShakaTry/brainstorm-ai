import pytest
from brainstorm_ai.agents.creative import prompt_creatif, prompt_defense

def test_prompt_creatif(mock_gpt):
    """
    Tests that prompt_creatif calls GPT with the correct prompt structure.
    """
    objectif = "Test Objectif"
    contexte = "Test Contexte"
    contraintes = "Test Contraintes"
    historique = "Ancienne idée 1\nAncienne idée 2"
    
    # Configurer le mock pour retourner une réponse test
    mock_gpt.return_value = "Test response from GPT"
    
    # Appeler la fonction
    result = prompt_creatif(objectif, contexte, contraintes, historique)
    
    # Vérifier que GPT a été appelé
    assert mock_gpt.called
    
    # Vérifier que le prompt envoyé à GPT contient nos variables
    call_args, call_kwargs = mock_gpt.call_args
    sent_prompt = call_args[0]  # Premier argument est le prompt
    
    assert isinstance(sent_prompt, str)
    assert objectif in sent_prompt
    assert contexte in sent_prompt
    assert contraintes in sent_prompt
    assert historique in sent_prompt
    assert "Tu es un agent créatif" in sent_prompt
    
    # Vérifier que la fonction retourne la réponse de GPT
    assert result == "Test response from GPT"

def test_prompt_defense(mock_gpt):
    """
    Tests that prompt_defense calls GPT with the correct prompt structure.
    """
    idee = "Mon idée test"
    critique = "Ma critique test"
    
    # Configurer le mock pour retourner une réponse test
    mock_gpt.return_value = "Test defense response"
    
    # Appeler la fonction
    result = prompt_defense(idee, critique)
    
    # Vérifier que GPT a été appelé
    assert mock_gpt.called
    
    # Vérifier que le prompt envoyé à GPT contient nos variables
    call_args, call_kwargs = mock_gpt.call_args
    sent_prompt = call_args[0]  # Premier argument est le prompt
    
    assert isinstance(sent_prompt, str)
    assert idee in sent_prompt
    assert critique in sent_prompt
    assert "Défends ton idée" in sent_prompt
    
    # Vérifier que la fonction retourne la réponse de GPT
    assert result == "Test defense response" 