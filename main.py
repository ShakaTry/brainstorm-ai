#!/usr/bin/env python3
"""
Point d'entrée principal du projet Brainstorm AI.
Redirige vers le fichier main.py dans le dossier src/brainstorm_ai/cli.
"""

try:
    from src.brainstorm_ai.cli.main import main
except ImportError:
    # Fallback si le module n'est pas installé
    import sys
    from pathlib import Path
    
    # Ajouter le dossier src au path Python de manière plus sûre
    src_path = Path(__file__).parent / "src"
    if src_path.exists() and str(src_path) not in sys.path:
        sys.path.append(str(src_path))
    
    try:
        from brainstorm_ai.cli.main import main
    except ImportError as e:
        print(f"❌ Erreur : Impossible d'importer le module brainstorm_ai")
        print(f"   Détails : {e}")
        print(f"   Assurez-vous que le projet est correctement installé avec : pip install -e .")
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⚠️ Programme interrompu par l'utilisateur")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erreur fatale : {e}")
        sys.exit(1) 