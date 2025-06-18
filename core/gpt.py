import os
from typing import Optional
from openai import OpenAI
from core.config import config

def gpt(prompt: str, role: str, model_override: Optional[str] = None, temperature: float = None) -> str:
    """
    Fonction centrale pour appeler l'API GPT avec un routage intelligent selon le rôle.
    
    Args:
        prompt: Le prompt à envoyer à l'API
        role: Le rôle de l'agent (creatif, critique, revision, etc.)
        model_override: Permet de forcer un modèle spécifique (optionnel)
        temperature: Température du modèle (par défaut selon la config du rôle)
        
    Returns:
        Le contenu de la réponse de l'API
    """
    # Vérifier la clé API
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("La clé API OpenAI n'est pas configurée dans OPENAI_API_KEY")
    
    # Initialiser le client OpenAI
    client = OpenAI(api_key=api_key)
    
    # Déterminer le modèle à utiliser depuis la configuration
    model = model_override if model_override else config.get_model_for_role(role)
    
    # Déterminer la température depuis la configuration si non spécifiée
    if temperature is None:
        temperature = config.get_temperature_for_role(role)
    
    try:
        # Appel à l'API OpenAI
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature
        )
        
        # Retourner uniquement le contenu de la réponse
        return response.choices[0].message.content
        
    except Exception as e:
        raise Exception(f"Erreur lors de l'appel à l'API GPT: {str(e)}") 