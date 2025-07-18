# facturation_app/src/affichage.py

import pandas as pd
from utils import clear_screen

def afficher_clients():
    """
    Affiche la liste des clients depuis le fichier Clients.xlsx
    """
    try:
        df = pd.read_excel('../data/Clients.xlsx')
        clear_screen()
        print("\n=== LISTE DES CLIENTS ===")
        print(df.to_string(index=False))
        input("\nAppuyez sur Entrée pour continuer...")
    except FileNotFoundError:
        print("Erreur: Fichier Clients.xlsx introuvable.")
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier: {e}")

def afficher_produits():
    """
    Affiche la liste des produits depuis le fichier Produits.xlsx
    """
    try:
        df = pd.read_excel('../data/Produits.xlsx')
        clear_screen()
        print("\n=== LISTE DES PRODUITS ===")
        print(df.to_string(index=False))
        input("\nAppuyez sur Entrée pour continuer...")
    except FileNotFoundError:
        print("Erreur: Fichier Produits.xlsx introuvable.")
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier: {e}")

def afficher_cartes_reduction():
    """
    Affiche la liste des cartes de réduction depuis le fichier CartesReduction.xlsx
    """
    try:
        df = pd.read_excel('../data/CartesReduction.xlsx')
        clear_screen()
        print("\n=== LISTE DES CARTES DE RÉDUCTION ===")
        print(df.to_string(index=False))
        input("\nAppuyez sur Entrée pour continuer...")
    except FileNotFoundError:
        print("Erreur: Fichier CartesReduction.xlsx introuvable.")
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier: {e}")

def menu_affichage():
    """
    Sous-menu pour l'affichage des données
    """
    while True:
        clear_screen()
        print("""
=== MENU AFFICHAGE ===
1. Afficher les clients
2. Afficher les produits
3. Afficher les cartes de réduction
4. Retour au menu principal
        """)
        
        choix = input("Votre choix (1-4): ")
        
        if choix == '1':
            afficher_clients()
        elif choix == '2':
            afficher_produits()
        elif choix == '3':
            afficher_cartes_reduction()
        elif choix == '4':
            break
        else:
            print("Choix invalide. Veuillez saisir un nombre entre 1 et 4.")
            input("Appuyez sur Entrée pour continuer...")