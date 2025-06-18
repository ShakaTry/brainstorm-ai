"""
Agent créatif pour la génération d'idées innovantes.
"""

from agents.base_agent import BaseAgent, PromptRegistry


class AgentCreatif(BaseAgent):
    """Agent responsable de la génération d'idées créatives."""
    
    def __init__(self):
        super().__init__("creatif")
    
    def get_prompts(self):
        """Retourne les prompts utilisés par l'agent créatif."""
        return {
            "generation": PromptRegistry.get_prompt("creatif", "generation"),
            "defense": PromptRegistry.get_prompt("creatif", "defense")
        }
    
    def generer_idees(self, objectif: str, contexte: str, contraintes: str, historique: str) -> str:
        """
        Génère de nouvelles idées créatives.
        
        Args:
            objectif: L'objectif du brainstorming
            contexte: Le contexte du projet
            contraintes: Les contraintes à respecter
            historique: L'historique des idées déjà proposées
            
        Returns:
            Les nouvelles idées générées
        """
        prompt = PromptRegistry.get_prompt("creatif", "generation")
        return self.execute_prompt(prompt, 
                                   objectif=objectif,
                                   contexte=contexte,
                                   contraintes=contraintes,
                                   historique=historique)
    
    def defendre_idee(self, idee: str, critique: str) -> str:
        """
        Défend une idée face aux critiques.
        
        Args:
            idee: L'idée à défendre
            critique: Les critiques émises
            
        Returns:
            La défense de l'idée
        """
        prompt = PromptRegistry.get_prompt("creatif", "defense")
        return self.execute_prompt(prompt, idee=idee, critique=critique)


# Instance globale pour compatibilité avec l'ancien code
_agent = AgentCreatif()


# Fonctions de compatibilité avec l'ancien code
def prompt_creatif(objectif: str, contexte: str, contraintes: str, historique: str) -> str:
    """Wrapper pour compatibilité avec l'ancien code."""
    return _agent.generer_idees(objectif, contexte, contraintes, historique)


def prompt_defense(idee: str, critique: str) -> str:
    """Wrapper pour compatibilité avec l'ancien code."""
    return _agent.defendre_idee(idee, critique)