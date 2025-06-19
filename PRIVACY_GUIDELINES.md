# 🔒 Directives de Confidentialité - Brainstorm AI

## ⚠️ Informations Sensibles à Protéger

Ce projet peut traiter des informations sensibles qui **NE DOIVENT JAMAIS** être commitées dans le repository public.

### 🚨 Données Strictement Confidentielles

#### 1. Clés API et Authentification
- ❌ `OPENAI_API_KEY` - Clé API OpenAI
- ❌ Tokens GitHub personnels
- ❌ Mots de passe et secrets
- ❌ Configurations personnalisées avec identifiants

#### 2. Données Utilisateur
- ❌ Logs de sessions réelles avec objectifs personnels/professionnels
- ❌ Exports contenant des idées propriétaires
- ❌ Informations identifiantes (noms, entreprises, projets spécifiques)
- ❌ Données de brainstorming confidentielles

#### 3. Configurations Locales
- ❌ Fichiers `config_local.yaml` ou `*_private.yaml`
- ❌ Configurations personnalisées d'IDE
- ❌ Caches et données temporaires

## ✅ Bonnes Pratiques de Sécurité

### Configuration Environnement
```bash
# 1. Copiez le fichier d'exemple
cp config/env.example .env

# 2. Ajoutez votre clé API (jamais committée)
echo "OPENAI_API_KEY=sk-votre-clé-ici" >> .env

# 3. Vérifiez que .env est dans .gitignore
git status  # .env ne doit PAS apparaître
```

### Gestion des Logs et Exports
```bash
# Les vrais logs/exports sont automatiquement ignorés
# Seuls les fichiers example_* sont versionnés

# ✅ Fichiers d'exemple (versionnés)
data/logs/example_brainstorm_session.yaml
data/exports/example_idees_innovantes.txt

# ❌ Fichiers réels (ignorés)
data/logs/brainstorm_2024-*.yaml
data/exports/mes_idees_*.txt
```

### Anonymisation des Données
Avant de partager ou déboguer :

1. **Remplacez les identifiants** par des exemples génériques
2. **Supprimez les références** à des personnes/entreprises réelles  
3. **Utilisez des données factices** pour les tests publics
4. **Vérifiez le contenu** avant tout commit

## 🛡️ Vérifications Automatiques

### Avant Chaque Commit
```bash
# Vérifiez qu'aucune info sensible n'est ajoutée
git status
git diff --cached

# Les fichiers suivants ne doivent JAMAIS apparaître :
# - .env (sauf .env.example)
# - data/logs/*.yaml (sauf example_*)
# - Fichiers avec des clés API ou mots de passe
```

### Commandes de Vérification
```bash
# Recherche de clés API potentielles
grep -r "sk-" . --exclude-dir=.git
grep -r "OPENAI_API_KEY=" . --exclude-dir=.git

# Recherche d'emails/noms dans les logs
grep -r "@" data/logs/ --include="*.yaml" --exclude="example_*"
```

## 🔍 Que Faire en Cas de Fuite

### Si Vous Avez Commité des Données Sensibles

1. **Action Immédiate**
   ```bash
   # Supprimez le fichier sensible
   git rm --cached fichier_sensible.yaml
   git commit -m "Suppression données sensibles"
   ```

2. **Nettoyage Historique (si nécessaire)**
   ```bash
   # ATTENTION: Modifie l'historique Git
   git filter-branch --force --index-filter 'git rm --cached --ignore-unmatch fichier_sensible.yaml' HEAD
   ```

3. **Régénération des Clés**
   - Régénérez immédiatement les clés API compromises
   - Mettez à jour les configurations locales

## 📝 Exemples de Données Acceptables

### ✅ Données d'Exemple (OK pour Git)
```yaml
objectif: "Développer une stratégie marketing innovante"
contexte: "Entreprise fictive dans le secteur technologique"
user_id: "user_example_001"
```

### ❌ Données Réelles (Interdit)
```yaml
objectif: "Développer la stratégie 2024 pour TechCorp SA"
contexte: "Réunion avec Jean Dupont, CMO de TechCorp"  
user_id: "jean.dupont@techcorp.fr"
```

## 🎯 Responsabilités

### Développeurs
- Vérifier le contenu avant chaque commit
- Utiliser les fichiers d'exemple pour les tests
- Maintenir le `.gitignore` à jour

### Utilisateurs
- Configurer correctement leur environnement local
- Ne jamais partager leurs fichiers `.env`
- Signaler toute donnée sensible accidentellement exposée

---

🔐 **Rappel** : La sécurité est l'affaire de tous. En cas de doute, demandez conseil avant de commiter ! 