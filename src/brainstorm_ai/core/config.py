"""
Module de gestion de la configuration centralisée.
Charge et gère les paramètres depuis config.yaml
"""

import logging
import threading
from pathlib import Path
from typing import Any, Optional

import yaml

logger = logging.getLogger(__name__)


class ConfigError(Exception):
    """Exception de base pour les erreurs de configuration."""

    pass


class ConfigFileError(ConfigError):
    """Exception levée pour les erreurs liées aux fichiers de configuration."""

    pass


class ConfigValidationError(ConfigError):
    """Exception levée pour les erreurs de validation de configuration."""

    pass


class Config:
    """Gestionnaire de configuration singleton thread-safe."""

    _instance = None
    _lock = threading.Lock()
    _config = None
    _initialized = False

    def __new__(cls):
        # Double-checked locking pattern pour thread-safety
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        # S'assurer que l'initialisation ne se fait qu'une fois avec protection thread-safe
        with self._lock:
            if not Config._initialized:
                self.load_config()
                Config._initialized = True

    def load_config(self, config_path: Optional[str] = None):
        """
        Charge la configuration depuis un fichier YAML.

        Args:
            config_path: Chemin vers le fichier de configuration (optionnel)

        Raises:
            ConfigFileError: Si le fichier n'est pas trouvé ou illisible
            ConfigValidationError: Si le fichier YAML est invalide ou incomplet
        """
        if config_path is None:
            # Chercher config.yaml dans le dossier config
            config_path = Path(__file__).parent.parent.parent.parent / "config" / "config.yaml"

        config_path = Path(config_path)
        logger.info(f"Chargement de la configuration depuis {config_path}")

        try:
            if not config_path.exists():
                raise ConfigFileError(f"Fichier de configuration non trouvé : {config_path}")

            if not config_path.is_file():
                raise ConfigFileError(f"Le chemin n'est pas un fichier : {config_path}")

            with open(config_path, encoding="utf-8") as f:
                self._config = yaml.safe_load(f)

            if self._config is None:
                raise ConfigValidationError("Le fichier de configuration est vide")

            self._validate_config()
            logger.info("Configuration chargée avec succès")

        except FileNotFoundError as e:
            logger.error(f"Fichier de configuration non trouvé : {config_path}")
            raise ConfigFileError(f"Fichier de configuration non trouvé : {config_path}") from e
        except yaml.YAMLError as e:
            logger.error(f"Erreur de parsing YAML : {e}")
            raise ConfigValidationError(f"Erreur dans le fichier YAML : {e}") from e
        except PermissionError as e:
            logger.error(f"Permission refusée pour lire le fichier : {config_path}")
            raise ConfigFileError(f"Permission refusée : {config_path}") from e
        except Exception as e:
            logger.error(
                f"Erreur inattendue lors du chargement de la configuration : {type(e).__name__}: {e}"
            )
            raise ConfigError(f"Erreur inattendue : {type(e).__name__}: {e}") from e

    def reload_config(self, config_path: Optional[str] = None):
        """Force le rechargement de la configuration."""
        with self._lock:
            self._config = None
            self.load_config(config_path)

    def _validate_config(self):
        """
        Valide que la configuration contient toutes les sections requises.

        Raises:
            ConfigValidationError: Si des sections requises sont manquantes
        """
        required_sections = ["general", "agents", "api", "export", "display"]
        missing_sections = []

        for section in required_sections:
            if section not in self._config:
                missing_sections.append(section)

        if missing_sections:
            raise ConfigValidationError(
                f"Sections requises manquantes dans la configuration : {', '.join(missing_sections)}"
            )

    def get(self, key_path: str, default: Any = None) -> Any:
        """
        Récupère une valeur de configuration avec notation pointée.

        Args:
            key_path: Chemin vers la clé (ex: "agents.models.creatif")
            default: Valeur par défaut si la clé n'existe pas

        Returns:
            La valeur de configuration ou la valeur par défaut
        """
        if self._config is None:
            logger.warning("Configuration non chargée, utilisation de la valeur par défaut")
            return default

        keys = key_path.split(".")
        value = self._config

        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default

        return value

    def get_model_for_role(self, role: str) -> str:
        """Retourne le modèle GPT à utiliser pour un rôle donné."""
        return self.get(f"agents.models.{role}", self.get("agents.models.default", "gpt-4o"))

    def get_temperature_for_role(self, role: str) -> float:
        """Retourne la température à utiliser pour un rôle donné."""
        return self.get(f"agents.temperatures.{role}", self.get("agents.temperatures.default", 0.7))

    def get_emoji(self, name: str) -> str:
        """Retourne l'emoji pour un nom donné, ou une chaîne vide si désactivé."""
        if not self.get("display.use_emojis", True):
            return ""
        return self.get(f"display.emojis.{name}", "")

    @property
    def objectif(self) -> str:
        return self.get("general.objectif", "")

    @property
    def contexte(self) -> str:
        return self.get("general.contexte", "")

    @property
    def contraintes(self) -> str:
        return self.get("general.contraintes", "")

    @property
    def cycles(self) -> int:
        return self.get("general.cycles", 3)

    @property
    def max_context_chars(self) -> int:
        return self.get("agents.max_context_chars", 120000)

    @property
    def max_retries(self) -> int:
        return self.get("api.max_retries", 3)

    @property
    def retry_delay_base(self) -> int:
        return self.get("api.retry_delay_base", 2)

    @property
    def logs_dir(self) -> str:
        return self.get("export.paths.logs_dir", "data/logs")

    @property
    def exports_dir(self) -> str:
        return self.get("export.paths.exports_dir", "data/exports")

    @property
    def top_ideas_count(self) -> int:
        return self.get("general.top_ideas_count", 3)

    @property
    def ask_confirmation(self) -> bool:
        return self.get("general.ask_confirmation", True)

    @property
    def show_token_usage(self) -> bool:
        return self.get("display.show_token_usage", True)

    def get_log_filename(self, timestamp: str) -> str:
        """Génère le nom du fichier de log avec le pattern configuré."""
        pattern = self.get("export.log_filename_pattern", "brainstorm_{timestamp}")
        return pattern.format(timestamp=timestamp)

    def should_export_format(self, format_name: str) -> bool:
        """Vérifie si un format d'export est activé."""
        return self.get(f"export.formats.{format_name}", False)

    def get_idea_extraction_strategies(self) -> list:
        """Retourne les stratégies d'extraction d'idées."""
        return self.get(
            "advanced.idea_extraction_strategies", ["numbered", "starred", "bullet", "fallback"]
        )

    def get_score_validation_config(self) -> dict:
        """Retourne la configuration de validation des scores."""
        return self.get(
            "advanced.score_validation",
            {
                "min_value": 1,
                "max_value": 10,
                "required_keys": ["impact", "faisabilite", "originalite", "clarte"],
                "fallback_value": 6,
            },
        )

    def get_optimization_config(self) -> dict:
        """Retourne la configuration d'optimisation."""
        return self.get(
            "advanced.optimization",
            {
                "detect_redundancy": True,
                "similarity_threshold": 0.8,
                "enforce_diversity": True,
                "min_idea_length": 20,
                "originality_bonus": 1.2,
            },
        )

    @property
    def detect_redundancy(self) -> bool:
        return self.get("advanced.optimization.detect_redundancy", True)

    @property
    def similarity_threshold(self) -> float:
        return self.get("advanced.optimization.similarity_threshold", 0.8)

    @property
    def enforce_diversity(self) -> bool:
        return self.get("advanced.optimization.enforce_diversity", True)

    @property
    def min_idea_length(self) -> int:
        return self.get("advanced.optimization.min_idea_length", 20)

    @property
    def originality_bonus(self) -> float:
        return self.get("advanced.optimization.originality_bonus", 1.2)

    def get_model_pricing(self, model: str) -> dict:
        """Retourne les prix d'un modèle (input/output en $ per 1000 tokens)."""
        return self.get(
            f"api.pricing.{model}",
            {
                "input": 0.001,  # Prix par défaut si non trouvé
                "output": 0.002,
            },
        )

    def calculate_cost(self, model: str, input_tokens: int, output_tokens: int) -> float:
        """Calcule le coût d'un appel API en dollars."""
        pricing = self.get_model_pricing(model)
        input_cost = (input_tokens / 1000) * pricing["input"]
        output_cost = (output_tokens / 1000) * pricing["output"]
        return input_cost + output_cost

    def estimate_total_cost(self, cycles: int, ideas_count: int) -> dict:
        """Estime le coût total d'un brainstorm complet."""
        # Estimation basée sur l'usage moyen observé
        avg_input_per_call = 2000  # tokens d'input moyens par appel
        avg_output_per_call = 800  # tokens d'output moyens par appel

        # Calcul du nombre d'appels total
        calls_per_cycle = 6  # créatif, critique, défense, réplique, révision, score
        synthesis_calls = 1
        idea_calls = ideas_count * 4  # plan, critique, défense, révision par idée

        total_calls = (cycles * calls_per_cycle) + synthesis_calls + idea_calls

        # Estimation par modèle
        estimates = {}
        for role in ["creatif", "critique", "revision", "synthese", "score", "application"]:
            model = self.get_model_for_role(role)
            if model not in estimates:
                estimates[model] = {"calls": 0, "input_tokens": 0, "output_tokens": 0, "cost": 0.0}

        # Répartition des appels par type de modèle
        default_model = self.get_model_for_role("default")

        estimates[default_model]["calls"] = total_calls
        estimates[default_model]["input_tokens"] = total_calls * avg_input_per_call
        estimates[default_model]["output_tokens"] = total_calls * avg_output_per_call
        estimates[default_model]["cost"] = self.calculate_cost(
            default_model,
            estimates[default_model]["input_tokens"],
            estimates[default_model]["output_tokens"],
        )

        return {
            "total_calls": total_calls,
            "estimates": estimates,
            "total_cost": sum(est["cost"] for est in estimates.values()),
        }


# Instance globale de configuration
config = Config()
