import pandas as pd

def ajouter_client():
    print("\n--- Ajout d’un client ---")
    code_client = input("Code client (unique) : ")
    nom = input("Nom : ")
    contact = input("Contact : ")
    ifu = input("IFU (13 caractères) : ")

    if len(ifu) != 13:
        print("IFU invalide, doit faire 13 caractères.")
        return

    df = pd.read_excel("data/Clients.xlsx")
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
    df.to_excel("data/Clients.xlsx", index=False)
    print("Client ajouté avec succès.")

