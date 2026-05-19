from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, Float, Date, Index, String
from core.base import Base
from datetime import date


class PPI(Base):
    __tablename__ = "ppi"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    year: Mapped[int] = mapped_column(Integer, nullable=False, index=True) # type: ignore
    PPI: Mapped[float] = mapped_column(Float, nullable=False)
    
    # Optionnel
    PPIChange: Mapped[float] = mapped_column(Float, nullable=False)
    PPIPctChange: Mapped[str] = mapped_column(String, nullable=False)
    PPIPctChangeReference: Mapped[str] = mapped_column(String, nullable=False)
    __table_args__ = (
        Index("ix_ppi_date", "year", unique=True),
    )

    def __repr__(self):
        return f"<PPI(date={self.date}, value={self.value})>"