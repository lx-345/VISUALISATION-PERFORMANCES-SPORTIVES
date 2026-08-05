import os

import pandas as pd
import s3fs
from dotenv import load_dotenv

# Charge les variables d'environnement depuis le fichier .env à la racine
load_dotenv()


def get_clean_data() -> pd.DataFrame:
    """
    Récupère les données nettoyées directement depuis le bucket S3 Onyxia
    et retourne un DataFrame pandas prêt pour l'analyse.
    """
    chemin_s3 = "paleo/donnees_strava/activites_clean.csv"

    # Configuration du système de fichiers S3 avec les identifiants du .env
    fs = s3fs.S3FileSystem(
        client_kwargs={"endpoint_url": f"https://{os.getenv('AWS_S3_ENDPOINT')}"},
        key=os.getenv("AWS_ACCESS_KEY_ID"),
        secret=os.getenv("AWS_SECRET_ACCESS_KEY"),
        token=os.getenv("AWS_SESSION_TOKEN"),
    )

    # Lecture directe du CSV distant sans le télécharger localement
    with fs.open(chemin_s3, "rb") as f:
        df = pd.read_csv(f)

    return df


if __name__ == "__main__":
    # Test rapide de la fonction
    df_strava = get_clean_data()
    print(f"Données chargées avec succès : {df_strava.shape[0]} lignes trouvées.")
