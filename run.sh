#!/bin/bash

# Arrête le script immédiatement si une commande échoue
set -e

echo "=================================================="
echo "   Initialisation et Lancement de l'App AMCHO     "
echo "=================================================="

# 1. Vérification et création du venv
if [ ! -d "venv" ]; then
    echo "📦 Le dossier 'venv' n'existe pas. Création en cours..."
    python3 -m venv venv
    
    echo "⏳ Activation du venv pour installation des dépendances..."
    source venv/bin/activate
    
    echo "📥 Mise à jour de pip et installation des packages requis..."
    pip install --upgrade pip
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
    else
        echo "⚠️ Attention : 'requirements.txt' introuvable à la racine."
    fi
else
    echo "✅ Environnement virtuel 'venv' détecté."
    source venv/bin/activate
fi

# 2. Exécution de l'ETL
echo "⏳ Déplacement dans ./etl et exécution de l'ETL..."
cd etl
python main.py
cd ..

# 3. Lancement de l'application Streamlit
echo "🚀 Déplacement dans ./app et lancement de Streamlit..."
cd app
streamlit run main.py