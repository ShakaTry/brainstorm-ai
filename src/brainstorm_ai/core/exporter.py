import os
import yaml
import json
from datetime import datetime

def export_yaml(data, filename="logs/brainstorm_export.yaml"):
    with open(filename, "w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True, sort_keys=False)

def export_json(data, filename="logs/brainstorm_export.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def escape_markdown(text):
    """Échappe les caractères spéciaux pour le Markdown."""
    return text.replace("`", "\`").replace("*", "\*").replace("_", "\_")

def export_markdown(data, filename="logs/brainstorm_export.md"):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"# Brainstorming Report - {datetime.now().isoformat()}\n")

        f.write(f"## Objectif\n{escape_markdown(data.get('objectif', ''))}\n\n")
        f.write(f"## Contexte\n{escape_markdown(data.get('contexte', ''))}\n\n")
        f.write(f"## Contraintes\n{escape_markdown(data.get('contraintes', ''))}\n\n")
        for cycle in data.get("logs", []):
            f.write(f"### Cycle {cycle.get('cycle', '')}\n")
            f.write("**Créatif :**\n``\n" + escape_markdown(cycle.get("creation", "")) + "\n``\n")
            f.write("**Critique :**\n``\n" + escape_markdown(cycle.get("critique", "")) + "\n``\n\n")