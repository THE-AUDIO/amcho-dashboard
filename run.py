import sys
import subprocess

def run_app():
    """Point d'entrée pour lancer l'application Streamlit."""
    print("Lancement de l'application Streamlit...")
    subprocess.run([sys.executable, "-m", "streamlit", "run", "app/main.py"])

def run_etl():
    print("Lancement du script ETL...")
    # Removed "-m" and "python3"
    subprocess.run([sys.executable, "etl/main.py"]) 


if __name__ == "__main__":
    run_etl()
    run_app()