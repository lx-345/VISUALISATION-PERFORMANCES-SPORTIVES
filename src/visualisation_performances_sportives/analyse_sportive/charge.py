from .styles import appliquer_theme_global, get_base_styles


def construire_page_charge(wb, max_data_row, len_y, len_t, len_d):
    """
    Génère l'onglet 'Charge de travail' (suivi de l'effort, fatigue, etc.).
    """
    ws = wb.create_sheet(title="Charge de travail")
    appliquer_theme_global(ws)

    couleur_fond, police_titre, _, align_center, bordure = get_base_styles()

    # Titre de la page
    ws["A1"] = "SUIVI DE LA CHARGE DE TRAVAIL"
    ws["A1"].font = police_titre
    ws["A1"].fill = couleur_fond
    ws["A1"].alignment = align_center
    ws["A1"].border = bordure
    ws.merge_cells("A1:L2")
