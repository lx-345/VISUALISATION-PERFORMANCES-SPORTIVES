import streamlit as st

def apply_custom_css():
    css = """
    <style>
    /* Importation d'une police moderne et épurée (proche de Typia Nesia / Emelind) */
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700;800;900&display=swap');

    /* Application de la police à toute l'application */
    html, body, [class*="css"] {
        font-family: 'Montserrat', sans-serif;
    }

    /* Fond noir global pour l'espace performance */
    .stApp {
        background-color: #0A0A0A; /* Noir très profond */
        color: #F5F5DC; /* Texte Beige par défaut */
    }

    /* Style des Titres (Reproduction de l'effet massif et blanc de l'image) */
    h1, h2, h3 {
        font-family: 'Montserrat', sans-serif;
        font-weight: 900 !important;
        color: #FFFFFF !important; /* Titres éclatants */
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* ----------------------------------- */
    /* STYLE DU BOUTON CENTRAL (Marine & Beige) */
    /* ----------------------------------- */
    .stButton {
        display: flex;
        justify-content: center;
    }

    .stButton>button {
        background-color: #1D3557 !important; /* Bleu Marine dominant */
        color: #F5F5DC !important; /* Texte Beige */
        font-family: 'Montserrat', sans-serif;
        font-weight: 800;
        font-size: 24px !important;
        padding: 20px 40px !important;
        border-radius: 0px !important; /* Bords droits pour l'effet épuré/minimaliste */
        border: 2px solid #1D3557 !important;
        transition: all 0.4s ease;
        text-transform: uppercase;
        box-shadow: 0px 10px 30px rgba(29, 53, 87, 0.4);
    }

    /* Effet au survol du bouton */
    .stButton>button:hover {
        background-color: #F5F5DC !important; /* Devient Beige */
        color: #0A0A0A !important; /* Texte Noir */
        border: 2px solid #F5F5DC !important;
        box-shadow: 0px 10px 30px rgba(245, 245, 220, 0.2);
        transform: translateY(-3px);
    }

    /* ----------------------------------- */
    /* STYLE DES CARTES KPIs (Performances)*/
    /* ----------------------------------- */
    div[data-testid="metric-container"] {
        background-color: #141414; /* Noir légèrement plus clair pour détacher la carte */
        border-left: 4px solid #1D3557; /* Ligne Bleu Marine */
        padding: 20px;
        color: #F5F5DC;
    }
    
    div[data-testid="metric-container"] label {
        color: #D3CBB8 !important; /* Beige assombri pour les sous-titres */
        font-weight: 700;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)