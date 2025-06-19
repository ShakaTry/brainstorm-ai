#!/usr/bin/env python3
"""
Génère requirements.txt à partir de pyproject.toml.
Usage: python scripts/generate_requirements.py
"""

import toml
from pathlib import Path


def generate_requirements():
    """Génère requirements.txt depuis pyproject.toml."""
    root_dir = Path(__file__).parent.parent
    pyproject_path = root_dir / "pyproject.toml"
    requirements_path = root_dir / "requirements.txt"
    
    if not pyproject_path.exists():
        print("❌ Erreur: pyproject.toml non trouvé")
        return
    
    # Charger pyproject.toml
    with open(pyproject_path, "r", encoding="utf-8") as f:
        data = toml.load(f)
    
    # Extraire les dépendances
    dependencies = data.get("project", {}).get("dependencies", [])
    dev_dependencies = data.get("project", {}).get("optional-dependencies", {}).get("dev", [])
    
    # Écrire requirements.txt
    with open(requirements_path, "w", encoding="utf-8") as f:
        f.write("# Generated from pyproject.toml\n")
        f.write("# Core dependencies\n")
        for dep in dependencies:
            f.write(f"{dep}\n")
        
        if dev_dependencies:
            f.write("\n# Development dependencies\n")
            for dep in dev_dependencies:
                f.write(f"{dep}\n")
    
    print(f"✅ requirements.txt généré avec succès")
    print(f"   {len(dependencies)} dépendances principales")
    print(f"   {len(dev_dependencies)} dépendances de développement")


if __name__ == "__main__":
    try:
        generate_requirements()
    except ImportError:
        print("❌ Erreur: Le module 'toml' n'est pas installé")
        print("   Installez-le avec: pip install toml")
    except Exception as e:
        print(f"❌ Erreur: {e}") 