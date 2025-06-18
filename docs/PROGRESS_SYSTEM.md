# 📊 Système de Progression Visuelle

## Vue d'ensemble

Le système de progression visuelle a été ajouté pour offrir un suivi en temps réel de l'avancement du brainstorm. Il affiche une barre de progression, des indicateurs de phase et des émojis pour une meilleure expérience utilisateur.

## 🎯 Fonctionnalités

### Barre de Progression
- **Affichage en temps réel** : `[████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░] 35.2%`
- **Calcul automatique** : Basé sur le nombre total d'étapes prévues
- **Mise à jour dynamique** : Progression en temps réel pendant l'exécution

### Indicateurs de Phase
- **Phase actuelle** : Affiche le cycle, l'étape et l'action en cours
- **Émojis contextuels** : Chaque étape a son emoji dédié
- **Messages de statut** : Indique ce qui se passe actuellement

### 💰 **Suivi des Coûts et Tokens (NOUVEAU)**
- **Suivi temps réel** : `💰 15,247 tokens | $0.0654`
- **Estimation préalable** : Coût total estimé avant confirmation
- **Résumé détaillé** : Récapitulatif complet en fin de session
- **Support multi-modèles** : Calcul précis selon les prix OpenAI
- **Transparence totale** : Aucune surprise sur les coûts

### Suivi Multi-niveaux
1. **Cycles de brainstorming** (6 étapes par cycle)
   - 🎨 Créatif
   - 🔍 Critique
   - 🛡️ Défense
   - 💬 Réplique
   - ✏️ Révision
   - 📊 Score

2. **Synthèse finale** (1 étape)
   - 🧠 Génération de la synthèse

3. **Traitement des idées** (4 étapes par idée)
   - 📋 Plan
   - 🔍 Critique
   - 🛡️ Défense
   - ✏️ Révision

4. **Export** (1 étape)
   - 💾 Sauvegarde des résultats

## 🛠️ Configuration

### Activation/Désactivation
Dans `config.yaml` :

```yaml
display:
  # Afficher la barre de progression
  show_progress: true
  
  # Utiliser des emojis
  use_emojis: true
```

### Personnalisation des Émojis
```yaml
display:
  emojis:
    start: "🚀"     # Démarrage
    cycle: "🔄"     # Cycles
    creatif: "🎨"   # Phase créative
    critique: "🔍"  # Phase critique
    defense: "🛡️"   # Phase défense
    replique: "💬"  # Phase réplique
    revision: "✏️"  # Phase révision
    synthese: "🧠"  # Synthèse
    application: "📌" # Application
    export: "💾"    # Export
    success: "✅"   # Succès
```

## 📋 Structure des Étapes

### Calcul du Total d'Étapes
```
Total = (Cycles × 6) + 1 + (Idées × 4) + 1

Exemple avec 3 cycles, 5 idées :
Total = (3 × 6) + 1 + (5 × 4) + 1 = 18 + 1 + 20 + 1 = 40 étapes
```

### Progression Détaillée
1. **Initialisation** (0 étapes comptées)
2. **Cycles** : 6 étapes × nombre de cycles
3. **Synthèse** : 1 étape
4. **Traitement des idées** : 4 étapes × nombre d'idées extraites
5. **Export** : 1 étape

## 🎨 Affichage Type

```
🚀 === DÉBUT DU BRAINSTORM ===
📊 Progression totale: 40 étapes
🔄 Cycles prévus: 3
💡 Idées à traiter: 5

[████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░] 20.0% | Phase: Cycle 1/3 - Créatif | 🎨 Créatif...
[█████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░] 22.5% | Phase: Cycle 1/3 - Créatif | 🎨 Créatif ✓

🔄 === CYCLE 1 ===
[content cycle affiché normalement]

[████████████████████████████████████████] 100.0% | Phase: Export | 💾 Export terminé ✓

✅ === BRAINSTORM TERMINÉ ===
✅ Toutes les étapes ont été complétées avec succès!
📊 40/40 étapes accomplies
```

## 🔧 Classes et Méthodes

### ProgressTracker
Classe principale de gestion de la progression.

#### Méthodes Principales
- `start_brainstorm()` : Initialise le suivi
- `start_cycle(cycle_num)` : Démarre un nouveau cycle
- `start_cycle_step(step_num)` : Démarre une étape de cycle
- `complete_cycle_step(step_num)` : Complète une étape de cycle
- `start_synthesis()` : Démarre la synthèse
- `complete_synthesis()` : Complète la synthèse
- `start_idea_processing(total_ideas)` : Démarre le traitement des idées
- `start_idea(idea_num, idea_text)` : Démarre une idée
- `start_idea_step(step_num)` : Démarre une étape d'idée
- `complete_idea_step(step_num)` : Complète une étape d'idée
- `start_export()` : Démarre l'export
- `complete_export()` : Complète l'export
- `finish()` : Termine le suivi

## 🧪 Test et Démonstration

### Script de Démonstration
```bash
python demo_progression.py
```

Ce script simule un brainstorm complet pour montrer le système de progression sans faire d'appels API réels.

### Intégration dans le Code Principal
Le système est automatiquement intégré dans `main.py` et `loop_manager.py`. Aucune action supplémentaire n'est requise.

## 🎛️ Désactivation
Pour désactiver le système de progression :

```yaml
display:
  show_progress: false
```

Le brainstorm fonctionnera normalement sans affichage de progression.

## 🔍 Dépannage

### Affichage Incorrect
- Vérifiez que `display.show_progress: true` dans `config.yaml`
- Assurez-vous que le terminal supporte les caractères Unicode

### Performance
- Le système ajoute un délai minimal (0.2s) entre les étapes pour la lisibilité
- Peut être désactivé si nécessaire pour des performances maximales

### Compatibilité Terminal
- Fonctionne avec la plupart des terminaux modernes
- Supporte les caractères Unicode pour les barres de progression et émojis
- Fallback gracieux si les émojis ne sont pas supportés

## 💰 **Système de Suivi des Coûts et Tokens**

### 🎯 **Vue d'Ensemble**
Le système de suivi des coûts offre une transparence totale sur la consommation de tokens et les coûts associés aux appels API OpenAI.

### 📊 **Fonctionnalités**

#### 📋 **Estimation Préalable**
Avant le démarrage du brainstorm, une estimation complète est affichée :

```
💰 === ESTIMATION DU COÛT ===
📞 Appels API prévus: 21
💵 Coût estimé: $0.2730

📊 Répartition par modèle:
   • gpt-4o: 21 appels - $0.2730
```

#### 📈 **Suivi Temps Réel**
Pendant l'exécution, les informations de coût sont intégrées à la barre de progression :

```
[████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░] 35.2% | Phase: Cycle 2/3 - Critique | 💰 15,247 tokens | $0.0654 | 🔍 Analyse...
```

**Éléments affichés :**
- `💰 15,247 tokens` : Nombre total de tokens consommés
- `$0.0654` : Coût cumulé en dollars américains
- Mise à jour automatique après chaque appel API

#### 📊 **Résumé Final Détaillé**
À la fin du brainstorm, un résumé complet est affiché :

```
💰 === RÉSUMÉ DES COÛTS ===
📝 Total d'appels API: 21
🔤 Tokens d'entrée: 47,668
🔤 Tokens de sortie: 15,644
🔤 Tokens totaux: 63,312
💵 Coût total: $0.2756

📊 Répartition par modèle:
   • gpt-4o: 21 appels - $0.2756
```

### ⚙️ **Configuration des Prix**

Les prix des modèles OpenAI sont configurés dans `config.yaml` :

```yaml
api:
  # Prix des modèles OpenAI (en dollars par 1000 tokens)
  pricing:
    gpt-4o:
      input: 0.0025      # $2.50 per 1K input tokens
      output: 0.01       # $10.00 per 1K output tokens
    gpt-4o-mini:
      input: 0.00015     # $0.15 per 1K input tokens
      output: 0.0006     # $0.60 per 1K output tokens
    gpt-4:
      input: 0.03        # $30.00 per 1K input tokens
      output: 0.06       # $60.00 per 1K output tokens
    gpt-3.5-turbo:
      input: 0.0005      # $0.50 per 1K input tokens
      output: 0.0015     # $1.50 per 1K output tokens
```

### 🔧 **Méthodes de Calcul**

#### Estimation du Coût Total
```python
config.estimate_total_cost(cycles, ideas_count)
```

#### Calcul du Coût d'un Appel
```python
config.calculate_cost(model, input_tokens, output_tokens)
```

#### Suivi des Appels API
```python
progress_tracker.add_api_call(model, input_tokens, output_tokens)
```

### 📈 **Avantages**

1. **Transparence totale** : Aucune surprise sur les coûts
2. **Contrôle budgétaire** : Estimation avant confirmation
3. **Optimisation** : Identification des phases coûteuses
4. **Historique** : Suivi détaillé par session
5. **Multi-modèles** : Support de tous les modèles OpenAI

### 🎮 **Test du Système**

Utilisez la démonstration pour voir le système en action :

```bash
python demo_progression.py
```

La démonstration simule les appels API et montre le suivi des coûts sans consommer de tokens réels. 