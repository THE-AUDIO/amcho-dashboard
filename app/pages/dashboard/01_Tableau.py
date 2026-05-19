import streamlit as st
import pandas as pd
from service.db import get_cocoa_data, get_ppi_data

from core.dashboard import ( 
    yearly_avg, build_indicators, show_kpis, build_table, 
)

def main():
    st.title("📋 Tableau Récapitulatif")
    
    # Chargement données (tu peux mettre en cache)
    cocoa_df = get_cocoa_data()
    ppi_df = get_ppi_data()
    
    cocoa = yearly_avg(cocoa_df, "CocoaPrice")
    ppi = yearly_avg(ppi_df, "PPI")
    ind = build_indicators(cocoa, ppi)
    
    show_kpis(cocoa, ppi)
    st.plotly_chart(build_table(ind), width='stretch')

if __name__ == "__main__":
    main()