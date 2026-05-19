from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Float, Date
from core.base import Base


class PPI(Base):
    __tablename__ = "ppi"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    date: Mapped[str] = mapped_column(Date)
    value: Mapped[float] = mapped_column(Float)