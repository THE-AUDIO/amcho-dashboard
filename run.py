import sys
import subprocess
from pathlib import Path

# On récupère le dossier racine où se trouve ce script run_app.py
BASE_DIR = Path(__file__).parent.resolve()


def run_etl() -> bool:
  
    print("⏳ [ETL] Déplacement dans ./etl et lancement du script...")
    

    result = subprocess.run(
        [sys.executable, "main.py"], 
        cwd=BASE_DIR / "etl"  
    )
    
    if result.returncode == 0:
        print("✅ ETL terminé avec succès.")
        return True
    

    return False


def run_app() -> None:

    print("🚀 [Streamlit] Déplacement dans ./app et lancement du Dashboard...")
    
    # Équivalent de : cd app && streamlit run main.py
    subprocess.run(
        [sys.executable, "-m", "streamlit", "run", "main.py"], 
        cwd=BASE_DIR / "app" 
    )


if __name__ == "__main__":
    if run_etl():
        run_app()