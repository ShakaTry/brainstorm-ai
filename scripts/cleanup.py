#!/usr/bin/env python3
"""
Script de nettoyage pour supprimer les fichiers temporaires et caches.
"""

import os
import shutil
from pathlib import Path


def cleanup_project():
    """Nettoie les fichiers temporaires et caches du projet."""
    
    project_root = Path(__file__).parent.parent
    
    # Patterns de fichiers/dossiers à nettoyer
    patterns_to_clean = [
        "**/__pycache__",
        "**/*.pyc",
        "**/*.pyo",
        "**/*.pyd",
        "**/.mypy_cache",
        "**/.pytest_cache",
        "**/.coverage",
        "**/*.egg-info",
        "**/dist",
        "**/build",
        "**/.DS_Store",
        "**/.env.local",
        "**/.env.*.local",
        "**/Thumbs.db",
    ]
    
    total_cleaned = 0
    
    print("🧹 Nettoyage du projet en cours...")
    
    for pattern in patterns_to_clean:
        for path in project_root.glob(pattern):
            try:
                if path.is_dir():
                    shutil.rmtree(path)
                    print(f"  ✅ Dossier supprimé : {path.relative_to(project_root)}")
                else:
                    path.unlink()
                    print(f"  ✅ Fichier supprimé : {path.relative_to(project_root)}")
                total_cleaned += 1
            except Exception as e:
                print(f"  ⚠️  Erreur lors de la suppression de {path}: {e}")
    
    # Vider le cache de données si demandé
    cache_dir = project_root / "data" / "cache"
    if cache_dir.exists() and cache_dir.is_dir():
        response = input("\n🗑️  Voulez-vous vider le cache de données ? (o/N) : ")
        if response.lower() == 'o':
            try:
                shutil.rmtree(cache_dir)
                cache_dir.mkdir(exist_ok=True)
                print(f"  ✅ Cache vidé : {cache_dir.relative_to(project_root)}")
                total_cleaned += 1
            except Exception as e:
                print(f"  ⚠️  Erreur lors du vidage du cache : {e}")
    
    if total_cleaned > 0:
        print(f"\n✨ Nettoyage terminé ! {total_cleaned} éléments supprimés.")
    else:
        print("\n✨ Projet déjà propre, rien à nettoyer !")


if __name__ == "__main__":
    cleanup_project() 