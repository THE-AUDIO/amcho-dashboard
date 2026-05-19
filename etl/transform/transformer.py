import pandas as pd

PPI_REF_2011 = 100.0

def format_percentage(value: float) -> str:
    """Ajoute le symbole % et gère les couleurs plus tard"""
    if pd.isna(value):
        return "0%"
    return f"{value:.2f}%"

def _base_transform(df: pd.DataFrame) -> pd.DataFrame:
    """Filtre les années 2020-2026 et calcule la moyenne annuelle"""
    df = df.copy()
    
    # Conversion et nettoyage
    df["date"] = pd.to_datetime(df["date"])
    df = df[df["date"].dt.year.between(2020, 2026)]
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df = df.dropna(subset=["value"])
    
    # Moyenne annuelle
    yearly = df.groupby(df["date"].dt.year)["value"].mean().reset_index()
    yearly.columns = ["year", "value"]
    yearly["year"] = yearly["year"].astype(int)
    
    return yearly


def transform_cocoa(df: pd.DataFrame) -> pd.DataFrame:
    """Transformation complète pour Cocoa Price"""
    df = _base_transform(df)
    
    df["CocoaPrice"] = df["value"].round(2)
    df["CocoaPriceChange"] = df["CocoaPrice"].diff().fillna(0).round(2)
    df["CocoaPricePctChange"] = (df["CocoaPrice"].pct_change().fillna(0) * 100).round(2).apply(format_percentage)
    
    # Suppression de la colonne temporaire
    df = df[["year", "CocoaPrice", "CocoaPriceChange", "CocoaPricePctChange"]]
    
    print(f"[TRANSFORM] Cocoa Price : {len(df)} années calculées (2020-2026)")
    return df


def transform_ppi(df: pd.DataFrame) -> pd.DataFrame:
    """Transformation complète pour PPI - conforme à l'énoncé"""
    df = _base_transform(df)
    
    df["PPI"] = df["value"].round(2)
    df["PPIChange"] = df["PPI"].diff().fillna(0).round(2)
    
    # % de variation par rapport à l'année précédente
    df["PPIPctChange"] = (df["PPI"].pct_change().fillna(0) * 100).round(2).apply(format_percentage)
    
    # PPI % Change Reference (par rapport à la base 2011 = 100)
    # Selon l'énoncé : différence en pourcentage par rapport à 100
    df["PPIPctChangeReference"] = ((df["PPI"] - PPI_REF_2011)).round(2).apply(format_percentage)
    
    df = df[["year", "PPI", "PPIChange", "PPIPctChange", "PPIPctChangeReference"]]
    
    print(f"[TRANSFORM] PPI : {len(df)} années calculées (2020-2026)")
    return df