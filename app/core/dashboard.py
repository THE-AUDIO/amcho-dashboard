"""
page/dashboard.py – Interface principale de visualisation.

Contient :
  1. Table récapitulative (Cocoa + PPI, 2020-2026)
     – valeurs négatives en rouge, positives en vert
  2. Graphique 1 : Évolution annuelle du prix du cacao (line chart)
  3. Graphique 2 : Évolution annuelle du PPI (line chart)
  4. Graphique 3 : Comparaison mixte bar (cacao) + ligne (PPI)

Sidebar : navigation pour choisir quelle vue afficher.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from service.db import get_cocoa_data, get_ppi_data
from .side_bar import build_sidebar
from .all_chart import  *

# ── Constantes ───────────────────────────────────────────────────────────────
YEARS = list(range(2020, 2027))
PPI_BASE_YEAR_VALUE = 100  # Valeur de référence PPI 2011


# ────────────────────────────────────────────────────────────────────────────
#  Calculs
# ────────────────────────────────────────────────────────────────────────────

def yearly_avg(df: pd.DataFrame, val: str) -> pd.Series:
    """Moyenne annuelle des valeurs mensuelles, réindexée sur YEARS."""
    return df.groupby("year")[val].mean().reindex(YEARS)


def build_indicators(cocoa: pd.Series, ppi: pd.Series) -> dict:
    cocoa_change = cocoa.diff()
    cocoa_pct    = cocoa.pct_change() * 100
    ppi_change   = ppi.diff()
    ppi_pct      = ppi.pct_change() * 100
    ppi_ref_pct  = ((ppi - PPI_BASE_YEAR_VALUE) / PPI_BASE_YEAR_VALUE) * 100

    return {
        "cocoa_price":  cocoa,
        "cocoa_change": cocoa_change,
        "cocoa_pct":    cocoa_pct,
        "ppi_price":    ppi,
        "ppi_change":   ppi_change,
        "ppi_pct":      ppi_pct,
        "ppi_ref_pct":  ppi_ref_pct,
    }


# ────────────────────────────────────────────────────────────────────────────
#  Métriques KPI (cartes en haut du dashboard)
# ────────────────────────────────────────────────────────────────────────────

def show_kpis(cocoa: pd.Series, ppi: pd.Series) -> None:
    """Affiche 4 métriques clés sous forme de cartes."""
    # Dernière valeur connue (non-NaN)
    last_cocoa = cocoa.dropna().iloc[-1]
    prev_cocoa = cocoa.dropna().iloc[-2]
    delta_cocoa = last_cocoa - prev_cocoa

    last_ppi = ppi.dropna().iloc[-1]
    prev_ppi = ppi.dropna().iloc[-2]
    delta_ppi = last_ppi - prev_ppi

    last_year  = int(cocoa.dropna().index[-1])
    peak_cocoa = cocoa.max()
    peak_year  = int(cocoa.idxmax())

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label=f"🍫 Cocoa Price {last_year}",
            value=f"${last_cocoa:,.0f}",
            delta=f"{delta_cocoa:+,.0f} USD/MT",
        )
    with col2:
        st.metric(
            label=f"📈 PPI {last_year}",
            value=f"{last_ppi:.1f}",
            delta=f"{delta_ppi:+.2f} pts",
        )
    with col3:
        st.metric(
            label="🏆 Prix Cacao Record",
            value=f"${peak_cocoa:,.0f}",
            delta=f"en {peak_year}",
            delta_color="off",
        )
    with col4:
        ppi_vs_ref = last_ppi - PPI_BASE_YEAR_VALUE
        st.metric(
            label="📊 PPI vs Référence 2011",
            value=f"{last_ppi:.1f}",
            delta=f"{ppi_vs_ref:+.1f}% vs base 100",
        )


# ────────────────────────────────────────────────────────────────────────────
#  Construction du tableau Plotly
# ────────────────────────────────────────────────────────────────────────────

def build_table(ind: dict) -> go.Figure:
    return tab_view(ind=ind)


# ────────────────────────────────────────────────────────────────────────────
#  Rendu conditionnel selon la vue choisie
# ────────────────────────────────────────────────────────────────────────────

def _section(label: str) -> None:
    st.markdown(
        f'<div class="section-label">{label}</div>',
        unsafe_allow_html=True,
    )

def _hint(text: str) -> None:
    st.markdown(
        f"<small style='color:#7a7a7a'>{text}</small>",
        unsafe_allow_html=True,
    )


def render_view(view: str, cocoa: pd.Series, ppi: pd.Series, ind: dict) -> None:
    """Affiche la section correspondant à la vue sélectionnée."""

    # ── Filtrage temporel selon le slider de la sidebar ──
    yr = st.session_state.get("year_range", (YEARS[0], YEARS[-1]))
    filtered_years = [y for y in YEARS if yr[0] <= y <= yr[1]]
    cocoa_f = cocoa.reindex(filtered_years)
    ppi_f   = ppi.reindex(filtered_years)
    ind_f   = build_indicators(cocoa_f, ppi_f)

    if view in ("table", "all"):
        _section("Tableau récapitulatif")
        _hint(
            "💡 Valeurs positives en <span style='color:#16a34a'>vert</span>, "
            "négatives en <span style='color:#dc2626'>rouge</span>. "
            "Prix cacao en USD/Tonne Métrique."
        )
        st.plotly_chart(build_table(ind_f), width='strectch')

    if view in ("cocoa", "all"):
        _section("Prix du Cacao (2020 – 2026)")
        st.plotly_chart(chart_cocoa(cocoa_f), width='strectch', key="cocoa_chart")

    if view in ("ppi", "all"):
        _section("PPI – Producer Price Index")
        st.plotly_chart(chart_ppi(ppi_f), width='strectch', key="ppi_chart")

    if view in ("mixed", "all"):
        _section("Comparaison Cacao & PPI")
        st.plotly_chart(chart_mixed(cocoa_f, ppi_f), width='strectch', key="mixed_chart")


# ────────────────────────────────────────────────────────────────────────────
#  Page principale
# ────────────────────────────────────────────────────────────────────────────

def show_dashboard() -> None:
    """Affiche l'interface de visualisation complète."""

    # ── CSS global ─────────────────────────────────────────────────────────
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@400;500;600&display=swap');

        html, body, [class*="css"] {
            font-family: 'DM Sans', sans-serif;
        }
        .dash-header {
            display: flex;
            align-items: center;
            padding: 0.5rem 0 1rem 0;
            border-bottom: 2px solid #e8e0d5;
            margin-bottom: 1.5rem;
        }
        .dash-title {
            font-family: 'DM Serif Display', serif;
            font-size: 1.7rem;
            color: #1a1a1a;
            margin: 0;
        }
        .dash-user {
            font-size: 0.8rem;
            color: #7a7a7a;
            margin-top: 0.2rem;
        }
        .section-label {
            font-size: 0.75rem;
            font-weight: 600;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            color: #92400e;
            margin: 1.5rem 0 0.4rem 0;
        }
        /* Masquer le label du radio dans la sidebar */
        div[data-testid="stSidebar"] .stRadio > div:first-child {
            display: none;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # ── Sidebar ────────────────────────────────────────────────────────────
    view = build_sidebar()

    # ── En-tête principal ──────────────────────────────────────────────────
    st.markdown(
        f"""
        <div class="dash-header">
            <div>
                <div class="dash-title">📊 AMCHO Dashboard</div>
                <div class="dash-user">
                    Connecté en tant que <b>{st.session_state.get("username", "—")}</b>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Chargement des données ─────────────────────────────────────────────
    with st.spinner("Chargement des données…"):
        try:
            cocoa_df = get_cocoa_data()
            ppi_df   = get_ppi_data()
        except Exception as e:
            st.error(f"Erreur de connexion à la base de données : {e}")
            st.stop()

    cocoa = yearly_avg(cocoa_df, "CocoaPrice")
    ppi   = yearly_avg(ppi_df, "PPI")
    ind   = build_indicators(cocoa, ppi)

    # ── KPIs toujours visibles ─────────────────────────────────────────────
    show_kpis(cocoa, ppi)
    st.markdown("<div style='margin-bottom:0.5rem'></div>", unsafe_allow_html=True)

    # ── Rendu de la vue sélectionnée ───────────────────────────────────────
    render_view(view, cocoa, ppi, ind)

    # ── Footer ─────────────────────────────────────────────────────────────
    st.markdown(
        "<hr style='margin-top:2rem;border-color:#e8e0d5'>"
        "<p style='text-align:center;color:#9ca3af;font-size:0.75rem'>"
        "Sources : FRED – PCOCOUSDM & PCU3113513113517 | AMCHO Dashboard 2026"
        "</p>",
        unsafe_allow_html=True,
    )