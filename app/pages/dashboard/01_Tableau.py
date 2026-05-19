"""Page du tableau récapitulatif avec les KPIs principaux."""

import streamlit as st
import pandas as pd
from service.db import get_cocoa_data, get_ppi_data

from core.dashboard import ( 
    yearly_avg, build_indicators, show_kpis, build_table, 
)

def main():
    """Affiche le tableau récapitulatif avec les indicateurs clés."""
    st.title("📋 Tableau Récapitulatif")
    
    # Charger les données du cacao et du PPI
    cocoa_df = get_cocoa_data()
    ppi_df = get_ppi_data()
    
    # Calculer les moyennes annuelles
    cocoa = yearly_avg(cocoa_df, "CocoaPrice")
    ppi = yearly_avg(ppi_df, "PPI")
    
    # Construire les indicateurs
    ind = build_indicators(cocoa, ppi)
    
    # Afficher les KPIs et le tableau
    show_kpis(cocoa, ppi)
    st.plotly_chart(build_table(ind), width='stretch')

if __name__ == "__main__":
    main()