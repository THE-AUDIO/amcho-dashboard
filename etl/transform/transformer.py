import pandas as pd

PPI_REF_2011 = 100 # base de référence fixée par l'énoncé

def _base_transform(df: pd.DataFrame) -> pd.DataFrame:
    """Filtre 2020-2026, nettoie, agrège par année"""
    df = df[df["date"].dt.year.between(2020, 2026)].copy()
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df = df.dropna(subset=["value"])
    df["year"] = df["date"].dt.year
    yearly = df.groupby("year")["value"].mean().reset_index()
    yearly.columns = ["year", "value"]
    return yearly

def transform_cocoa(df: pd.DataFrame) -> pd.DataFrame:
    """Ajoute Change et %Change pour le cacao"""
    df = _base_transform(df)
    df["change"]    = df["value"].diff().fillna(0)
    df["pct_change"] = df["value"].pct_change().fillna(0) * 100
    print(f"[TRANSFORM] Cacao : {len(df)} années calculées")
    df.columns = ["year", "Cocoa Price", "Cocoa Price Change", "Cocoa Price %Change"]
    return df

def transform_ppi(df: pd.DataFrame) -> pd.DataFrame:
    """Ajoute Change, %Change et %Change Reference pour le PPI"""
    df = _base_transform(df)
    df["change"]    = df["value"].diff().fillna(0)
    df["pct_change"] = df["value"].pct_change().fillna(0) * 100
    # %Ref = (valeur - base 2011) / base 2011 * 100
    df["pct_ref"]   = ((df["value"] - PPI_REF_2011) / PPI_REF_2011) * 100
    df.columns = ["year", "PPI", "PPI Change", "PPI % Change", "PPI Change Reference"]
    print(f"[TRANSFORM] PPI : {len(df)} années calculées")
    
    return df