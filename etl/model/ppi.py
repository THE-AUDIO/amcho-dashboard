"""Modèle de données pour l'indice PPI."""

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, Float, Date, Index, String
from core.base import Base
from datetime import date


class PPI(Base):
    """Modèle pour stocker les données de l'indice des prix à la production."""
    __tablename__ = "ppi"

    # Clé primaire auto-incrémentée
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    # Année (indexée pour les requêtes)
    year: Mapped[int] = mapped_column(Integer, nullable=False, index=True) # type: ignore
    # Valeur de l'indice PPI
    PPI: Mapped[float] = mapped_column(Float, nullable=False)
    
    # Variation et changement en pourcentage
    PPIChange: Mapped[float] = mapped_column(Float, nullable=False)
    PPIPctChange: Mapped[str] = mapped_column(String, nullable=False)
    PPIPctChangeReference: Mapped[str] = mapped_column(String, nullable=False)
    
    # Index unique sur l'année pour éviter les doublons
    __table_args__ = (
        Index("ix_ppi_date", "year", unique=True),
    )

    def __repr__(self):
        return f"<PPI(date={self.date}, value={self.value})>"