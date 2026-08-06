import os

import pandas as pd
import s3fs
from dotenv import load_dotenv

load_dotenv()


def get_clean_data() -> pd.DataFrame:
    """Récupère les données nettoyées depuis le bucket S3

    et retourne un DataFrame pandas prêt pour l'analyse.
    """
    # 1. Récupération dynamique du bucket et sécurisation du chemin
    bucket = os.getenv("S3_BUCKET", "paleo")
    chemin_s3 = f"{bucket}/donnees_strava/activites_clean.csv"

    # 2. Récupération et formatage de l'endpoint HTTPS pour s3fs
    endpoint = os.getenv("AWS_S3_ENDPOINT", "https://minio.lab.sspcloud.fr")
    if endpoint and not endpoint.startswith("http"):
        endpoint = f"https://{endpoint}"

    # 3. Configuration du système de fichiers S3
    fs = s3fs.S3FileSystem(
        client_kwargs={"endpoint_url": endpoint},
        key=os.getenv("AWS_ACCESS_KEY_ID"),
        secret=os.getenv("AWS_SECRET_ACCESS_KEY"),
        token=os.getenv("AWS_SESSION_TOKEN"),
    )

    # 4. Lecture directe du CSV distant
    with fs.open(chemin_s3, "rb") as f:
        df = pd.read_csv(f)

    return df


if __name__ == "__main__":
    df_strava = get_clean_data()
    print(f"Données chargées avec succès : {df_strava.shape[0]} lignes trouvées.")
