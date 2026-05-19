# Utiliser l'image Python 3.11 officielle
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Définir les variables d'environnement
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copier le fichier requirements.txt
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --upgrade pip setuptools wheel && \
    pip install -r requirements.txt

# Copier le code de l'application
COPY . .

# Créer un répertoire pour les données de Streamlit
RUN mkdir -p ~/.streamlit

# Configurer Streamlit
RUN echo '\
[client]\n\
showErrorDetails = true\n\
\n\
[logger]\n\
level = "info"\n\
\n\
[server]\n\
port = 8501\n\
headless = true\n\
runOnSave = true\n\
' > ~/.streamlit/config.toml

# Exposer le port de Streamlit
EXPOSE 8501

# Vérifier que l'app démarre correctement
HEALTHCHECK CMD python -c "import requests; requests.get('http://localhost:8501/_stcore/health')" || exit 1

# Lancer l'application
CMD ["python", "run.py"]
