"""Page de comparaison entre les prix du cacao et l'indice PPI."""

import streamlit as st
from core.dashboard import yearly_avg, chart_mixed, get_cocoa_data, get_ppi_data

# Titre de la page
st.title("🔀 Comparaison Cacao & PPI")

# Charger les données avec indicateur de chargement
with st.spinner("Chargement des données…"):
    cocoa_df = get_cocoa_data()
    ppi_df = get_ppi_data()

# Traiter les données pour les deux indicateurs
cocoa = yearly_avg(cocoa_df, "CocoaPrice")
ppi = yearly_avg(ppi_df, "PPI")

# Afficher le graphique de comparaison
st.plotly_chart(chart_mixed(cocoa, ppi), width='stretch')