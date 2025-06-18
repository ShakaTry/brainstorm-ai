"""
Agent critique pour l'analyse constructive des idées.
"""

from agents.base_agent import BaseAgent, PromptRegistry


class AgentCritique(BaseAgent):
    """Agent responsable de l'analyse critique constructive."""
    
    def __init__(self):
        super().__init__("critique")
    
    def get_prompts(self):
        """Retourne les prompts utilisés par l'agent critique."""
        return {
            "analyse": PromptRegistry.get_prompt("critique", "analyse"),
            "replique": PromptRegistry.get_prompt("critique", "replique")
        }
    
    def analyser(self, texte: str) -> str:
        """
        Analyse de manière critique un texte/idée.
        
        Args:
            texte: Le texte à analyser
            
        Returns:
            L'analyse critique constructive
        """
        prompt = PromptRegistry.get_prompt("critique", "analyse")
        return self.execute_prompt(prompt, texte=texte)
    
    def repliquer(self, defense: str, idee: str) -> str:
        """
        Évalue une défense par rapport à l'idée originale.
        
        Args:
            defense: La défense proposée
            idee: L'idée originale
            
        Returns:
            L'évaluation de la défense
        """
        prompt = PromptRegistry.get_prompt("critique", "replique")
        return self.execute_prompt(prompt, defense=defense, idee=idee)


# Instance globale pour compatibilité avec l'ancien code
_agent = AgentCritique()


# Fonctions de compatibilité avec l'ancien code
def prompt_critique(texte: str) -> str:
    """Wrapper pour compatibilité avec l'ancien code."""
    return _agent.analyser(texte)


def prompt_replique(defense: str, idee: str) -> str:
    """Wrapper pour compatibilité avec l'ancien code."""
    return _agent.repliquer(defense, idee)