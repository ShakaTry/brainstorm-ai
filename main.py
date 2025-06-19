#!/usr/bin/env python3
"""
Point d'entrée principal du projet Brainstorm AI.
Redirige vers le module CLI.
"""

import sys
import logging
from pathlib import Path

# Configuration du logging de base
logging.basicConfig(
    level=logging.WARNING,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Ajouter le dossier src au path si nécessaire
src_path = Path(__file__).parent / "src"
if src_path.exists() and str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

try:
    from brainstorm_ai.cli.main import main
except ImportError as e:
    logging.error(f"Impossible d'importer le module brainstorm_ai: {e}")
    print(f"❌ Erreur : Impossible d'importer le module brainstorm_ai")
    print(f"   Assurez-vous que le projet est correctement installé avec : pip install -e .")
    sys.exit(1)

if __name__ == "__main__":
    main() 