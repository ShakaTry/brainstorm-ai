#!/usr/bin/env python3
"""
Script de démonstration du système de progression visuelle.
Simule un brainstorm complet pour montrer l'affichage de progression.
"""

import time
import random
from brainstorm_ai.core.progress_tracker import ProgressTracker
from brainstorm_ai.core.config import config

def simulate_gpt_call(min_delay=0.5, max_delay=2.0, progress_tracker=None):
    """Simule un appel GPT avec un délai aléatoire et suivi des tokens."""
    delay = random.uniform(min_delay, max_delay)
    
    # Simulation des tokens
    input_tokens = random.randint(1500, 3000)
    output_tokens = random.randint(400, 1200)
    model = "gpt-4o"  # Modèle par défaut pour la simulation
    
    # Ajouter au tracker si disponible
    if progress_tracker:
        progress_tracker.add_api_call(model, input_tokens, output_tokens)
    
    time.sleep(delay)
    return f"Résultat simulé (délai: {delay:.1f}s, tokens: {input_tokens+output_tokens})"

def demo_brainstorm_progression():
    """Démonstration complète du système de progression."""
    
    print("🚀 === DÉMONSTRATION DU SYSTÈME DE PROGRESSION ===\n")
    
    # Configuration de démonstration
    cycles = 2  # Réduire pour la démo
    top_ideas_count = 2  # Réduire pour la démo
    
    # Affichage de l'estimation du coût
    cost_estimate = config.estimate_total_cost(cycles, top_ideas_count)
    print(f"💰 === ESTIMATION DU COÛT (SIMULATION) ===")
    print(f"📞 Appels API prévus: {cost_estimate['total_calls']}")
    print(f"💵 Coût estimé: ${cost_estimate['total_cost']:.4f}")
    
    print(f"\n📊 Configuration de la démo:")
    print(f"   • {cycles} cycles de brainstorming")
    print(f"   • {top_ideas_count} idées finales")
    print(f"   • Total d'étapes prévues: {cycles * 6 + 1 + top_ideas_count * 4 + 1}")
    
    print(f"\n⏳ Démarrage dans 3 secondes...")
    time.sleep(3)
    
    # Initialiser le tracker
    progress_tracker = ProgressTracker(cycles, top_ideas_count)
    progress_tracker.start_brainstorm()
    
    # Simuler les cycles de brainstorming
    for cycle_num in range(1, cycles + 1):
        progress_tracker.start_cycle(cycle_num)
        
        # Simuler chaque étape du cycle
        for step_num in range(6):  # 6 étapes par cycle
            progress_tracker.start_cycle_step(step_num)
            simulate_gpt_call(0.3, 1.0, progress_tracker)  # Plus rapide pour la démo
            progress_tracker.complete_cycle_step(step_num)
    
    # Simuler la synthèse
    progress_tracker.start_synthesis()
    simulate_gpt_call(1.0, 2.0, progress_tracker)
    progress_tracker.complete_synthesis()
    
    # Simuler le traitement des idées
    progress_tracker.start_idea_processing(top_ideas_count)
    
    idees_demo = [
        "Plateforme collaborative de co-création urbaine avec IA distribuée",
        "Réseau de capteurs citoyens pour la gouvernance participative"
    ]
    
    for idx, idee in enumerate(idees_demo, 1):
        progress_tracker.start_idea(idx, idee)
        
        # Simuler les 4 étapes du traitement d'idée
        for step_num in range(4):
            progress_tracker.start_idea_step(step_num)
            simulate_gpt_call(0.5, 1.5, progress_tracker)
            progress_tracker.complete_idea_step(step_num)
    
    # Simuler l'export
    progress_tracker.start_export()
    time.sleep(0.5)
    progress_tracker.complete_export()
    
    # Terminer
    progress_tracker.finish()
    
    print("\n\n🎉 Démonstration terminée !")
    print("✨ Le système de progression est maintenant intégré dans votre brainstorm.")
    print("\n📝 Fonctionnalités ajoutées :")
    print("   • Barre de progression en temps réel")
    print("   • Indicateurs visuels pour chaque étape")
    print("   • Suivi du cycle et de la phase en cours")
    print("   • Pourcentage d'avancement global")
    print("   • 💰 Suivi des tokens et coût en temps réel")
    print("   • 📊 Estimation du coût total avant démarrage")
    print("   • 📈 Résumé détaillé des coûts en fin de session")
    print("   • Émojis pour une meilleure lisibilité")

def show_configuration_options():
    """Affiche les options de configuration disponibles."""
    print("\n⚙️ === OPTIONS DE CONFIGURATION ===")
    print("\nDans votre config.yaml, vous pouvez personnaliser :")
    print("• display.show_progress: true/false - Activer/désactiver la progression")
    print("• display.use_emojis: true/false - Activer/désactiver les emojis")
    print("• display.emojis.* - Personnaliser les emojis utilisés")
    
    print(f"\n📊 Configuration actuelle :")
    print(f"   • Progression activée: {config.get('display.show_progress', True)}")
    print(f"   • Emojis activés: {config.get('display.use_emojis', True)}")
    print(f"   • Usage des tokens affiché: {config.show_token_usage}")

if __name__ == "__main__":
    try:
        demo_brainstorm_progression()
        show_configuration_options()
    except KeyboardInterrupt:
        print("\n\n⏹️ Démonstration interrompue par l'utilisateur.")
    except Exception as e:
        print(f"\n❌ Erreur lors de la démonstration : {e}") 