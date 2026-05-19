"""Chargement des données transformées dans la base de données."""

import pandas as pd
from sqlalchemy import text, Engine



class BaseLoader:
    """Classe pour charger les DataFrames dans la base de données."""
    
    def __init__(self, engine: Engine):
        """Initialise le loader avec le moteur SQLAlchemy."""
        self.engine = engine

    def replace_table(self, table_name: str, df: pd.DataFrame) -> None:
        """Remplace les données d'une table (supprime puis insère)."""
        try:
            # Supprimer les anciennes données
            with self.engine.begin() as conn:
                conn.execute(text(f"DELETE FROM {table_name}"))

            # Insérer les nouvelles données
            df.to_sql(
                table_name,
                self.engine,
                if_exists="append",
                index=False,
                method="multi",  # Insertion optimisée
                chunksize=1000  # Traiter par lots
            )

            print(f"[LOAD] {table_name} : {len(df)} lignes insérées")

        except Exception as e:
            print(f"[ERROR] {table_name} failed: {e}")
            raise