#!/usr/bin/env python3
"""
Point d'entrée principal du projet Brainstorm AI.
Redirige vers le fichier main.py dans le dossier src/brainstorm_ai/cli.
"""

import sys
from pathlib import Path

# Ajouter le dossier src au path Python
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# Importer et exécuter le main depuis brainstorm_ai.cli
from brainstorm_ai.cli.main import main

if __name__ == "__main__":
    main() 