from unittest.mock import patch

import pandas as pd
import pytest
from visualisation_performances_sportives.analyse_sportive.data import (
    get_clean_data,
)


@pytest.mark.unit
def test_get_clean_data_is_callable():
    """Vérifie que la fonction get_clean_data est accessible."""
    msg = "La fonction get_clean_data doit être définie et appelable."
    assert callable(get_clean_data), msg


@pytest.mark.unit
@patch("visualisation_performances_sportives.analyse_sportive.data.s3fs.S3FileSystem")
@patch("visualisation_performances_sportives.analyse_sportive.data.pd.read_csv")
def test_get_clean_data_deployment_simulation(mock_read_csv, mock_s3fs, monkeypatch):
    """Simule le pod en déploiement (clés permanentes)."""
    # 1. Variables d'environnement de production
    monkeypatch.setenv("AWS_ACCESS_KEY_ID", "fake_prod_key")
    monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "fake_prod_secret")
    monkeypatch.setenv("AWS_S3_ENDPOINT", "https://minio.lab.sspcloud.fr")
    monkeypatch.setenv("S3_BUCKET", "paleo")
    monkeypatch.delenv("AWS_SESSION_TOKEN", raising=False)

    # 2. Mock du retour de pandas
    faux_df = pd.DataFrame(
        {
            "annee": [2023, 2023],
            "trimestre": ["T1", "T2"],
            "distance_cible": ["10k", "Semi"],
        }
    )
    mock_read_csv.return_value = faux_df

    # 3. Exécution
    df_resultat = get_clean_data()

    # 4. Vérification de l'instanciation s3fs (sans token)
    mock_s3fs.assert_called_once_with(
        client_kwargs={"endpoint_url": "https://minio.lab.sspcloud.fr"},
        key="fake_prod_key",
        secret="fake_prod_secret",
    )

    # 5. Assertions sur les données
    assert not df_resultat.empty, "Le DataFrame ne devrait pas être vide."
    assert len(df_resultat) == 2, "Le DataFrame devrait contenir 2 lignes."
    assert (
        "distance_cible" in df_resultat.columns
    ), "La colonne 'distance_cible' devrait être présente."
