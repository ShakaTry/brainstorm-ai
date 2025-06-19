import datetime
import json
import logging
import os
import re
from pathlib import Path
from typing import List, Optional

from ..agents.application import (
    prompt_critique_plan,
    prompt_defense_plan,
    prompt_plan,
    prompt_revision_plan,
)
from ..agents.creative import prompt_creatif, prompt_defense
from ..agents.critic import prompt_critique, prompt_replique
from ..agents.revision import prompt_revision
from ..agents.score import prompt_score
from ..agents.synthesis import prompt_synthese
from .config import config
from .exporter import export_json, export_markdown, export_yaml
from .gpt import get_gpt_stats
from .progress_tracker import ProgressTracker
from .types import ApplicationLog, BrainstormLog, CycleLog
from .utils import dedupe

logger = logging.getLogger(__name__)


def limiter_historique(historique: List[str]) -> List[str]:
    """Réduit la taille du contexte historique en supprimant les plus anciennes entrées."""
    max_context_chars = config.max_context_chars
    contenu = "\n".join(historique)
    while len(contenu) > max_context_chars and historique:
        historique.pop(0)
        contenu = "\n".join(historique)
    return historique


def traiter_cycle(
    objectif: str,
    contexte: str,
    contraintes: str,
    historique: List[str],
    cycle_num: int,
    progress_tracker: Optional[ProgressTracker] = None,
) -> CycleLog:
    """Traite un cycle complet de brainstorming."""
    historique = limiter_historique(historique)

    # Étape 1: Créatif
    if progress_tracker:
        progress_tracker.start_cycle_step(0)
    creation = prompt_creatif(objectif, contexte, contraintes, "\n".join(historique))
    if progress_tracker:
        progress_tracker.complete_cycle_step(0)

    historique.append(creation)

    # Étape 2: Critique
    if progress_tracker:
        progress_tracker.start_cycle_step(1)
    critique = prompt_critique(creation)
    if progress_tracker:
        progress_tracker.complete_cycle_step(1)

    # Étape 3: Défense
    if progress_tracker:
        progress_tracker.start_cycle_step(2)
    defense = prompt_defense(creation, critique)
    if progress_tracker:
        progress_tracker.complete_cycle_step(2)

    # Étape 4: Réplique
    if progress_tracker:
        progress_tracker.start_cycle_step(3)
    replique = prompt_replique(defense, creation)
    if progress_tracker:
        progress_tracker.complete_cycle_step(3)

    # Étape 5: Révision
    if progress_tracker:
        progress_tracker.start_cycle_step(4)
    revision = prompt_revision(creation, critique)
    if progress_tracker:
        progress_tracker.complete_cycle_step(4)

    # Étape 6: Score
    if progress_tracker:
        progress_tracker.start_cycle_step(5)
    score_json = prompt_score(revision)
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
        "score": score,
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

        logger.info(f"=== Cycle {i} ===")
        logger.info(f"{config.get_emoji('creatif')} [Créatif]\n{log['creation']}")
        logger.info(f"{config.get_emoji('critique')} [Critique]\n{log['critique']}")
        logger.info(f"{config.get_emoji('defense')} [Défense]\n{log['defense']}")
        logger.info(f"{config.get_emoji('replique')} [Réplique]\n{log['replique']}")
        logger.info(f"{config.get_emoji('revision')} [Révision]\n{log['revision']}")

    # Synthèse
    progress_tracker.start_synthesis()
    revisions_uniques = dedupe([log["revision"] for log in logs])
    synthese = prompt_synthese(revisions_uniques, config.top_ideas_count)
    progress_tracker.complete_synthesis()

    logger.info(f"{config.get_emoji('synthese')} [Synthèse Finale]\n" + synthese)

    # Traitement des idées et sauvegarde avec progression
    save_full_log(objectif, contexte, contraintes, logs, synthese, progress_tracker)

    if config.show_token_usage:
        stats = get_gpt_stats()
        logger.info(f"{config.get_emoji('stats')} === STATISTIQUES D'UTILISATION ===")
        logger.info(f"📊 Appels API : {stats['api_calls']}")
        logger.info(
            f"📝 Tokens utilisés : {stats['total_tokens']} (entrée: {stats['prompt_tokens']}, sortie: {stats['completion_tokens']})"
        )
        logger.info(f"💰 Coût total : ${stats['total_cost']:.4f}")

    # Terminer le suivi de progression
    progress_tracker.finish()


def process_ideas(
    idees: List[str], progress_tracker: Optional[ProgressTracker] = None
) -> List[ApplicationLog]:
    """
    Traite chaque idée sélectionnée pour créer des plans détaillés.

    Args:
        idees: Liste des idées à traiter
        progress_tracker: Tracker de progression optionnel

    Returns:
        Liste des logs d'application
    """
    application_logs = []

    for idx, idee in enumerate(idees, 1):
        if progress_tracker:
            progress_tracker.start_idea(idx, idee)

        logger.info(f"Traitement de l'idée {idx}: {idee[:50]}...")
        logger.info(
            f"{config.get_emoji('application')} Traitement de l'idée sélectionnée :\n{idee}"
        )

        # Étape 1: Plan
        if progress_tracker:
            progress_tracker.start_idea_step(0)
        plan = prompt_plan(idee)
        if progress_tracker:
            progress_tracker.complete_idea_step(0)

        # Étape 2: Critique du plan
        if progress_tracker:
            progress_tracker.start_idea_step(1)
        critique_plan = prompt_critique_plan(plan)
        if progress_tracker:
            progress_tracker.complete_idea_step(1)

        # Étape 3: Défense du plan
        if progress_tracker:
            progress_tracker.start_idea_step(2)
        defense_plan = prompt_defense_plan(plan, critique_plan)
        if progress_tracker:
            progress_tracker.complete_idea_step(2)

        # Étape 4: Révision du plan
        if progress_tracker:
            progress_tracker.start_idea_step(3)
        plan_revise = prompt_revision_plan(plan, critique_plan)
        if progress_tracker:
            progress_tracker.complete_idea_step(3)

        application_logs.append(
            {
                "idee": idee,
                "plan_initial": plan,
                "critique": critique_plan,
                "defense": defense_plan,
                "revision": plan_revise,
            }
        )

        logger.info(f"{config.get_emoji('success')} Plan final révisé :\n{plan_revise}")

    return application_logs


def save_full_log(
    objectif: str,
    contexte: str,
    contraintes: str,
    logs: List[CycleLog],
    synthese: str,
    progress_tracker: Optional[ProgressTracker] = None,
) -> None:
    """
    Sauvegarde les résultats complets du brainstorming.

    Args:
        objectif: L'objectif du brainstorming
        contexte: Le contexte
        contraintes: Les contraintes
        logs: Les logs de tous les cycles
        synthese: La synthèse finale
        progress_tracker: Tracker de progression optionnel
    """
    log_data: BrainstormLog = {
        "objectif": objectif,
        "contexte": contexte,
        "contraintes": contraintes,
        "date": datetime.datetime.now().isoformat(),
        "logs": logs,
        "synthese_finale": synthese,
        "application": [],
    }

    # Extraire les meilleures idées
    lignes = extract_top_ideas_robust(synthese, config.top_ideas_count)

    # Mettre à jour le nombre d'idées si différent de la configuration
    if progress_tracker and len(lignes) != progress_tracker.top_ideas_count:
        progress_tracker.update_total_ideas(len(lignes))

    # Démarrer le traitement des idées
    if progress_tracker:
        progress_tracker.start_idea_processing(len(lignes))

    # Traiter chaque idée
    application_logs = process_ideas(lignes, progress_tracker)

    # Export des idées dans des fichiers séparés si activé
    if config.get("export.save_individual_ideas", True):
        try:
            os.makedirs(config.exports_dir, exist_ok=True)
            for idx, app_log in enumerate(application_logs, 1):
                idee = app_log["idee"]
                safe_title = re.sub(r"[^a-zA-Z0-9_\-]", "_", idee[:40]).strip("_")
                # Utiliser le format configuré ou format par défaut
                if config.get("export.project_presentation.filename_pattern"):
                    filename_pattern = config.get("export.project_presentation.filename_pattern")
                    filename_formatted = filename_pattern.format(index=idx, title_slug=safe_title)
                    filename = Path(config.exports_dir) / f"{filename_formatted}.md"
                else:
                    filename = Path(config.exports_dir) / f"PROJET_{idx:02d}_{safe_title}.md"

                # Créer un document de présentation professionnel
                content = f"""# 🚀 PROJET #{idx:02d} - PRÉSENTATION EXÉCUTIVE

## 💡 **CONCEPT PRINCIPAL**
> {idee}

---

## 📋 **PLAN D'AFFAIRES DÉTAILLÉ**

{app_log["plan_initial"]}

---

## 🔍 **ANALYSE CRITIQUE ET ÉVALUATION**

### ⚠️ Points d'Attention Identifiés
{app_log["critique"]}

---

## 🛡️ **ARGUMENTATION ET JUSTIFICATIONS**

### 💪 Défense Stratégique du Projet
{app_log["defense"]}

---

## ✅ **PLAN FINAL OPTIMISÉ**

### 🎯 Version Finale Intégrant Tous les Retours
{app_log["revision"]}

---

## 📊 **FICHE TECHNIQUE DU PROJET**

| **Critère** | **Détail** |
|-------------|------------|
| **🎯 Projet** | Projet #{idx:02d} |
| **📅 Date de création** | {datetime.datetime.now().strftime("%d/%m/%Y à %H:%M")} |
| **🏷️ Statut** | Prêt pour mise en œuvre |
| **📈 Niveau de maturité** | Plan d'affaires complet |
| **🔄 Processus** | Idée → Critique → Défense → Optimisation |

---

## 🎯 **RÉSUMÉ EXÉCUTIF - PRÊT À PRÉSENTER**

Ce projet a été développé et affiné par un système de brainstorming multi-agents comprenant :
- ✅ **Génération créative** de l'idée originale
- ✅ **Analyse critique** approfondie par des experts
- ✅ **Défense argumentée** avec justifications
- ✅ **Optimisation finale** intégrant tous les retours

**Le projet est maintenant prêt pour :**
- 📋 Présentation aux parties prenantes
- 💰 Recherche de financement
- 🚀 Mise en œuvre opérationnelle
- 📊 Suivi et mesure des résultats

---

*📝 Document généré automatiquement par Brainstorm AI*  
*🤖 Système de brainstorming intelligent multi-agents*  
*⚡ Optimisé pour la prise de décision et l'action*
"""

                try:
                    with open(filename, "w", encoding="utf-8") as f:
                        f.write(content)
                    logger.info(f"📄 Export projet #{idx}: {filename}")
                except OSError as e:
                    logger.error(f"Erreur lors de l'écriture du fichier {filename}: {e}")
        except OSError as e:
            logger.error(f"Erreur lors de la création du dossier {config.exports_dir}: {e}")

    log_data["application"] = application_logs

    # Démarrer l'export
    if progress_tracker:
        progress_tracker.start_export()

    try:
        os.makedirs(config.logs_dir, exist_ok=True)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_filename = config.get_log_filename(timestamp)

        # Export dans les formats activés
        if config.should_export_format("yaml"):
            try:
                export_yaml(
                    log_data, filename=os.path.join(config.logs_dir, f"{log_filename}.yaml")
                )
            except Exception as e:
                logger.error(f"Erreur lors de l'export YAML: {e}")

        if config.should_export_format("json"):
            try:
                export_json(
                    log_data, filename=os.path.join(config.logs_dir, f"{log_filename}.json")
                )
            except Exception as e:
                logger.error(f"Erreur lors de l'export JSON: {e}")

        if config.should_export_format("markdown"):
            try:
                export_markdown(
                    log_data, filename=os.path.join(config.logs_dir, f"{log_filename}.md")
                )
            except Exception as e:
                logger.error(f"Erreur lors de l'export Markdown: {e}")
    except OSError as e:
        logger.error(f"Erreur lors de la création du dossier de logs {config.logs_dir}: {e}")

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
    fallback_score = dict.fromkeys(required_keys, fallback_val)
    fallback_score["total"] = fallback_val * len(required_keys)
    return fallback_score


def extract_top_ideas_robust(synthese_text: str, count: int = 3) -> list[str]:
    """Extraction robuste des meilleures idées avec plusieurs stratégies."""
    strategies = config.get_idea_extraction_strategies()

    # Construire le pattern numéroté correctement
    numbered_pattern = r"^\s*1\.\s*(.+)$" if count == 1 else rf"^\s*[1-{count}]\.\s*(.+)$"

    pattern_map = {
        "numbered": numbered_pattern,
        "starred": r"^\s*\*\s*(.+)$",
        "bullet": r"^\s*-\s*(.+)$",
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
    lines = [line.strip() for line in synthese_text.splitlines() if line.strip()]
    return lines[:count] if len(lines) >= count else lines
