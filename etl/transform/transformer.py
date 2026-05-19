"""Transformation des données extraites."""

import pandas as pd

# Indice de référence PPI pour l'année 2011
PPI_REF_2011 = 100.0

def format_percentage(value: float) -> str:
    """Formate une valeur en pourcentage avec symbole %."""
    if pd.isna(value):
        return "0%"
    return f"{value:.2f}%"

def _base_transform(df: pd.DataFrame) -> pd.DataFrame:
    """Transformation de base : filtre 2020-2026 et moyenne annuelle."""
    df = df.copy()
    
    # Conversion et nettoyage des données
    df["date"] = pd.to_datetime(df["date"])
    df = df[df["date"].dt.year.between(2020, 2026)]
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df = df.dropna(subset=["value"])
    
    # Calcul de la moyenne annuelle
    yearly = df.groupby(df["date"].dt.year)["value"].mean().reset_index()
    yearly.columns = ["year", "value"]
    yearly["year"] = yearly["year"].astype(int)
    
    return yearly


def transform_cocoa(df: pd.DataFrame) -> pd.DataFrame:
    """Transformation complète pour les prix du cacao."""
    df = _base_transform(df)
    
    # Calcul des métriques
    df["CocoaPrice"] = df["value"].round(2)
    df["CocoaPriceChange"] = df["CocoaPrice"].diff().fillna(0).round(2)
    df["CocoaPricePctChange"] = (df["CocoaPrice"].pct_change().fillna(0) * 100).round(2).apply(format_percentage)
    
    # Sélectionner les colonnes finales
    df = df[["year", "CocoaPrice", "CocoaPriceChange", "CocoaPricePctChange"]]
    
    print(f"[TRANSFORM] Cocoa Price : {len(df)} années calculées (2020-2026)")
    return df


def transform_ppi(df: pd.DataFrame) -> pd.DataFrame:
    """Transformation complète pour l'indice PPI."""
    df = _base_transform(df)
    
    df["PPI"] = df["value"].round(2)
    df["PPIChange"] = df["PPI"].diff().fillna(0).round(2)
    
    # Variation annuelle en pourcentage
    df["PPIPctChange"] = (df["PPI"].pct_change().fillna(0) * 100).round(2).apply(format_percentage)
    
    # Variation par rapport à l'indice de référence 2011
    df["PPIPctChangeReference"] = ((df["PPI"] - PPI_REF_2011)).round(2).apply(format_percentage)
    
    # Sélectionner les colonnes finales
    df = df[["year", "PPI", "PPIChange", "PPIPctChange", "PPIPctChangeReference"]]
    
    print(f"[TRANSFORM] PPI : {len(df)} années calculées (2020-2026)")
    return df