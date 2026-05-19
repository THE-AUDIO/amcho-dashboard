from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, Float, Date
from core.base import Base

class CocoaPrice(Base):
    __tablename__ = "cocoa_price"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    date: Mapped[str] = mapped_column(Date, nullable=False)
    value: Mapped[float] = mapped_column(Float, nullable=False)