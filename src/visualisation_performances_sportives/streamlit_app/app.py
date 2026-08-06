import plotly.express as px
import streamlit as st

from visualisation_performances_sportives.analyse_sportive.data import (
    get_clean_data,
)
from visualisation_performances_sportives.streamlit_app.style import (
    apply_custom_css,
)

# Configuration de la page
st.set_page_config(
    page_title="Espace Performance",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

apply_custom_css()


@st.cache_data
def load_data():
    """Charge les données nettoyées depuis S3."""
    return get_clean_data()


# Gestion de la navigation
if "entered_app" not in st.session_state:
    st.session_state.entered_app = False

if not st.session_state.entered_app:
    # Page d'accueil
    st.markdown("<br><br><br><br><br><br>", unsafe_allow_html=True)
    st.markdown(
        "<h1 style='text-align: center; font-size: 70px; "
        "line-height: 1.1;'>ANALYSE</h1>",
        unsafe_allow_html=True,
    )
    st.markdown("<br><br>", unsafe_allow_html=True)

    if st.button("ACCÉDER AUX PERFORMANCES"):
        st.session_state.entered_app = True
        st.rerun()

else:
    # Dashboard
    try:
        df = load_data()
    except Exception as e:
        st.error(f"Erreur lors du chargement des données depuis S3 : {e}")
        st.stop()

    # Barre latérale (Filtres)
    if st.sidebar.button("← Retour à l'accueil"):
        st.session_state.entered_app = False
        st.rerun()

    st.sidebar.markdown("---")
    st.sidebar.header("⚙️ Filtres Globaux")

    if "annee" in df.columns:
        annees = df["annee"].dropna().unique().tolist()
        annee_selection = st.sidebar.selectbox(
            "Sélectionnez l'année", options=["Toutes"] + sorted(annees, reverse=True)
        )
    else:
        annee_selection = "Toutes"

    if "type_entrainement" in df.columns:
        types_entrainement = df["type_entrainement"].dropna().unique().tolist()
        type_selection = st.sidebar.multiselect(
            "Type d'entraînement",
            options=types_entrainement,
            default=types_entrainement,
        )
    else:
        type_selection = []

    # Filtrage des données
    df_filtered = df.copy()
    if annee_selection != "Toutes" and "annee" in df_filtered.columns:
        df_filtered = df_filtered[df_filtered["annee"] == annee_selection]
    if type_selection and "type_entrainement" in df_filtered.columns:
        df_filtered = df_filtered[df_filtered["type_entrainement"].isin(type_selection)]

    st.title("⚡ DASHBOARD PERFORMANCES")
    st.markdown("---")

    tab1, tab2, tab3 = st.tabs(
        [
            "📅 Bilan Hebdomadaire",
            "📊 Analyse Globale",
            "⚖️ Suivi de la Charge (ACWR)",
        ]
    )

    # 1. Bilan Hebdomadaire
    with tab1:
        st.header("Résumé des Performances")
        col1, col2, col3, col4 = st.columns(4)

        vol_total = (
            df_filtered["distance_km"].sum()
            if "distance_km" in df_filtered.columns
            else 0
        )
        temps_total = (
            df_filtered["moving_time_min"].sum()
            if "moving_time_min" in df_filtered.columns
            else 0
        )
        vma_moyenne = df_filtered["VMA"].mean() if "VMA" in df_filtered.columns else 0
        stress_mec = (
            df_filtered["stress_mecanique"].sum()
            if "stress_mecanique" in df_filtered.columns
            else 0
        )

        col1.metric("Volume Total (km)", f"{vol_total:.1f}")
        col2.metric("Temps Total (min)", f"{temps_total:.0f}")
        col3.metric("VMA Moyenne", f"{vma_moyenne:.2f}")
        col4.metric("Stress Mécanique", f"{stress_mec:.0f}")

        st.subheader("Détail des dernières séances")
        cols_to_show = [
            "start_date_local",
            "name",
            "type_entrainement",
            "distance_km",
            "VMA",
        ]
        cols_to_show = [c for c in cols_to_show if c in df_filtered.columns]

        if cols_to_show:
            st.dataframe(df_filtered[cols_to_show].tail(10), use_container_width=True)

    # 2. Analyse Globale
    with tab2:
        st.header("Tendances et Répartition")
        col_chart1, col_chart2 = st.columns(2)

        with col_chart1:
            st.subheader("Volume par Trimestre")
            if (
                "trimestre" in df_filtered.columns
                and "distance_km" in df_filtered.columns
            ):
                df_trimestre = (
                    df_filtered.groupby("trimestre")["distance_km"].sum().reset_index()
                )
                fig_vol = px.bar(
                    df_trimestre,
                    x="trimestre",
                    y="distance_km",
                    text_auto=".1f",
                    color_discrete_sequence=["#1D3557"],
                )
                fig_vol.update_layout(
                    plot_bgcolor="#141414",
                    paper_bgcolor="#141414",
                    font_color="#F5F5DC",
                    title_font_color="#FFFFFF",
                    xaxis_title="Trimestre",
                    yaxis_title="Distance (km)",
                )
                st.plotly_chart(fig_vol, use_container_width=True)
            else:
                st.info("Données trimestrielles non disponibles.")

        with col_chart2:
            st.subheader("Répartition par Type d'entraînement")
            if (
                "type_entrainement" in df_filtered.columns
                and "distance_km" in df_filtered.columns
            ):
                fig_pie = px.pie(
                    df_filtered,
                    names="type_entrainement",
                    values="distance_km",
                    hole=0.4,
                    color_discrete_sequence=["#1D3557", "#457B9D", "#F5F5DC"],
                )
                fig_pie.update_layout(
                    plot_bgcolor="#141414",
                    paper_bgcolor="#141414",
                    font_color="#F5F5DC",
                )
                st.plotly_chart(fig_pie, use_container_width=True)
            else:
                st.info("Types d'entraînement non disponibles.")

    # 3. Suivi de la Charge (ACWR)
    with tab3:
        st.header("Analyse de la Fatigue et du Rendement (ACWR)")

        if (
            "Ratio_ACWR" in df_filtered.columns
            and "start_date_local" in df_filtered.columns
        ):
            st.subheader("Évolution du Ratio ACWR")
            df_chrono = df_filtered.sort_values("start_date_local").dropna(
                subset=["Ratio_ACWR"]
            )

            fig_acwr = px.line(
                df_chrono,
                x="start_date_local",
                y="Ratio_ACWR",
                markers=True,
                color_discrete_sequence=["#F5F5DC"],
            )
            fig_acwr.add_hline(
                y=1.5,
                line_dash="dash",
                line_color="#FF4B4B",
                annotation_text="Zone de danger (>1.5)",
            )
            fig_acwr.add_hline(
                y=0.8,
                line_dash="dash",
                line_color="#E9C46A",
                annotation_text="Sous-entraînement (<0.8)",
            )
            fig_acwr.add_hrect(
                y0=0.8,
                y1=1.3,
                line_width=0,
                fillcolor="#2A9D8F",
                opacity=0.1,
                annotation_text="Zone Optimale",
            )
            fig_acwr.update_layout(
                plot_bgcolor="#141414",
                paper_bgcolor="#141414",
                font_color="#F5F5DC",
                title_font_color="#FFFFFF",
                yaxis_title="Ratio ACWR",
                xaxis_title="Date",
            )
            st.plotly_chart(fig_acwr, use_container_width=True)
        else:
            st.warning(
                "Les colonnes 'Ratio_ACWR' ou 'start_date_local' "
                "sont absentes des données traitées."
            )

        if "Statut Alerte" in df_filtered.columns:
            st.subheader("Aperçu des Statuts d'Alerte")
            alert_counts = df_filtered["Statut Alerte"].value_counts().reset_index()
            alert_counts.columns = ["Statut", "Nombre de séances"]
            st.dataframe(alert_counts, use_container_width=True)


def run():
    """Point d'entrée CLI pour lancer l'application Streamlit."""
    import subprocess
    import sys
    from pathlib import Path

    app_path = Path(__file__).resolve()
    subprocess.run([sys.executable, "-m", "streamlit", "run", str(app_path)])


if __name__ == "__main__":
    run()
