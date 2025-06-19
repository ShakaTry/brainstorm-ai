@echo off
title Brainstorm AI - Lancement Rapide
echo.
echo 🧠 === BRAINSTORM AI - LANCEMENT RAPIDE ===
echo.

REM Vérifier si Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python n'est pas installé ou pas dans le PATH
    echo 💡 Installez Python depuis https://python.org
    pause
    exit /b 1
)

REM Vérifier la clé API
if "%OPENAI_API_KEY%"=="" (
    echo ❌ Clé API OpenAI manquante !
    echo.
    set /p api_key="🔑 Entrez votre clé API OpenAI : "
    set OPENAI_API_KEY=%api_key%
    echo.
    echo ✅ Clé API configurée pour cette session
)

REM Installer les dépendances si nécessaire
if not exist "src\brainstorm_ai\__init__.py" (
    echo 📦 Installation du projet...
    pip install -e .
)

REM Lancer le brainstorm
echo 🚀 Lancement du brainstorm...
echo.
python run.py

echo.
echo 🎉 Session terminée ! 
echo 📁 Consultez les dossiers data/logs/ et data/exports/ pour vos résultats
echo.
pause 