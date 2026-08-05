import pandas as pd
from openpyxl.utils.dataframe import dataframe_to_rows


def preparer_donnees_agregees(df: pd.DataFrame):
    """
    Aggrége les données brutes pour alimenter les graphiques.
    """
    if df.empty:
        return pd.DataFrame(columns=["annee", "distance_km"]), pd.DataFrame(
            columns=["annee", "trimestre", "distance_km"]
        )

    df_yearly = df.groupby("annee").sum(numeric_only=True).reset_index()

    if "trimestre" in df.columns:
        df_trimestriel = (
            df.groupby(["annee", "trimestre"]).sum(numeric_only=True).reset_index()
        )
    else:
        df_trimestriel = pd.DataFrame()

    return df_yearly, df_trimestriel


def construire_onglets_back(wb, df: pd.DataFrame):
    """
    Crée les onglets cachés dans le classeur Excel.
    """
    df_yearly, df_trimestriel = preparer_donnees_agregees(df)

    # Onglet des données brutes
    ws_data = wb.create_sheet(title="Data")
    for r in dataframe_to_rows(df, index=False, header=True):
        ws_data.append(r)
    ws_data.sheet_state = "hidden"

    # Onglet des données agrégées (Backend)
    ws_back = wb.create_sheet(title="Backend")
    ws_back.append(["Année", "Distance (km)"])

    if not df_yearly.empty and "distance_km" in df_yearly.columns:
        for r in dataframe_to_rows(
            df_yearly[["annee", "distance_km"]], index=False, header=False
        ):
            ws_back.append(r)

    ws_back.sheet_state = "hidden"

    return len(df_yearly) + 1, len(df_trimestriel) + 1
