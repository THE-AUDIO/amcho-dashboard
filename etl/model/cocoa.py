
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, Float, Date, Index, Integer, String
from core.base import Base
from datetime import date


class CocoaPrice(Base):
    __tablename__ = "cocoa_price"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    year: Mapped[int] = mapped_column(Integer, nullable=False, index=True) # type: ignore
    CocoaPrice: Mapped[float] = mapped_column(Float, nullable=False)
    
    # Optionnel : pour garder la date originale au format string si besoin
    CocoaPriceChange: Mapped[float] = mapped_column(Float, nullable=True)  # ex: 5.23
    CocoaPricePctChange: Mapped[str] = mapped_column(String, nullable=False)  # ex: "5.23%"
    __table_args__ = (
        Index("ix_cocoa_price_date", "year", unique=True),  # Empêche les doublons de date
    )

    def __repr__(self):
        return f"<CocoaPrice(date={self.date}, value={self.value})>"