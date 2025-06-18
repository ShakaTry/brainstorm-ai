"""
Agent d'application pour la planification de mise en œuvre.
"""

from .base import BaseAgent, PromptRegistry


class AgentApplication(BaseAgent):
    """Agent responsable de la planification détaillée de mise en œuvre."""
    
    def __init__(self):
        super().__init__("application")
    
    def get_prompts(self):
        """Retourne les prompts utilisés par l'agent d'application."""
        return {
            "plan": PromptRegistry.get_prompt("application", "plan"),
            "critique_plan": PromptRegistry.get_prompt("application", "critique_plan"),
            "defense_plan": PromptRegistry.get_prompt("application", "defense_plan"),
            "revision_plan": PromptRegistry.get_prompt("application", "revision_plan")
        }
    
    def creer_plan(self, idee: str) -> str:
        """
        Crée un plan de mise en œuvre détaillé pour une idée.
        
        Args:
            idee: L'idée pour laquelle créer un plan
            
        Returns:
            Le plan de mise en œuvre détaillé
        """
        prompt = PromptRegistry.get_prompt("application", "plan")
        return self.execute_prompt(prompt, idee=idee)
    
    def critiquer_plan(self, plan: str) -> str:
        """
        Analyse critique d'un plan de mise en œuvre.
        
        Args:
            plan: Le plan à critiquer
            
        Returns:
            L'analyse critique du plan
        """
        prompt = PromptRegistry.get_prompt("application", "critique_plan")
        return self.execute_prompt(prompt, plan=plan)
    
    def defendre_plan(self, plan: str, critique: str) -> str:
        """
        Défend un plan face aux critiques.
        
        Args:
            plan: Le plan original
            critique: Les critiques émises
            
        Returns:
            La défense du plan
        """
        prompt = PromptRegistry.get_prompt("application", "defense_plan")
        return self.execute_prompt(prompt, plan=plan, critique=critique)
    
    def reviser_plan(self, plan: str, critique: str) -> str:
        """
        Révise un plan en tenant compte des critiques.
        
        Args:
            plan: Le plan initial
            critique: Les critiques émises
            
        Returns:
            Le plan révisé
        """
        prompt = PromptRegistry.get_prompt("application", "revision_plan")
        return self.execute_prompt(prompt, plan=plan, critique=critique)


# Instance globale pour compatibilité avec l'ancien code
_agent = AgentApplication()


# Fonctions de compatibilité avec l'ancien code
def prompt_plan(idee: str) -> str:
    """Wrapper pour compatibilité avec l'ancien code."""
    return _agent.creer_plan(idee)


def prompt_critique_plan(plan: str) -> str:
    """Wrapper pour compatibilité avec l'ancien code."""
    return _agent.critiquer_plan(plan)


def prompt_defense_plan(plan: str, critique: str) -> str:
    """Wrapper pour compatibilité avec l'ancien code."""
    return _agent.defendre_plan(plan, critique)


def prompt_revision_plan(plan: str, critique: str) -> str:
    """Wrapper pour compatibilité avec l'ancien code."""
    return _agent.reviser_plan(plan, critique)
