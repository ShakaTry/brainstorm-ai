# Guide de Configuration - Brainstorm AI

## Vue d'ensemble

Le système de brainstorming IA utilise désormais un fichier de configuration centralisé `config.yaml` qui permet de personnaliser tous les aspects du système sans modifier le code.

## Structure du fichier de configuration

### 1. Configuration générale (`general`)

```yaml
general:
  objectif: "Votre objectif de brainstorming"
  contexte: "Le contexte du projet"
  contraintes: "Les contraintes à respecter"
  cycles: 5  # Nombre de cycles de brainstorming
  top_ideas_count: 3  # Nombre d'idées à développer
  ask_confirmation: true  # Demander confirmation avant de démarrer
```

### 2. Configuration des agents IA (`agents`)

#### Modèles par rôle
```yaml
agents:
  models:
    creatif: "gpt-4"      # Pour la génération d'idées
    critique: "gpt-4"     # Pour l'analyse critique
    revision: "gpt-3.5-turbo"  # Pour la reformulation
    synthese: "gpt-4"     # Pour la synthèse finale
    score: "gpt-3.5-turbo"  # Pour l'évaluation
    application: "gpt-4"  # Pour la planification
```

#### Températures (créativité vs précision)
```yaml
agents:
  temperatures:
    creatif: 0.7   # Plus créatif
    score: 0.3     # Plus précis
    default: 0.7   # Valeur par défaut
```

### 3. Configuration de l'API (`api`)

```yaml
api:
  max_retries: 3        # Nombre de tentatives en cas d'erreur
  retry_delay_base: 2   # Délai entre tentatives
  request_timeout: 60   # Timeout des requêtes
```

### 4. Configuration des exports (`export`)

```yaml
export:
  formats:
    yaml: true      # Export en YAML
    json: false     # Export en JSON
    markdown: false # Export en Markdown
  paths:
    logs_dir: "logs"
    exports_dir: "exports"
  log_filename_pattern: "brainstorm_{timestamp}"
  save_individual_ideas: true
```

### 5. Configuration de l'affichage (`display`)

```yaml
display:
  use_emojis: true       # Utiliser des emojis
  show_token_usage: true # Afficher la consommation de tokens
  emojis:
    creatif: "💡"
    critique: "🔍"
    # ... etc
```

## Exemples d'utilisation

### Modifier l'objectif du brainstorming

Changez simplement la valeur dans `config.yaml` :
```yaml
general:
  objectif: "Développer une application mobile innovante"
```

### Utiliser GPT-3.5 pour économiser des tokens

```yaml
agents:
  models:
    creatif: "gpt-3.5-turbo"
    critique: "gpt-3.5-turbo"
```

### Désactiver l'affichage des emojis

```yaml
display:
  use_emojis: false
```

### Exporter dans plusieurs formats

```yaml
export:
  formats:
    yaml: true
    json: true
    markdown: true
```

## Configuration avancée

### Stratégies d'extraction d'idées

Le système peut extraire les idées principales selon différents formats :
```yaml
advanced:
  idea_extraction_strategies:
    - "numbered"    # 1. 2. 3.
    - "starred"     # * idée
    - "bullet"      # - idée
    - "fallback"    # Premières lignes
```

### Validation des scores

Personnalisez les critères d'évaluation :
```yaml
advanced:
  score_validation:
    min_value: 0
    max_value: 10
    required_keys: ["impact", "faisabilite", "originalite", "clarte"]
    fallback_value: 5
```

## Configuration de la clé API OpenAI

La clé API OpenAI doit être configurée comme variable d'environnement système pour des raisons de sécurité.

### Sous Windows
1. Ouvrir les "Paramètres système avancés"
2. Cliquer sur "Variables d'environnement"
3. Dans les variables utilisateur ou système, ajouter :
   - **Nom** : `OPENAI_API_KEY`
   - **Valeur** : votre clé API OpenAI

### Alternative avec PowerShell (temporaire)
```powershell
$env:OPENAI_API_KEY = "votre-clé-api-ici"
```

### Vérification
Pour vérifier que la variable est correctement définie :
```powershell
echo $env:OPENAI_API_KEY
```

## Notes importantes

- La clé API OpenAI doit être définie comme variable d'environnement système (`OPENAI_API_KEY`) pour des raisons de sécurité
- Les chemins de fichiers sont relatifs au répertoire du projet
- Les modifications du fichier `config.yaml` sont prises en compte au prochain lancement du programme

## Dépannage

Si vous rencontrez une erreur :
1. Vérifiez que `config.yaml` existe à la racine du projet
2. Assurez-vous que toutes les sections requises sont présentes
3. Vérifiez la syntaxe YAML (indentation, guillemets, etc.)
4. Consultez les valeurs par défaut dans le code si nécessaire 