""" import pandas as pd
import os

# Détermine le chemin vers data/
base_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(base_dir, "..", "data")
file_path = os.path.join(data_dir, "CartesReduction.xlsx")

# Crée un DataFrame vide avec les bonnes colonnes
df = pd.DataFrame(columns=["numero_carte", "code_client", "taux_reduction"])

# Enregistre le fichier
df.to_excel(file_path, index=False)

print("Fichier CartesReduction.xlsx créé avec succès.")
 """