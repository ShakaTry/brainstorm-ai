import pytest
from brainstorm_ai.agents.application import (
    prompt_plan,
    prompt_critique_plan,
    prompt_defense_plan,
    prompt_revision_plan
)

def test_prompt_plan():
    """Tests the prompt_plan function."""
    idee = "Une idée à planifier."
    prompt = prompt_plan(idee)
    assert isinstance(prompt, str)
    assert idee in prompt
    assert "Tu es un agent d'application." in prompt

def test_prompt_critique_plan():
    """Tests the prompt_critique_plan function."""
    plan = "Un plan à critiquer."
    prompt = prompt_critique_plan(plan)
    assert isinstance(prompt, str)
    assert plan in prompt
    assert "Analyse ce plan" in prompt

def test_prompt_defense_plan():
    """Tests the prompt_defense_plan function."""
    plan = "Un plan à défendre."
    critique = "Une critique du plan."
    prompt = prompt_defense_plan(plan, critique)
    assert isinstance(prompt, str)
    assert plan in prompt
    assert critique in prompt
    assert "Réponds à cette critique." in prompt

def test_prompt_revision_plan():
    """Tests the prompt_revision_plan function."""
    plan = "Un plan à réviser."
    critique = "Une critique pour la révision."
    prompt = prompt_revision_plan(plan, critique)
    assert isinstance(prompt, str)
    assert plan in prompt
    assert critique in prompt
    assert "Réécris un plan plus robuste" in prompt 