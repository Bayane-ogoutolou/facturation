import pandas as pd

def ajouter_produit():
    print("\n--- Ajout d’un produit ---")
    code = input("Code produit (4 caractères) : ")
    if len(code) != 4:
        print("Le code produit doit contenir exactement 6 caractères.")
        return

    libelle = input("Libellé : ")
    try:
        prix = float(input("Prix unitaire : "))
    except ValueError:
        print("Prix invalide.")
        return

    try:
        df = pd.read_excel("data/Produits.xlsx")
    except FileNotFoundError:
        print("Erreur : fichier Produits.xlsx non trouvé.")
        return
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier : {e}")
        return

    if code in df['code_produit'].values:
        print("Ce code produit existe déjà.")
        return

    nouveau_produit = {
        'code_produit': code,
        'libelle': libelle,
        'prix_unitaire': prix
    }

    df = pd.concat([df, pd.DataFrame([nouveau_produit])], ignore_index=True)

    try:
        df.to_excel("data/Produits.xlsx", index=False)
        print("Produit ajouté avec succès.")
    except Exception as e:
        print(f"Erreur lors de l’écriture du fichier : {e}")
