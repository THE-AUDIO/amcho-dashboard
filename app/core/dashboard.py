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

# ── Constantes ───────────────────────────────────────────────────────────────
YEARS = list(range(2020, 2027))
PPI_BASE_YEAR_VALUE = 100  # Valeur de référence PPI 2011

COCOA_COLOR = "#92400e"
PPI_COLOR   = "#1e40af"
GRID_COLOR  = "#f1ece6"

# Vues disponibles dans la sidebar
VIEWS = {
    "📋 Tableau récapitulatif":  "table",
    "🍫 Prix du Cacao":          "cocoa",
    "📈 PPI (Producer Price Index)": "ppi",
    "🔀 Comparaison Cacao & PPI": "mixed",
    "🗂️ Vue complète":           "all",
}

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
    if not is_change_row or pd.isna(v) or v == 0:
        return "#1a1a1a"
    return "#16a34a" if v > 0 else "#dc2626"

def cell_bg_color(v, is_change_row: bool) -> str:
    if not is_change_row or pd.isna(v) or v == 0:
        return "white"
    return "#f0fdf4" if v > 0 else "#fef2f2"


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
    ROW_META = [
        ("cocoa_price",  "Cocoa Price",          True,  False, False),
        ("cocoa_change", "Cocoa Price Change",    False, True,  False),
        ("cocoa_pct",    "Cocoa Price % Change",  False, True,  True),
        ("ppi_price",    "PPI",                   True,  False, False),
        ("ppi_change",   "PPI Change",            False, True,  False),
        ("ppi_pct",      "PPI % Change",          False, True,  True),
        ("ppi_ref_pct",  "PPI % Change Reference",False, True,  True),
    ]

    n_rows = len(ROW_META)
    col_labels       = [meta[1] for meta in ROW_META]
    col_label_colors = ["#f8f4ef"] * n_rows
    col_label_fonts  = ["#1a1a1a"] * n_rows

    year_col_vals, year_col_bgs, year_col_fonts = [], [], []

    for y_idx, year in enumerate(YEARS):
        col_v, col_bg, col_fc = [], [], []
        for key, _label, is_price, is_change, is_pct in ROW_META:
            val = ind[key].get(year)
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

    all_vals  = [col_labels]        + year_col_vals
    all_bgs   = [col_label_colors]  + year_col_bgs
    all_fonts = [col_label_fonts]   + year_col_fonts

    fig = go.Figure(
        data=[go.Table(
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
        )]
    )
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), height=280)
    return fig


# ────────────────────────────────────────────────────────────────────────────
#  Graphiques
# ────────────────────────────────────────────────────────────────────────────

def chart_cocoa(cocoa: pd.Series) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=YEARS, y=cocoa.values,
        mode="lines+markers",
        name="Cocoa Price",
        line=dict(color=COCOA_COLOR, width=2.5),
        marker=dict(size=7, color=COCOA_COLOR, symbol="circle"),
        hovertemplate="<b>%{x}</b><br>Prix : %{y:,.2f} USD/MT<extra></extra>",
    ))
    fig.update_layout(
        **CHART_LAYOUT,
        title=dict(text="Évolution du Prix du Cacao", font=dict(size=13)),
        yaxis_title="USD / Tonne Métrique",
    )
    return fig


def chart_ppi(ppi: pd.Series) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=YEARS, y=ppi.values,
        mode="lines+markers",
        name="PPI",
        line=dict(color=PPI_COLOR, width=2.5),
        marker=dict(size=7, color=PPI_COLOR, symbol="diamond"),
        hovertemplate="<b>%{x}</b><br>PPI : %{y:.2f}<extra></extra>",
    ))
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
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(
        x=YEARS, y=cocoa.values,
        name="Cocoa Price (USD/MT)",
        marker_color="#c8a97e",
        opacity=0.85,
        hovertemplate="<b>%{x}</b><br>Prix cacao : %{y:,.2f} USD/MT<extra></extra>",
    ), secondary_y=False)
    fig.add_trace(go.Scatter(
        x=YEARS, y=ppi.values,
        name="PPI",
        mode="lines+markers",
        line=dict(color=PPI_COLOR, width=2.5),
        marker=dict(size=7, symbol="diamond"),
        hovertemplate="<b>%{x}</b><br>PPI : %{y:.2f}<extra></extra>",
    ), secondary_y=True)
    fig.update_xaxes(showgrid=False, tickmode="array", tickvals=YEARS, ticktext=[str(y) for y in YEARS])
    fig.update_yaxes(title_text="<b>Cocoa Price</b> (USD/MT)", gridcolor=GRID_COLOR, secondary_y=False)
    fig.update_yaxes(title_text="<b>PPI</b> Index", secondary_y=True)
    fig.update_layout(
        font=dict(family="DM Sans", size=11, color="#4b4b4b"),
        plot_bgcolor="white", paper_bgcolor="white",
        hovermode="x unified",
        margin=dict(l=50, r=60, t=30, b=40),
        title=dict(text="Comparaison Cocoa Price & PPI", font=dict(size=13)),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        barmode="group",
    )
    return fig


# ────────────────────────────────────────────────────────────────────────────
#  Sidebar
# ────────────────────────────────────────────────────────────────────────────

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