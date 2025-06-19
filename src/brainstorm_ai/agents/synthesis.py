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
        return {"consolidation": PromptRegistry.get_prompt("synthese", "consolidation")}

    def consolider(self, idees_revisees: List[str], count: int = 3) -> str:
        """
        Consolide et synthétise les meilleures idées.

        Args:
            idees_revisees: Liste des idées révisées
            count: Nombre d'idées à sélectionner

        Returns:
            La synthèse des meilleures idées
        """
        # Joindre les idées avec des séparateurs clairs
        idees_text = "\n\n---\n\n".join(
            [f"Idée {i + 1}:\n{idee}" for i, idee in enumerate(idees_revisees)]
        )

        prompt = PromptRegistry.get_prompt("synthese", "consolidation")
        return self.execute_prompt(prompt, idees=idees_text, count=count)


# Instance globale pour les fonctions de compatibilité
_agent_synthese = AgentSynthese()


# Fonction de compatibilité avec l'interface attendue
def prompt_synthese(idees_revisees: List[str], count: int = 3) -> str:
    """
    Interface de compatibilité pour la synthèse d'idées.

    Args:
        idees_revisees: Liste des idées révisées
        count: Nombre d'idées à sélectionner

    Returns:
        La synthèse des meilleures idées
    """
    return _agent_synthese.consolider(idees_revisees, count)
