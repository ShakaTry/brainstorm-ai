from unittest.mock import MagicMock

import pytest


@pytest.fixture(scope="function", autouse=True)
def mock_openai_client(mocker):
    """
    Automatically mocks the OpenAI client for each test function
    to prevent API key errors during module import.
    Scope is 'function' to match the scope of the 'mocker' fixture.
    """
    # Mock l'environnement pour éviter les erreurs de clé API
    mocker.patch.dict("os.environ", {"OPENAI_API_KEY": "sk-test-key-for-tests"})
    # Mock la classe OpenAI à la source
    mocker.patch("openai.OpenAI", return_value=MagicMock())


@pytest.fixture(autouse=True)
def mock_gpt(mocker):
    """
    Fixture to mock the gpt function where it's used.
    Returns the mock object to allow setting return values in tests.
    This relies on the OpenAI client already being mocked.
    """
    # Par défaut, retourner un JSON valide pour les tests de score
    # On mock là où c'est importé dans base.py
    mock = mocker.patch("brainstorm_ai.agents.base.gpt")
    mock.return_value = '{"impact": 8, "faisabilite": 7, "originalite": 9, "clarte": 8}'
    return mock
