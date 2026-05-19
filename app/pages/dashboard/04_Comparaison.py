import streamlit as st
from core.dashboard import yearly_avg, chart_mixed, get_cocoa_data, get_ppi_data

st.title("🔀 Comparaison Cacao & PPI")

with st.spinner("Chargement des données…"):
    cocoa_df = get_cocoa_data()
    ppi_df = get_ppi_data()

cocoa = yearly_avg(cocoa_df, "CocoaPrice")
ppi = yearly_avg(ppi_df, "PPI")

st.plotly_chart(chart_mixed(cocoa, ppi), width='stretch')