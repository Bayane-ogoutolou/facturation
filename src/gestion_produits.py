import pandas as pd

def ajouter_produit():
    print("\n--- Ajout d’un produit ---")
    code = input("Code produit (6 caractères) : ")
    libelle = input("Libellé : ")
    try:
        prix = float(input("Prix unitaire : "))
    except ValueError:
        print("Prix invalide.")
        return

    df = pd.read_excel("data/Produits.xlsx")
    if code in df['code_produit'].values:
        print("Ce code produit existe déjà.")
        return

    nouveau_produit = {
        'code_produit': code,
        'libelle': libelle,
        'prix_unitaire': prix
    }

    df = pd.concat([df, pd.DataFrame([nouveau_produit])], ignore_index=True)
    df.to_excel("data/Produits.xlsx", index=False)
    print("Produit ajouté avec succès.")
