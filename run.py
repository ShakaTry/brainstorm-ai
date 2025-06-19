#!/usr/bin/env python3
"""
🚀 Script de lancement rapide pour Brainstorm AI
Usage: python run.py
"""

import os
import sys
from pathlib import Path

def check_requirements():
    """Vérifie les prérequis de base."""
    print("🔍 Vérification des prérequis...")
    
    # Vérifier Python
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ requis. Version actuelle:", sys.version)
        return False
    print("✅ Python version OK")
    
    # Vérifier la clé API
    if not os.environ.get("OPENAI_API_KEY"):
        print("❌ Clé API OpenAI manquante !")
        print("💡 Configurez-la avec :")
        print("   Windows: set OPENAI_API_KEY=votre-clé")
        print("   Linux/Mac: export OPENAI_API_KEY=votre-clé")
        return False
    print("✅ Clé API OpenAI configurée")
    
    # Vérifier que le module est installé
    try:
        import brainstorm_ai
        print("✅ Module brainstorm_ai installé")
    except ImportError:
        print("❌ Module brainstorm_ai non installé !")
        print("💡 Installez-le avec : pip install -e .")
        return False
    
    return True

def quick_start():
    """Lance le brainstorm avec une interface simplifiée."""
    print("\n🧠 === BRAINSTORM AI - DÉMARRAGE RAPIDE ===\n")
    
    print("📝 Remplissez les informations suivantes (appuyez sur Entrée pour les valeurs par défaut) :\n")
    
    # Inputs utilisateur avec valeurs par défaut
    objectif = input("🎯 Objectif (que voulez-vous créer/résoudre ?) : ").strip()
    if not objectif:
        objectif = "Créer une solution innovante"
        print(f"   → Utilisation de l'objectif par défaut : {objectif}")
    
    contexte = input("🌍 Contexte (environnement, marché, situation) : ").strip()
    if not contexte:
        contexte = "Marché concurrentiel nécessitant de l'innovation"
        print(f"   → Utilisation du contexte par défaut : {contexte}")
    
    contraintes = input("⚠️  Contraintes (budget, temps, ressources) : ").strip()
    if not contraintes:
        contraintes = "Ressources limitées, besoin d'efficacité"
        print(f"   → Utilisation des contraintes par défaut : {contraintes}")
    
    cycles = input("🔄 Nombre de cycles (3 par défaut) : ").strip()
    if not cycles or not cycles.isdigit():
        cycles = "3"
        print(f"   → Utilisation de {cycles} cycles")
    
    # Lancement du brainstorm
    print(f"\n🚀 Lancement du brainstorm...")
    print(f"⏱️  Durée estimée : {int(cycles) * 2}-{int(cycles) * 3} minutes")
    print(f"💰 Coût estimé : $0.50-$2.00 (selon la complexité)\n")
    
    # Import et lancement
    try:
        from brainstorm_ai.cli.main import run_brainstorm
        run_brainstorm(
            objectif=objectif,
            contexte=contexte,
            contraintes=contraintes,
            cycles=int(cycles)
        )
    except Exception as e:
        print(f"❌ Erreur lors du lancement : {e}")
        print("💡 Essayez : python main.py")
        return False
    
    print("\n🎉 Brainstorm terminé !")
    print("📁 Retrouvez vos résultats dans :")
    print("   • data/logs/ (logs complets)")
    print("   • data/exports/ (idées individuelles)")
    
    return True

def main():
    """Fonction principale."""
    print("🚀 Brainstorm AI - Lancement Rapide")
    print("=" * 50)
    
    if not check_requirements():
        print("\n❌ Prérequis non satisfaits. Consultez QUICK_START.md pour l'installation.")
        sys.exit(1)
    
    try:
        quick_start()
    except KeyboardInterrupt:
        print("\n\n⏹️  Brainstorm interrompu par l'utilisateur.")
    except Exception as e:
        print(f"\n❌ Erreur inattendue : {e}")
        print("💡 Consultez la documentation ou lancez : python main.py")

if __name__ == "__main__":
    main() 