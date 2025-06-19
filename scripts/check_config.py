#!/usr/bin/env python3
"""
Script de vérification de la configuration du système.
Usage: python -m scripts.check_config
"""

try:
    from brainstorm_ai.core.config import config
except ImportError:
    print("❌ Erreur: Impossible d'importer brainstorm_ai")
    print("   Assurez-vous d'exécuter ce script depuis la racine du projet avec:")
    print("   python -m scripts.check_config")
    print("   ou installez le projet avec: pip install -e .")
    exit(1)

def test_configuration():
    print("🧪 Test de la configuration du système de brainstorming IA\n")
    
    # Vérifier la clé API
    import os
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key:
        print(f"✅ Clé API OpenAI détectée : {'*' * 10}{api_key[-4:]}")
    else:
        print("⚠️  Clé API OpenAI non détectée dans les variables d'environnement")
    
    # Test de la configuration générale
    print("1. Configuration générale:")
    print(f"   - Objectif: {config.objectif}")
    print(f"   - Contexte: {config.contexte}")
    print(f"   - Contraintes: {config.contraintes}")
    print(f"   - Cycles: {config.cycles}")
    print(f"   - Nombre d'idées top: {config.top_ideas_count}")
    print(f"   - Demander confirmation: {config.ask_confirmation}")
    
    # Test de la configuration des agents
    print("\n2. Configuration des agents:")
    for role in ["creatif", "critique", "revision", "synthese", "score", "application"]:
        model = config.get_model_for_role(role)
        temp = config.get_temperature_for_role(role)
        print(f"   - {role}: {model} (température: {temp})")
    
    # Test de la configuration API
    print("\n3. Configuration API:")
    print(f"   - Max retries: {config.max_retries}")
    print(f"   - Retry delay base: {config.retry_delay_base}")
    print(f"   - Max context chars: {config.max_context_chars}")
    
    # Test de la configuration d'export
    print("\n4. Configuration d'export:")
    print(f"   - Répertoire logs: {config.logs_dir}")
    print(f"   - Répertoire exports: {config.exports_dir}")
    print(f"   - Formats activés:")
    for format_name in ["yaml", "json", "markdown"]:
        print(f"     * {format_name}: {config.should_export_format(format_name)}")
    
    # Test de la configuration d'affichage
    print("\n5. Configuration d'affichage:")
    print(f"   - Utiliser emojis: {config.get('display.use_emojis', True)}")
    print(f"   - Afficher tokens: {config.show_token_usage}")
    if config.get('display.use_emojis', True):
        print("   - Exemples d'emojis:")
        for emoji_name in ["creatif", "critique", "synthese"]:
            print(f"     * {emoji_name}: {config.get_emoji(emoji_name)}")
    
    # Test de la configuration avancée
    print("\n6. Configuration avancée:")
    print(f"   - Stratégies d'extraction: {config.get_idea_extraction_strategies()}")
    score_config = config.get_score_validation_config()
    print(f"   - Validation des scores:")
    print(f"     * Valeurs: {score_config['min_value']}-{score_config['max_value']}")
    print(f"     * Clés requises: {score_config['required_keys']}")
    print(f"     * Valeur fallback: {score_config['fallback_value']}")
    
    # Test des nouvelles optimizations
    print("\n7. Optimisations:")
    opt_config = config.get_optimization_config()
    print(f"   - Détection redondance: {opt_config['detect_redundancy']}")
    print(f"   - Seuil similarité: {opt_config['similarity_threshold']}")
    print(f"   - Diversité forcée: {opt_config['enforce_diversity']}")
    print(f"   - Longueur min idée: {opt_config['min_idea_length']} mots")
    print(f"   - Bonus originalité: {opt_config['originality_bonus']}x")
    
    print("\n✅ Test terminé avec succès!")

if __name__ == "__main__":
    try:
        test_configuration()
    except Exception as e:
        print(f"\n❌ Erreur lors du test: {e}")
        print("\nVérifiez que le fichier config.yaml existe et est correctement formaté.") 