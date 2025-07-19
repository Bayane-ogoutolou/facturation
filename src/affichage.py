import pandas as pd
import os

# chemin absolu vers le dossier racine (facturation)
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_dir = os.path.join(base_dir, "data")

def afficher_clients():
    fichier_clients = os.path.join(data_dir, "Clients.xlsx")
    df = pd.read_excel(fichier_clients)
    print("\n--- Liste des Clients ---")
    print(df)

def afficher_produits():
    fichier_produits = os.path.join(data_dir, "Produits.xlsx")
    df = pd.read_excel(fichier_produits)
    print("\n--- Liste des Produits ---")
    print(df)

def afficher_cartes():
    fichier_cartes = os.path.join(data_dir, "CartesReduction.xlsx")
    df = pd.read_excel(fichier_cartes)
    print("\n--- Cartes de Réduction ---")
    print(df)
