import streamlit as st
from visualisation_performances_sportives.analyse_sportive.data import get_clean_data
from visualisation_performances_sportives.analyse_sportive.backend import preparer_donnees_agregees

st.set_page_config(page_title="Performances Sportives", layout="wide")

st.title("🏃‍♂️ Tableau de Bord - Performances Sportives")

@st.cache_data
def charger_donnees():
    return get_clean_data()

try:
    df = charger_donnees()
    st.success("Données chargées avec succès depuis le stockage S3 !")
    
    # Utilisation du backend existant
    df_yearly, _ = preparer_donnees_agregees(df)
    
    st.subheader("Évolution de la distance par année")
    if not df_yearly.empty:
        st.bar_chart(df_yearly.set_index('annee')['distance_km'])
    else:
        st.warning("Aucune donnée annuelle disponible.")
        
except Exception as e:
    st.error(f"Erreur lors du chargement des données : {e}")