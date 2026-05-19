import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from .formatage import *

# Graphiques et tableaux utilisés par le dashboard (commentaires minimalistes)

YEARS = list(range(2020, 2027))  # années affichées

COCOA_COLOR = "#92400e"  # couleur principale cacao
PPI_COLOR   = "#1e40af"  # couleur PPI
GRID_COLOR  = "#f1ece6"  # couleur des grilles

CHART_LAYOUT = dict(  # mise en page commune aux graphiques
    font=dict(family="DM Sans", size=11, color="#1a1a1a"),  # Forcé en noir/gris très foncé
    plot_bgcolor="white",
    paper_bgcolor="white",
    hovermode="x unified",
    margin=dict(l=50, r=20, t=30, b=40),
    xaxis=dict(
        showgrid=False,
        linecolor="#4b4b4b",  # Ajoute une ligne d'axe visible
        tickfont=dict(color="#1a1a1a", size=11) # Force la couleur des années
    ),
    yaxis=dict(
        gridcolor=GRID_COLOR, 
        showgrid=True,
        tickfont=dict(color="#1a1a1a", size=11)
    ),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
)

def chart_mixed(cocoa: pd.Series, ppi: pd.Series) -> go.Figure:
    # Graphe mixte: barres pour le prix du cacao et ligne pour le PPI
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
        font=dict(family="DM Sans", size=11, color="#000000"),
        # plot_bgcolor="white",
        # paper_bgcolor="white",
        hovermode="x unified",
        margin=dict(l=50, r=60, t=30, b=40),
        title=dict(text="Comparaison Cocoa Price & PPI", font=dict(size=13)),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        barmode="group",
    )
    return fig



def tab_view(ind: dict) -> go.Figure:
    # Tableau récapitulatif des indicateurs par année
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

def chart_cocoa(cocoa: pd.Series) -> go.Figure:
    # Série temporelle: prix du cacao
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
    # Série temporelle: indice PPI avec ligne de référence (100)
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