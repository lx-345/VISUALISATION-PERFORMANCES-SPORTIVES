from unittest.mock import patch

import pandas as pd
import pytest  # <-- À ajouter

from visualisation_performances_sportives.analyse_sportive.data import get_clean_data


@pytest.mark.unit  # <-- À ajouter
def test_get_clean_data_is_callable():
    """
    Vérifie que la fonction de récupération des données est bien accessible
    et qu'elle est exécutable (callable).
    """
    assert callable(get_clean_data), (
        "La fonction get_clean_data doit être définie et appelable."
    )


@pytest.mark.unit  # <-- À ajouter
@patch("visualisation_performances_sportives.analyse_sportive.data.s3fs.S3FileSystem")
@patch("visualisation_performances_sportives.analyse_sportive.data.pd.read_csv")
def test_get_clean_data_with_mock(mock_read_csv, mock_s3fs):
    """
    Test unitaire avec Mock : on simule la connexion S3...
    """
    faux_df = pd.DataFrame(
        {
            "annee": [2023, 2023],
            "trimestre": ["T1", "T2"],
            "distance_cible": ["10k", "Semi"],
        }
    )

    mock_read_csv.return_value = faux_df

    df_resultat = get_clean_data()

    mock_s3fs.assert_called_once()
    assert not df_resultat.empty, "Le DataFrame renvoyé ne devrait pas être vide."
    assert len(df_resultat) == 2, "Le DataFrame devrait contenir exactement 2 lignes."
    assert "distance_cible" in df_resultat.columns, (
        "La colonne 'distance_cible' devrait être présente."
    )
