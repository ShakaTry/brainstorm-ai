import pytest
from unittest.mock import MagicMock

@pytest.fixture(scope="function", autouse=True)
def mock_openai_client(mocker):
    """
    Automatically mocks the OpenAI client for each test function
    to prevent API key errors during module import.
    Scope is 'function' to match the scope of the 'mocker' fixture.
    """
    mocker.patch('core.loop_manager.OpenAI', return_value=MagicMock())

@pytest.fixture
def mock_gpt(mocker):
    """
    Fixture to mock the gpt function in core.loop_manager.
    Returns the mock object to allow setting return values in tests.
    This relies on the OpenAI client already being mocked.
    """
    return mocker.patch('core.loop_manager.gpt') 