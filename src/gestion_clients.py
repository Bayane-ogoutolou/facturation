import pandas as pd
import os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
clients_path = os.path.join(base_dir, "data", "Clients.xlsx")

def ajouter_client():
    print("\n--- Ajout d’un client ---")
    code_client = input("Code client (unique) : ")
    nom = input("Nom : ")
    contact = input("Contact : ")
    ifu = input("IFU (13 caractères) : ")

    if len(ifu) != 13:
        print("IFU invalide, doit faire 13 caractères.")
        return

    df = pd.read_excel(clients_path)
    if code_client in df['code_client'].values:
        print("Ce code client existe déjà.")
        return

    nouveau_client = {
        'code_client': code_client,
        'nom': nom,
        'contact': contact,
        'IFU': ifu
    }

    df = pd.concat([df, pd.DataFrame([nouveau_client])], ignore_index=True)
    df.to_excel(clients_path, index=False)
    print("Client ajouté avec succès.")
