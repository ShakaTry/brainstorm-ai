# Script PowerShell pour gestion du versioning avec bump2version
# Usage: .\scripts\bump_version.ps1 [patch|minor|major]

param(
    [Parameter(Position=0)]
    [ValidateSet("patch", "minor", "major")]
    [string]$Type = "patch"
)

Write-Host "🔧 Bump Version - Brainstorm AI" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan

# Vérifier que bump2version est installé
try {
    $null = Get-Command bump2version -ErrorAction Stop
} catch {
    Write-Host "❌ bump2version n'est pas installé. Installation..." -ForegroundColor Red
    pip install bump2version
}

# Afficher la version actuelle
$currentVersion = Get-Content VERSION
Write-Host "📋 Version actuelle: $currentVersion" -ForegroundColor Yellow

# Calculer la nouvelle version pour affichage
$versionParts = $currentVersion.Split('.')
$major = [int]$versionParts[0]
$minor = [int]$versionParts[1] 
$patch = [int]$versionParts[2]

switch ($Type) {
    "patch" { $patch++; $newVersion = "$major.$minor.$patch" }
    "minor" { $minor++; $patch = 0; $newVersion = "$major.$minor.$patch" }
    "major" { $major++; $minor = 0; $patch = 0; $newVersion = "$major.$minor.$patch" }
}

Write-Host "🚀 Nouvelle version: $newVersion" -ForegroundColor Green

# Demander confirmation
$confirmation = Read-Host "Confirmer le bump de version? (y/N)"
if ($confirmation -ne 'y' -and $confirmation -ne 'Y') {
    Write-Host "❌ Opération annulée." -ForegroundColor Red
    exit 1
}

# Exécuter bump2version
Write-Host "⚡ Exécution de bump2version $Type..." -ForegroundColor Blue
try {
    bump2version $Type
    Write-Host "✅ Version mise à jour avec succès!" -ForegroundColor Green
    Write-Host "📁 Fichiers modifiés:" -ForegroundColor Cyan
    Write-Host "   - VERSION" -ForegroundColor White
    Write-Host "   - pyproject.toml" -ForegroundColor White
    Write-Host "   - src/brainstorm_ai/__init__.py" -ForegroundColor White
    Write-Host "   - .bumpversion.cfg" -ForegroundColor White
    Write-Host "🏷️  Tag Git créé: v$newVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Erreur lors du bump de version: $_" -ForegroundColor Red
    exit 1
} 