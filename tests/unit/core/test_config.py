"""
Tests unitaires pour le module de configuration.
"""

import pytest
from unittest.mock import patch, mock_open
import yaml
from pathlib import Path

from brainstorm_ai.core.config import (
    Config, ConfigError, ConfigFileError, ConfigValidationError
)


class TestConfig:
    """Tests pour la classe Config."""
    
    def test_singleton_pattern(self):
        """Test que Config est un singleton."""
        config1 = Config()
        config2 = Config()
        assert config1 is config2
    
    def test_thread_safe_singleton(self):
        """Test que le singleton est thread-safe."""
        import threading
        instances = []
        
        def create_instance():
            instances.append(Config())
        
        threads = [threading.Thread(target=create_instance) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        # Toutes les instances doivent être identiques
        assert all(inst is instances[0] for inst in instances)
    
    @patch('builtins.open', new_callable=mock_open, read_data="""
general:
  objectif: "Test objectif"
  contexte: "Test contexte"
  contraintes: "Test contraintes"
  cycles: 3
agents:
  models:
    default: "gpt-4"
api:
  max_retries: 3
export:
  paths:
    logs_dir: "data/logs"
display:
  use_emojis: true
""")
    @patch('pathlib.Path.exists', return_value=True)
    @patch('pathlib.Path.is_file', return_value=True)
    def test_load_config_success(self, mock_is_file, mock_exists, mock_file):
        """Test le chargement réussi de la configuration."""
        config = Config()
        config.reload_config("test_config.yaml")
        
        assert config.get("general.objectif") == "Test objectif"
        assert config.get("general.cycles") == 3
    
    @patch('pathlib.Path.exists', return_value=False)
    def test_load_config_file_not_found(self, mock_exists):
        """Test l'erreur quand le fichier n'existe pas."""
        config = Config()
        with pytest.raises(ConfigFileError, match="Fichier de configuration non trouvé"):
            config.reload_config("inexistant.yaml")
    
    @patch('pathlib.Path.exists', return_value=True)
    @patch('pathlib.Path.is_file', return_value=False)
    def test_load_config_not_a_file(self, mock_is_file, mock_exists):
        """Test l'erreur quand le chemin n'est pas un fichier."""
        config = Config()
        with pytest.raises(ConfigFileError, match="Le chemin n'est pas un fichier"):
            config.reload_config("/some/directory")
    
    @patch('builtins.open', new_callable=mock_open, read_data="invalid: yaml: content:")
    @patch('pathlib.Path.exists', return_value=True)
    @patch('pathlib.Path.is_file', return_value=True)
    def test_load_config_invalid_yaml(self, mock_is_file, mock_exists, mock_file):
        """Test l'erreur avec un YAML invalide."""
        config = Config()
        with pytest.raises(ConfigValidationError, match="Erreur dans le fichier YAML"):
            config.reload_config("invalid.yaml")
    
    @patch('builtins.open', new_callable=mock_open, read_data="")
    @patch('pathlib.Path.exists', return_value=True)
    @patch('pathlib.Path.is_file', return_value=True)
    def test_load_config_empty_file(self, mock_is_file, mock_exists, mock_file):
        """Test l'erreur avec un fichier vide."""
        config = Config()
        with pytest.raises(ConfigValidationError, match="Le fichier de configuration est vide"):
            config.reload_config("empty.yaml")
    
    @patch('builtins.open', new_callable=mock_open, read_data="""
general:
  objectif: "Test"
# Manque les sections requises
""")
    @patch('pathlib.Path.exists', return_value=True)
    @patch('pathlib.Path.is_file', return_value=True)
    def test_validate_config_missing_sections(self, mock_is_file, mock_exists, mock_file):
        """Test la validation avec des sections manquantes."""
        config = Config()
        with pytest.raises(ConfigValidationError, match="Sections requises manquantes"):
            config.reload_config("incomplete.yaml")
    
    def test_get_with_default(self):
        """Test la méthode get avec valeur par défaut."""
        config = Config()
        assert config.get("inexistant.key", "default") == "default"
    
    def test_get_nested_value(self):
        """Test la récupération de valeurs imbriquées."""
        config = Config()
        config._config = {
            "level1": {
                "level2": {
                    "level3": "value"
                }
            }
        }
        assert config.get("level1.level2.level3") == "value"
        assert config.get("level1.level2.inexistant", "default") == "default"
    
    def test_properties(self):
        """Test les propriétés de configuration."""
        config = Config()
        config._config = {
            "general": {
                "objectif": "Mon objectif",
                "contexte": "Mon contexte",
                "contraintes": "Mes contraintes",
                "cycles": 5,
                "top_ideas_count": 3,
                "ask_confirmation": False
            },
            "agents": {
                "max_context_chars": 100000
            },
            "api": {
                "max_retries": 5,
                "retry_delay_base": 3
            },
            "export": {
                "paths": {
                    "logs_dir": "custom/logs",
                    "exports_dir": "custom/exports"
                }
            },
            "display": {
                "show_token_usage": True,
                "use_emojis": False
            }
        }
        
        assert config.objectif == "Mon objectif"
        assert config.contexte == "Mon contexte"
        assert config.contraintes == "Mes contraintes"
        assert config.cycles == 5
        assert config.max_context_chars == 100000
        assert config.max_retries == 5
        assert config.retry_delay_base == 3
        assert config.logs_dir == "custom/logs"
        assert config.exports_dir == "custom/exports"
        assert config.top_ideas_count == 3
        assert config.ask_confirmation == False
        assert config.show_token_usage == True
    
    def test_get_model_for_role(self):
        """Test la récupération du modèle par rôle."""
        config = Config()
        config._config = {
            "agents": {
                "models": {
                    "creatif": "gpt-4-turbo",
                    "critique": "gpt-3.5-turbo",
                    "default": "gpt-4"
                }
            }
        }
        
        assert config.get_model_for_role("creatif") == "gpt-4-turbo"
        assert config.get_model_for_role("critique") == "gpt-3.5-turbo"
        assert config.get_model_for_role("inexistant") == "gpt-4"
    
    def test_calculate_cost(self):
        """Test le calcul du coût."""
        config = Config()
        config._config = {
            "api": {
                "pricing": {
                    "gpt-4": {
                        "input": 0.03,
                        "output": 0.06
                    }
                }
            }
        }
        
        cost = config.calculate_cost("gpt-4", 1000, 500)
        assert cost == pytest.approx(0.06)  # (1000/1000 * 0.03) + (500/1000 * 0.06) 