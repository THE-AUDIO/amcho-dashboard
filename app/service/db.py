
"""
service/db.py
Couche d'accès à la base de données avec SQLAlchemy.
"""

import os
import pandas as pd
import bcrypt

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from contextlib import contextmanager

# ─────────────────────────────────────────────────────────────
# Charger les variables d'environnement
# ─────────────────────────────────────────────────────────────
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not defined in .env")

print(f"[DB] Connected using DATABASE_URL")

# ─────────────────────────────────────────────────────────────
# Création du moteur SQLAlchemy
# ─────────────────────────────────────────────────────────────
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
    echo=False
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# ─────────────────────────────────────────────────────────────
# Gestion des sessions
# ─────────────────────────────────────────────────────────────
@contextmanager
def get_session():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

# ─────────────────────────────────────────────────────────────
# Authentification
# ─────────────────────────────────────────────────────────────
def authenticate_user(username: str, password: str) -> bool:
    """
    Vérifie le login utilisateur.
    """

    try:
        with get_session() as session:

            query = text("""
                SELECT password
                FROM users
                WHERE username = :username
            """)

            result = session.execute(
                query,
                {"username": username}
            ).fetchone()

            if not result:
                return False

            stored_hash = result[0]

            return bcrypt.checkpw(
                password.encode("utf-8"),
                stored_hash.encode("utf-8")
            )

    except SQLAlchemyError as e:
        print(f"[AUTH ERROR] {e}")
        return False

# ─────────────────────────────────────────────────────────────
# Création utilisateur
# ─────────────────────────────────────────────────────────────
def create_user(username: str, plain_password: str) -> bool:
    """
    Crée un utilisateur avec mot de passe hashé.
    """

    try:
        hashed = bcrypt.hashpw(
            plain_password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        with get_session() as session:

            query = text("""
                INSERT INTO users (username, password)
                VALUES (:username, :password)
                ON CONFLICT (username) DO NOTHING
            """)

            session.execute(
                query,
                {
                    "username": username,
                    "password": hashed
                }
            )

        print(f"[OK] User '{username}' created.")
        return True

    except SQLAlchemyError as e:
        print(f"[CREATE USER ERROR] {e}")
        return False

# ─────────────────────────────────────────────────────────────
# Cocoa Data
# ─────────────────────────────────────────────────────────────
def get_cocoa_data() -> pd.DataFrame:
    """
    Retourne les données du prix du cacao.
    """

    try:
        query = """
            SELECT *
            FROM cocoa_price
            WHERE year >= 2020
            AND year <= 2026
            ORDER BY year
        """

        df = pd.read_sql(query, engine)

        return df

    except Exception as e:
        print(f"[COCOA DATA ERROR] {e}")
        return pd.DataFrame()

# ─────────────────────────────────────────────────────────────
# PPI Data
# ─────────────────────────────────────────────────────────────
def get_ppi_data() -> pd.DataFrame:
    """
    Retourne les données PPI.
    """

    try:
        query = """
            SELECT *
            FROM ppi
            WHERE year >= 2020
            AND year <= 2026
            ORDER BY year
        """

        df = pd.read_sql(query, engine)

        return df

    except Exception as e:
        print(f"[PPI DATA ERROR] {e}")
        return pd.DataFrame()
