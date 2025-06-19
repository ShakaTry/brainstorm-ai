"""
Module de suivi de progression du brainstorming.
Affiche la progression en temps réel et gère les statistiques.
"""

import logging
import sys
from datetime import datetime
from typing import Any, Dict, List, Optional

from ..core.config import config

logger = logging.getLogger(__name__)


class ProgressTracker:
    """Gestionnaire de suivi de progression pour le brainstorming."""

    def __init__(self, total_cycles: int, top_ideas_count: int):
        """
        Initialise le tracker de progression.

        Args:
            total_cycles: Nombre total de cycles prévus
            top_ideas_count: Nombre d'idées top à traiter
        """
        self.total_cycles = total_cycles
        self.top_ideas_count = top_ideas_count

        # Calcul du nombre total d'étapes
        steps_per_cycle = 5  # création, critique, défense, réplique, révision
        self.total_steps = (total_cycles * steps_per_cycle) + 1 + (top_ideas_count * 4)

        self.completed_steps = 0
        self.current_stage = ""
        self.start_time = datetime.now()
        self.session_costs: List[Dict[str, Any]] = []

        # Stats globales
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.total_cost = 0.0

        # Handler spécial pour la console
        self.console_handler = logging.StreamHandler(sys.stdout)
        self.console_handler.setLevel(logging.INFO)
        formatter = logging.Formatter("%(message)s")
        self.console_handler.setFormatter(formatter)

    def _log_console(self, message: str, level: int = logging.INFO):
        """Affiche un message dans la console et le log."""
        # Log normal
        logger.log(level, message)

        # Affichage console direct pour l'utilisateur
        record = logger.makeRecord(logger.name, level, "", 0, message, (), None)
        self.console_handler.emit(record)

    def update_stage(self, stage: str):
        """Met à jour l'étape actuelle."""
        self.current_stage = stage
        self.completed_steps += 1
        self._display_progress()

    def add_cost(self, model: str, input_tokens: int, output_tokens: int, cost: float):
        """
        Ajoute des statistiques de coût pour un appel API.

        Args:
            model: Le modèle utilisé
            input_tokens: Nombre de tokens d'entrée
            output_tokens: Nombre de tokens de sortie
            cost: Coût en dollars
        """
        self.session_costs.append(
            {
                "model": model,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "cost": cost,
                "timestamp": datetime.now(),
            }
        )

        self.total_input_tokens += input_tokens
        self.total_output_tokens += output_tokens
        self.total_cost += cost

        logger.debug(f"Coût ajouté: {model} - ${cost:.4f} ({input_tokens}+{output_tokens} tokens)")

    def _display_progress(self):
        """Affiche la barre de progression."""
        progress = self.completed_steps / self.total_steps
        bar_length = 50
        filled = int(bar_length * progress)
        bar = "█" * filled + "░" * (bar_length - filled)

        # Efface la ligne précédente
        sys.stdout.write("\r" + " " * 120 + "\r")
        sys.stdout.flush()

        # Temps écoulé
        elapsed = (datetime.now() - self.start_time).total_seconds()
        if elapsed > 0 and progress > 0:
            estimated_total = elapsed / progress
            remaining = estimated_total - elapsed
            time_str = f" | Temps restant: {int(remaining)}s"
        else:
            time_str = ""

        status_line = f"[{bar}] {progress * 100:.1f}% | {self.current_stage}{time_str}"
        sys.stdout.write(f"\r{status_line}")
        sys.stdout.flush()

    def start_brainstorm(self):
        """Marque le début du brainstorming."""
        self._log_console(f"\n{config.get_emoji('start')} === DÉBUT DU BRAINSTORM ===")
        self._log_console(f"📊 Progression totale: {self.total_steps} étapes")
        self._log_console(f"🔄 Cycles prévus: {self.total_cycles}")
        self._log_console(f"💡 Idées à traiter: {self.top_ideas_count}")
        self._log_console("")
        logger.info("Brainstorm démarré")

    def start_cycle(self, cycle_num: int):
        """
        Marque le début d'un cycle.

        Args:
            cycle_num: Numéro du cycle (1-based)
        """
        self._log_console(f"\n\n{config.get_emoji('cycle')} === CYCLE {cycle_num} ===")
        logger.info(f"Début du cycle {cycle_num}")

    def log_step(self, step_name: str, content: str):
        """
        Log une étape avec son contenu.

        Args:
            step_name: Nom de l'étape
            content: Contenu à logger
        """
        # Log complet dans le fichier
        logger.info(f"{step_name}: {content[:500]}...")

        # Version tronquée pour la progression
        self.update_stage(step_name)

    def start_cycle_step(self, step_num: int):
        """
        Marque le début d'une étape de cycle.

        Args:
            step_num: Numéro de l'étape (0-based)
        """
        step_names = ["Créatif", "Critique", "Défense", "Réplique", "Révision", "Score"]
        step_name = step_names[step_num] if step_num < len(step_names) else f"Étape {step_num}"
        self.update_stage(f"Cycle - {step_name}")
        logger.debug(f"Début de l'étape {step_num}: {step_name}")

    def complete_cycle_step(self, step_num: int):
        """
        Marque la fin d'une étape de cycle.

        Args:
            step_num: Numéro de l'étape (0-based)
        """
        step_names = ["Créatif", "Critique", "Défense", "Réplique", "Révision", "Score"]
        step_name = step_names[step_num] if step_num < len(step_names) else f"Étape {step_num}"
        logger.debug(f"Fin de l'étape {step_num}: {step_name}")

    def start_idea_step(self, step_num: int):
        """
        Marque le début d'une étape de traitement d'idée.

        Args:
            step_num: Numéro de l'étape (0-based)
        """
        step_names = ["Plan", "Critique Plan", "Défense Plan", "Révision Plan"]
        step_name = step_names[step_num] if step_num < len(step_names) else f"Étape {step_num}"
        self.update_stage(f"Idée - {step_name}")
        logger.debug(f"Début de l'étape idée {step_num}: {step_name}")

    def complete_idea_step(self, step_num: int):
        """
        Marque la fin d'une étape de traitement d'idée.

        Args:
            step_num: Numéro de l'étape (0-based)
        """
        step_names = ["Plan", "Critique Plan", "Défense Plan", "Révision Plan"]
        step_name = step_names[step_num] if step_num < len(step_names) else f"Étape {step_num}"
        logger.debug(f"Fin de l'étape idée {step_num}: {step_name}")

    def start_idea(self, idea_num: int, idea_text: str):
        """
        Marque le début du traitement d'une idée.

        Args:
            idea_num: Numéro de l'idée
            idea_text: Texte de l'idée
        """
        idea_preview = idea_text[:50] + "..." if len(idea_text) > 50 else idea_text
        self._log_console(f"\n💡 Traitement de l'idée {idea_num}: {idea_preview}")
        logger.info(f"Traitement de l'idée {idea_num}")

    def complete_synthesis(self):
        """Marque la fin de la synthèse."""
        logger.info("Synthèse terminée")

    def start_synthesis(self):
        """Marque le début de la synthèse."""
        self._log_console(f"\n\n{config.get_emoji('synthese')} === SYNTHÈSE FINALE ===")
        logger.info("Début de la synthèse finale")

    def log_synthesis(self, content: str):
        """Log le résultat de la synthèse."""
        logger.info(f"Synthèse: {content}")
        self.update_stage("Synthèse finale")

    def start_application(self):
        """Marque le début du traitement des idées."""
        self._log_console(f"\n\n{config.get_emoji('application')} === TRAITEMENT DES IDÉES ===")
        logger.info("Début du traitement des idées sélectionnées")

    def start_idea_processing(self, total_ideas: int):
        """
        Marque le début du traitement des idées.

        Args:
            total_ideas: Nombre total d'idées à traiter
        """
        self._log_console(f"\n\n{config.get_emoji('application')} === TRAITEMENT DES IDÉES ===")
        self._log_console(f"💡 {total_ideas} idée(s) sélectionnée(s) à développer")
        logger.info(f"Début du traitement de {total_ideas} idées")

    def log_idea_step(self, step_name: str, content: str):
        """
        Log une étape du traitement d'idée.

        Args:
            step_name: Nom de l'étape
            content: Contenu à logger
        """
        logger.info(f"{step_name}: {content[:500]}...")
        self.update_stage(f"Idée - {step_name}")

    def get_cost_by_model(self) -> Dict[str, Dict[str, Any]]:
        """Retourne les statistiques de coût groupées par modèle."""
        model_stats = {}

        for cost_entry in self.session_costs:
            model = cost_entry["model"]
            if model not in model_stats:
                model_stats[model] = {
                    "calls": 0,
                    "input_tokens": 0,
                    "output_tokens": 0,
                    "cost": 0.0,
                }

            model_stats[model]["calls"] += 1
            model_stats[model]["input_tokens"] += cost_entry["input_tokens"]
            model_stats[model]["output_tokens"] += cost_entry["output_tokens"]
            model_stats[model]["cost"] += cost_entry["cost"]

        return model_stats

    def finish_brainstorm(self):
        """Marque la fin du brainstorming et affiche le résumé."""
        self._log_console(f"\n\n{config.get_emoji('success')} === BRAINSTORM TERMINÉ ===")
        self._log_console("✅ Toutes les étapes ont été complétées avec succès!")
        self._log_console(f"📊 {self.completed_steps}/{self.total_steps} étapes accomplies")

        # Affichage des coûts
        if config.show_token_usage:
            self._log_console("\n💰 === RÉSUMÉ DES COÛTS ===")
            self._log_console(f"📝 Total d'appels API: {len(self.session_costs)}")
            self._log_console(f"🔤 Tokens d'entrée: {self.total_input_tokens:,}")
            self._log_console(f"🔤 Tokens de sortie: {self.total_output_tokens:,}")
            self._log_console(
                f"🔤 Tokens totaux: {self.total_input_tokens + self.total_output_tokens:,}"
            )
            self._log_console(f"💵 Coût total: ${self.total_cost:.4f}")

            # Répartition par modèle si plusieurs modèles utilisés
            model_stats = self.get_cost_by_model()
            if len(model_stats) > 1:
                self._log_console("\n📊 Répartition par modèle:")
                for model, stats in model_stats.items():
                    self._log_console(
                        f"   • {model}: {stats['calls']} appels - ${stats['cost']:.4f}"
                    )

        # Log final
        logger.info(f"Brainstorm terminé - Coût total: ${self.total_cost:.4f}")

    def update_total_ideas(self, count: int):
        """
        Met à jour le nombre total d'idées à traiter.

        Args:
            count: Nouveau nombre d'idées
        """
        self.top_ideas_count = count
        logger.debug(f"Nombre d'idées mis à jour: {count}")

    def start_export(self):
        """Marque le début de l'export."""
        self.update_stage("Export")
        logger.info("Début de l'export des résultats")

    def complete_export(self):
        """Marque la fin de l'export."""
        logger.info("Export terminé")

    def finish(self):
        """Alias pour finish_brainstorm()."""
        self.finish_brainstorm()

    def export_session_costs(self) -> List[Dict[str, Any]]:
        """Exporte les données de coût de la session."""
        return self.session_costs.copy()


# Instance globale (sera créée par le loop_manager)
tracker: Optional[ProgressTracker] = None
