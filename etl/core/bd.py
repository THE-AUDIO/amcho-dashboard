from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .config import settings

engine = create_engine(settings.DATABASE_URL)

Session = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)

def get_db_session():
    print("Connecting to the database...")
    return Session()