"""
page/dashboard.py – Interface principale de visualisation.

Contient :
  1. Table récapitulative (Cocoa + PPI, 2020-2026)
     – valeurs négatives en rouge, positives en vert
  2. Graphique 1 : Évolution annuelle du prix du cacao (line chart)
  3. Graphique 2 : Évolution annuelle du PPI (line chart)
  4. Graphique 3 : Comparaison mixte bar (cacao) + ligne (PPI)
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from service.db import get_cocoa_data, get_ppi_data

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
    """
    Calcule toutes les lignes du tableau :
      cocoa_price, cocoa_change, cocoa_pct,
      ppi_price, ppi_change, ppi_pct, ppi_ref_pct
    """
    cocoa_change = cocoa.diff()
    # pct_change = (val_n - val_(n-1)) / |val_(n-1)| * 100
    cocoa_pct    = cocoa.pct_change() * 100

    ppi_change   = ppi.diff()
    ppi_pct      = ppi.pct_change() * 100
    # PPI % Change Reference = (PPI_année - 100) / 100 * 100 = PPI_année - 100
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
#  Formatage
# ────────────────────────────────────────────────────────────────────────────

def fmt_price(v, decimals: int = 2) -> str:
    if pd.isna(v):
        return "—"
    return f"{v:,.{decimals}f}"

def fmt_change(v, is_pct: bool = False) -> str:
    if pd.isna(v):
        return "—"
    suffix = "%" if is_pct else ""
    sign = "+" if v > 0 else ""
    return f"{sign}{v:.2f}{suffix}"

def cell_font_color(v, is_change_row: bool) -> str:
    """Rouge si négatif, vert si positif, noir pour les prix absolus."""
    if not is_change_row or pd.isna(v) or v == 0:
        return "#1a1a1a"
    return "#16a34a" if v > 0 else "#dc2626"

def cell_bg_color(v, is_change_row: bool) -> str:
    if not is_change_row or pd.isna(v) or v == 0:
        return "white"
    return "#f0fdf4" if v > 0 else "#fef2f2"


# ────────────────────────────────────────────────────────────────────────────
#  Construction du tableau Plotly
# ────────────────────────────────────────────────────────────────────────────

def build_table(ind: dict) -> go.Figure:
    """
    Construit la go.Table avec coloration conditionnelle.
    Structure : 8 colonnes (Indicateur + 7 années) x 7 lignes.
    """
    ROW_META = [
        # (key,           label,                        is_price, is_change, is_pct)
        ("cocoa_price",  "Cocoa Price",                 True,  False, False),
        ("cocoa_change", "Cocoa Price Change",           False, True,  False),
        ("cocoa_pct",    "Cocoa Price % Change",         False, True,  True),
        ("ppi_price",    "PPI",                          True,  False, False),
        ("ppi_change",   "PPI Change",                   False, True,  False),
        ("ppi_pct",      "PPI % Change",                 False, True,  True),
        ("ppi_ref_pct",  "PPI % Change Reference",       False, True,  True),
    ]

    n_rows = len(ROW_META)

    # Colonne 0 : noms d'indicateurs
    col_labels = [meta[1] for meta in ROW_META]
    col_label_colors = ["#f8f4ef"] * n_rows
    col_label_fonts  = ["#1a1a1a"] * n_rows

    # Colonnes 1-7 : une par année
    year_col_vals   = []  # liste de listes (une par année)
    year_col_bgs    = []
    year_col_fonts  = []

    for y_idx, year in enumerate(YEARS):
        col_v, col_bg, col_fc = [], [], []

        for key, _label, is_price, is_change, is_pct in ROW_META:
            val = ind[key].get(year)

            # Première année : les "change" valent 0 par définition
            if y_idx == 0 and is_change:
                col_v.append("0%" if is_pct else "0")
                col_bg.append("white")
                col_fc.append("#1a1a1a")
            elif pd.isna(val) or val is None:
                col_v.append("—")
                col_bg.append("white")
                col_fc.append("#9ca3af")
            elif is_price:
                col_v.append(fmt_price(val))
                col_bg.append("white")
                col_fc.append("#1a1a1a")
            else:
                col_v.append(fmt_change(val, is_pct=is_pct))
                col_bg.append(cell_bg_color(val, is_change))
                col_fc.append(cell_font_color(val, is_change))

        year_col_vals.append(col_v)
        year_col_bgs.append(col_bg)
        year_col_fonts.append(col_fc)

    # Assemblage pour go.Table (chaque élément = une colonne)
    all_vals   = [col_labels]   + year_col_vals
    all_bgs    = [col_label_colors] + year_col_bgs
    all_fonts  = [col_label_fonts]  + year_col_fonts

    fig = go.Figure(
        data=[
            go.Table(
                columnwidth=[220] + [100] * len(YEARS),
                header=dict(
                    values=["<b>Indicateurs</b>"] + [f"<b>{y}</b>" for y in YEARS],
                    fill_color="#1a1a1a",
                    font=dict(color="white", size=12, family="DM Sans"),
                    align=["left"] + ["center"] * len(YEARS),
                    height=36,
                ),
                cells=dict(
                    values=all_vals,
                    fill_color=all_bgs,
                    font=dict(color=all_fonts, size=12, family="DM Sans"),
                    align=["left"] + ["center"] * len(YEARS),
                    height=32,
                ),
            )
        ]
    )
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), height=280)
    return fig


# ────────────────────────────────────────────────────────────────────────────
#  Graphiques
# ────────────────────────────────────────────────────────────────────────────

COCOA_COLOR = "#92400e"
PPI_COLOR   = "#1e40af"
GRID_COLOR  = "#f1ece6"

CHART_LAYOUT = dict(
    font=dict(family="DM Sans", size=11, color="#4b4b4b"),
    plot_bgcolor="white",
    paper_bgcolor="white",
    hovermode="x unified",
    margin=dict(l=50, r=20, t=30, b=40),
    xaxis=dict(
        showgrid=False,
        tickmode="array",
        tickvals=YEARS,
        ticktext=[str(y) for y in YEARS],
    ),
    yaxis=dict(gridcolor=GRID_COLOR, showgrid=True),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
)


def chart_cocoa(cocoa: pd.Series) -> go.Figure:
    """Graphique 1 – Prix annuel du cacao (line chart)."""
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=YEARS,
            y=cocoa.values,
            mode="lines+markers",
            name="Cocoa Price",
            line=dict(color=COCOA_COLOR, width=2.5),
            marker=dict(size=7, color=COCOA_COLOR, symbol="circle"),
            hovertemplate="<b>%{x}</b><br>Prix : %{y:,.2f} USD/MT<extra></extra>",
        )
    )
    fig.update_layout(
        **CHART_LAYOUT,
        title=dict(text="Évolution du Prix du Cacao", font=dict(size=13)),
        yaxis_title="USD / Tonne Métrique",
    )
    return fig


def chart_ppi(ppi: pd.Series) -> go.Figure:
    """Graphique 2 – PPI annuel (line chart)."""
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=YEARS,
            y=ppi.values,
            mode="lines+markers",
            name="PPI",
            line=dict(color=PPI_COLOR, width=2.5),
            marker=dict(size=7, color=PPI_COLOR, symbol="diamond"),
            hovertemplate="<b>%{x}</b><br>PPI : %{y:.2f}<extra></extra>",
        )
    )
    # Ligne de référence à 100
    fig.add_hline(
        y=100, line_dash="dot", line_color="#9ca3af",
        annotation_text="Référence 2011 (100)",
        annotation_position="bottom right",
    )
    fig.update_layout(
        **CHART_LAYOUT,
        title=dict(text="Évolution du PPI (Producer Price Index)", font=dict(size=13)),
        yaxis_title="Indice PPI",
    )
    return fig


def chart_mixed(cocoa: pd.Series, ppi: pd.Series) -> go.Figure:
    """Graphique 3 – Bar (Cacao) + Ligne (PPI) sur double axe."""
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Barres : prix du cacao
    fig.add_trace(
        go.Bar(
            x=YEARS,
            y=cocoa.values,
            name="Cocoa Price (USD/MT)",
            marker_color="#c8a97e",
            opacity=0.85,
            hovertemplate="<b>%{x}</b><br>Prix cacao : %{y:,.2f} USD/MT<extra></extra>",
        ),
        secondary_y=False,
    )

    # Ligne : PPI
    fig.add_trace(
        go.Scatter(
            x=YEARS,
            y=ppi.values,
            name="PPI",
            mode="lines+markers",
            line=dict(color=PPI_COLOR, width=2.5),
            marker=dict(size=7, symbol="diamond"),
            hovertemplate="<b>%{x}</b><br>PPI : %{y:.2f}<extra></extra>",
        ),
        secondary_y=True,
    )

    fig.update_xaxes(
        showgrid=False,
        tickmode="array",
        tickvals=YEARS,
        ticktext=[str(y) for y in YEARS],
    )
    fig.update_yaxes(
        title_text="<b>Cocoa Price</b> (USD/MT)",
        gridcolor=GRID_COLOR,
        secondary_y=False,
    )
    fig.update_yaxes(title_text="<b>PPI</b> Index", secondary_y=True)
    fig.update_layout(
        font=dict(family="DM Sans", size=11, color="#4b4b4b"),
        plot_bgcolor="white",
        paper_bgcolor="white",
        hovermode="x unified",
        margin=dict(l=50, r=60, t=30, b=40),
        title=dict(text="Comparaison Cocoa Price & PPI", font=dict(size=13)),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        barmode="group",
    )
    return fig


# ────────────────────────────────────────────────────────────────────────────
#  Page principale
# ────────────────────────────────────────────────────────────────────────────

def show_dashboard() -> None:
    """Affiche l'interface de visualisation complète."""

    # ── CSS dashboard ──────────────────────────────────────────────────────
    st.markdown(
        """
        <style>
        .dash-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
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
        }
        .section-label {
            font-size: 0.75rem;
            font-weight: 600;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            color: #92400e;
            margin: 1.5rem 0 0.4rem 0;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # ── En-tête avec bouton logout ─────────────────────────────────────────
    hdr_l, hdr_r = st.columns([8, 1])
    with hdr_l:
        st.markdown(
            f"""
            <div class="dash-header">
                <div>
                    <div class="dash-title">📊 AMCHO Dashboard</div>
                    <div class="dash-user">Connecté en tant que <b>{st.session_state.username}</b></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with hdr_r:
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.username = None
            st.rerun()

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

    # ── Section 1 : Tableau ────────────────────────────────────────────────
    st.markdown('<div class="section-label">Tableau récapitulatif (2020 – 2026)</div>', unsafe_allow_html=True)
    st.markdown(
        "<small style='color:#7a7a7a'>💡 Valeurs positives en <span style='color:#16a34a'>vert</span>, "
        "négatives en <span style='color:#dc2626'>rouge</span>. Prix cacao en USD/Tonne Métrique.</small>",
        unsafe_allow_html=True,
    )
    st.plotly_chart(build_table(ind), use_container_width=True)

    # ── Section 2 : Graphiques ─────────────────────────────────────────────
    st.markdown('<div class="section-label">Graphiques</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(chart_cocoa(cocoa), use_container_width=True, key="cocoa_chart")
    with col2:
        st.plotly_chart(chart_ppi(ppi), use_container_width=True, key="ppi_chart")

    # Graphique mixte pleine largeur
    st.plotly_chart(chart_mixed(cocoa, ppi), use_container_width=True, key="mixed_chart")

    # ── Footer ─────────────────────────────────────────────────────────────
    st.markdown(
        "<hr style='margin-top:2rem;border-color:#e8e0d5'>"
        "<p style='text-align:center;color:#9ca3af;font-size:0.75rem'>"
        "Sources : FRED – PCOCOUSDM & PCU3113513113517 | AMCHO Dashboard 2026"
        "</p>",
        unsafe_allow_html=True,
    )