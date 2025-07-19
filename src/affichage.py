import pandas as pd

def afficher_clients():
    df = pd.read_excel("data/Clients.xlsx")
    print("\n--- Liste des Clients ---")
    print(df)

def afficher_produits():
    df = pd.read_excel("data/Produits.xlsx")
    print("\n--- Liste des Produits ---")
    print(df)

def afficher_cartes():
    df = pd.read_excel("data/CartesReduction.xlsx")
    print("\n--- Cartes de Réduction ---")
    print(df)
