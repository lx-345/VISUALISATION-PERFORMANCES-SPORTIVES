from .styles import appliquer_theme_global, get_base_styles


def construire_page_bilan(wb, max_data_row, len_y, len_s, len_n):
    """
    Génère l'onglet 'Bilan' récapitulant les temps forts et statistiques globales.
    """
    ws = wb.create_sheet(title="Bilan")
    appliquer_theme_global(ws)

    couleur_fond, police_titre, _, align_center, bordure = get_base_styles()

    # Titre de la page
    ws["A1"] = "BILAN GLOBAL"
    ws["A1"].font = police_titre
    ws["A1"].fill = couleur_fond
    ws["A1"].alignment = align_center
    ws["A1"].border = bordure
    ws.merge_cells("A1:H2")

    # Insertion de KPIs utilisant des formules Excel natives
    ws["B5"] = "Total Activités:"
    ws["C5"] = f"=COUNTA(Data!A2:A{max_data_row})"
