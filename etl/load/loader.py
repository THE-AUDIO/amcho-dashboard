import pandas as pd
from sqlalchemy import text, Engine


class BaseLoader:
    def __init__(self, engine: Engine):
        self.engine = engine

    def replace_table(self, table_name: str, df: pd.DataFrame) -> None:
        """Delete + insert safely in transaction"""
        try:
            with self.engine.begin() as conn:
                conn.execute(text(f"DELETE FROM {table_name}"))

            df.to_sql(
                table_name,
                self.engine,
                if_exists="append",
                index=False,
                method="multi",
                chunksize=1000
            )

            print(f"[LOAD] {table_name} : {len(df)} lignes insérées")

        except Exception as e:
            print(f"[ERROR] {table_name} failed: {e}")
            raise