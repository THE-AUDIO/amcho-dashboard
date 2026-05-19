import pandas as pd

# Fonctions utilitaires pour formater valeurs et styles de cellules
# (minimal comments pour clarifier l'usage)

# Formatte un prix numérique; renvoie un tiret si manquant
def fmt_price(v, decimals: int = 2) -> str:
    if pd.isna(v):
        return "—"
    return f"{v:,.{decimals}f}"

# Formatte un changement (avec ou sans pourcentage)
def fmt_change(v, is_pct: bool = False) -> str:
    if pd.isna(v):
        return "—"
    suffix = "%" if is_pct else ""
    sign = "+" if v > 0 else ""
    return f"{sign}{v:.2f}{suffix}"

# Couleur du texte selon signe du changement
def cell_font_color(v, is_change_row: bool) -> str:
    if not is_change_row or pd.isna(v) or v == 0:
        return "#1a1a1a"
    return "#16a34a" if v > 0 else "#dc2626"

# Couleur de fond de cellule selon signe du changement
def cell_bg_color(v, is_change_row: bool) -> str:
    if not is_change_row or pd.isna(v) or v == 0:
        return "white"
    return "#f0fdf4" if v > 0 else "#fef2f2"

