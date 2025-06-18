"""
Définitions de types pour le système de brainstorming.
"""

from typing import TypedDict, Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class AgentRole(str, Enum):
    """Rôles disponibles pour les agents."""
    CREATIF = "creatif"
    CRITIQUE = "critique"
    REVISION = "revision"
    SYNTHESE = "synthese"
    SCORE = "score"
    APPLICATION = "application"


class ScoreDict(TypedDict):
    """Structure des scores d'évaluation."""
    impact: int
    faisabilite: int
    originalite: int
    clarte: int
    total: int


class CycleLog(TypedDict):
    """Structure d'un log de cycle."""
    cycle: int
    creation: str
    critique: str
    defense: str
    replique: str
    revision: str
    score: ScoreDict


class ApplicationLog(TypedDict):
    """Structure d'un log d'application."""
    idee: str
    plan_initial: str
    critique: str
    defense: str
    revision: str


class BrainstormLog(TypedDict):
    """Structure complète d'un log de brainstorming."""
    objectif: str
    contexte: str
    contraintes: str
    date: str
    logs: List[CycleLog]
    synthese_finale: str
    application: List[ApplicationLog]


@dataclass
class APIUsage:
    """Statistiques d'utilisation de l'API."""
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    cost: float = 0.0
    api_calls: int = 0
    
    def add_call(self, prompt_tokens: int, completion_tokens: int, cost: float):
        """Ajoute les statistiques d'un appel API."""
        self.prompt_tokens += prompt_tokens
        self.completion_tokens += completion_tokens
        self.total_tokens += prompt_tokens + completion_tokens
        self.cost += cost
        self.api_calls += 1


@dataclass
class ModelConfig:
    """Configuration d'un modèle GPT."""
    name: str
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    pricing_input: float = 0.001  # $ per 1000 tokens
    pricing_output: float = 0.002  # $ per 1000 tokens


@dataclass
class BrainstormSession:
    """Session complète de brainstorming."""
    session_id: str
    started_at: datetime
    objectif: str
    contexte: str
    contraintes: str
    cycles: int
    status: str = "running"  # running, completed, failed
    usage: APIUsage = field(default_factory=APIUsage)
    logs: List[CycleLog] = field(default_factory=list)
    synthese: Optional[str] = None
    applications: List[ApplicationLog] = field(default_factory=list)
    ended_at: Optional[datetime] = None
    error: Optional[str] = None
    
    def complete(self):
        """Marque la session comme terminée."""
        self.status = "completed"
        self.ended_at = datetime.now()
    
    def fail(self, error: str):
        """Marque la session comme échouée."""
        self.status = "failed"
        self.error = error
        self.ended_at = datetime.now()
    
    @property
    def duration(self) -> Optional[float]:
        """Retourne la durée de la session en secondes."""
        if self.ended_at:
            return (self.ended_at - self.started_at).total_seconds()
        return None


@dataclass 
class IdeaEvaluation:
    """Évaluation détaillée d'une idée."""
    idea_text: str
    scores: ScoreDict
    strengths: List[str] = field(default_factory=list)
    weaknesses: List[str] = field(default_factory=list)
    improvements: List[str] = field(default_factory=list)
    implementation_plan: Optional[str] = None
    
    @property
    def average_score(self) -> float:
        """Calcule le score moyen."""
        return self.scores["total"] / 4.0 