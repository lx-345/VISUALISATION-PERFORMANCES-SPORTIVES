from unittest.mock import patch
import pandas as pd
from openpyxl import Workbook
from visualisation_performances_sportives.analyse_sportive.reporting import generer_reporting_excel

@patch('visualisation_performances_sportives.analyse_sportive.reporting.get_clean_data')
def test_generer_reporting_excel(mock_get_clean_data, tmp_path):
    """Vérifie que l'orchestrateur génère bien un fichier Excel à partir de données mockées."""
    # Préparation d'un faux DataFrame
    mock_get_clean_data.return_value = pd.DataFrame({
        'annee': [2023, 2024],
        'trimestre': ['T1', 'T2'],
        'distance_km': [12.0, 15.5]
    })
    
    # Chemin de sortie temporaire pour le test
    fichier_sortie = tmp_path / "test_bord.xlsx"
    
    # Exécution de la fonction
    generer_reporting_excel(str(fichier_sortie))
    
    # Vérification que le fichier a bien été créé
    assert fichier_sortie.exists(), "Le fichier Excel final n'a pas été généré."