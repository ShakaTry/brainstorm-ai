"""
Agent de scoring pour l'évaluation objective des idées.
"""

from .base import BaseAgent, PromptRegistry


class AgentScore(BaseAgent):
    """Agent responsable de l'évaluation objective des idées."""
    
    def __init__(self):
        super().__init__("score")
    
    def get_prompts(self):
        """Retourne les prompts utilisés par l'agent de score."""
        return {
            "evaluation": PromptRegistry.get_prompt("score", "evaluation")
        }
    
    def evaluer(self, texte: str) -> str:
        """
        Évalue objectivement une proposition selon plusieurs critères.
        
        Args:
            texte: Le texte/idée à évaluer
            
        Returns:
            Un JSON avec les scores d'évaluation
        """
        prompt = PromptRegistry.get_prompt("score", "evaluation")
        return self.execute_prompt(prompt, texte=texte)


# Instance globale pour compatibilité avec l'ancien code
_agent = AgentScore()


# Fonction de compatibilité avec l'ancien code
def prompt_score(texte: str) -> str:
    """Wrapper pour compatibilité avec l'ancien code."""
    return _agent.evaluer(texte)
