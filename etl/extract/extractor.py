import pandas as pd
import os

BASE_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data")

def extract_cocoa() -> pd.DataFrame:
    """Lit le CSV du prix du cacao depuis data/"""
    path = os.path.join(BASE_DIR, "cocoa_price.csv")
    df = pd.read_csv(path, parse_dates=["observation_date"])
    df.columns = ["date", "value"]
    print(f"[EXTRACT] Cacao : {len(df)} lignes lues")
    return df

def extract_ppi() -> pd.DataFrame:
    """Lit le CSV du PPI depuis datasources/"""
    path = os.path.join(BASE_DIR, "ppi.csv")
    df = pd.read_csv(path, parse_dates=["observation_date"])
    df.columns = ["date", "value"]
    print(f"[EXTRACT] PPI : {len(df)} lignes lues")
    return df