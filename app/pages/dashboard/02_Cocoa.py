import streamlit as st
from core.dashboard import yearly_avg, chart_cocoa, get_cocoa_data

st.title("🍫 Évolution du Prix du Cacao")

cocoa_df = get_cocoa_data()
cocoa = yearly_avg(cocoa_df, "CocoaPrice")

st.plotly_chart(chart_cocoa(cocoa), width='stretch')