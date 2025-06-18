#!/usr/bin/env python3
"""
Script de debug pour vérifier la configuration et diagnostiquer les problèmes.
"""

from core.config import config
import datetime

def debug_config():
    """Debug de la configuration."""
    print("🔍 === DEBUG DE LA CONFIGURATION ===\n")
    
    # Forcer le rechargement
    print("🔄 Rechargement forcé de la configuration...")
    config.reload_config()
    print("✅ Configuration rechargée\n")
    
    # Vérifier le pattern log_filename
    print("📝 === PATTERN LOG FILENAME ===")
    pattern = config.get("export.log_filename_pattern", "NOT FOUND")
    print(f"Pattern configuré: '{pattern}'")
    
    # Tester la génération du nom de fichier
    print("\n🧪 === TEST GÉNÉRATION NOM FICHIER ===")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    print(f"Timestamp: {timestamp}")
    
    try:
        log_filename = config.get_log_filename(timestamp)
        print(f"✅ Nom de fichier généré: '{log_filename}'")
    except Exception as e:
        print(f"❌ Erreur génération nom: {e}")
        print(f"Type d'erreur: {type(e).__name__}")
    
    # Vérifier d'autres paramètres importants
    print(f"\n⚙️ === AUTRES PARAMÈTRES ===")
    print(f"Cycles: {config.cycles}")
    print(f"Top ideas count: {config.top_ideas_count}")
    print(f"Logs dir: {config.logs_dir}")
    print(f"Exports dir: {config.exports_dir}")
    
    # Vérifier les formats d'export
    print(f"\n📁 === FORMATS D'EXPORT ===")
    formats = ["yaml", "json", "markdown"]
    for fmt in formats:
        enabled = config.should_export_format(fmt)
        print(f"{fmt}: {'✅' if enabled else '❌'}")
    
    # Vérifier l'export des idées individuelles
    save_individual = config.get("export.save_individual_ideas", False)
    print(f"\n💡 Sauvegarder idées individuelles: {'✅' if save_individual else '❌'}")
    
    # Tester le calcul de coût
    print(f"\n💰 === TEST CALCUL COÛT ===")
    try:
        cost_estimate = config.estimate_total_cost(3, 5)
        print(f"✅ Estimation coût: ${cost_estimate['total_cost']:.4f}")
        print(f"   Appels prévus: {cost_estimate['total_calls']}")
    except Exception as e:
        print(f"❌ Erreur calcul coût: {e}")

if __name__ == "__main__":
    try:
        debug_config()
    except Exception as e:
        print(f"\n💥 ERREUR CRITIQUE: {e}")
        print(f"Type: {type(e).__name__}")
        import traceback
        traceback.print_exc() 