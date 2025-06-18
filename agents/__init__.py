"""
Module des agents de brainstorming.

Ce module contient tous les agents spécialisés du système :
- Agent Créatif : génération d'idées
- Agent Critique : analyse critique
- Agent Révision : amélioration des idées
- Agent Score : évaluation objective
- Agent Synthèse : consolidation des résultats
- Agent Application : planification de mise en œuvre
"""

from agents.base_agent import BaseAgent, PromptRegistry
from agents.agent_creatif import AgentCreatif, prompt_creatif, prompt_defense
from agents.agent_critique import prompt_critique, prompt_replique
from agents.agent_revision import prompt_revision
from agents.agent_score import prompt_score
from agents.agent_synthese import prompt_synthese
from agents.agent_application import (
    prompt_plan, 
    prompt_critique_plan, 
    prompt_defense_plan, 
    prompt_revision_plan
)

__all__ = [
    'BaseAgent',
    'PromptRegistry',
    'AgentCreatif',
    'prompt_creatif',
    'prompt_defense',
    'prompt_critique',
    'prompt_replique',
    'prompt_revision',
    'prompt_score',
    'prompt_synthese',
    'prompt_plan',
    'prompt_critique_plan',
    'prompt_defense_plan',
    'prompt_revision_plan'
] 