"""
Module de base pour tous les agents du système de brainstorming.
Fournit une classe abstraite et des utilitaires communs.
"""

import logging
import yaml
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from pathlib import Path
from ..core.gpt import gpt

logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """Classe de base pour tous les agents du système."""
    
    def __init__(self, role: str):
        """
        Initialise un agent avec son rôle.
        
        Args:
            role: Le rôle de l'agent (creatif, critique, revision, etc.)
        """
        self.role = role
        self.logger = logging.getLogger(f"agents.{role}")
    
    def execute_prompt(self, prompt_template: str, **kwargs) -> str:
        """
        Exécute un prompt en remplaçant les variables et en appelant GPT.
        
        Args:
            prompt_template: Template du prompt avec des placeholders
            **kwargs: Variables à substituer dans le template
            
        Returns:
            La réponse de GPT
        """
        # Formater le prompt avec les variables
        prompt = prompt_template.format(**kwargs)
        
        # Log du prompt pour debug (tronqué)
        self.logger.debug(f"Exécution du prompt ({len(prompt)} chars): {prompt[:200]}...")
        
        # Appel à GPT
        try:
            response = gpt(prompt, role=self.role)
            self.logger.info(f"Réponse reçue ({len(response)} chars)")
            return response
        except Exception as e:
            self.logger.error(f"Erreur lors de l'exécution du prompt: {str(e)}")
            raise
    
    @abstractmethod
    def get_prompts(self) -> Dict[str, str]:
        """
        Retourne un dictionnaire des prompts utilisés par cet agent.
        Doit être implémenté par chaque agent spécifique.
        
        Returns:
            Dict avec les noms et templates des prompts
        """
        pass


class PromptRegistry:
    """Registre centralisé pour tous les prompts du système."""
    
    _prompts: Dict[str, Dict[str, str]] = {}
    _loaded = False
    
    @classmethod
    def _load_prompts(cls) -> None:
        """Charge les prompts depuis le fichier de configuration."""
        if cls._loaded:
            return
            
        try:
            # Chemin vers le fichier de prompts
            prompts_path = Path(__file__).parent.parent.parent.parent / "config" / "prompts.yaml"
            
            if not prompts_path.exists():
                logger.warning(f"Fichier de prompts non trouvé : {prompts_path}")
                cls._load_default_prompts()
                return
            
            with open(prompts_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
            
            if "prompts" in data:
                cls._prompts = data["prompts"]
                logger.info(f"Prompts chargés depuis {prompts_path}")
            else:
                logger.warning("Structure de prompts invalide, chargement des prompts par défaut")
                cls._load_default_prompts()
                
            cls._loaded = True
            
        except Exception as e:
            logger.error(f"Erreur lors du chargement des prompts : {e}")
            cls._load_default_prompts()
    
    @classmethod
    def _load_default_prompts(cls) -> None:
        """Charge les prompts par défaut en cas d'erreur."""
        cls._prompts = {
            "creatif": {
                "generation": """Tu es un agent créatif. Ta mission est de générer des idées innovantes, réalistes et utiles.

Objectif : {objectif}
Contexte : {contexte}
Contraintes : {contraintes}

Idées déjà proposées :
{historique}

Génère 3 nouvelles idées numérotées, originales et non redondantes. Pour la plus prometteuse, fournis un plan de mise en œuvre synthétique.""",
                
                "defense": """Tu es un agent créatif. Voici une idée qui a été critiquée :

Idée : {idee}
Critique : {critique}

Défends ton idée en expliquant pourquoi elle est valable et comment elle peut être améliorée pour répondre aux critiques."""
            },
            
            "critique": {
                "analyse": """Tu es un agent critique constructif. Analyse cette idée/proposition de manière objective :

{texte}

Identifie les faiblesses, risques et limites potentiels. Propose des améliorations concrètes.""",
                
                "replique": """Tu es un agent critique. Suite à cette défense :

{defense}

Concernant l'idée originale : {idee}

Évalue si la défense répond vraiment aux critiques. Identifie les points qui restent problématiques."""
            },
            
            "revision": {
                "amelioration": """Tu es un agent de révision. Voici une idée et sa critique :

Idée : {idee}
Critique : {critique}

Propose une version améliorée de cette idée qui tient compte des critiques tout en préservant ses points forts."""
            },
            
            "score": {
                "evaluation": """Tu es un agent d'évaluation. Évalue objectivement cette proposition selon 4 critères :

{texte}

Retourne UNIQUEMENT un JSON avec ces scores (1-10) :
{{
    "impact": <score>,
    "faisabilite": <score>,
    "originalite": <score>,
    "clarte": <score>
}}"""
            },
            
            "synthese": {
                "consolidation": """Tu es un agent de synthèse. Voici toutes les idées révisées :

{idees}

Sélectionne les 3 meilleures idées en les classant par ordre de pertinence. Pour chaque idée, fournis :
1. Un titre concis
2. Une description claire
3. Les principaux avantages
4. Les étapes clés de mise en œuvre"""
            },
            
            "application": {
                "plan": """Tu es un agent d'application. Pour cette idée :

{idee}

Développe un plan de mise en œuvre détaillé avec :
- Objectifs spécifiques
- Étapes concrètes
- Ressources nécessaires
- Timeline réaliste
- Indicateurs de succès""",
                
                "critique_plan": """Tu es un agent critique spécialisé dans l'évaluation de plans. Analyse ce plan :

{plan}

Identifie les lacunes, les risques d'exécution et les points d'amélioration.""",
                
                "defense_plan": """Tu es un agent d'application. Voici ton plan et les critiques :

Plan : {plan}
Critique : {critique}

Défends la viabilité du plan et propose des ajustements pour répondre aux critiques.""",
                
                "revision_plan": """Tu es un agent de révision de plans. En tenant compte de ces éléments :

Plan initial : {plan}
Critiques : {critique}

Propose une version finale optimisée du plan qui intègre les retours constructifs."""
            }
        }
        cls._loaded = True
        logger.info("Prompts par défaut chargés")
    
    @classmethod
    def get_prompt(cls, role: str, prompt_name: str) -> str:
        """
        Récupère un prompt spécifique pour un rôle donné.
        
        Args:
            role: Le rôle de l'agent
            prompt_name: Le nom du prompt
            
        Returns:
            Le template du prompt
            
        Raises:
            KeyError: Si le rôle ou le prompt n'existe pas
        """
        # S'assurer que les prompts sont chargés
        if not cls._loaded:
            cls._load_prompts()
        
        if role not in cls._prompts:
            raise KeyError(f"Rôle inconnu : {role}")
        
        if prompt_name not in cls._prompts[role]:
            raise KeyError(f"Prompt '{prompt_name}' inconnu pour le rôle '{role}'")
        
        return cls._prompts[role][prompt_name]
    
    @classmethod
    def register_prompt(cls, role: str, prompt_name: str, template: str) -> None:
        """
        Enregistre un nouveau prompt ou met à jour un existant.
        
        Args:
            role: Le rôle de l'agent
            prompt_name: Le nom du prompt
            template: Le template du prompt
        """
        # S'assurer que les prompts sont chargés
        if not cls._loaded:
            cls._load_prompts()
            
        if role not in cls._prompts:
            cls._prompts[role] = {}
        
        cls._prompts[role][prompt_name] = template
        logger.info(f"Prompt '{prompt_name}' enregistré pour le rôle '{role}'") 