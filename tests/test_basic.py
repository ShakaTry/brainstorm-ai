"""Tests basiques pour brainstorm_ai."""

import pytest


def test_import_brainstorm_ai():
    """Test que le module brainstorm_ai peut être importé."""
    try:
        import brainstorm_ai
        assert brainstorm_ai is not None
    except ImportError as e:
        pytest.fail(f"Impossible d'importer brainstorm_ai: {e}")


def test_python_version():
    """Test que la version Python est supportée."""
    import sys
    
    # Vérifie que Python >= 3.8
    assert sys.version_info >= (3, 8), f"Python {sys.version_info} non supporté (requis: >= 3.8)"


def test_dependencies_importable():
    """Test que les dépendances principales sont importables."""
    dependencies = [
        "openai",
        "yaml", 
        "dotenv"
    ]
    
    for dep in dependencies:
        try:
            __import__(dep)
        except ImportError as e:
            pytest.fail(f"Dépendance manquante: {dep} - {e}")


def test_config_module():
    """Test que le module config peut être importé."""
    try:
        from brainstorm_ai.core import config
        assert config is not None
    except ImportError as e:
        pytest.fail(f"Impossible d'importer config: {e}") 