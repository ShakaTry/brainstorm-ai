import pytest
import yaml
import json
from pathlib import Path
from brainstorm_ai.core.exporter import export_yaml, export_json, escape_markdown, export_markdown

@pytest.fixture
def sample_data():
    """Provides sample data for export tests."""
    return {
        "objectif": "Test Objectif",
        "contexte": "Test Contexte",
        "contraintes": "Test Contraintes",
        "logs": [
            {
                "cycle": 1,
                "creation": "Idée 1 avec `code` et *italique*.",
                "critique": "Critique 1 avec _souligné_."
            }
        ]
    }

def test_export_yaml(tmp_path, sample_data):
    """
    Tests that export_yaml correctly creates a YAML file with the given data.
    """
    file_path = tmp_path / "test.yaml"
    export_yaml(sample_data, file_path)
    
    assert file_path.exists()
    with open(file_path, "r", encoding="utf-8") as f:
        loaded_data = yaml.safe_load(f)
    assert loaded_data == sample_data

def test_export_json(tmp_path, sample_data):
    """
    Tests that export_json correctly creates a JSON file with the given data.
    """
    file_path = tmp_path / "test.json"
    export_json(sample_data, file_path)
    
    assert file_path.exists()
    with open(file_path, "r", encoding="utf-8") as f:
        loaded_data = json.load(f)
    assert loaded_data == sample_data

def test_escape_markdown():
    """
    Tests the escape_markdown function to ensure it escapes special characters.
    """
    text = "This is `code`, *italic*, and _underline_."
    expected = r"This is \`code\`, \*italic\*, and \_underline\_."
    assert escape_markdown(text) == expected

def test_export_markdown(tmp_path, sample_data):
    """
    Tests that export_markdown correctly creates a Markdown file.
    """
    file_path = tmp_path / "test.md"
    export_markdown(sample_data, file_path)
    
    assert file_path.exists()
    content = file_path.read_text(encoding="utf-8")
    
    assert "Brainstorming Report" in content
    assert "Test Objectif" in content
    assert r"Idée 1 avec \`code\` et \*italique\*." in content
    assert r"Critique 1 avec \_souligné\_." in content

def test_export_functions_create_directories(tmp_path):
    """
    Tests that export functions create parent directories if they don't exist.
    This test is not implemented as the current functions don't do it.
    It's a placeholder for future improvements.
    """
    # Note: The current implementation of export functions will fail if the parent
    # directory does not exist. A more robust implementation would handle this.
    # For example: os.makedirs(os.path.dirname(filename), exist_ok=True)
    pass 