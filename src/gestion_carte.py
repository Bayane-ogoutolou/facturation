import os
import pandas as pd
import time

# Récupère le chemin vers le fichier CartesReduction.xlsx
base_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(base_dir, "..", "data")
file_path = os.path.join(data_dir, "CartesReduction.xlsx")  # <- c’est ce chemin qu’on utilisera


def creer_carte_reduction(code_client, montant_facture):
    # Étape 1 : Chargement du fichier CartesReduction
    try:
        df = pd.read_excel(file_path)

    except FileNotFoundError:
        # S'il n'existe pas encore, on crée un DataFrame vide avec les bonnes colonnes
        df = pd.DataFrame(columns=["numero_carte", "code_client", "taux_reduction"])

    # Étape 2 : Vérifier si le client a déjà une carte
    if code_client in df["code_client"].values:
        print("Le client a déjà une carte de réduction.")
        return None  # Pas de création, il en a déjà une

    # Étape 3 : Vérifier les plages de montant pour attribuer une réduction
    if 50000 <= montant_facture <= 100000:
        taux = 5
    elif 100001 <= montant_facture <= 200000:
        taux = 10
    elif montant_facture > 200000:
        taux = 15
    else:
        print(" Montant insuffisant pour générer une carte.")
        return None

    # Étape 4 : Générer le numéro de carte (basé sur timestamp)
    numero_carte = f"C{int(time.time())}"

    # Étape 5 : Ajouter la carte au DataFrame
    nouvelle_carte = pd.DataFrame([{
        "numero_carte": numero_carte,
        "code_client": code_client,
        "taux_reduction": taux
    }])

    df = pd.concat([df, nouvelle_carte], ignore_index=True)

    # Étape 6 : Sauvegarder le fichier Excel
    df.to_excel(file_path, index=False)
    print("Carte créée avec succès (utilisable uniquement à partir de la prochaine facture).")

    # Ne pas retourner de taux ici, car cette carte NE DOIT PAS s'appliquer maintenant
    return None
#lire le fichier contenant les cartes, chercher la carte correspondant au code_client.
def get_taux_reduction_client(code_client: str) -> float:
    try:
        df = pd.read_excel(file_path)
    except FileNotFoundError:
        return 0.0

    carte = df[df["code_client"] == code_client]
    if carte.empty:
        return 0.0

    return float(carte.iloc[0]["taux_reduction"])


