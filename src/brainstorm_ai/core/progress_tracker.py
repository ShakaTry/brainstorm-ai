"""
Module de suivi et d'affichage de la progression du brainstorm.
Affiche une barre de progression et des indicateurs visuels pour suivre l'avancement.
"""

import sys
import time
from typing import Optional
from .config import config

class ProgressTracker:
    """Gestionnaire de progression pour le brainstorm."""
    
    def __init__(self, total_cycles: int, top_ideas_count: int = 3):
        self.total_cycles = total_cycles
        self.top_ideas_count = top_ideas_count
        self.current_cycle = 0
        self.current_step = 0
        self.current_phase = ""
        self.current_idea = 0
        
        # Calcul du nombre total d'étapes
        # Cycles: 6 étapes par cycle (créatif, critique, défense, réplique, révision, score)
        # Synthèse: 1 étape
        # Idées: 4 étapes par idée (plan, critique, défense, révision)
        # Export: 1 étape
        self.steps_per_cycle = 6
        self.total_steps = (
            self.total_cycles * self.steps_per_cycle +  # Cycles
            1 +  # Synthèse
            self.top_ideas_count * 4 +  # Traitement des idées
            1  # Export
        )
        self.completed_steps = 0
        
        # Suivi des tokens et coûts
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.total_cost = 0.0
        self.session_costs = []  # Liste des coûts par appel
        
        # Emojis et labels pour chaque étape
        self.cycle_steps = [
            ("🎨", "Créatif"),
            ("🔍", "Critique"), 
            ("🛡️", "Défense"),
            ("💬", "Réplique"),
            ("✏️", "Révision"),
            ("📊", "Score")
        ]
        
        self.idea_steps = [
            ("📋", "Plan"),
            ("🔍", "Critique"),
            ("🛡️", "Défense"),
            ("✏️", "Révision")
        ]
    
    def _get_progress_bar(self, width: int = 40) -> str:
        """Génère une barre de progression."""
        filled = int(width * self.completed_steps / self.total_steps)
        bar = "█" * filled + "░" * (width - filled)
        percentage = (self.completed_steps / self.total_steps) * 100
        return f"[{bar}] {percentage:.1f}%"
    
    def add_api_call(self, model: str, input_tokens: int, output_tokens: int):
        """Ajoute un appel API au suivi des coûts."""
        self.total_input_tokens += input_tokens
        self.total_output_tokens += output_tokens
        
        # Calcul du coût de cet appel
        call_cost = config.calculate_cost(model, input_tokens, output_tokens)
        self.total_cost += call_cost
        self.session_costs.append({
            "model": model,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "cost": call_cost
        })
    
    def _get_cost_info(self) -> str:
        """Génère l'information de coût."""
        if self.total_cost == 0:
            return ""
        
        total_tokens = self.total_input_tokens + self.total_output_tokens
        return f"💰 {total_tokens:,} tokens | ${self.total_cost:.4f}"
    
    def _print_status(self, message: str = ""):
        """Affiche le statut actuel avec la barre de progression."""
        if not config.get("display.show_progress", True):
            return
            
        # Effacer la ligne précédente
        print("\r" + " " * 120 + "\r", end="")
        
        progress_bar = self._get_progress_bar()
        phase_info = f"Phase: {self.current_phase}"
        cost_info = self._get_cost_info()
        
        # Construction de la ligne de status
        parts = [progress_bar, phase_info]
        if cost_info:
            parts.append(cost_info)
        if message:
            parts.append(message)
        
        status_line = " | ".join(parts)
        print(f"\r{status_line}", end="", flush=True)
    
    def start_brainstorm(self):
        """Démarre le suivi de progression."""
        print(f"\n{config.get_emoji('start')} === DÉBUT DU BRAINSTORM ===")
        print(f"📊 Progression totale: {self.total_steps} étapes")
        print(f"🔄 Cycles prévus: {self.total_cycles}")
        print(f"💡 Idées à traiter: {self.top_ideas_count}")
        print()
        self.current_phase = "Initialisation"
        self._print_status("Démarrage...")
        time.sleep(0.5)
    
    def start_cycle(self, cycle_num: int):
        """Démarre un nouveau cycle."""
        self.current_cycle = cycle_num
        self.current_step = 0
        self.current_phase = f"Cycle {cycle_num}/{self.total_cycles}"
        print(f"\n\n{config.get_emoji('cycle')} === CYCLE {cycle_num} ===")
        self._print_status()
    
    def start_cycle_step(self, step_num: int):
        """Démarre une étape du cycle."""
        self.current_step = step_num
        emoji, label = self.cycle_steps[step_num]
        self.current_phase = f"Cycle {self.current_cycle}/{self.total_cycles} - {label}"
        self._print_status(f"{emoji} {label}...")
    
    def complete_cycle_step(self, step_num: int):
        """Complète une étape du cycle."""
        self.completed_steps += 1
        emoji, label = self.cycle_steps[step_num]
        self._print_status(f"{emoji} {label} ✓")
        time.sleep(0.2)
    
    def start_synthesis(self):
        """Démarre la phase de synthèse."""
        self.current_phase = "Synthèse finale"
        print(f"\n\n{config.get_emoji('synthese')} === SYNTHÈSE FINALE ===")
        self._print_status("🔄 Génération de la synthèse...")
    
    def complete_synthesis(self):
        """Complète la synthèse."""
        self.completed_steps += 1
        self._print_status("✅ Synthèse terminée")
        time.sleep(0.2)
    
    def start_idea_processing(self, total_ideas: int):
        """Démarre le traitement des idées."""
        self.top_ideas_count = total_ideas
        self.current_idea = 0
        self.current_phase = f"Traitement des idées (0/{total_ideas})"
        print(f"\n\n{config.get_emoji('application')} === TRAITEMENT DES IDÉES ===")
        self._print_status()
    
    def start_idea(self, idea_num: int, idea_text: str):
        """Démarre le traitement d'une idée."""
        self.current_idea = idea_num
        self.current_phase = f"Idée {idea_num}/{self.top_ideas_count}"
        idea_preview = idea_text[:50] + "..." if len(idea_text) > 50 else idea_text
        print(f"\n💡 Traitement de l'idée {idea_num}: {idea_preview}")
        self._print_status()
    
    def start_idea_step(self, step_num: int):
        """Démarre une étape du traitement d'idée."""
        emoji, label = self.idea_steps[step_num]
        self.current_phase = f"Idée {self.current_idea}/{self.top_ideas_count} - {label}"
        self._print_status(f"{emoji} {label}...")
    
    def complete_idea_step(self, step_num: int):
        """Complète une étape du traitement d'idée."""
        self.completed_steps += 1
        emoji, label = self.idea_steps[step_num]
        self._print_status(f"{emoji} {label} ✓")
        time.sleep(0.2)
    
    def start_export(self):
        """Démarre l'export."""
        self.current_phase = "Export"
        self._print_status("💾 Export des résultats...")
    
    def complete_export(self):
        """Complète l'export."""
        self.completed_steps += 1
        self._print_status("💾 Export terminé ✓")
        time.sleep(0.2)
    
    def finish(self):
        """Termine le suivi de progression."""
        print(f"\n\n{config.get_emoji('success')} === BRAINSTORM TERMINÉ ===")
        print(f"✅ Toutes les étapes ont été complétées avec succès!")
        print(f"📊 {self.completed_steps}/{self.total_steps} étapes accomplies")
        
        # Affichage du résumé des coûts
        if self.total_cost > 0:
            print(f"\n💰 === RÉSUMÉ DES COÛTS ===")
            print(f"📝 Total d'appels API: {len(self.session_costs)}")
            print(f"🔤 Tokens d'entrée: {self.total_input_tokens:,}")
            print(f"🔤 Tokens de sortie: {self.total_output_tokens:,}")
            print(f"🔤 Tokens totaux: {self.total_input_tokens + self.total_output_tokens:,}")
            print(f"💵 Coût total: ${self.total_cost:.4f}")
            
            # Affichage par modèle
            model_costs = {}
            for call in self.session_costs:
                model = call["model"]
                if model not in model_costs:
                    model_costs[model] = {"calls": 0, "cost": 0.0}
                model_costs[model]["calls"] += 1
                model_costs[model]["cost"] += call["cost"]
            
            if len(model_costs) > 1:
                print(f"\n📊 Répartition par modèle:")
                for model, stats in model_costs.items():
                    print(f"   • {model}: {stats['calls']} appels - ${stats['cost']:.4f}")
    
    def get_cost_summary(self) -> dict:
        """Retourne un résumé des coûts."""
        return {
            "total_calls": len(self.session_costs),
            "total_input_tokens": self.total_input_tokens,
            "total_output_tokens": self.total_output_tokens,
            "total_tokens": self.total_input_tokens + self.total_output_tokens,
            "total_cost": self.total_cost,
            "session_costs": self.session_costs
        }
    
    def update_total_ideas(self, count: int):
        """Met à jour le nombre total d'idées (utile si extrait différemment)."""
        old_idea_steps = self.top_ideas_count * 4
        new_idea_steps = count * 4
        self.total_steps = self.total_steps - old_idea_steps + new_idea_steps
        self.top_ideas_count = count 