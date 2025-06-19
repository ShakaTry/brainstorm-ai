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
    """Échappe les caractères spéciaux pour le Markdown."""
    if not isinstance(text, str):
        text = str(text)
    # Échapper les caractères spéciaux Markdown
    chars_to_escape = [
        "\\",
        "`",
        "*",
        "_",
        "{",
        "}",
        "[",
        "]",
        "(",
        ")",
        "#",
        "+",
        "-",
        ".",
        "!",
        "|",
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
                f.write("## 💡 Plans d'Application\n\n")
                for idx, app in enumerate(data["application"], 1):
                    f.write(f"### Idée {idx}\n\n")
                    f.write(f"**Idée:** {escape_markdown(app.get('idee', ''))}\n\n")

                    if "plan_initial" in app:
                        f.write("#### Plan Initial\n")
                        f.write("```\n")
                        f.write(app.get("plan_initial", ""))
                        f.write("\n```\n\n")

                    if "revision" in app:
                        f.write("#### Plan Révisé\n")
                        f.write("```\n")
                        f.write(app.get("revision", ""))
                        f.write("\n```\n\n")

        logger.info(f"Export Markdown réussi : {filename}")

    except OSError as e:
        logger.error(f"Erreur lors de l'export Markdown vers {filename}: {e}")
        raise ExportError(f"Impossible d'écrire le fichier Markdown {filename}: {e}") from e
    except Exception as e:
        logger.error(f"Erreur inattendue lors de l'export Markdown : {type(e).__name__}: {e}")
        raise ExportError(f"Erreur inattendue : {type(e).__name__}: {e}") from e
