import os
import sys
import logging
from pathlib import Path
import openai

from ..core.loop_manager import run_brainstorm_loop
from ..core.config import config

# Configuration du logging
log_dir = Path("data/logs")
log_dir.mkdir(exist_ok=True, parents=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_dir / 'brainstorm.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Essayer de charger le fichier .env si disponible
try:
    from dotenv import load_dotenv
    if load_dotenv():
        logger.info("Variables d'environnement chargées depuis .env")
    else:
        logger.warning("Fichier .env non trouvé, utilisation des variables système")
except ImportError:
    logger.info("Module python-dotenv non installé, utilisation des variables d'environnement système uniquement")
except Exception as e:
    logger.warning(f"Erreur lors du chargement du fichier .env : {e}")

# Validation de la clé API
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    logger.error("Clé API OpenAI manquante")
    print("\n❌ ERREUR : Clé API OpenAI non configurée")
    print("👉 Configurez la variable d'environnement OPENAI_API_KEY")
    print("   ou créez un fichier .env avec : OPENAI_API_KEY=votre_clé_ici")
    sys.exit(1)

# Validation du format de la clé API
if not api_key.startswith(('sk-', 'sk-proj-')):
    logger.warning("Format de clé API OpenAI potentiellement invalide")
    print("\n⚠️  ATTENTION : Le format de la clé API semble incorrect")
    print("   Les clés OpenAI commencent généralement par 'sk-' ou 'sk-proj-'")

openai.api_key = api_key
logger.info("Clé API OpenAI configurée avec succès")

def main():
    """Point d'entrée principal du CLI."""
    # Charger les paramètres depuis la configuration
    objectif = config.objectif
    contexte = config.contexte
    contraintes = config.contraintes
    cycles = config.cycles

    print(f"\n{config.get_emoji('confirmation')} [Confirmation QOS]")
    print(f"{config.get_emoji('objectif')} Objectif     : {objectif}")
    print(f"{config.get_emoji('contexte')} Contexte     : {contexte}")
    print(f"{config.get_emoji('contraintes')} Contraintes  : {contraintes}")
    print(f"{config.get_emoji('cycles')} Cycles       : {cycles}")
    
    # Estimation du coût total
    cost_estimate = config.estimate_total_cost(cycles, config.top_ideas_count)
    print(f"\n💰 === ESTIMATION DU COÛT ===")
    print(f"📞 Appels API prévus: {cost_estimate['total_calls']}")
    print(f"💵 Coût estimé: ${cost_estimate['total_cost']:.4f}")
    
    # Affichage détaillé par modèle si plusieurs
    if len(cost_estimate['estimates']) > 1:
        print(f"\n📊 Répartition par modèle:")
        for model, estimate in cost_estimate['estimates'].items():
            if estimate['cost'] > 0:
                print(f"   • {model}: {estimate['calls']} appels - ${estimate['cost']:.4f}")
    
    if config.ask_confirmation:
        input("\nAppuyez sur ENTRÉE pour valider et démarrer le brainstorming...\n")

    try:
        logger.info(f"Démarrage du brainstorming - Objectif: {objectif}")
        run_brainstorm_loop(objectif, contexte, contraintes, cycles=cycles)
        logger.info("Brainstorming terminé avec succès")
    except KeyboardInterrupt:
        logger.warning("Brainstorming interrompu par l'utilisateur")
        print("\n⚠️ Brainstorming interrompu par l'utilisateur")
        sys.exit(0)
    except Exception as e:
        logger.exception("Erreur fatale durant le brainstorming")
        print(f"\n❌ Erreur fatale : {str(e)}")
        print("Consultez logs/brainstorm.log pour plus de détails")
        sys.exit(1)

if __name__ == "__main__":
    main()