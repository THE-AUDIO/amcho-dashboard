"""Page d'analyse de l'évolution des prix du cacao."""

import streamlit as st
from core.dashboard import yearly_avg, chart_cocoa, get_cocoa_data

# Titre de la page
st.title("🍫 Évolution du Prix du Cacao")

# Charger et traiter les données
cocoa_df = get_cocoa_data()
cocoa = yearly_avg(cocoa_df, "CocoaPrice")

# Afficher le graphique d'évolution
st.plotly_chart(chart_cocoa(cocoa), width='stretch')