import os

import pandas as pd
import s3fs
from dotenv import load_dotenv

# Charge les variables d'environnement depuis le fichier .env à la racine
load_dotenv()


def get_clean_data() -> pd.DataFrame:
    """
    Récupère les données nettoyées depuis le bucket S3
    et retourne un DataFrame pandas prêt pour l'analyse.
    """
    # On ajoute le bucket "medas" au début du chemin
    chemin_s3 = "medas/paleo/donnees_strava/activites_clean.csv"

    # On récupère l'URL brute telle qu'elle est dans le fichier Kubernetes
    endpoint = os.getenv("AWS_S3_ENDPOINT")

    # Configuration du système de fichiers S3
    fs = s3fs.S3FileSystem(
        client_kwargs={"endpoint_url": endpoint},
        key=os.getenv("AWS_ACCESS_KEY_ID"),
        secret=os.getenv("AWS_SECRET_ACCESS_KEY"),
        token=os.getenv("AWS_SESSION_TOKEN"),
    )

    # Lecture directe du CSV distant
    with fs.open(chemin_s3, "rb") as f:
        df = pd.read_csv(f)

    return df


if __name__ == "__main__":
    # Test rapide de la fonction
    df_strava = get_clean_data()
    print(f"Données chargées avec succès : {df_strava.shape[0]} lignes trouvées.")
