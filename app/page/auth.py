"""
page/auth.py – Interface d'authentification.
"""

import streamlit as st
from service.db import authenticate_user


def show_login() -> None:
    """Affiche la page de connexion et gère la soumission du formulaire."""

    # ── CSS spécifique à la page login ──────────────────────────────────────
    st.markdown(
        """
        <style>
        .login-container {
            max-width: 420px;
            margin: 6vh auto 0 auto;
            padding: 2.5rem 2.5rem 2rem 2.5rem;
            background: #ffffff;
            border: 1px solid #e8e0d5;
            border-radius: 16px;
            box-shadow: 0 8px 40px rgba(0,0,0,0.08);
        }
        .login-logo {
            font-family: 'DM Serif Display', serif;
            font-size: 2rem;
            color: #1a1a1a;
            text-align: center;
            margin-bottom: 0.25rem;
        }
        .login-sub {
            text-align: center;
            color: #7a7a7a;
            font-size: 0.85rem;
            margin-bottom: 1.8rem;
        }
        /* Bouton principal */
        div[data-testid="stFormSubmitButton"] > button {
            width: 100%;
            background: #1a1a1a !important;
            color: #ffffff !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 0.6rem 0 !important;
            font-weight: 600;
            font-size: 0.95rem;
            letter-spacing: 0.03em;
            transition: opacity 0.2s;
        }
        div[data-testid="stFormSubmitButton"] > button:hover {
            opacity: 0.85;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # ── Layout centré ────────────────────────────────────────────────────────
    _, center, _ = st.columns([1, 1.4, 1])
   

    with center:
        st.markdown(
            """
            <div class="login-logo">📊 AMCHO</div>
            <div class="login-sub">Cocoa & PPI Analytics Dashboard</div>
            """,
            unsafe_allow_html=True,
        )

        with st.form("login_form", clear_on_submit=False):
            username = st.text_input("Nom d'utilisateur", placeholder="ex. admin")
            password = st.text_input("Mot de passe", type="password", placeholder="mot de passe")
            submitted = st.form_submit_button("Se connecter", use_container_width=True)
        if st.button("Pas de compte ? S'inscrire"):
            st.session_state.page = "register"
            st.rerun()

        if submitted:
            if not username or not password:
                st.warning("Veuillez remplir tous les champs.")
            elif authenticate_user(username, password):
                st.session_state.authenticated = True
                st.session_state.username = username
                st.success("Connexion réussie ! Redirection…")
                st.rerun()
            else:
                st.error("Identifiants incorrects. Réessayez.")