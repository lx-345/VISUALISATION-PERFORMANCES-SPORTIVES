import os

import pandas as pd
import s3fs
from dotenv import load_dotenv

load_dotenv()


def get_clean_data() -> pd.DataFrame:
    """Récupère les données nettoyées depuis le bucket S3

    et retourne un DataFrame pandas prêt pour l'analyse.
    """
    # 1. Récupération dynamique du bucket et du chemin
    bucket = os.getenv("S3_BUCKET", "paleo")
    chemin_s3 = f"{bucket}/donnees_strava/activites_clean.csv"

    # 2. Formatage sécurisé de l'endpoint (HTTP par défaut pour le cluster)
    endpoint = os.getenv("AWS_S3_ENDPOINT", "http://minio-medas-usid0f:9000")
    if not endpoint.startswith("http://") and not endpoint.startswith("https://"):
        endpoint = f"http://{endpoint}"

    # 3. Configuration du système de fichiers S3
    fs = s3fs.S3FileSystem(
        client_kwargs={"endpoint_url": endpoint},
        key=os.getenv("AWS_ACCESS_KEY_ID"),
        secret=os.getenv("AWS_SECRET_ACCESS_KEY"),
        token=os.getenv("AWS_SESSION_TOKEN"),
    )

    # 4. Lecture directe du CSV distant
    with fs.open(chemin_s3, "rb") as f:
        return pd.read_csv(f)


if __name__ == "__main__":
    df_strava = get_clean_data()
    print(f"Données chargées avec succès : {df_strava.shape[0]} lignes trouvées.")
