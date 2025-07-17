from gestion_produits import ajouter_produit
from gestion_carte import creer_carte_reduction, get_taux_reduction_client

def generer_facture():
    code_client = input("Code client : ")
    try:
        montant = float(input("Montant total de la facture : "))
    except ValueError:
        print("Montant invalide.")
        return

    taux = get_taux_reduction_client(code_client)

    if taux == 0:
        print("Aucune réduction appliquée (1re facture).")
        print(f"Total à payer : {montant:.2f} FCFA")
        creer_carte_reduction(code_client, montant)
    else:
        reduction = montant * (taux / 100)
        total = montant - reduction
        print(f"Réduction de {taux}% appliquée ({reduction:.2f} FCFA)")
        print(f"Total à payer : {total:.2f} FCFA")

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
