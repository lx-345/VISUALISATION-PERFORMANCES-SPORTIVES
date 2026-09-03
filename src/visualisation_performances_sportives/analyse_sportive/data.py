import os

import pandas as pd
import s3fs
from dotenv import load_dotenv

load_dotenv()


def get_clean_data() -> pd.DataFrame:
    """Récupère les données nettoyées depuis le bucket S3
    et retourne un DataFrame pandas prêt pour l'analyse.
    """
    bucket = os.getenv("S3_BUCKET", "paleo")
    chemin_s3 = f"{bucket}/donnees_strava/activites_clean.csv"

    endpoint = os.getenv("AWS_S3_ENDPOINT", "https://minio.lab.sspcloud.fr")
    if not endpoint.startswith("http://") and not endpoint.startswith("https://"):
        endpoint = f"https://{endpoint}"

    # Connexion S3 basée sur les clés temporaires incluant le token de session
    fs = s3fs.S3FileSystem(
        client_kwargs={"endpoint_url": endpoint},
        key=os.getenv("AWS_ACCESS_KEY_ID"),
        secret=os.getenv("AWS_SECRET_ACCESS_KEY"),
        token=os.getenv("AWS_SESSION_TOKEN"),
    )

    with fs.open(chemin_s3, "rb") as f:
        return pd.read_csv(f)


if __name__ == "__main__":
    df_strava = get_clean_data()
    print(f"Données chargées avec succès : {df_strava.shape[0]} lignes trouvées.")
