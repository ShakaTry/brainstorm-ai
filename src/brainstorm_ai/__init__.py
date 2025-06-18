"""
Brainstorm AI - Système de brainstorming intelligent
"""

__version__ = "2.1.0"
__author__ = "Brainstorm AI Team"

from .core import Config
from .agents import (
    AgentCreatif,
    AgentCritique,
    AgentRevision,
    AgentSynthese,
    AgentApplication,
    AgentScore
)

__all__ = [
    "Config",
    "AgentCreatif",
    "AgentCritique", 
    "AgentRevision",
    "AgentSynthese",
    "AgentApplication",
    "AgentScore"
] 