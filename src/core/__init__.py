"""
Module principal du système de brainstorming.

Ce module contient les composants centraux :
- Configuration : gestion centralisée des paramètres
- GPT : interface avec l'API OpenAI
- Loop Manager : orchestration du processus de brainstorming
- Exporter : export des résultats dans différents formats
- Progress Tracker : suivi de progression en temps réel
- Utils : fonctions utilitaires
- Types : définitions de types pour la validation
"""

from core.config import Config, config
from core.gpt import gpt, get_gpt_stats, reset_gpt_stats, GPTClient
from core.loop_manager import run_brainstorm_loop
from core.exporter import export_yaml, export_json, export_markdown
from core.progress_tracker import ProgressTracker
from core.utils import dedupe
from core.types import (
    AgentRole,
    ScoreDict,
    CycleLog,
    ApplicationLog,
    BrainstormLog,
    APIUsage,
    ModelConfig,
    BrainstormSession,
    IdeaEvaluation
)

__all__ = [
    # Configuration
    'Config',
    'config',
    
    # GPT Interface
    'gpt',
    'get_gpt_stats',
    'reset_gpt_stats',
    'GPTClient',
    
    # Core Functions
    'run_brainstorm_loop',
    
    # Export
    'export_yaml',
    'export_json',
    'export_markdown',
    
    # Tracking
    'ProgressTracker',
    
    # Utils
    'dedupe',
    
    # Types
    'AgentRole',
    'ScoreDict',
    'CycleLog',
    'ApplicationLog',
    'BrainstormLog',
    'APIUsage',
    'ModelConfig',
    'BrainstormSession',
    'IdeaEvaluation'
] 