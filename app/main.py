from typing import Dict, List
import streamlit as st

# ── CONSTANTES DE CONFIGURATION ───────────────────────────────────────
PAGE_TITLE = "AMCHO Dashboard"
PAGE_ICON = "📊"
LAYOUT = "wide"

# Valeurs d'état pour l'authentification
AUTH_LOGIN = "login"
AUTH_REGISTER = "register"


def init_session_state() -> None:
    """Initialise proprement toutes les variables d'état de la session."""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "username" not in st.session_state:
        st.session_state.username = None
    if "page" not in st.session_state:
        st.session_state.page = AUTH_LOGIN


def load_local_css(file_name: str) -> None:
    """Charge et injecte de manière sécurisée un fichier CSS local."""
    try:
        with open(file_name, encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning(f"Fichier de style introuvable : {file_name}")


def get_dashboard_pages() -> Dict[str, List[st.Page]]:
    """Définit et retourne la structure des pages du tableau de bord."""
    return {
        "Menu": [
            st.Page("pages/dashboard/01_Tableau.py",     title="Tableau récapitulatif", icon="📋"),
            st.Page("pages/dashboard/02_Cocoa.py",       title="Prix du Cacao",         icon="🍫"),
            st.Page("pages/dashboard/03_PPI.py",         title="PPI",                    icon="📈"),
            st.Page("pages/dashboard/04_Comparaison.py", title="Comparaison",            icon="🔀"),
        ]
    }


def get_auth_navigation() -> st.navigation:
    """Gère le routage d'authentification en masquant la sidebar."""
    if st.session_state.page == AUTH_REGISTER:
        target_page = st.Page("pages/02_Register.py", title="Inscription", icon="✍️")
    else:
        target_page = st.Page("pages/01_Login.py", title="Connexion", icon="🔑")
        
    return st.navigation([target_page], position="hidden")


def main() -> None:
    """Point d'entrée principal de l'application."""
    st.set_page_config(
        page_title=PAGE_TITLE,
        page_icon=PAGE_ICON,
        layout=LAYOUT,
    )

    init_session_state()

    # Exemple d'usage si vous avez un fichier global.css :
    # load_local_css("assets/global.css")

    # Détermination du routeur selon le statut de connexion
    if not st.session_state.authenticated:
        router = get_auth_navigation()
    else:
        router = st.navigation(get_dashboard_pages(), position="sidebar", expanded=True)

    # Exécution de la page sélectionnée par le routeur
    router.run()


if __name__ == "__main__":
    main()