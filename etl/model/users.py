"""Modèle de données pour les utilisateurs."""

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, Float, String
from core.base import Base


class users(Base):
    """Modèle pour stocker les informations d'authentification des utilisateurs."""
    __tablename__ = "users"

    # Clé primaire auto-incrémentée
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    # Nom d'utilisateur (unique et indexé)
    username: Mapped[str] = mapped_column(String, nullable=False, index=True, unique=True) # type: ignore
    # Mot de passe (hashé)
    password: Mapped[str] = mapped_column(String, nullable=False)
    