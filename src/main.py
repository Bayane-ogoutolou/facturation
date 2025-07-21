
from gestion_produits import ajouter_produit
from gestion_carte import creer_carte_reduction, get_taux_reduction_client
# src/main.py

import sys
from affichage import afficher_clients, afficher_produits, afficher_cartes
from gestion_produits import ajouter_produit
from facturation import generer_facture

def afficher_menu_principal():
    print("\n=== MENU PRINCIPAL ===")
    print("1. Consulter un fichier")
    print("2. Générer une facture")
    print("3. Ajouter un produit")
    print("4. Quitter")

def afficher_sous_menu_consultation():
    print("\n-- Consultation de fichiers --")
    print("a. Afficher les clients")
    print("b. Afficher les produits")
    print("c. Afficher les cartes de réduction")
    print("d. Retour")

def menu():
    while True:
        afficher_menu_principal()
        choix = input("Votre choix : ")

        if choix == '1':
            while True:
                afficher_sous_menu_consultation()
                sous_choix = input("Choisissez une option (a, b, c, d) : ")

                if sous_choix == 'a':
                    afficher_clients()
                elif sous_choix == 'b':
                    afficher_produits()
                elif sous_choix == 'c':
                    afficher_cartes()
                elif sous_choix == 'd':
                    break
                else:
                    print("Option invalide.")
        
        elif choix == '2':
           generer_facture()

        elif choix == '3':
            ajouter_produit()

        elif choix == '4':
            print("Merci d’avoir utilisé l’application. À bientôt !")
            sys.exit(0)

        else:
            print("Choix invalide. Veuillez réessayer.")

if __name__ == "__main__":
    menu()


#def generer_facture():
  

def afficher_menu():
    print("\n--- MENU PRINCIPAL ---")
    print("1. Consulter un fichier")
    print("2. Générer une facture")
    print("3. Ajouter un produit")
    print("4. Quitter")

def main():
    while True:
        afficher_menu()
        choix = input("Votre choix : ")

        if choix == "1":
            print(" Option non encore implémentée.")
        elif choix == "2":
            generer_facture()
        elif choix == "3":
            ajouter_produit()
        elif choix == "4":
            print(" Au revoir !")
            break
        else:
            print(" Choix invalide. Essayez encore.")

if __name__ == "__main__":
    main()
