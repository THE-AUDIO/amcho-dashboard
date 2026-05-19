"""
Configuration de l'application ETL avec Pydantic Settings.
Charge les variables d'environnement depuis le fichier .env
"""

from pydantic_settings import BaseSettings, SettingsConfigDict

# Classe de configuration qui gère les variables d'environnement
class Settings(BaseSettings):
    """Classe pour gérer les paramètres de configuration via Pydantic."""
    
    # URL de connexion à la base de données
    DATABASE_URL: str

    # Configuration Pydantic pour charger depuis .env
    model_config = SettingsConfigDict(
        env_file=".env",  # Fichier à charger
        env_file_encoding="utf-8",  # Encodage du fichier
        extra="ignore"  # Ignorer les variables non déclarées
    )

# Instance globale des paramètres
settings = Settings()
