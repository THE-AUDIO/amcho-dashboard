@echo off
:: Active l'extension des variables pour la gestion des erreurs au fur et à mesure (équivalent partiel de set -e)
setlocal enabledelayedexpansion

echo ==================================================
echo    Initialisation et Lancement de l'App AMCHO     
echo ==================================================

:: 1. Vérification et création du venv
if not exist "venv" (
    echo 📦 Le dossier 'venv' n'existe pas. Création en cours...
    python -m venv venv
    if !errorlevel! neq 0 (
        echo ❌ Erreur lors de la création de l'environnement virtuel.
        exit /b !errorlevel!
    )
    
    echo ⏳ Activation du venv pour installation des dépendances...
    call venv\Scripts\activate
    
    echo 📥 Mise à jour de pip et installation des packages requis...
    python -m pip install --upgrade pip
    if exist "requirements.txt" (
        pip install -r requirements.txt
    ) else (
        echo ⚠️ Attention : 'requirements.txt' introuvable à la racine.
    )
) else (
    echo ✅ Environnement virtuel 'venv' détecté.
    call venv\Scripts\activate
)

:: 2. Exécution de l'ETL ET STREAMLIT
echo LOADING ...
python run.py

if !errorlevel! neq 0 (
    echo ❌ Une erreur est survenue lors de l'exécution de run.py.
    exit /b !errorlevel!
)

pause