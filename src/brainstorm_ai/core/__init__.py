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
from .gpt import gpt, get_gpt_stats, reset_gpt_stats, GPTClient
from .loop_manager import run_brainstorm_loop
from .exporter import export_yaml, export_json, export_markdown
from .progress_tracker import ProgressTracker
from .utils import dedupe
from .types import (
    ScoreDict,
    CycleLog,
    ApplicationLog,
    BrainstormLog
)

__all__ = [
    # Configuration
    'Config',
    'config',
    
    # GPT
    'gpt',
    'get_gpt_stats',
    'reset_gpt_stats',
    'GPTClient',
    
    # Loop Manager
    'run_brainstorm_loop',
    
    # Exporters
    'export_yaml',
    'export_json',
    'export_markdown',
    
    # Progress
    'ProgressTracker',
    
    # Utils
    'dedupe',
    
    # Types
    'ScoreDict',
    'CycleLog',
    'ApplicationLog',
    'BrainstormLog'
] 