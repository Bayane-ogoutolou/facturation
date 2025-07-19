import pandas as pd
import os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cartes_path = os.path.join(base_dir, "data", "CartesReduction.xlsx")

def verifier_carte(code_client):
    df = pd.read_excel(cartes_path)
    cartes_client = df[df['code_client'] == code_client]
    if not cartes_client.empty:
        return cartes_client.iloc[0]
    else:
        return None

def ajouter_carte_reduction(code_client, taux_reduction, numero_carte):
    df = pd.read_excel(cartes_path)
    nouvelle_carte = {
        'numero_carte': numero_carte,
        'code_client': code_client,
        'taux_reduction': taux_reduction
    }
    df = pd.concat([df, pd.DataFrame([nouvelle_carte])], ignore_index=True)
    df.to_excel(cartes_path, index=False)
    print(f"Carte de réduction créée pour le client {code_client} avec {taux_reduction}% de réduction.")
