# 🏷️ Guide du Versioning Automatique

## 📋 Vue d'ensemble

Le projet utilise **bump2version** pour gérer automatiquement le versioning dans tous les fichiers concernés.

## 🔧 Configuration

Le versioning est configuré dans `.bumpversion.cfg` et met à jour automatiquement :
- `VERSION` - Fichier de version simple
- `pyproject.toml` - Configuration du package Python
- `src/brainstorm_ai/__init__.py` - Version dans le module Python

## 🚀 Utilisation

### Méthode 1 : Commande directe

```bash
# Increment patch (2.1.0 → 2.1.1)
bump2version patch

# Increment minor (2.1.0 → 2.2.0)  
bump2version minor

# Increment major (2.1.0 → 3.0.0)
bump2version major
```

### Méthode 2 : Script PowerShell (Windows)

```powershell
# Version patch par défaut
.\scripts\bump_version.ps1

# Version spécifique
.\scripts\bump_version.ps1 patch
.\scripts\bump_version.ps1 minor  
.\scripts\bump_version.ps1 major
```

### Méthode 3 : Makefile (Linux/Mac)

```bash
make bump-patch
make bump-minor
make bump-major
```

## ✅ Ce qui se passe automatiquement

1. **Mise à jour des fichiers** : Tous les fichiers contenant la version sont mis à jour
2. **Commit Git** : Un commit automatique est créé avec le message "Bump version: X.Y.Z → A.B.C"
3. **Tag Git** : Un tag `vA.B.C` est créé automatiquement
4. **Mise à jour config** : Le fichier `.bumpversion.cfg` est mis à jour avec la nouvelle version

## 🛡️ Sécurités

- **Répertoire propre requis** : Git doit être dans un état propre (pas de modifications non commitées)
- **Validation automatique** : Vérification que tous les fichiers contiennent bien la version actuelle
- **Confirmation requise** : Le script PowerShell demande une confirmation avant d'agir

## 🔍 Vérification

Pour vérifier que tout est synchronisé :

```bash
# Afficher la version actuelle
cat VERSION
grep version pyproject.toml
grep __version__ src/brainstorm_ai/__init__.py

# Test en mode dry-run
bump2version --dry-run patch
```

## 🐛 Dépannage

### Erreur "Working directory is dirty"
```bash
# Vérifier les fichiers modifiés
git status

# Commiter ou annuler les modifications
git add . && git commit -m "message"
# ou
git checkout .
```

### Erreur "bump2version not found"
```bash
# Installer bump2version
pip install bump2version

# Ou via les dépendances dev
pip install -r requirements-dev.txt
```

## 📝 Bonnes pratiques

1. **Toujours tester** en mode `--dry-run` d'abord
2. **Commiter** toutes les modifications avant un bump
3. **Choisir le bon type** :
   - `patch` : corrections de bugs, petites améliorations
   - `minor` : nouvelles fonctionnalités, compatibles
   - `major` : changements majeurs, possibles incompatibilités
4. **Vérifier** après le bump que tout est correct 