"""Page d'analyse de l'indice des prix à la production (PPI)."""

import streamlit as st
from core.dashboard import yearly_avg, chart_ppi, get_ppi_data

# Titre de la page
st.title("📈 Producer Price Index (PPI)")

# Charger les données avec indicateur de chargement
with st.spinner("Chargement des données…"):
    ppi_df = get_ppi_data()

# Traiter et afficher les données
ppi = yearly_avg(ppi_df, "PPI")
st.plotly_chart(chart_ppi(ppi), width='stretch')