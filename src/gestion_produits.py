# Gestion des produits
import os
import pandas as pd

# Récupère le chemin absolu du dossier où se trouve CE fichier
base_dir = os.path.dirname(os.path.abspath(__file__))

# Construit le chemin absolu du fichier Excel à partir de ce dossier
excel_path = os.path.join(base_dir, "..", "data", "Produits.xlsx")

# Lecture du fichier Excel
produits_df = pd.read_excel(excel_path)

# Fonction pour ajouter un produit
def ajouter_produit():
    while True:
        code = input("Entrez le code produit (commence par 'P') : ")
        if not code.startswith("P"):
            print(" Le code produit doit commencer par la lettre 'P'.")
            continue
        break

    while True:
        libelle = input("Entrez le libelle du produit : ")
        if libelle.strip() == "":
            print("Le libellé ne peut pas être vide.")
            continue
        break

    while True:
        try:
            prix = float(input("Entrez le prix du produit : "))  
            break
        except ValueError:
            print("Le prix doit être un nombre.")

    try:
        df = pd.read_excel(excel_path)
    except FileNotFoundError:
        # Si le fichier n'existe pas encore, on crée un DataFrame vide
        df = pd.DataFrame(columns=["code_produit", "libelle", "prix_unitaire"])

    # Vérifier si le code produit existe déjà
    if code in df["code_produit"].values:
        print(" Ce code produit existe déjà.")
        return

    # Ajouter la nouvelle ligne
    nouvelle_ligne = pd.DataFrame([{
        "code_produit": code,
        "libelle": libelle,
        "prix_unitaire": prix
    }])
    df = pd.concat([df, nouvelle_ligne], ignore_index=True)

    # Réécriture du fichier Excel
    df.to_excel(excel_path, index=False)
    print(" Produit ajouté avec succès.")


""" # Gestion des produits
import os
import pandas as pd

# Récupère le chemin absolu du dossier où se trouve CE fichier
base_dir = os.path.dirname(os.path.abspath(__file__))

# Construit le chemin absolu du fichier Excel à partir de ce dossier
excel_path = os.path.join(base_dir, "..", "data", "Produits.xlsx")

# Lecture du fichier Excel
produits_df = pd.read_excel(excel_path)

# Fonction pour ajouter un produit
def ajouter_produit():
    code = input("Entrez le code produit (commence par 'P') : ")
    # Vérifier que le code du produit commence effectivement par "P"
    if not code.startswith("P"):
        print(" Le code produit doit commencer par la lettre 'P'.")
        return

    libelle = input("Entrez le libelle du produit : ")
    try:
        prix = float(input("Entrez le prix du produit : "))  
    except ValueError:
        print("Le prix doit être un nombre.")
        return 

    try:
        df = pd.read_excel(excel_path)
    except FileNotFoundError:
        # Si le fichier n'existe pas encore, on crée un DataFrame vide
        df = pd.DataFrame(columns=["code_produit", "libelle", "prix_unitaire"])

    # Vérifier si le code produit existe déjà
    if code in df["code_produit"].values:
        print(" Ce code produit existe déjà.")
        return

    # Ajouter la nouvelle ligne
    nouvelle_ligne = pd.DataFrame([{
        "code_produit": code,
        "libelle": libelle,
        "prix_unitaire": prix
    }])
    df = pd.concat([df, nouvelle_ligne], ignore_index=True)

    # Réécriture du fichier Excel
    df.to_excel(excel_path, index=False)
    print(" Produit ajouté avec succès.")


 """