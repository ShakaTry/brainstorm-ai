# 🚀 Démarrage Rapide - Brainstorm AI

Guide ultra-rapide pour lancer votre premier brainstorming en moins de 5 minutes !

## ⚡ Installation Express

### 1. Prérequis
- Python 3.8+ installé
- Clé API OpenAI

### 2. Installation
```bash
# Cloner et installer
git clone https://github.com/ShakaTry/brainstorm-ai.git
cd brainstorm-ai
pip install -e .
```

### 3. Configuration de la clé API
```bash
# Windows (recommandé)
set OPENAI_API_KEY=votre-clé-api-openai

# Linux/Mac
export OPENAI_API_KEY="votre-clé-api-openai"
```

## 🎯 Lancement Immédiat

### Option 1: Mode Interactif (Recommandé)
```bash
python main.py
```
Le programme vous demandera :
- **Objectif** : Que voulez-vous créer/résoudre ?
- **Contexte** : Dans quel environnement/marché ?
- **Contraintes** : Quelles sont vos limites ?

### Option 2: Configuration Personnalisée
1. Éditez `config/config.yaml`
2. Modifiez la section `general` :
```yaml
general:
  objectif: "Votre objectif ici"
  contexte: "Votre contexte ici"
  contraintes: "Vos contraintes ici"
  cycles: 3
  top_ideas_count: 3
```
3. Lancez : `python main.py`

## 💡 Exemple Rapide

```bash
# Lancer avec une question simple
python main.py
```

**Exemple d'inputs :**
- 🎯 **Objectif :** "Créer une app mobile pour améliorer la productivité"
- 🌍 **Contexte :** "Marché saturé d'apps de productivité, utilisateurs fatigués des outils complexes"
- ⚠️ **Contraintes :** "Budget limité, équipe de 2 développeurs, lancement en 3 mois"

## 📊 Ce Qui Va Se Passer

1. **🔄 Cycles de Brainstorming** (3 par défaut)
   - Génération d'idées créatives
   - Critique constructive
   - Défense et amélioration
   - Révision finale

2. **🧠 Synthèse Intelligente**
   - Compilation des meilleures idées
   - Sélection automatique des plus prometteuses

3. **📋 Plans d'Action**
   - Développement de plans concrets
   - Stratégies de mise en œuvre

## 📁 Résultats

Après exécution, vous trouverez :
- **📄 Logs complets** : `data/logs/brainstorm_YYYY-MM-DD_HH-MM-SS.yaml`
- **💡 Idées détaillées** : `data/exports/` (fichiers individuels)
- **📊 Statistiques** : Coûts et tokens utilisés

## ⚙️ Personnalisation Rapide

### Changer le nombre de cycles
```yaml
general:
  cycles: 5  # Plus de cycles = plus d'idées raffinées
```

### Changer le nombre d'idées finales
```yaml
general:
  top_ideas_count: 5  # Plus d'idées développées
```

### Activer les formats d'export
```yaml
export:
  formats:
    yaml: true
    json: true
    markdown: true
```

## 🔧 Dépannage Rapide

### Erreur "No module named 'brainstorm_ai'"
```bash
pip install -e .
```

### Erreur "OpenAI API key not found"
```bash
# Vérifiez votre clé
echo $OPENAI_API_KEY  # Linux/Mac
echo %OPENAI_API_KEY%  # Windows
```

### Validation de la configuration
```bash
python scripts/check_config.py
```

## 🎉 Première Utilisation Réussie !

Une fois lancé, vous devriez voir :
```
🧠 === BRAINSTORM AI === 
🎯 Objectif : [votre objectif]
💰 Coût estimé : $X.XX
🔄 Cycles prévus : 3
💡 Idées finales : 3

🚀 Démarrage du brainstorming...
```

## 📚 Pour Aller Plus Loin

- **Configuration avancée** : `docs/CONFIG_README.md`
- **Documentation complète** : `README.md`
- **Scripts utilitaires** : `scripts/README.md`

---
🎯 **Conseil** : Commencez par un objectif simple pour votre premier test, puis explorez les options avancées ! 