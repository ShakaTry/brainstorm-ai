"""
Tests d'intégration pour le flux complet de brainstorming.
"""

import os
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock
import pytest
import yaml

from core.loop_manager import run_brainstorm_loop
from core.config import config
from core.gpt import reset_gpt_stats, get_gpt_stats


class TestBrainstormFlow:
    """Tests d'intégration pour le processus complet de brainstorming."""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Configuration avant chaque test."""
        # Réinitialiser les stats
        reset_gpt_stats()
        
        # Créer un répertoire temporaire pour les exports
        self.temp_dir = tempfile.mkdtemp()
        self.original_logs_dir = config.logs_dir
        self.original_exports_dir = config.exports_dir
        
        # Rediriger vers le répertoire temporaire
        config._config['export']['paths']['logs_dir'] = self.temp_dir
        config._config['export']['paths']['exports_dir'] = self.temp_dir
        
        yield
        
        # Nettoyer après le test
        config._config['export']['paths']['logs_dir'] = self.original_logs_dir
        config._config['export']['paths']['exports_dir'] = self.original_exports_dir
        
        # Supprimer les fichiers temporaires
        import shutil
        shutil.rmtree(self.temp_dir)
    
    @patch('core.gpt.GPTClient.client')
    def test_complete_brainstorm_flow(self, mock_client):
        """Test du flux complet avec des réponses mockées."""
        # Configuration des réponses mockées
        mock_responses = [
            # Cycle 1
            MagicMock(choices=[MagicMock(message=MagicMock(content=
                "1. **Idée innovante 1**: Description de l'idée 1\n"
                "2. **Idée créative 2**: Description de l'idée 2\n"
                "3. **Idée originale 3**: Description de l'idée 3"
            ))], usage=MagicMock(prompt_tokens=100, completion_tokens=50)),
            
            # Critique
            MagicMock(choices=[MagicMock(message=MagicMock(content=
                "Points faibles identifiés: manque de détails sur l'implémentation"
            ))], usage=MagicMock(prompt_tokens=80, completion_tokens=30)),
            
            # Défense
            MagicMock(choices=[MagicMock(message=MagicMock(content=
                "L'idée reste valable car elle apporte une vraie innovation"
            ))], usage=MagicMock(prompt_tokens=90, completion_tokens=35)),
            
            # Réplique
            MagicMock(choices=[MagicMock(message=MagicMock(content=
                "Les arguments sont convaincants mais nécessitent plus de précisions"
            ))], usage=MagicMock(prompt_tokens=85, completion_tokens=32)),
            
            # Révision
            MagicMock(choices=[MagicMock(message=MagicMock(content=
                "Version améliorée de l'idée avec plus de détails techniques"
            ))], usage=MagicMock(prompt_tokens=95, completion_tokens=40)),
            
            # Score
            MagicMock(choices=[MagicMock(message=MagicMock(content=
                '{"impact": 8, "faisabilite": 7, "originalite": 9, "clarte": 8}'
            ))], usage=MagicMock(prompt_tokens=70, completion_tokens=20)),
            
            # Synthèse
            MagicMock(choices=[MagicMock(message=MagicMock(content=
                "1. Idée sélectionnée 1: La meilleure idée\n"
                "2. Idée sélectionnée 2: Une autre bonne idée\n"
                "3. Idée sélectionnée 3: Troisième idée prometteuse"
            ))], usage=MagicMock(prompt_tokens=120, completion_tokens=60)),
        ]
        
        # Ajouter les réponses pour l'application (4 appels par idée × 3 idées)
        for _ in range(12):
            mock_responses.append(
                MagicMock(choices=[MagicMock(message=MagicMock(content=
                    "Plan détaillé / Critique du plan / Défense / Révision"
                ))], usage=MagicMock(prompt_tokens=100, completion_tokens=50))
            )
        
        mock_client.chat.completions.create.side_effect = mock_responses
        
        # Paramètres du test
        objectif = "Créer une application innovante"
        contexte = "Startup technologique"
        contraintes = "Budget limité, équipe de 3 personnes"
        cycles = 1
        
        # Exécuter le brainstorming
        run_brainstorm_loop(objectif, contexte, contraintes, cycles=cycles)
        
        # Vérifications
        assert mock_client.chat.completions.create.call_count >= 7  # Au minimum
        
        # Vérifier les statistiques
        stats = get_gpt_stats()
        assert stats['api_calls'] >= 7
        assert stats['total_tokens'] > 0
        assert stats['total_cost'] > 0
        
        # Vérifier que les fichiers ont été créés
        log_files = list(Path(self.temp_dir).glob("*.yaml"))
        assert len(log_files) > 0
        
        # Vérifier le contenu du log
        with open(log_files[0], 'r', encoding='utf-8') as f:
            log_data = yaml.safe_load(f)
        
        assert log_data['objectif'] == objectif
        assert log_data['contexte'] == contexte
        assert log_data['contraintes'] == contraintes
        assert len(log_data['logs']) == cycles
        assert 'synthese_finale' in log_data
        assert 'application' in log_data
        assert len(log_data['application']) > 0
    
    @patch('core.gpt.GPTClient.client')
    def test_error_handling_during_flow(self, mock_client):
        """Test de la gestion d'erreur pendant le flux."""
        # Simuler une erreur après quelques appels réussis
        mock_client.chat.completions.create.side_effect = [
            MagicMock(choices=[MagicMock(message=MagicMock(content="Idée 1"))], 
                     usage=MagicMock(prompt_tokens=50, completion_tokens=25)),
            Exception("Erreur API simulée"),
        ]
        
        # Le brainstorming devrait échouer avec une exception
        with pytest.raises(Exception) as exc_info:
            run_brainstorm_loop("Test", "Test", "Test", cycles=1)
        
        assert "Échec GPT après" in str(exc_info.value)
    
    @patch('core.gpt.GPTClient.client')
    def test_multiple_cycles(self, mock_client):
        """Test avec plusieurs cycles de brainstorming."""
        # Préparer les réponses pour 2 cycles
        responses_per_cycle = 6  # création, critique, défense, réplique, révision, score
        num_cycles = 2
        
        mock_responses = []
        for cycle in range(num_cycles):
            # Réponses pour chaque étape du cycle
            for step in range(responses_per_cycle):
                mock_responses.append(
                    MagicMock(
                        choices=[MagicMock(message=MagicMock(
                            content=f"Réponse cycle {cycle+1} étape {step+1}"
                        ))],
                        usage=MagicMock(prompt_tokens=100, completion_tokens=50)
                    )
                )
        
        # Ajouter la synthèse et les applications
        mock_responses.extend([
            # Synthèse
            MagicMock(choices=[MagicMock(message=MagicMock(content="1. Idée finale"))], 
                     usage=MagicMock(prompt_tokens=100, completion_tokens=50)),
            # Application (4 étapes)
            *[MagicMock(choices=[MagicMock(message=MagicMock(content="Plan/Critique/Défense/Révision"))], 
                       usage=MagicMock(prompt_tokens=100, completion_tokens=50)) for _ in range(4)]
        ])
        
        # Remplacer le score JSON pour éviter les erreurs de parsing
        for i in range(5, len(mock_responses), responses_per_cycle):
            if i < len(mock_responses) - 5:  # Ne pas modifier les dernières réponses (synthèse/application)
                mock_responses[i] = MagicMock(
                    choices=[MagicMock(message=MagicMock(
                        content='{"impact": 8, "faisabilite": 7, "originalite": 9, "clarte": 8}'
                    ))],
                    usage=MagicMock(prompt_tokens=70, completion_tokens=20)
                )
        
        mock_client.chat.completions.create.side_effect = mock_responses
        
        # Exécuter avec 2 cycles
        run_brainstorm_loop("Test multi-cycles", "Contexte test", "Contraintes test", cycles=num_cycles)
        
        # Vérifier le nombre d'appels
        expected_calls = (num_cycles * responses_per_cycle) + 1 + 4  # cycles + synthèse + application
        assert mock_client.chat.completions.create.call_count == expected_calls
        
        # Vérifier les logs
        log_files = list(Path(self.temp_dir).glob("*.yaml"))
        with open(log_files[0], 'r', encoding='utf-8') as f:
            log_data = yaml.safe_load(f)
        
        assert len(log_data['logs']) == num_cycles
        
    def test_config_override(self):
        """Test de la surcharge de configuration."""
        # Sauvegarder la config originale
        original_cycles = config.cycles
        original_top_ideas = config.top_ideas_count
        
        try:
            # Modifier la configuration
            config._config['general']['cycles'] = 5
            config._config['general']['top_ideas_count'] = 2
            
            # Vérifier que les changements sont pris en compte
            assert config.cycles == 5
            assert config.top_ideas_count == 2
            
        finally:
            # Restaurer la configuration originale
            config._config['general']['cycles'] = original_cycles
            config._config['general']['top_ideas_count'] = original_top_ideas 