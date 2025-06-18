import pytest
import json
import os
from core.loop_manager import traiter_cycle, save_full_log
from unittest.mock import patch

def test_traiter_cycle_success(mock_gpt):
    """
    Tests a successful run of traiter_cycle, including correct JSON parsing for the score.
    """
    # Arrange: Set up the mock return values for all gpt calls in order
    mock_gpt.side_effect = [
        "1. Idée créative",  # creation
        "Critique de l'idée",  # critique
        "Défense de l'idée",  # defense
        "Réplique à la défense",  # replique
        "Idée révisée",  # revision
        json.dumps({  # score_json
            "impact": 8, "faisabilite": 7,
            "originalite": 9, "clarte": 8, "total": 32
        })
    ]
    
    # Act
    result = traiter_cycle("objectif", "contexte", "contraintes", [], 1)
    
    # Assert
    assert result['cycle'] == 1
    assert result['creation'] == "1. Idée créative"
    assert result['critique'] == "Critique de l'idée"
    assert result['revision'] == "Idée révisée"
    assert result['score']['total'] == 32
    assert mock_gpt.call_count == 6

def test_traiter_cycle_json_parse_error(mock_gpt):
    """
    Tests that traiter_cycle handles a JSON parsing error gracefully.
    """
    # Arrange
    mock_gpt.side_effect = [
        "Idée créative", "Critique", "Défense", "Réplique", "Révision",
        "ceci n'est pas du json"  # Invalid JSON
    ]
    
    # Act
    result = traiter_cycle("objectif", "contexte", "contraintes", [], 1)
    
    # Assert
    assert result['score']['total'] == 0
    assert result['score']['impact'] == 0

def test_save_full_log(mock_gpt, tmp_path):
    """
    Tests that save_full_log creates a uniquely timestamped YAML file.
    """
    # Arrange
    # Mock gpt calls made within save_full_log for the 'application' part
    mock_gpt.side_effect = [
        "Plan d'action", "Critique du plan", "Défense du plan", "Plan révisé"
    ]
    
    objectif = "Test Objectif"
    logs = [{"cycle": 1, "revision": "Idée finale 1"}]
    synthese = "1. Idée finale 1"
    
    # The function will create a 'logs' directory inside tmp_path.
    # We must pass the full path to the function to ensure it writes there.
    # To do this, we need to patch 'export_yaml'.
    
    # Let's adjust the test to patch export_yaml instead of changing CWD.
    # This is a cleaner approach.
    
    # We need to find the full path of export_yaml to patch it
    with patch('core.loop_manager.export_yaml') as mock_export_yaml:
        # Act
        save_full_log(objectif, "contexte", "contraintes", logs, synthese)
        
        # Assert
        mock_export_yaml.assert_called_once()
        args, kwargs = mock_export_yaml.call_args
        
        # Check the data passed to export_yaml
        log_data = args[0]
        assert log_data['objectif'] == objectif
        assert 'application' in log_data
        
        # Check the filename format
        filename = kwargs['filename']
        assert filename.startswith("logs/brainstorm_")
        assert filename.endswith(".yaml")