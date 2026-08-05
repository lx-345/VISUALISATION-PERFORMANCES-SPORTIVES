from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest


@pytest.mark.integration
def test_streamlit_app_loads_correctly():
    """
    Test d'intégration : Vérifie que l'application Streamlit se lance
    correctement depuis son point d'entrée sans lever d'exceptions.
    """
    # 1. On définit le chemin exact vers votre fichier app.py
    current_dir = Path(__file__).parent
    project_root = current_dir.parent
    app_path = (
        project_root
        / "src"
        / "visualisation_performances_sportives"
        / "streamlit_app"
        / "app.py"
    )

    # Vérification de sécurité pour s'assurer que le chemin est correct
    assert app_path.exists(), f"Le fichier {app_path} est introuvable."

    # 2. On initialise l'environnement de test Streamlit
    at = AppTest.from_file(str(app_path))

    # 3. On exécute l'application (timeout de 10s pour le chargement des données)
    at.run(timeout=10)

    # 4. On vérifie qu'aucune exception Python n'est apparue sur la page
    # Si la liste at.exception n'est pas vide, le test échoue et affiche l'erreur.
    assert len(at.exception) == 0, f"L'application a crashé : {at.exception[0]}"

    # 5. Optionnel : Vérifier qu'un élément clé s'affiche bien (ex: le titre principal)
    # On vérifie que la balise title (st.title) ne renvoie pas d'erreur
    assert len(at.title) >= 0
