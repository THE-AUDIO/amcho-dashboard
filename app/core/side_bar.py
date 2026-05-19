import streamlit as st

# Vues disponibles dans la sidebar
VIEWS = {
    "📋 Tableau récapitulatif":  "table",
    "🍫 Prix du Cacao":          "cocoa",
    "📈 PPI (Producer Price Index)": "ppi",
    "🔀 Comparaison Cacao & PPI": "mixed",
    "🗂️ Vue complète":           "all",
}
YEARS = list(range(2020, 2027))


def build_sidebar() -> str:
    """
    Construit la sidebar de navigation et retourne la clé de vue sélectionnée.
    Retourne l'une des valeurs de VIEWS : 'table','cocoa','ppi','mixed','all'.
    """
    with st.sidebar:
        # Logo / Titre sidebar
        st.markdown(
            """
            <style>
            /* ── Sidebar styling ── */
            [data-testid="stSidebar"] {
                background: #1a1a1a;
            }
            [data-testid="stSidebar"] * {
                color: #f5f0e8 !important;
            }
            .sb-brand {
                font-family: 'DM Serif Display', serif;
                font-size: 1.4rem;
                font-weight: 700;
                color: #c8a97e !important;
                letter-spacing: 0.05em;
                margin-bottom: 0.1rem;
            }
            .sb-brand-sub {
                font-size: 0.7rem;
                color: #9ca3af !important;
                letter-spacing: 0.15em;
                text-transform: uppercase;
                margin-bottom: 1.5rem;
            }
            .sb-section-title {
                font-size: 0.65rem;
                font-weight: 700;
                letter-spacing: 0.15em;
                text-transform: uppercase;
                color: #6b7280 !important;
                margin: 1.2rem 0 0.5rem 0;
            }
            /* Boutons radio dans la sidebar */
            [data-testid="stSidebar"] .stRadio label {
                padding: 0.45rem 0.6rem;
                border-radius: 6px;
                cursor: pointer;
                font-size: 0.85rem;
                transition: background 0.15s;
            }
            [data-testid="stSidebar"] .stRadio label:hover {
                background: rgba(200, 169, 126, 0.15);
            }
            .sb-divider {
                border: none;
                border-top: 1px solid #2d2d2d;
                margin: 1rem 0;
            }
            .sb-info-box {
                background: #2d2d2d;
                border-left: 3px solid #c8a97e;
                border-radius: 4px;
                padding: 0.6rem 0.75rem;
                font-size: 0.75rem;
                color: #9ca3af !important;
                line-height: 1.4;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

        st.markdown('<div class="sb-brand">📊 AMCHO</div>', unsafe_allow_html=True)
        st.markdown('<div class="sb-brand-sub">Dashboard analytique</div>', unsafe_allow_html=True)

        st.markdown('<hr class="sb-divider">', unsafe_allow_html=True)

        # Navigation principale
        st.markdown('<div class="sb-section-title">Navigation</div>', unsafe_allow_html=True)

        selected_label = st.radio(
            label="Vue",
            options=list(VIEWS.keys()),
            label_visibility="collapsed",
        )

        st.markdown('<hr class="sb-divider">', unsafe_allow_html=True)

        # Filtres temporels (optionnel – informatif, peut étendre la logique)
        st.markdown('<div class="sb-section-title">Période</div>', unsafe_allow_html=True)
        year_range = st.select_slider(
            "Années affichées",
            options=YEARS,
            value=(YEARS[0], YEARS[-1]),
            label_visibility="visible",
        )
        # Stocker dans session_state pour usage global
        st.session_state["year_range"] = year_range

        st.markdown('<hr class="sb-divider">', unsafe_allow_html=True)

        # Informations sources
        st.markdown(
            '<div class="sb-info-box">'
            '🔗 <b>Sources</b><br>'
            'FRED – PCOCOUSDM<br>'
            'PCU3113513113517<br>'
            '<span style="color:#6b7280">Mise à jour : 2026</span>'
            '</div>',
            unsafe_allow_html=True,
        )

        st.markdown('<hr class="sb-divider">', unsafe_allow_html=True)

        # Bouton logout en bas
        if st.button("🚪 Se déconnecter", width='strectch'):
            st.session_state.authenticated = False
            st.session_state.username = None
            st.rerun()

    return VIEWS[selected_label]

