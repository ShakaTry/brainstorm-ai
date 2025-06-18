import os
import datetime
import json
import re
import time
from openai import OpenAI
from agents.agent_creatif import prompt_creatif, prompt_defense
from agents.agent_critique import prompt_critique, prompt_replique
from agents.agent_revision import prompt_revision
from agents.agent_synthese import prompt_synthese
from agents.agent_score import prompt_score
from agents.agent_application import prompt_plan, prompt_critique_plan, prompt_defense_plan, prompt_revision_plan
from core.exporter import export_yaml, export_json, export_markdown
from core.utils import dedupe
from core.config import config
from core.progress_tracker import ProgressTracker

def limiter_historique(historique: list[str]) -> list[str]:
    """Réduit la taille du contexte historique en supprimant les plus anciennes entrées."""
    max_context_chars = config.max_context_chars
    contenu = "\n".join(historique)
    while len(contenu) > max_context_chars and historique:
        historique.pop(0)
        contenu = "\n".join(historique)
    return historique

client = None
total_tokens_used = 0

def get_client():
    global client
    if client is None:
        client = OpenAI()
    return client

def gpt(prompt, temperature=0.7, progress_tracker=None):
    global total_tokens_used
    model = config.get_model_for_role("default")
    response = get_client().chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature
    )
    usage = response.usage
    prompt_tokens = usage.prompt_tokens if usage else 0
    completion_tokens = usage.completion_tokens if usage else 0
    total_tokens_used += prompt_tokens + completion_tokens
    
    # Ajouter au suivi de progression si disponible
    if progress_tracker:
        progress_tracker.add_api_call(model, prompt_tokens, completion_tokens)
    
    return response.choices[0].message.content.strip()

def gpt_with_retry(prompt, temperature=0.7, max_retries=None, progress_tracker=None):
    """Appel GPT avec retry automatique."""
    if max_retries is None:
        max_retries = config.max_retries
    
    model = config.get_model_for_role("default")
    for attempt in range(max_retries):
        try:
            response = get_client().chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature
            )
            
            # Ajouter au suivi de progression si disponible
            if progress_tracker:
                usage = response.usage
                prompt_tokens = usage.prompt_tokens if usage else 0
                completion_tokens = usage.completion_tokens if usage else 0
                progress_tracker.add_api_call(model, prompt_tokens, completion_tokens)
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            if attempt == max_retries - 1:
                raise GPTError(f"Échec GPT après {max_retries} tentatives: {e}")
            time.sleep(config.retry_delay_base ** attempt)  # Backoff exponentiel

def traiter_cycle(objectif, contexte, contraintes, historique, cycle_num, progress_tracker=None):
    historique = limiter_historique(historique)
    
    # Étape 1: Créatif
    if progress_tracker:
        progress_tracker.start_cycle_step(0)
    prompt1 = prompt_creatif(objectif, contexte, contraintes, "\n".join(historique))
    creation = gpt_with_retry(prompt1, progress_tracker=progress_tracker)
    if progress_tracker:
        progress_tracker.complete_cycle_step(0)

    historique.append(creation)

    # Étape 2: Critique
    if progress_tracker:
        progress_tracker.start_cycle_step(1)
    prompt2 = prompt_critique(creation)
    critique = gpt_with_retry(prompt2, progress_tracker=progress_tracker)
    if progress_tracker:
        progress_tracker.complete_cycle_step(1)

    # Étape 3: Défense
    if progress_tracker:
        progress_tracker.start_cycle_step(2)
    prompt3 = prompt_defense(creation, critique)
    defense = gpt_with_retry(prompt3, progress_tracker=progress_tracker)
    if progress_tracker:
        progress_tracker.complete_cycle_step(2)

    # Étape 4: Réplique
    if progress_tracker:
        progress_tracker.start_cycle_step(3)
    prompt4 = prompt_replique(defense, creation)
    replique = gpt_with_retry(prompt4, progress_tracker=progress_tracker)
    if progress_tracker:
        progress_tracker.complete_cycle_step(3)

    # Étape 5: Révision
    if progress_tracker:
        progress_tracker.start_cycle_step(4)
    prompt5 = prompt_revision(creation, critique)
    revision = gpt_with_retry(prompt5, progress_tracker=progress_tracker)
    if progress_tracker:
        progress_tracker.complete_cycle_step(4)

    # Étape 6: Score
    if progress_tracker:
        progress_tracker.start_cycle_step(5)
    score_prompt = prompt_score(revision)
    score_json = gpt_with_retry(score_prompt, progress_tracker=progress_tracker)
    score = validate_score(score_json)
    if progress_tracker:
        progress_tracker.complete_cycle_step(5)

    return {
        "cycle": cycle_num,
        "creation": creation,
        "critique": critique,
        "defense": defense,
        "replique": replique,
        "revision": revision,
        "score": score
    }

def run_brainstorm_loop(objectif, contexte, contraintes, cycles=3):
    historique = []
    logs = []
    
    # Initialiser le tracker de progression
    progress_tracker = ProgressTracker(cycles, config.top_ideas_count)
    progress_tracker.start_brainstorm()

    # Cycles de brainstorming
    for i in range(1, cycles + 1):
        progress_tracker.start_cycle(i)
        log = traiter_cycle(objectif, contexte, contraintes, historique, i, progress_tracker)
        logs.append(log)

        print(f"\n=== Cycle {i} ===")
        print(f"\n{config.get_emoji('creatif')} [Créatif]\n{log['creation']}")
        print(f"\n{config.get_emoji('critique')} [Critique]\n{log['critique']}")
        print(f"\n{config.get_emoji('defense')} [Défense]\n{log['defense']}")
        print(f"\n{config.get_emoji('replique')} [Réplique]\n{log['replique']}")
        print(f"\n{config.get_emoji('revision')} [Révision]\n{log['revision']}")

    # Synthèse
    progress_tracker.start_synthesis()
    revisions_uniques = dedupe([log["revision"] for log in logs])
    synth_prompt = prompt_synthese(revisions_uniques)
    synthese = gpt(synth_prompt, progress_tracker=progress_tracker)
    progress_tracker.complete_synthesis()

    print(f"\n{config.get_emoji('synthese')} [Synthèse Finale]\n" + synthese)
    
    # Traitement des idées et sauvegarde avec progression
    save_full_log(objectif, contexte, contraintes, logs, synthese, progress_tracker)
    
    if config.show_token_usage:
        print(f"\n{config.get_emoji('stats')} Total de tokens consommés : {total_tokens_used}")
    
    # Terminer le suivi de progression
    progress_tracker.finish()

def save_full_log(objectif, contexte, contraintes, logs, synthese, progress_tracker=None):
    log_data = {
        "objectif": objectif,
        "contexte": contexte,
        "contraintes": contraintes,
        "date": datetime.datetime.now().isoformat(),
        "logs": logs,
        "synthese_finale": synthese
    }

    lignes = extract_top_ideas_robust(synthese, config.top_ideas_count)
    
    # Mettre à jour le nombre d'idées si différent de la configuration
    if progress_tracker and len(lignes) != progress_tracker.top_ideas_count:
        progress_tracker.update_total_ideas(len(lignes))
    
    # Démarrer le traitement des idées
    if progress_tracker:
        progress_tracker.start_idea_processing(len(lignes))

    application_logs = []
    for idx, idee in enumerate(lignes, 1):
        if progress_tracker:
            progress_tracker.start_idea(idx, idee)
        
        print(f"\n{config.get_emoji('application')} Traitement de l'idée sélectionnée :\n", idee)

        # Étape 1: Plan
        if progress_tracker:
            progress_tracker.start_idea_step(0)
        plan = gpt(prompt_plan(idee), progress_tracker=progress_tracker)
        if progress_tracker:
            progress_tracker.complete_idea_step(0)

        # Étape 2: Critique du plan
        if progress_tracker:
            progress_tracker.start_idea_step(1)
        critique_plan = gpt(prompt_critique_plan(plan), progress_tracker=progress_tracker)
        if progress_tracker:
            progress_tracker.complete_idea_step(1)

        # Étape 3: Défense du plan
        if progress_tracker:
            progress_tracker.start_idea_step(2)
        defense_plan = gpt(prompt_defense_plan(plan, critique_plan), progress_tracker=progress_tracker)
        if progress_tracker:
            progress_tracker.complete_idea_step(2)

        # Étape 4: Révision du plan
        if progress_tracker:
            progress_tracker.start_idea_step(3)
        plan_revise = gpt(prompt_revision_plan(plan, critique_plan), progress_tracker=progress_tracker)
        if progress_tracker:
            progress_tracker.complete_idea_step(3)

        application_logs.append({
            "idee": idee,
            "plan_initial": plan,
            "critique": critique_plan,
            "defense": defense_plan,
            "revision": plan_revise
        })

        print(f"\n{config.get_emoji('success')} Plan final révisé :\n", plan_revise)

    # Export des idées dans des fichiers séparés si activé
    if config.get("export.save_individual_ideas", True):
        from pathlib import Path
        import re

        os.makedirs(config.exports_dir, exist_ok=True)
        for idx, app_log in enumerate(application_logs, 1):
            idee = app_log["idee"]
            safe_title = re.sub(r'[^a-zA-Z0-9_\-]', '_', idee[:40]).strip('_')
            filename = Path(config.exports_dir) / f"{idx}_{safe_title}.md"
            
            # Créer un contenu détaillé avec l'idée et son plan développé
            content = f"""# Idée #{idx}: {idee}

## 📋 Plan Initial
{app_log["plan_initial"]}

## 🔍 Critique du Plan
{app_log["critique"]}

## 🛡️ Défense du Plan
{app_log["defense"]}

## ✏️ Plan Final Révisé
{app_log["revision"]}

---
*Généré automatiquement par le système de brainstorm AI*
"""
            
            with open(filename, "w", encoding="utf-8") as f:
                f.write(content)

    log_data["application"] = application_logs

    # Démarrer l'export
    if progress_tracker:
        progress_tracker.start_export()

    os.makedirs(config.logs_dir, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_filename = config.get_log_filename(timestamp)
    
    # Export dans les formats activés
    if config.should_export_format("yaml"):
        export_yaml(log_data, filename=os.path.join(config.logs_dir, f"{log_filename}.yaml"))
    
    if config.should_export_format("json"):
        export_json(log_data, filename=os.path.join(config.logs_dir, f"{log_filename}.json"))
    
    if config.should_export_format("markdown"):
        export_markdown(log_data, filename=os.path.join(config.logs_dir, f"{log_filename}.md"))
    
    # Terminer l'export
    if progress_tracker:
        progress_tracker.complete_export()

def validate_score(score_json: str) -> dict:
    """Validation et nettoyage des scores avec fallback intelligent."""
    score_config = config.get_score_validation_config()
    min_val = score_config["min_value"]
    max_val = score_config["max_value"]
    required_keys = score_config["required_keys"]
    fallback_val = score_config["fallback_value"]
    
    try:
        score = json.loads(score_json)
        # Validation des clés requises
        if all(key in score for key in required_keys):
            # Validation des valeurs
            for key in required_keys:
                score[key] = max(min_val, min(max_val, int(score[key])))
            score["total"] = sum(score[key] for key in required_keys)
            return score
    except (json.JSONDecodeError, ValueError, KeyError):
        pass
    # Fallback avec score configuré
    fallback_score = {key: fallback_val for key in required_keys}
    fallback_score["total"] = fallback_val * len(required_keys)
    return fallback_score

def extract_top_ideas_robust(synthese_text: str, count: int = 3) -> list[str]:
    """Extraction robuste des meilleures idées avec plusieurs stratégies."""
    strategies = config.get_idea_extraction_strategies()
    
    pattern_map = {
        "numbered": rf"^\s*[1-{count}]\.\s*(.+)$",
        "starred": r"^\s*\*\s*(.+)$",
        "bullet": r"^\s*-\s*(.+)$"
    }
    
    for strategy in strategies:
        if strategy == "fallback":
            continue
        pattern = pattern_map.get(strategy)
        if pattern:
            matches = re.findall(pattern, synthese_text, re.MULTILINE)
            if len(matches) >= count:
                return matches[:count]
    
    # Fallback: prendre les premières lignes non vides
    lines = [l.strip() for l in synthese_text.splitlines() if l.strip()]
    return lines[:count] if len(lines) >= count else lines

class GPTError(Exception):
    """Exception personnalisée pour les erreurs GPT."""
    pass