import os
from core.loop_manager import run_brainstorm_loop
from core.config import config
import openai

# Essayer de charger le fichier .env si disponible (optionnel)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv n'est pas installé, utiliser les variables d'environnement système

api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError("La clé API OpenAI est manquante. Veuillez la définir comme variable d'environnement système ou dans un fichier .env.")

openai.api_key = api_key

if __name__ == "__main__":
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
    
    if config.ask_confirmation:
        input("\nAppuyez sur ENTRÉE pour valider et démarrer le brainstorming...\n")

    run_brainstorm_loop(objectif, contexte, contraintes, cycles=cycles)