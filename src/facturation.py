import pandas as pd
from gestion_clients import ajouter_client
from gestion_cartes import verifier_carte, ajouter_carte_reduction
from fpdf import FPDF
from datetime import datetime
import os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
produits_path = os.path.join(base_dir, "data", "Produits.xlsx")

def generer_facture():
    print("\n--- Génération de facture ---")
    type_client = input("Nouveau client (n) ou existant (e) ? ").lower()

    if type_client == 'n':
        ajouter_client()
    code_client = input("Entrez le code client : ")

    df_produits = pd.read_excel(produits_path)
    lignes_facture = []
    total_ht = 0

    while True:
        code_prod = input("Code produit (ou 'fin' pour terminer) : ")
        if code_prod.lower() == 'fin':
            break

        if code_prod not in df_produits['code_produit'].values:
            print("Code produit invalide.")
            continue

        try:
            quantite = int(input("Quantité : "))
        except ValueError:
            print("Quantité invalide.")
            continue

        produit = df_produits[df_produits['code_produit'] == code_prod].iloc[0]
        prix_unitaire = produit['prix_unitaire']
        total_ligne = prix_unitaire * quantite
        total_ht += total_ligne

        lignes_facture.append({
            'code_produit': code_prod,
            'libelle': produit['libelle'],
            'quantite': quantite,
            'prix_unitaire': prix_unitaire,
            'total_ligne': total_ligne
        })

    carte = verifier_carte(code_client)
    taux_reduction = 0
    if carte is not None:
        taux_reduction = carte['taux_reduction']

    montant_remise = total_ht * taux_reduction / 100
    total_apres_remise = total_ht - montant_remise
    tva = total_apres_remise * 0.18
    total_ttc = total_apres_remise + tva

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(0, 10, "Facture", ln=True, align="C")
    pdf.cell(0, 10, f"Client : {code_client}", ln=True)
    pdf.cell(0, 10, f"Date : {datetime.now().strftime('%d/%m/%Y')}", ln=True)
    pdf.ln(10)

    for ligne in lignes_facture:
        pdf.cell(0, 10, f"{ligne['libelle']} x {ligne['quantite']} = {ligne['total_ligne']} FCFA", ln=True)

    pdf.ln(5)
    pdf.cell(0, 10, f"Total HT : {total_ht} FCFA", ln=True)
    pdf.cell(0, 10, f"Remise : {montant_remise} FCFA", ln=True)
    pdf.cell(0, 10, f"TVA (18%) : {tva} FCFA", ln=True)
    pdf.cell(0, 10, f"Total TTC : {total_ttc} FCFA", ln=True)

    if not os.path.exists("factures"):
        os.mkdir("factures")

    num_facture = datetime.now().strftime("%Y%m%d%H%M%S")
    nom_pdf = f"factures/Facture_{num_facture}.pdf"
    pdf.output(nom_pdf)
    print(f"Facture générée : {nom_pdf}")
