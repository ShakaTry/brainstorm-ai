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

from .base import BaseAgent, PromptRegistry
from .creative import AgentCreatif
from .critic import AgentCritique
from .revision import AgentRevision
from .score import AgentScore
from .synthesis import AgentSynthese
from .application import AgentApplication

# Instances singleton des agents
_agents = {
    'creatif': None,
    'critique': None,
    'revision': None,
    'score': None,
    'synthese': None,
    'application': None
}

def get_agent(agent_type: str):
    """Retourne l'instance singleton de l'agent demandé."""
    if agent_type not in _agents:
        raise ValueError(f"Type d'agent inconnu : {agent_type}")
    
    if _agents[agent_type] is None:
        if agent_type == 'creatif':
            _agents[agent_type] = AgentCreatif()
        elif agent_type == 'critique':
            _agents[agent_type] = AgentCritique()
        elif agent_type == 'revision':
            _agents[agent_type] = AgentRevision()
        elif agent_type == 'score':
            _agents[agent_type] = AgentScore()
        elif agent_type == 'synthese':
            _agents[agent_type] = AgentSynthese()
        elif agent_type == 'application':
            _agents[agent_type] = AgentApplication()
    
    return _agents[agent_type]

# Fonctions de compatibilité pour l'ancien code
def prompt_creatif(objectif: str, contexte: str, contraintes: str, historique: str) -> str:
    """Wrapper pour compatibilité avec l'ancien code."""
    return get_agent('creatif').generer_idees(objectif, contexte, contraintes, historique)

def prompt_defense(idee: str, critique: str) -> str:
    """Wrapper pour compatibilité avec l'ancien code."""
    return get_agent('creatif').defendre_idee(idee, critique)

def prompt_critique(texte: str) -> str:
    """Wrapper pour compatibilité avec l'ancien code."""
    return get_agent('critique').analyser(texte)

def prompt_replique(defense: str, idee: str) -> str:
    """Wrapper pour compatibilité avec l'ancien code."""
    return get_agent('critique').repliquer(defense, idee)

def prompt_revision(idee: str, critique: str) -> str:
    """Wrapper pour compatibilité avec l'ancien code."""
    return get_agent('revision').ameliorer_idee(idee, critique)

def prompt_score(texte: str) -> str:
    """Wrapper pour compatibilité avec l'ancien code."""
    return get_agent('score').evaluer(texte)

def prompt_synthese(idees_revisees: list) -> str:
    """Wrapper pour compatibilité avec l'ancien code."""
    return get_agent('synthese').consolider(idees_revisees)

def prompt_plan(idee: str) -> str:
    """Wrapper pour compatibilité avec l'ancien code."""
    return get_agent('application').creer_plan(idee)

def prompt_critique_plan(plan: str) -> str:
    """Wrapper pour compatibilité avec l'ancien code."""
    return get_agent('application').critiquer_plan(plan)

def prompt_defense_plan(plan: str, critique: str) -> str:
    """Wrapper pour compatibilité avec l'ancien code."""
    return get_agent('application').defendre_plan(plan, critique)

def prompt_revision_plan(plan: str, critique: str) -> str:
    """Wrapper pour compatibilité avec l'ancien code."""
    return get_agent('application').reviser_plan(plan, critique)

__all__ = [
    'BaseAgent',
    'PromptRegistry',
    'AgentCreatif',
    'AgentCritique', 
    'AgentRevision',
    'AgentScore',
    'AgentSynthese',
    'AgentApplication',
    'get_agent',
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