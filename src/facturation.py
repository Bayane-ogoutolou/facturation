import pandas as pd
from gestion_clients import ajouter_client
from gestion_cartes import verifier_carte
from gestion_carte import creer_carte_reduction
from fpdf import FPDF
from datetime import datetime
import os
from num2words import num2words  # Pour convertir montant en lettres

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

    # Récupérer taux de réduction applicable
    taux_reduction = 0
    carte = verifier_carte(code_client)
    if carte is not None:
        taux_reduction = carte['taux_reduction']

    montant_remise = total_ht * taux_reduction / 100
    total_apres_remise = total_ht - montant_remise  # <- ceci est THT Remise
    tva = total_apres_remise * 0.18
    total_ttc = total_apres_remise + tva


    # Si aucune carte, créer potentiellement une nouvelle carte si conditions remplies
    if taux_reduction == 0:
        creer_carte_reduction(code_client, total_ht)

    # Générer un numéro de facture unique
    num_facture = datetime.now().strftime("%Y%m%d%H%M%S")

    # Lecture infos client pour afficher (tu peux adapter selon ta structure)
    df_clients = pd.read_excel(os.path.join(base_dir, "data", "Clients.xlsx"))
    client_info = df_clients[df_clients['code_client'] == code_client].iloc[0]
    nom_client = client_info['nom']
    contact_client = client_info['contact']
    ifu_client = client_info.get('IFU', '')

    # Génération PDF
    pdf = FPDF()
    pdf.add_page()

    # En-tête : gauche nom groupe, droite date
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Groupe Étudiant XYZ", 0, 0, 'L')  # À adapter au nom réel
    pdf.cell(0, 10, f"Date : {datetime.now().strftime('%d/%m/%Y')}", 0, 1, 'R')

    pdf.ln(3)

    # Infos client en dessous
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 6, f"Client : {nom_client} (Code: {code_client})", ln=True)
    pdf.cell(0, 6, f"Contact : {contact_client}", ln=True)
    pdf.cell(0, 6, f"IFU : {ifu_client}", ln=True)

    pdf.ln(10)

    # Titre centré FACTURE n° XXXXXX
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, f"FACTURE n° {num_facture}", ln=True, align="C")

    pdf.ln(10)

    # Lignes de produits
    pdf.set_font("Arial", size=12)
    for ligne in lignes_facture:
        pdf.cell(0, 10, f"{ligne['libelle']} x {ligne['quantite']} = {ligne['total_ligne']:.2f} FCFA", ln=True)

    pdf.ln(5)
    pdf.cell(0, 10, f"Total HT : {total_ht:.2f} FCFA", ln=True)
    pdf.cell(0, 10, f"Remise ({taux_reduction}%) : -{montant_remise:.2f} FCFA", ln=True)
    pdf.cell(0, 10, f"THT Remise : {total_apres_remise:.2f} FCFA", ln=True)  # << AJOUTÉ ICI
    pdf.cell(0, 10, f"TVA (18%) : {tva:.2f} FCFA", ln=True)
    pdf.cell(0, 10, f"Total TTC : {total_ttc:.2f} FCFA", ln=True)


    pdf.ln(15)

   # Bas de page (en bas de la page)
    montant_en_lettres = num2words(int(round(total_ttc)), lang='fr').capitalize()
    pdf.set_y(-30)  # Positionne 30mm avant le bas de page
    pdf.set_font("Arial", 'I', 12)
    pdf.cell(0, 10, f"Arrêtée, la présente facture à la somme de : {montant_en_lettres} francs CFA.", 0, 0, 'C')


    # Création dossier si nécessaire
    if not os.path.exists("factures"):
        os.mkdir("factures")

    nom_pdf = f"factures/Facture_{num_facture}.pdf"
    pdf.output(nom_pdf)

    print(f"Facture générée : {nom_pdf}")
    print(f"Montant total TTC à payer : {total_ttc:.2f} FCFA")
