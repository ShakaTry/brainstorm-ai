#!/usr/bin/env python3
"""
Script de test pour vérifier la correction du système d'export.
"""

import os
import tempfile
from pathlib import Path

from brainstorm_ai.core.config import config
from brainstorm_ai.core.loop_manager import save_full_log


def test_export_fix():
    """Test de la correction des exports."""
    print("🧪 === TEST DE CORRECTION DES EXPORTS ===\n")

    # Données de test
    test_objectif = "Créer une solution innovante"
    test_contexte = "Contexte de test"
    test_contraintes = "Contraintes de test"

    # Logs de test simulés
    test_logs = [
        {
            "cycle": 1,
            "creation": "Idée créative test",
            "critique": "Critique de l'idée",
            "defense": "Défense de l'idée",
            "replique": "Réplique",
            "revision": "Révision finale",
            "score": {"impact": 8, "faisabilite": 7, "originalite": 9, "clarte": 8, "total": 32},
        }
    ]

    # Synthèse de test qui contient des idées numérotées
    test_synthese = """Voici les meilleures idées du brainstorm :

1. Plateforme collaborative de co-création urbaine avec IA distribuée
2. Réseau de capteurs citoyens pour la gouvernance participative  
3. Application mobile de participation citoyenne gamifiée

Ces idées représentent les solutions les plus prometteuses."""

    # Créer un répertoire temporaire pour les tests
    with tempfile.TemporaryDirectory() as temp_dir:
        # Rediriger temporairement les exports vers le répertoire de test
        original_exports_dir = config.exports_dir
        original_logs_dir = config.logs_dir

        config._config["export"]["paths"]["exports_dir"] = os.path.join(temp_dir, "exports")
        config._config["export"]["paths"]["logs_dir"] = os.path.join(temp_dir, "logs")

        print(f"📁 Répertoire de test: {temp_dir}")
        print(f"📁 Exports: {config.exports_dir}")
        print(f"📁 Logs: {config.logs_dir}")

        try:
            # Exécuter la fonction de sauvegarde (simulation sans progress_tracker)
            print("\n🔄 Exécution de save_full_log...")
            save_full_log(
                test_objectif, test_contexte, test_contraintes, test_logs, test_synthese, None
            )
            print("✅ save_full_log terminé sans erreur")

            # Vérifier les fichiers générés
            print("\n📊 === VÉRIFICATION DES FICHIERS GÉNÉRÉS ===")

            # Vérifier les logs
            logs_path = Path(config.logs_dir)
            if logs_path.exists():
                log_files = (
                    list(logs_path.glob("*.yaml"))
                    + list(logs_path.glob("*.json"))
                    + list(logs_path.glob("*.md"))
                )
                print(f"📋 Fichiers de log générés: {len(log_files)}")
                for f in log_files:
                    print(f"   • {f.name} ({f.stat().st_size} bytes)")
            else:
                print("❌ Répertoire logs non trouvé")

            # Vérifier les exports
            exports_path = Path(config.exports_dir)
            if exports_path.exists():
                export_files = list(exports_path.glob("*.md")) + list(exports_path.glob("*.txt"))
                print(f"💡 Fichiers d'idées exportés: {len(export_files)}")

                for f in export_files:
                    size = f.stat().st_size
                    print(f"   • {f.name} ({size} bytes)")

                    # Lire le contenu pour vérifier
                    if size > 50:  # Si plus de 50 bytes, probablement un contenu détaillé
                        print("     ✅ Contenu détaillé (> 50 bytes)")

                        # Afficher un aperçu du contenu
                        try:
                            with open(f, encoding="utf-8") as file:
                                content = file.read()
                                lines = content.splitlines()
                                print(
                                    f"     📄 Aperçu: {lines[0][:60]}..."
                                    if lines
                                    else "     📄 Fichier vide"
                                )

                                # Vérifier la présence des sections attendues
                                sections = [
                                    "Plan Initial",
                                    "Critique du Plan",
                                    "Défense du Plan",
                                    "Plan Final Révisé",
                                ]
                                found_sections = [s for s in sections if s in content]
                                print(
                                    f"     📋 Sections trouvées: {len(found_sections)}/{len(sections)}"
                                )
                        except Exception as e:
                            print(f"     ❌ Erreur lecture: {e}")
                    else:
                        print("     ⚠️ Contenu probablement trop court")
            else:
                print("❌ Répertoire exports non trouvé")

        except Exception as e:
            print(f"❌ Erreur pendant le test: {e}")
            import traceback

            traceback.print_exc()
        finally:
            # Restaurer les répertoires originaux
            config._config["export"]["paths"]["exports_dir"] = original_exports_dir
            config._config["export"]["paths"]["logs_dir"] = original_logs_dir

    print("\n✅ Test terminé")


if __name__ == "__main__":
    test_export_fix()
