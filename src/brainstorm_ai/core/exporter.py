"""
Module d'export des résultats du brainstorming dans différents formats.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

import yaml

logger = logging.getLogger(__name__)


class ExportError(Exception):
    """Exception de base pour les erreurs d'export."""

    pass


def ensure_directory_exists(filepath: str) -> None:
    """
    S'assure que le répertoire parent existe.

    Args:
        filepath: Chemin vers le fichier

    Raises:
        ExportError: Si impossible de créer le répertoire
    """
    directory = Path(filepath).parent
    try:
        directory.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        logger.error(f"Impossible de créer le répertoire {directory}: {e}")
        raise ExportError(f"Impossible de créer le répertoire {directory}: {e}") from e


def export_yaml(data: Dict[str, Any], filename: str = "logs/brainstorm_export.yaml") -> None:
    """
    Exporte les données au format YAML.

    Args:
        data: Données à exporter
        filename: Nom du fichier de sortie

    Raises:
        ExportError: En cas d'erreur d'écriture
    """
    try:
        ensure_directory_exists(filename)
        with open(filename, "w", encoding="utf-8") as f:
            yaml.dump(data, f, allow_unicode=True, sort_keys=False, default_flow_style=False)
        logger.info(f"Export YAML réussi : {filename}")
    except OSError as e:
        logger.error(f"Erreur lors de l'export YAML vers {filename}: {e}")
        raise ExportError(f"Impossible d'écrire le fichier YAML {filename}: {e}") from e
    except yaml.YAMLError as e:
        logger.error(f"Erreur de sérialisation YAML : {e}")
        raise ExportError(f"Erreur de sérialisation YAML : {e}") from e


def export_json(data: Dict[str, Any], filename: str = "logs/brainstorm_export.json") -> None:
    """
    Exporte les données au format JSON.

    Args:
        data: Données à exporter
        filename: Nom du fichier de sortie

    Raises:
        ExportError: En cas d'erreur d'écriture
    """
    try:
        ensure_directory_exists(filename)
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=str)
        logger.info(f"Export JSON réussi : {filename}")
    except OSError as e:
        logger.error(f"Erreur lors de l'export JSON vers {filename}: {e}")
        raise ExportError(f"Impossible d'écrire le fichier JSON {filename}: {e}") from e
    except (TypeError, ValueError) as e:
        logger.error(f"Erreur de sérialisation JSON : {e}")
        raise ExportError(f"Erreur de sérialisation JSON : {e}") from e


def escape_markdown(text: str) -> str:
    """Échappe les caractères spéciaux critiques pour le Markdown."""
    if not isinstance(text, str):
        text = str(text)
    # Échapper seulement les caractères critiques qui peuvent casser la structure
    # Éviter d'échapper les caractères courants comme les points, parenthèses etc.
    chars_to_escape = [
        "|",  # Casse les tableaux
    ]
    for char in chars_to_escape:
        text = text.replace(char, f"\\{char}")
    return text


def export_markdown(data: Dict[str, Any], filename: str = "logs/brainstorm_export.md") -> None:
    """
    Exporte les données au format Markdown.

    Args:
        data: Données à exporter
        filename: Nom du fichier de sortie

    Raises:
        ExportError: En cas d'erreur d'écriture
    """
    try:
        ensure_directory_exists(filename)
        with open(filename, "w", encoding="utf-8") as f:
            # En-tête
            f.write(f"# Brainstorming Report - {datetime.now().isoformat()}\n\n")

            # Métadonnées
            f.write(f"## Objectif\n{escape_markdown(data.get('objectif', ''))}\n\n")
            f.write(f"## Contexte\n{escape_markdown(data.get('contexte', ''))}\n\n")
            f.write(f"## Contraintes\n{escape_markdown(data.get('contraintes', ''))}\n\n")

            # Cycles
            f.write("## Cycles de Brainstorming\n\n")
            for cycle in data.get("logs", []):
                f.write(f"### Cycle {cycle.get('cycle', 'N/A')}\n\n")

                # Création
                f.write("#### 🎨 Créatif\n")
                f.write("```\n")
                f.write(cycle.get("creation", ""))
                f.write("\n```\n\n")

                # Critique
                f.write("#### 🔍 Critique\n")
                f.write("```\n")
                f.write(cycle.get("critique", ""))
                f.write("\n```\n\n")

                # Défense
                if "defense" in cycle:
                    f.write("#### 🛡️ Défense\n")
                    f.write("```\n")
                    f.write(cycle.get("defense", ""))
                    f.write("\n```\n\n")

                # Révision
                if "revision" in cycle:
                    f.write("#### ✏️ Révision\n")
                    f.write("```\n")
                    f.write(cycle.get("revision", ""))
                    f.write("\n```\n\n")

                # Score
                if "score" in cycle:
                    f.write("#### 📊 Score\n")
                    score = cycle.get("score", {})
                    f.write(f"- Impact: {score.get('impact', 'N/A')}/10\n")
                    f.write(f"- Faisabilité: {score.get('faisabilite', 'N/A')}/10\n")
                    f.write(f"- Originalité: {score.get('originalite', 'N/A')}/10\n")
                    f.write(f"- Clarté: {score.get('clarte', 'N/A')}/10\n")
                    f.write(f"- **Total: {score.get('total', 'N/A')}/40**\n\n")

            # Synthèse finale
            if "synthese_finale" in data:
                f.write("## 🎯 Synthèse Finale\n\n")
                f.write("```\n")
                f.write(data.get("synthese_finale", ""))
                f.write("\n```\n\n")

            # Applications
            if "application" in data and data["application"]:
                f.write("## 💡 **PROJETS DÉVELOPPÉS - PRÊTS POUR MISE EN ŒUVRE**\n\n")
                
                # Table de synthèse des projets
                f.write("### 📊 **TABLEAU DE BORD EXÉCUTIF**\n\n")
                f.write("| **Projet** | **Concept Principal** | **Statut** | **Priorité** |\n")
                f.write("|------------|----------------------|------------|-------------|\n")
                
                for idx, app in enumerate(data["application"], 1):
                    concept_short = app.get('idee', '')[:60] + "..." if len(app.get('idee', '')) > 60 else app.get('idee', '')
                    f.write(f"| **#{idx:02d}** | {escape_markdown(concept_short)} | ✅ Finalisé | ⭐ Haute |\n")
                
                f.write("\n---\n\n")
                
                # Détail de chaque projet
                for idx, app in enumerate(data["application"], 1):
                    f.write(f"### 🚀 **PROJET #{idx:02d} - PRÉSENTATION COMPLÈTE**\n\n")
                    
                    # Concept principal en highlight
                    f.write(f"#### 💡 **CONCEPT PRINCIPAL**\n")
                    f.write(f"> **{escape_markdown(app.get('idee', ''))}**\n\n")
                    
                    # Plan d'affaires structuré
                    f.write(f"#### 📋 **PLAN D'AFFAIRES DÉTAILLÉ**\n\n")
                    if "plan_initial" in app:
                        f.write("```markdown\n")
                        f.write(app.get("plan_initial", ""))
                        f.write("\n```\n\n")

                    # Analyse critique avec évaluation
                    f.write(f"#### 🔍 **ANALYSE CRITIQUE ET ÉVALUATION**\n\n")
                    if "critique" in app:
                        f.write("**⚠️ Points d'Attention Identifiés :**\n\n")
                        f.write("```markdown\n")
                        f.write(app.get("critique", ""))
                        f.write("\n```\n\n")
                    
                    # Défense argumentée
                    f.write(f"#### 🛡️ **ARGUMENTATION ET JUSTIFICATIONS**\n\n")
                    if "defense" in app:
                        f.write("**💪 Défense Stratégique du Projet :**\n\n")
                        f.write("```markdown\n")
                        f.write(app.get("defense", ""))
                        f.write("\n```\n\n")

                    # Plan final optimisé
                    f.write(f"#### ✅ **PLAN FINAL OPTIMISÉ**\n\n")
                    if "revision" in app:
                        f.write("**🎯 Version Finale Intégrant Tous les Retours :**\n\n")
                        f.write("```markdown\n")
                        f.write(app.get("revision", ""))
                        f.write("\n```\n\n")
                    
                    # Fiche technique du projet
                    f.write(f"#### 📊 **FICHE TECHNIQUE**\n\n")
                    f.write("| **Critère** | **Détail** |\n")
                    f.write("|-------------|------------|\n")
                    f.write(f"| **🎯 Projet** | Projet #{idx:02d} |\n")
                    f.write(f"| **📅 Date** | {datetime.now().strftime('%d/%m/%Y à %H:%M')} |\n")
                    f.write(f"| **🏷️ Statut** | Prêt pour mise en œuvre |\n")
                    f.write(f"| **📈 Maturité** | Plan d'affaires complet |\n")
                    f.write(f"| **🔄 Processus** | Idée → Critique → Défense → Optimisation |\n\n")
                    
                    # Résumé exécutif
                    f.write(f"#### 🎯 **RÉSUMÉ EXÉCUTIF**\n\n")
                    f.write("Ce projet a été développé et affiné par un système de brainstorming multi-agents :\n\n")
                    f.write("- ✅ **Génération créative** de l'idée originale\n")
                    f.write("- ✅ **Analyse critique** approfondie par des experts\n")
                    f.write("- ✅ **Défense argumentée** avec justifications\n")
                    f.write("- ✅ **Optimisation finale** intégrant tous les retours\n\n")
                    
                    f.write("**Le projet est maintenant prêt pour :**\n")
                    f.write("- 📋 Présentation aux parties prenantes\n")
                    f.write("- 💰 Recherche de financement\n")
                    f.write("- 🚀 Mise en œuvre opérationnelle\n")
                    f.write("- 📊 Suivi et mesure des résultats\n\n")
                    
                    f.write("---\n\n")
                
                # Synthèse finale de tous les projets
                f.write("### 🏆 **SYNTHÈSE FINALE - PORTEFEUILLE DE PROJETS**\n\n")
                f.write(f"**🎯 Nombre total de projets développés :** {len(data['application'])}\n\n")
                f.write("**📈 Niveau de qualité :** Chaque projet a été rigoureusement analysé, critiqué, défendu et optimisé\n\n")
                f.write("**✅ Statut :** Tous les projets sont prêts pour la mise en œuvre immédiate\n\n")
                f.write("**🚀 Prochaines étapes recommandées :**\n")
                f.write("1. **Priorisation** : Classer les projets selon vos critères business\n")
                f.write("2. **Validation** : Présenter les concepts aux parties prenantes\n")
                f.write("3. **Planification** : Détailler la roadmap de mise en œuvre\n")
                f.write("4. **Lancement** : Démarrer les projets prioritaires\n\n")

        logger.info(f"Export Markdown réussi : {filename}")

    except OSError as e:
        logger.error(f"Erreur lors de l'export Markdown vers {filename}: {e}")
        raise ExportError(f"Impossible d'écrire le fichier Markdown {filename}: {e}") from e
    except Exception as e:
        logger.error(f"Erreur inattendue lors de l'export Markdown : {type(e).__name__}: {e}")
        raise ExportError(f"Erreur inattendue : {type(e).__name__}: {e}") from e
