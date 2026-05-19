import streamlit as st
from core.dashboard import yearly_avg, chart_ppi, get_ppi_data

st.title("📈 Producer Price Index (PPI)")

with st.spinner("Chargement des données…"):
    ppi_df = get_ppi_data()

ppi = yearly_avg(ppi_df, "PPI")
st.plotly_chart(chart_ppi(ppi), width='stretch')