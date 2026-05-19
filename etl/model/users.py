from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, Float,String
from core.base import Base


class users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    username: Mapped[str] = mapped_column(String, nullable=False, index=True) # type: ignore
    password: Mapped[str] = mapped_column(String, nullable=False)
    