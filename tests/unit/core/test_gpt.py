"""
Tests unitaires pour le module GPT.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import os
from openai import APIError, APIConnectionError, RateLimitError, Timeout

from brainstorm_ai.core.gpt import (
    GPTClient, GPTError, GPTConfigError, GPTAPIError,
    gpt, get_gpt_stats, reset_gpt_stats, estimate_tokens
)


class TestGPTClient:
    """Tests pour la classe GPTClient."""
    
    def test_singleton_pattern(self):
        """Test que GPTClient est un singleton."""
        client1 = GPTClient()
        client2 = GPTClient()
        assert client1 is client2
    
    @patch.dict(os.environ, {"OPENAI_API_KEY": "sk-test123"})
    @patch('brainstorm_ai.core.gpt.OpenAI')
    def test_initialize_client_success(self, mock_openai):
        """Test l'initialisation réussie du client."""
        client = GPTClient()
        client._client = None  # Reset pour forcer la réinitialisation
        client._initialize_client()
        
        mock_openai.assert_called_once_with(api_key="sk-test123")
        assert client._client is not None
    
    @patch.dict(os.environ, {}, clear=True)
    def test_initialize_client_no_api_key(self):
        """Test l'erreur quand la clé API n'est pas configurée."""
        client = GPTClient()
        client._client = None
        
        with pytest.raises(GPTConfigError, match="La clé API OpenAI n'est pas configurée"):
            client._initialize_client()
    
    @patch.dict(os.environ, {"OPENAI_API_KEY": "invalid-key"})
    @patch('brainstorm_ai.core.gpt.logger')
    @patch('brainstorm_ai.core.gpt.OpenAI')
    def test_initialize_client_invalid_format(self, mock_openai, mock_logger):
        """Test l'avertissement pour un format de clé invalide."""
        client = GPTClient()
        client._client = None
        client._initialize_client()
        
        mock_logger.warning.assert_called_once_with(
            "Le format de la clé API OpenAI semble incorrect"
        )
    
    def test_add_usage(self):
        """Test l'ajout de statistiques d'utilisation."""
        client = GPTClient()
        client._total_tokens = {"prompt": 0, "completion": 0}
        client._total_cost = 0.0
        client._api_calls = 0
        
        client.add_usage(100, 50, 0.15)
        
        assert client._total_tokens["prompt"] == 100
        assert client._total_tokens["completion"] == 50
        assert client._total_cost == 0.15
        assert client._api_calls == 1
    
    def test_get_stats(self):
        """Test la récupération des statistiques."""
        client = GPTClient()
        client._total_tokens = {"prompt": 1000, "completion": 500}
        client._total_cost = 1.5
        client._api_calls = 10
        
        stats = client.get_stats()
        
        assert stats["total_tokens"] == 1500
        assert stats["prompt_tokens"] == 1000
        assert stats["completion_tokens"] == 500
        assert stats["total_cost"] == 1.5
        assert stats["api_calls"] == 10
    
    def test_reset_stats(self):
        """Test la réinitialisation des statistiques."""
        client = GPTClient()
        client._total_tokens = {"prompt": 1000, "completion": 500}
        client._total_cost = 1.5
        client._api_calls = 10
        
        client.reset_stats()
        
        assert client._total_tokens == {"prompt": 0, "completion": 0}
        assert client._total_cost == 0.0
        assert client._api_calls == 0


class TestGPTFunction:
    """Tests pour la fonction gpt."""
    
    @patch('brainstorm_ai.core.gpt.config')
    @patch('brainstorm_ai.core.gpt._gpt_client')
    def test_gpt_success(self, mock_client, mock_config):
        """Test un appel GPT réussi."""
        # Configuration des mocks
        mock_config.get_model_for_role.return_value = "gpt-4"
        mock_config.get_temperature_for_role.return_value = 0.7
        mock_config.max_retries = 3
        mock_config.calculate_cost.return_value = 0.05
        
        # Mock de la réponse OpenAI
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content=" Test response "))]
        mock_response.usage = Mock(prompt_tokens=100, completion_tokens=50)
        
        mock_client.client.chat.completions.create.return_value = mock_response
        
        # Appel de la fonction
        result = gpt("Test prompt", "creatif")
        
        # Vérifications
        assert result == "Test response"
        mock_client.add_usage.assert_called_once_with(100, 50, 0.05)
    
    @patch('brainstorm_ai.core.gpt.config')
    @patch('brainstorm_ai.core.gpt._gpt_client')
    def test_gpt_with_overrides(self, mock_client, mock_config):
        """Test un appel GPT avec paramètres personnalisés."""
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content="Response"))]
        mock_response.usage = Mock(prompt_tokens=100, completion_tokens=50)
        
        mock_client.client.chat.completions.create.return_value = mock_response
        mock_config.calculate_cost.return_value = 0.05
        
        result = gpt(
            "Test prompt", 
            "creatif",
            model_override="gpt-3.5-turbo",
            temperature=0.5,
            max_retries=5
        )
        
        # Vérifier que le modèle override est utilisé
        mock_client.client.chat.completions.create.assert_called_once()
        call_args = mock_client.client.chat.completions.create.call_args
        assert call_args.kwargs["model"] == "gpt-3.5-turbo"
        assert call_args.kwargs["temperature"] == 0.5
    
    @patch('brainstorm_ai.core.gpt.time.sleep')
    @patch('brainstorm_ai.core.gpt.config')
    @patch('brainstorm_ai.core.gpt._gpt_client')
    def test_gpt_rate_limit_retry(self, mock_client, mock_config, mock_sleep):
        """Test le retry en cas de rate limit."""
        mock_config.get_model_for_role.return_value = "gpt-4"
        mock_config.get_temperature_for_role.return_value = 0.7
        mock_config.max_retries = 3
        mock_config.retry_delay_base = 2
        mock_config.calculate_cost.return_value = 0.05
        
        # Premier appel échoue avec RateLimitError, second réussit
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content="Success"))]
        mock_response.usage = Mock(prompt_tokens=100, completion_tokens=50)
        
        mock_client.client.chat.completions.create.side_effect = [
            RateLimitError("Rate limit exceeded"),
            mock_response
        ]
        
        result = gpt("Test prompt", "creatif")
        
        assert result == "Success"
        assert mock_client.client.chat.completions.create.call_count == 2
        mock_sleep.assert_called_once_with(4)  # 2^1 * 2
    
    @patch('brainstorm_ai.core.gpt.config')
    @patch('brainstorm_ai.core.gpt._gpt_client')
    def test_gpt_api_error_exhausted_retries(self, mock_client, mock_config):
        """Test l'échec après épuisement des tentatives."""
        mock_config.get_model_for_role.return_value = "gpt-4"
        mock_config.get_temperature_for_role.return_value = 0.7
        mock_config.max_retries = 2
        mock_config.retry_delay_base = 2
        
        mock_client.client.chat.completions.create.side_effect = APIError("API Error")
        
        with pytest.raises(GPTAPIError, match="Échec GPT après 2 tentatives"):
            gpt("Test prompt", "creatif")
        
        assert mock_client.client.chat.completions.create.call_count == 2
    
    @patch('brainstorm_ai.core.gpt.config')
    @patch('brainstorm_ai.core.gpt._gpt_client')
    def test_gpt_unexpected_error(self, mock_client, mock_config):
        """Test la gestion des erreurs inattendues."""
        mock_config.get_model_for_role.return_value = "gpt-4"
        mock_config.get_temperature_for_role.return_value = 0.7
        mock_config.max_retries = 3
        
        mock_client.client.chat.completions.create.side_effect = ValueError("Unexpected error")
        
        with pytest.raises(GPTAPIError, match="Erreur inattendue: ValueError"):
            gpt("Test prompt", "creatif")


class TestUtilityFunctions:
    """Tests pour les fonctions utilitaires."""
    
    def test_get_gpt_stats(self):
        """Test la récupération des statistiques."""
        with patch('brainstorm_ai.core.gpt._gpt_client') as mock_client:
            mock_client.get_stats.return_value = {"test": "stats"}
            
            stats = get_gpt_stats()
            
            assert stats == {"test": "stats"}
            mock_client.get_stats.assert_called_once()
    
    def test_reset_gpt_stats(self):
        """Test la réinitialisation des statistiques."""
        with patch('brainstorm_ai.core.gpt._gpt_client') as mock_client:
            reset_gpt_stats()
            
            mock_client.reset_stats.assert_called_once()
    
    def test_estimate_tokens(self):
        """Test l'estimation du nombre de tokens."""
        # Test avec différentes longueurs de texte
        assert estimate_tokens("Test") == 1  # 4 caractères / 4
        assert estimate_tokens("Hello world!") == 3  # 12 caractères / 4
        assert estimate_tokens("A" * 100) == 25  # 100 caractères / 4
        assert estimate_tokens("") == 0  # Chaîne vide
    
    def test_estimate_tokens_caching(self):
        """Test que estimate_tokens utilise le cache."""
        with patch('brainstorm_ai.core.gpt.len') as mock_len:
            mock_len.return_value = 100
            
            # Premier appel
            result1 = estimate_tokens("Test text")
            # Deuxième appel avec le même texte
            result2 = estimate_tokens("Test text")
            
            # len() ne devrait être appelé qu'une fois grâce au cache
            assert mock_len.call_count == 1
            assert result1 == result2 == 25 