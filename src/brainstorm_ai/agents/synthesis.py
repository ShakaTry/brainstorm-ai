"""
Agent de synthèse pour la consolidation des résultats.
"""

from typing import List
from .base import BaseAgent, PromptRegistry


class AgentSynthese(BaseAgent):
    """Agent responsable de la synthèse et consolidation des idées."""
    
    def __init__(self):
        super().__init__("synthese")
    
    def get_prompts(self):
        """Retourne les prompts utilisés par l'agent de synthèse."""
        return {
            "consolidation": PromptRegistry.get_prompt("synthese", "consolidation")
        }
    
    def consolider(self, idees_revisees: List[str]) -> str:
        """
        Consolide et synthétise les meilleures idées.
        
        Args:
            idees_revisees: Liste des idées révisées
            
        Returns:
            La synthèse des meilleures idées
        """
        # Joindre les idées avec des séparateurs clairs
        idees_text = "\n\n---\n\n".join([f"Idée {i+1}:\n{idee}" for i, idee in enumerate(idees_revisees)])
        
        prompt = PromptRegistry.get_prompt("synthese", "consolidation")
        return self.execute_prompt(prompt, idees=idees_text)