@echo off
chcp 65001 > nul
echo ==================================================
echo    Initialisation et Lancement de l'App AMCHO     
echo ==================================================

:: 1. Vérification et création du venv
if not exist venv (
    echo 📦 Le dossier 'venv' n'existe pas. Création en cours...
    python -m venv venv
    
    echo ⏳ Activation du venv pour installation des dépendances...
    call venv\Scripts\activate.bat
    
    echo 📥 Mise à jour de pip et installation des packages requis...
    python -m pip install --upgrade pip
    if exist requirements.txt (
        pip install -r requirements.txt
    ) else (
        echo ⚠️ Attention : 'requirements.txt' introuvable à la racine.
    )
) else (
    echo ✅ Environnement virtuel 'venv' détecté.
    call venv\Scripts\activate.bat
)

:: 2. Exécution de l'ETL
echo ⏳ Déplacement dans .\etl et exécution de l'ETL...
cd etl
python main.py
if %ERRORLEVEL% NEQ 0 (
    echo ❌ L'ETL a échoué. Arrêt du processus.
    cd ..
    pause
    exit /b %ERRORLEVEL%
)
cd ..

:: 3. Lancement de l'application Streamlit
echo 🚀 Déplacement dans .\app et lancement de Streamlit...
cd app
streamlit run main.py

cd ..
pause