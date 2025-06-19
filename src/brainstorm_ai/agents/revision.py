"""
Agent de révision pour l'amélioration des idées.
"""

from .base import BaseAgent, PromptRegistry


class AgentRevision(BaseAgent):
    """Agent responsable de la révision et amélioration des idées."""
    
    def __init__(self):
        super().__init__("revision")
    
    def get_prompts(self):
        """Retourne les prompts utilisés par l'agent de révision."""
        return {
            "amelioration": PromptRegistry.get_prompt("revision", "amelioration")
        }
    
    def ameliorer_idee(self, idee: str, critique: str) -> str:
        """
        Propose une version améliorée d'une idée en tenant compte des critiques.
        
        Args:
            idee: L'idée originale
            critique: Les critiques émises
            
        Returns:
            La version améliorée de l'idée
        """
        prompt = PromptRegistry.get_prompt("revision", "amelioration")
        return self.execute_prompt(prompt, idee=idee, critique=critique)