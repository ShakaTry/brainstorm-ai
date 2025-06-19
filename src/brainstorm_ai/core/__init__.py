"""
Module core du système de brainstorming.

Ce module contient toutes les fonctionnalités centrales :
- Configuration système
- Client GPT et gestion des tokens
- Gestionnaire de boucles de brainstorming
- Exportateurs de données
- Suivi de progression
- Types et utilitaires
"""

from .config import Config, config

# from .loop_manager import run_brainstorm_loop  # Removed to prevent circular import
from .exporter import export_json, export_markdown, export_yaml
from .gpt import GPTClient, get_gpt_stats, gpt, reset_gpt_stats
from .progress_tracker import ProgressTracker
from .types import ApplicationLog, BrainstormLog, CycleLog, ScoreDict
from .utils import dedupe

__all__ = [
    # Configuration
    "Config",
    "config",
    # GPT
    "gpt",
    "get_gpt_stats",
    "reset_gpt_stats",
    "GPTClient",
    # Loop Manager
    # 'run_brainstorm_loop',  # Removed to prevent circular import
    # Exporters
    "export_yaml",
    "export_json",
    "export_markdown",
    # Progress
    "ProgressTracker",
    # Utils
    "dedupe",
    # Types
    "ScoreDict",
    "CycleLog",
    "ApplicationLog",
    "BrainstormLog",
]
