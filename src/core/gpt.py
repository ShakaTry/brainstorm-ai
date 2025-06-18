import os
import time
import logging
from typing import Optional, Dict, Any
from functools import lru_cache
from openai import OpenAI
from core.config import config

logger = logging.getLogger(__name__)


class GPTClient:
    """Singleton pour gérer le client OpenAI et les statistiques."""
    
    _instance = None
    _client = None
    _total_tokens = {"prompt": 0, "completion": 0}
    _total_cost = 0.0
    _api_calls = 0
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._client is None:
            self._initialize_client()
    
    def _initialize_client(self):
        """Initialise le client OpenAI une seule fois."""
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("La clé API OpenAI n'est pas configurée dans OPENAI_API_KEY")
        
        self._client = OpenAI(api_key=api_key)
        logger.info("Client OpenAI initialisé avec succès")
    
    @property
    def client(self) -> OpenAI:
        """Retourne le client OpenAI."""
        if self._client is None:
            self._initialize_client()
        return self._client
    
    def add_usage(self, prompt_tokens: int, completion_tokens: int, cost: float):
        """Ajoute les statistiques d'utilisation."""
        self._total_tokens["prompt"] += prompt_tokens
        self._total_tokens["completion"] += completion_tokens
        self._total_cost += cost
        self._api_calls += 1
    
    def get_stats(self) -> Dict[str, Any]:
        """Retourne les statistiques d'utilisation."""
        return {
            "total_tokens": self._total_tokens["prompt"] + self._total_tokens["completion"],
            "prompt_tokens": self._total_tokens["prompt"],
            "completion_tokens": self._total_tokens["completion"],
            "total_cost": round(self._total_cost, 4),
            "api_calls": self._api_calls
        }
    
    def reset_stats(self):
        """Réinitialise les statistiques."""
        self._total_tokens = {"prompt": 0, "completion": 0}
        self._total_cost = 0.0
        self._api_calls = 0


# Instance globale du client
_gpt_client = GPTClient()


def gpt(prompt: str, role: str, model_override: Optional[str] = None, 
        temperature: Optional[float] = None, max_retries: Optional[int] = None) -> str:
    """
    Fonction centrale pour appeler l'API GPT avec retry et calcul des coûts.
    
    Args:
        prompt: Le prompt à envoyer à l'API
        role: Le rôle de l'agent (creatif, critique, revision, etc.)
        model_override: Permet de forcer un modèle spécifique (optionnel)
        temperature: Température du modèle (par défaut selon la config du rôle)
        max_retries: Nombre de tentatives (par défaut selon la config)
        
    Returns:
        Le contenu de la réponse de l'API
    """
    # Configuration
    model = model_override if model_override else config.get_model_for_role(role)
    if temperature is None:
        temperature = config.get_temperature_for_role(role)
    if max_retries is None:
        max_retries = config.max_retries
    
    # Retry avec backoff exponentiel
    last_error = None
    for attempt in range(max_retries):
        try:
            logger.debug(f"Appel GPT - Modèle: {model}, Rôle: {role}, Tentative: {attempt + 1}/{max_retries}")
            
            # Appel à l'API OpenAI
            response = _gpt_client.client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature
            )
            
            # Extraction des statistiques
            usage = response.usage
            prompt_tokens = usage.prompt_tokens if usage else 0
            completion_tokens = usage.completion_tokens if usage else 0
            
            # Calcul du coût
            cost = config.calculate_cost(model, prompt_tokens, completion_tokens)
            
            # Mise à jour des statistiques
            _gpt_client.add_usage(prompt_tokens, completion_tokens, cost)
            
            logger.info(f"Appel GPT réussi - Tokens: {prompt_tokens}+{completion_tokens}, Coût: ${cost:.4f}")
            
            # Retourner uniquement le contenu de la réponse
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            last_error = e
            logger.warning(f"Erreur GPT tentative {attempt + 1}/{max_retries}: {str(e)}")
            
            if attempt < max_retries - 1:
                # Backoff exponentiel
                delay = config.retry_delay_base ** attempt
                logger.debug(f"Attente de {delay}s avant nouvelle tentative...")
                time.sleep(delay)
            else:
                # Dernière tentative échouée
                logger.error(f"Échec définitif après {max_retries} tentatives")
                raise Exception(f"Échec GPT après {max_retries} tentatives: {str(last_error)}")


def get_gpt_stats() -> Dict[str, Any]:
    """Retourne les statistiques globales d'utilisation de l'API."""
    return _gpt_client.get_stats()


def reset_gpt_stats():
    """Réinitialise les statistiques d'utilisation."""
    _gpt_client.reset_stats()
    logger.info("Statistiques GPT réinitialisées")


@lru_cache(maxsize=128)
def estimate_tokens(text: str) -> int:
    """
    Estime le nombre de tokens dans un texte (approximation).
    
    Règle approximative : ~1 token pour 4 caractères en français.
    """
    return len(text) // 4 