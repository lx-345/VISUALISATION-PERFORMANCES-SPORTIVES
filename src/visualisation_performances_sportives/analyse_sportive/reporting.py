from openpyxl import Workbook
from .data import get_clean_data
from .backend import construire_onglets_back
from .analyse import construire_page_analyse
from .bilan import construire_page_bilan
from .charge import construire_page_charge

def generer_reporting_excel(chemin_sortie: str = "Tableau_Bord_Performances.xlsx"):
    """
    Télécharge les données et orchestre la génération complète du tableau de bord Excel.
    """
    print("1. Téléchargement des données depuis le bucket S3...")
    df = get_clean_data()
    
    max_data_row = len(df) + 1
    trimestres_uniques = sorted(df['trimestre'].dropna().unique().astype(str).tolist()) if 'trimestre' in df.columns else []
    
    print("2. Création du classeur Excel...")
    wb = Workbook()
    
    print("   - Construction du Backend...")
    len_y, len_t = construire_onglets_back(wb, df)
    
    print("   - Construction de la page Analyse...")
    construire_page_analyse(wb, max_data_row, len_y, len_t, len_d=5, max_pivot=10)
    
    print("   - Construction de la page Bilan...")
    construire_page_bilan(wb, max_data_row, len_y, len_s=4, len_n=3)
    
    print("   - Construction de la page Charge de travail...")
    construire_page_charge(wb, max_data_row, len_y, len_t, len_d=5)
    
    # Suppression de la feuille par défaut d'openpyxl
    if "Sheet" in wb.sheetnames:
        del wb["Sheet"]
        
    print(f"3. Sauvegarde du fichier sous '{chemin_sortie}'...")
    wb.save(chemin_sortie)
    print("Génération terminée avec succès !")

if __name__ == "__main__":
    generer_reporting_excel()