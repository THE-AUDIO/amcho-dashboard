"""
Module de configuration de la base de données.

Ce module gère la connexion et la session SQLAlchemy pour l'application ETL.
Il utilise le pattern Factory pour créer les sessions de base de données.

Exports:
    - engine: Moteur SQLAlchemy pour la base de données
    - Session: Classe de session SQLAlchemy
    - get_db_session(): Fonction pour obtenir une nouvelle session
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .config import settings

# ── CONFIGURATION DE LA BASE DE DONNÉES ───────────────────────────────────
# Crée le moteur SQLAlchemy qui gère la connexion à la base de données
# La chaîne de connexion (DATABASE_URL) est chargée depuis les variables d'environnement
# Format attendu : postgresql://user:password@host:port/database
engine = create_engine(settings.DATABASE_URL)

# ── FACTORY DE SESSION ───────────────────────────────────────────────────────
# Configure la fabrique de session pour créer des sessions de base de données
Session = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)

# ── FONCTION D'ACCÈS À LA SESSION ────────────────────────────────────────────
def get_db_session():
    """
    Crée et retourne une nouvelle session de base de données.
    
    Cette fonction établit une connexion à la base de données et retourne
    une session SQLAlchemy pour exécuter des requêtes.
    
    Returns:
        Session: Une nouvelle session SQLAlchemy pour interagir avec la BD
    """
    print("Connecting to the database...")
    return Session()
