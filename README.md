# 🧠 Brainstorm AI

Un système de brainstorming intelligent utilisant plusieurs agents IA spécialisés pour générer, critiquer, défendre et améliorer des idées de manière collaborative.

## 🎯 Description

Brainstorm AI est un outil de génération d'idées qui simule un processus de brainstorming collaboratif en utilisant différents agents IA avec des rôles spécialisés :

- **Agent Créatif** 💡 : Génère des idées innovantes et originales
- **Agent Critique** 🔍 : Analyse et critique constructive des idées
- **Agent de Défense** 🛡️ : Défend et améliore les idées critiquées
- **Agent de Révision** ✏️ : Reformule et peaufine les idées
- **Agent de Synthèse** 🧠 : Synthétise et structure les meilleures idées
- **Agent de Score** 📊 : Évalue les idées selon des critères objectifs
- **Agent d'Application** 📌 : Développe des plans concrets de mise en œuvre

## ✨ Caractéristiques

- **Processus itératif** : Système de cycles d'amélioration continue
- **Configuration flexible** : Personnalisation complète via `config.yaml`
- **Modèles IA optimisés** : Powered by GPT-4o pour des performances maximales
- **Export multi-format** : YAML, JSON, et Markdown
- **Gestion intelligente** : Détection de redondance et optimisation des tokens
- **Interface intuitive** : Affichage avec emojis et progression claire
- **Historique complet** : Sauvegarde de tous les cycles et analyses

## 🚀 Installation

### Prérequis

- Python 3.8+
- Clé API OpenAI
- Les dépendances Python (voir requirements.txt si disponible)

### Installation des dépendances

```bash
pip install openai python-dotenv pyyaml
```

### Configuration de la clé API OpenAI

#### Windows (Recommandé)
1. Ouvrir les "Paramètres système avancés"
2. Cliquer sur "Variables d'environnement"
3. Ajouter une nouvelle variable :
   - **Nom** : `OPENAI_API_KEY`
   - **Valeur** : votre clé API OpenAI

#### Alternative PowerShell (temporaire)
```powershell
$env:OPENAI_API_KEY = "votre-clé-api-ici"
```

#### Fichier .env (optionnel)
Créer un fichier `.env` à la racine du projet :
```env
OPENAI_API_KEY=votre-clé-api-ici
```

## 🎮 Utilisation

### Lancement rapide

```bash
python main.py
```

### Configuration personnalisée

1. Modifiez le fichier `config.yaml` selon vos besoins
2. Lancez le programme : `python main.py`

### Exemple de configuration

```yaml
general:
  objectif: "Créer un service IA innovant pour freelancers"
  contexte: "Marché en croissance de l'IA et du travail indépendant"
  contraintes: "Solution locale, pas de SaaS mensuel"
  cycles: 3
  top_ideas_count: 5
```

## 📊 Processus de brainstorming

### Cycle de développement d'idées

1. **Génération** 💡 : L'agent créatif propose 3 nouvelles idées
2. **Critique** 🔍 : Analyse objective des forces et faiblesses
3. **Défense** 🛡️ : Justification et amélioration des idées
4. **Réplique** 🔄 : Contre-argumentation et approfondissement
5. **Révision** ✏️ : Version finale améliorée de l'idée

### Synthèse et application

1. **Synthèse** 🧠 : Compilation des meilleures idées
2. **Sélection** 📌 : Extraction des idées les plus prometteuses
3. **Planification** 📋 : Développement de plans d'action concrets

## 📁 Structure du projet

```
brainstorm_ai/
├── agents/                 # Agents IA spécialisés
│   ├── agent_creatif.py   # Génération d'idées
│   ├── agent_critique.py  # Analyse critique
│   ├── agent_revision.py  # Amélioration des idées
│   ├── agent_synthese.py  # Synthèse finale
│   ├── agent_score.py     # Évaluation quantitative
│   └── agent_application.py # Plans d'action
├── core/                   # Moteur principal
│   ├── config.py          # Gestion de la configuration
│   ├── gpt.py            # Interface OpenAI
│   ├── loop_manager.py   # Orchestration des cycles
│   ├── exporter.py       # Export multi-format
│   └── utils.py          # Utilitaires
├── logs/                  # Historique des sessions
├── tests/                 # Tests unitaires
├── config.yaml           # Configuration principale
├── main.py               # Point d'entrée
└── README.md             # Documentation
```

## ⚙️ Configuration avancée

### Modèles IA optimisés

```yaml
agents:
  models:
    creatif: "gpt-4o"          # Créativité maximale et rapidité
    critique: "gpt-4o"         # Analyse approfondie et précise
    revision: "gpt-4o"         # Révision de qualité optimale
    synthese: "gpt-4o"         # Synthèse complexe et structurée
    score: "gpt-4o"            # Évaluation précise et cohérente
```

### Températures par rôle

```yaml
agents:
  temperatures:
    creatif: 0.9    # Très créatif
    critique: 0.4   # Très précis
    revision: 0.6   # Équilibré
    score: 0.2      # Très factuel
```

### Formats d'export

```yaml
export:
  formats:
    yaml: true      # Données structurées
    json: true      # Compatibilité outils
    markdown: true  # Documentation lisible
```

## 📈 Optimisations incluses

- **Gestion intelligente du contexte** : Limitation automatique pour optimiser les tokens
- **Stratégies d'extraction robustes** : Plusieurs méthodes pour identifier les meilleures idées
- **Validation des scores** : Système de fallback pour assurer la cohérence
- **Détection de redondance** : Évite la répétition d'idées similaires
- **Retry automatique** : Gestion des erreurs API avec backoff exponentiel

## 🧪 Tests

Lancer les tests unitaires :

```bash
pytest
```

Tests disponibles :
- Tests des agents individuels
- Tests du gestionnaire de boucles
- Tests d'export et configuration
- Tests des utilitaires

## 📝 Logs et exports

### Structure des logs

```yaml
objectif: "Votre objectif"
contexte: "Le contexte"
date: "2025-06-18T23:01:43"
logs:
  - cycle: 1
    creation: "Idées générées..."
    critique: "Analyse critique..."
    # ... autres étapes
synthese_finale: "Synthèse des meilleures idées"
application:
  - idee: "Idée sélectionnée"
    plan_initial: "Plan d'action"
    # ... développement du plan
```

### Exports automatiques

- **Logs complets** : Sauvegarde de chaque session dans `/logs`
- **Idées individuelles** : Fichiers séparés dans `/exports` (optionnel)
- **Statistiques** : Consommation de tokens et performances

## 🤝 Contribution

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/AmazingFeature`)
3. Commit vos changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🆘 Support

- **Documentation** : Consultez le fichier `CONFIG_README.md` pour la configuration détaillée
- **Issues** : Rapportez les bugs sur GitHub Issues
- **Optimisations** : Voir `OPTIMIZATIONS.md` pour les améliorations de performance

## 🏆 Exemples d'utilisation

### Cas d'usage typiques

- **Développement de produits** : Génération d'idées pour nouveaux services
- **Résolution de problèmes** : Approches créatives pour défis complexes
- **Innovation business** : Modèles économiques et stratégies
- **Amélioration de processus** : Optimisation de workflows existants

### Résultats attendus

- **3-5 idées finalisées** par session (configurable)
- **Plans d'action détaillés** pour chaque idée retenue
- **Analyse critique constructive** de chaque proposition
- **Scores quantitatifs** pour comparer objectivement les idées

---

*Développé avec 🧠 par une collaboration entre intelligence humaine et artificielle* 