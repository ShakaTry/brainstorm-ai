import logging
import os
import time
from functools import lru_cache
from typing import Any, Dict, Optional

from openai import (
    APIConnectionError,
    APIError,
    OpenAI,
    RateLimitError,
    Timeout,
)

from .config import config

logger = logging.getLogger(__name__)


class GPTError(Exception):
    """Exception de base pour les erreurs liées à GPT."""

    pass


class GPTConfigError(GPTError):
    """Exception levée pour les erreurs de configuration GPT."""

    pass


class GPTAPIError(GPTError):
    """Exception levée pour les erreurs d'API GPT."""

    pass


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
            raise GPTConfigError("La clé API OpenAI n'est pas configurée dans OPENAI_API_KEY")

        if not api_key.startswith(("sk-", "sk-proj-")):
            logger.warning("Le format de la clé API OpenAI semble incorrect")

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
            "api_calls": self._api_calls,
        }

    def reset_stats(self):
        """Réinitialise les statistiques."""
        self._total_tokens = {"prompt": 0, "completion": 0}
        self._total_cost = 0.0
        self._api_calls = 0


# Instance globale du client (initialisation lazy)
_gpt_client = None


def get_gpt_client() -> GPTClient:
    """Retourne l'instance GPT client (initialisation lazy)."""
    global _gpt_client
    if _gpt_client is None:
        _gpt_client = GPTClient()
    return _gpt_client


def gpt(
    prompt: str,
    role: str,
    model_override: Optional[str] = None,
    temperature: Optional[float] = None,
    max_retries: Optional[int] = None,
) -> str:
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

    Raises:
        GPTAPIError: En cas d'échec après toutes les tentatives
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
            logger.debug(
                f"Appel GPT - Modèle: {model}, Rôle: {role}, Tentative: {attempt + 1}/{max_retries}"
            )

            # Appel à l'API OpenAI
            client = get_gpt_client()
            response = client.client.chat.completions.create(
                model=model, messages=[{"role": "user", "content": prompt}], temperature=temperature
            )

            # Extraction des statistiques
            usage = response.usage
            prompt_tokens = usage.prompt_tokens if usage else 0
            completion_tokens = usage.completion_tokens if usage else 0

            # Calcul du coût
            cost = config.calculate_cost(model, prompt_tokens, completion_tokens)

            # Mise à jour des statistiques
            client.add_usage(prompt_tokens, completion_tokens, cost)

            logger.info(
                f"Appel GPT réussi - Tokens: {prompt_tokens}+{completion_tokens}, Coût: ${cost:.4f}"
            )

            # Retourner uniquement le contenu de la réponse
            return response.choices[0].message.content.strip()

        except RateLimitError as e:
            last_error = e
            logger.warning(
                f"Limite de taux atteinte, tentative {attempt + 1}/{max_retries}: {str(e)}"
            )
            # Pour les erreurs de rate limit, on attend plus longtemps
            if attempt < max_retries - 1:
                delay = config.retry_delay_base ** (attempt + 1) * 2
                logger.debug(f"Attente de {delay}s avant nouvelle tentative...")
                time.sleep(delay)

        except (APIError, APIConnectionError, Timeout) as e:
            last_error = e
            logger.warning(f"Erreur API tentative {attempt + 1}/{max_retries}: {str(e)}")

            if attempt < max_retries - 1:
                # Backoff exponentiel
                delay = config.retry_delay_base**attempt
                logger.debug(f"Attente de {delay}s avant nouvelle tentative...")
                time.sleep(delay)

        except Exception as e:
            # Pour les erreurs inattendues, on les logue et on les relance
            logger.error(f"Erreur inattendue lors de l'appel GPT: {type(e).__name__}: {str(e)}")
            raise GPTAPIError(f"Erreur inattendue: {type(e).__name__}: {str(e)}") from e

    # Dernière tentative échouée
    logger.error(f"Échec définitif après {max_retries} tentatives")
    raise GPTAPIError(
        f"Échec GPT après {max_retries} tentatives: {type(last_error).__name__}: {str(last_error)}"
    )


def get_gpt_stats() -> Dict[str, Any]:
    """Retourne les statistiques globales d'utilisation de l'API."""
    return get_gpt_client().get_stats()


def reset_gpt_stats():
    """Réinitialise les statistiques d'utilisation."""
    get_gpt_client().reset_stats()
    logger.info("Statistiques GPT réinitialisées")


@lru_cache(maxsize=128)
def estimate_tokens(text: str) -> int:
    """
    Estime le nombre de tokens dans un texte (approximation).

    Règle approximative : ~1 token pour 4 caractères en français.
    """
    return len(text) // 4
