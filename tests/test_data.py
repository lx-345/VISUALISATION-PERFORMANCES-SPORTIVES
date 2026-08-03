# On importe la fonction depuis notre propre package
from unittest.mock import patch

from visualisation_performances_sportives.analyse_sportive.data import get_clean_data
import pandas as pd
def test_get_clean_data_is_callable():
    """
    Vérifie que la fonction de récupération des données est bien accessible
    et qu'elle est exécutable (callable).
    """
    assert callable(get_clean_data), "La fonction get_clean_data doit être définie et appelable."


# On "intercepte" s3fs et read_csv directement dans le fichier data.py où ils sont utilisés
@patch('visualisation_performances_sportives.analyse_sportive.data.s3fs.S3FileSystem')
@patch('visualisation_performances_sportives.analyse_sportive.data.pd.read_csv')
def test_get_clean_data_with_mock(mock_read_csv, mock_s3fs):
    """
    Test unitaire avec Mock : on simule la connexion S3 et on injecte 
    un faux DataFrame pour vérifier la logique interne sans faire d'appel réseau.
    """
    
    # 1. PRÉPARATION DU MOCK (Le faux résultat)
    # On fabrique un minuscule DataFrame de 2 lignes
    faux_df = pd.DataFrame({
        'annee': [2023, 2023],
        'trimestre': ['T1', 'T2'],
        'distance_cible': ['10k', 'Semi']
    })
    
    # On ordonne au mock de pd.read_csv de renvoyer ce faux DataFrame
    mock_read_csv.return_value = faux_df
    
    # 2. EXÉCUTION DE LA FONCTION
    # La fonction s'exécute, mais S3FileSystem et read_csv sont court-circuités !
    df_resultat = get_clean_data()
    
    # 3. VÉRIFICATIONS (Les assertions)
    # On vérifie que notre mock S3 a bien été appelé 1 fois
    mock_s3fs.assert_called_once()
    
    # On vérifie que le résultat reçu est bien notre faux DataFrame
    assert not df_resultat.empty, "Le DataFrame renvoyé ne devrait pas être vide."
    assert len(df_resultat) == 2, "Le DataFrame devrait contenir exactement 2 lignes."
    assert 'distance_cible' in df_resultat.columns, "La colonne 'distance_cible' devrait être présente."