
"""Modèle de données pour les prix du cacao."""

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, Float, Date, Index, Integer, String
from core.base import Base
from datetime import date


class CocoaPrice(Base):
    """Modèle pour stocker les prix annuels du cacao."""
    __tablename__ = "cocoa_price"

    # Clé primaire auto-incrémentée
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    # Année (indexée pour les requêtes)
    year: Mapped[int] = mapped_column(Integer, nullable=False, index=True) # type: ignore
    # Prix moyen annuel du cacao
    CocoaPrice: Mapped[float] = mapped_column(Float, nullable=False)
    
    # Variation absolue et en pourcentage
    CocoaPriceChange: Mapped[float] = mapped_column(Float, nullable=True)
    CocoaPricePctChange: Mapped[str] = mapped_column(String, nullable=False)
    
    # Index unique sur l'année pour éviter les doublons
    __table_args__ = (
        Index("ix_cocoa_price_date", "year", unique=True),
    )

    def __repr__(self):
        return f"<CocoaPrice(date={self.date}, value={self.value})>"