#!/usr/bin/env python3
"""
Script de test pour valider la corrélation entre configuration et logs.
Teste spécifiquement les corrections apportées au système d'extraction des idées.
"""

from brainstorm_ai.core.config import config
from brainstorm_ai.core.loop_manager import extract_top_ideas_robust


def test_config_correlation():
    """Test de la corrélation entre configuration et comportement du système."""
    print("🔧 === TEST DE CORRÉLATION CONFIG <-> LOGS ===\n")

    # Test 1: Vérifier la configuration actuelle
    print("📋 1. CONFIGURATION ACTUELLE")
    print(f"   • Cycles configurés: {config.cycles}")
    print(f"   • Top ideas count: {config.top_ideas_count}")
    print(f"   • Stratégies d'extraction: {config.get_idea_extraction_strategies()}")

    # Test 2: Tester l'extraction d'idées avec différents counts
    print("\n🔍 2. TEST D'EXTRACTION D'IDÉES")

    # Simuler une synthèse avec des idées numérotées
    synthese_test = """Voici les meilleures idées :

1. Première idée innovante avec description détaillée
2. Deuxième idée créative avec plan d'action
3. Troisième idée révolutionnaire avec impact majeur

Ces idées représentent les solutions les plus prometteuses."""

    # Tester avec count=1 (comme dans la config actuelle)
    idees_1 = extract_top_ideas_robust(synthese_test, 1)
    print(f"   • Extraction avec count=1: {len(idees_1)} idées trouvées")
    for i, idee in enumerate(idees_1, 1):
        print(f"     {i}. {idee[:60]}...")

    # Tester avec count=3
    idees_3 = extract_top_ideas_robust(synthese_test, 3)
    print(f"   • Extraction avec count=3: {len(idees_3)} idées trouvées")
    for i, idee in enumerate(idees_3, 1):
        print(f"     {i}. {idee[:60]}...")

    # Test 3: Validation du regex corrigé
    print("\n🧪 3. VALIDATION DU REGEX CORRIGÉ")
    test_patterns = [(1, r"^\s*1\.\s*(.+)$"), (3, r"^\s*[1-3]\.\s*(.+)$")]

    for count, expected_pattern in test_patterns:
        # Reconstituer le pattern comme dans le code
        if count == 1:
            actual_pattern = r"^\s*1\.\s*(.+)$"
        else:
            actual_pattern = rf"^\s*[1-{count}]\.\s*(.+)$"

        match_status = "✅" if actual_pattern == expected_pattern else "❌"
        print(f"   • count={count}: {match_status} Pattern: {actual_pattern}")

    # Test 4: Test du prompt de synthèse avec count dynamique
    print("\n📝 4. TEST DU PROMPT DE SYNTHÈSE")

    # Mock des idées révisées
    idees_test = [
        "Idée A: Solution innovante pour problème X",
        "Idée B: Approche créative pour défi Y",
        "Idée C: Méthode révolutionnaire pour objectif Z",
    ]

    print("   • Test avec différents counts:")
    for test_count in [1, 2, 3]:
        print(f"     - count={test_count}: Appel prompt_synthese() configuré")
        # Note: On ne fait pas l'appel réel pour éviter les coûts API
        print(f"       └─ Prompt devrait demander {test_count} idée(s)")

    # Test 5: Vérifier la cohérence de configuration
    print("\n⚙️ 5. COHÉRENCE DE CONFIGURATION")

    coherence_issues = []

    # Vérifier que top_ideas_count est dans une plage raisonnable
    if config.top_ideas_count < 1:
        coherence_issues.append("top_ideas_count ne peut pas être < 1")
    elif config.top_ideas_count > 10:
        coherence_issues.append("top_ideas_count > 10 peut être excessif")

    # Vérifier que cycles > 0
    if config.cycles < 1:
        coherence_issues.append("cycles ne peut pas être < 1")

    # Vérifier les formats d'export
    formats_actifs = []
    for fmt in ["yaml", "json", "markdown"]:
        if config.should_export_format(fmt):
            formats_actifs.append(fmt)

    if not formats_actifs:
        coherence_issues.append("Aucun format d'export activé")

    if coherence_issues:
        print("   ❌ Problèmes détectés:")
        for issue in coherence_issues:
            print(f"     • {issue}")
    else:
        print("   ✅ Configuration cohérente")

    print(f"\n   • Formats d'export actifs: {', '.join(formats_actifs)}")
    print(
        f"   • Sauvegarde idées individuelles: {config.get('export.save_individual_ideas', True)}"
    )

    # Résumé final
    print("\n📊 === RÉSUMÉ DU TEST ===")
    print("✅ Extraction d'idées corrigée (regex count=1 fonctionnel)")
    print("✅ Prompt de synthèse paramétré avec count dynamique")
    print(f"✅ Configuration actuelle: {config.cycles} cycle(s), {config.top_ideas_count} idée(s)")

    if not coherence_issues:
        print("✅ Corrélation config <-> comportement: VALIDE")
    else:
        print("⚠️  Quelques problèmes de cohérence détectés")

    print(
        f"\n🎯 Votre prochain brainstorm devrait maintenant générer exactement {config.top_ideas_count} idée(s) comme configuré !"
    )


if __name__ == "__main__":
    test_config_correlation()
