#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module de facturation
Gère la création de factures, les calculs et les cartes de réduction
"""

import re
from datetime import datetime
from modules.gestion_fichiers import GestionFichiers

class Facturation:
    """Classe pour gérer la facturation"""
    
    def __init__(self):
        self.gestion_fichiers = GestionFichiers()
        self.taux_tva = 0.18  # 18% de TVA
        self.numero_facture_compteur = 1
        
        # Définition des plages de remise (à personnaliser)
        self.plages_remise = [
            {'min': 100000, 'max': 200000, 'taux': 5},    # 5% pour 100k-200k
            {'min': 200001, 'max': 500000, 'taux': 10},   # 10% pour 200k-500k
            {'min': 500001, 'max': float('inf'), 'taux': 15}  # 15% pour >500k
        ]
    
    def generer_numero_facture(self):
        """Génère un numéro de facture unique"""
        numero = f"FAC{self.numero_facture_compteur:06d}"
        self.numero_facture_compteur += 1
        return numero
    
    def valider_ifu(self, ifu):
        """Valide le format de l'IFU (13 caractères)"""
        return len(ifu) == 13 and ifu.isdigit()
    
    def valider_contact(self, contact):
        """Valide le format du contact (8 chiffres minimum)"""
        return len(contact) >= 8 and contact.isdigit()
    
    def saisir_nouveau_client(self):
        """Saisit les informations d'un nouveau client"""
        print("\n📝 SAISIE D'UN NOUVEAU CLIENT")
        print("-" * 40)
        
        try:
            # Générer automatiquement le code client
            code_client = self.gestion_fichiers.generer_prochain_code_client()
            print(f"Code client généré: {code_client}")
            
            # Saisir le nom
            while True:
                nom = input("Nom du client: ").strip()
                if nom:
                    break
                print("❌ Le nom ne peut pas être vide.")
            
            # Saisir le contact
            while True:
                contact = input("Contact (numéro de téléphone): ").strip()
                if self.valider_contact(contact):
                    break
                print("❌ Contact invalide. Minimum 8 chiffres.")
            
            # Saisir l'IFU
            while True:
                ifu = input("IFU (13 caractères): ").strip()
                if self.valider_ifu(ifu):
                    break
                print("❌ IFU invalide. Doit contenir exactement 13 chiffres.")
            
            client_info = {
                'code_client': code_client,
                'nom': nom,
                'contact': contact,
                'IFU': ifu
            }
            
            print(f"✅ Client {nom} enregistré avec le code {code_client}")
            return client_info
            
        except Exception as e:
            print(f"❌ Erreur lors de la saisie du client: {e}")
            return None
    
    def selectionner_client_existant(self):
        """Permet de sélectionner un client existant"""
        print("\n🔍 SÉLECTION D'UN CLIENT EXISTANT")
        print("-" * 40)
        
        # Afficher la liste des clients
        self.gestion_fichiers.afficher_clients()
        
        while True:
            code_client = input("\nEntrez le code du client: ").strip().upper()
            
            if not code_client:
                print("❌ Le code client ne peut pas être vide.")
                continue
            
            client_info = self.gestion_fichiers.obtenir_client_par_code(code_client)
            
            if client_info:
                print(f"✅ Client sélectionné: {client_info['nom']}")
                return client_info
            else:
                print("❌ Client non trouvé.")
                retry = input("Voulez-vous essayer à nouveau? (o/n): ").lower().strip()
                if retry != 'o':
                    return None
    
    def saisir_produits_facture(self):
        """Saisit les produits pour une facture"""
        print("\n🛒 SAISIE DES PRODUITS")
        print("-" * 40)
        
        # Afficher la liste des produits disponibles
        self.gestion_fichiers.afficher_produits()
        
        produits_facture = []
        
        while True:
            print(f"\nProduit n°{len(produits_facture) + 1}")
            
            # Saisir le code produit
            while True:
                code_produit = input("Code produit: ").strip().upper()
                
                if not code_produit:
                    print("❌ Le code produit ne peut pas être vide.")
                    continue
                
                produit_info = self.gestion_fichiers.obtenir_produit_par_code(code_produit)
                
                if produit_info:
                    break
                else:
                    print("❌ Produit non trouvé.")
                    print("Produits disponibles:")
                    for _, prod in self.gestion_fichiers.df_produits.iterrows():
                        print(f"  {prod['code_produit']} - {prod['libelle']}")
            
            # Saisir la quantité
            while True:
                try:
                    quantite = int(input("Quantité: "))
                    if quantite > 0:
                        break
                    else:
                        print("❌ La quantité doit être positive.")
                except ValueError:
                    print("❌ Veuillez entrer un nombre entier.")
            
            # Ajouter le produit à la facture
            produit_facture = {
                'code_produit': code_produit,
                'libelle': produit_info['libelle'],
                'prix_unitaire': produit_info['prix_unitaire'],
                'quantite': quantite,
                'total_ht': produit_info['prix_unitaire'] * quantite
            }
            
            produits_facture.append(produit_facture)
            
            print(f"✅ Produit ajouté: {produit_info['libelle']} x{quantite}")
            
            # Demander s'il y a d'autres produits
            continuer = input("Ajouter un autre produit? (o/n): ").lower().strip()
            if continuer != 'o':
                break
        
        return produits_facture
    
    def calculer_facture(self, client_info, produits_facture):
        """Calcule le montant total de la facture"""
        print("\n💰 CALCUL DE LA FACTURE")
        print("-" * 40)
        
        # Calculer le total HT
        total_ht = sum(produit['total_ht'] for produit in produits_facture)
        
        # Vérifier si le client a une carte de réduction
        carte_reduction = self.gestion_fichiers.obtenir_carte_par_client(client_info['code_client'])
        
        taux_reduction = 0
        montant_reduction = 0
        
        if carte_reduction:
            taux_reduction = carte_reduction['taux_reduction']
            montant_reduction = total_ht * (taux_reduction / 100)
            print(f"🎫 Carte de réduction appliquée: {taux_reduction}%")
        
        # Calculer le total HT après réduction
        total_ht_apres_reduction = total_ht - montant_reduction
        
        # Calculer la TVA
        montant_tva = total_ht_apres_reduction * self.taux_tva
        
        # Calculer le total TTC
        total_ttc = total_ht_apres_reduction + montant_tva
        
        # Créer la facture
        facture = {
            'numero_facture': self.generer_numero_facture(),
            'date_emission': datetime.now().strftime("%d/%m/%Y"),
            'client': client_info,
            'produits': produits_facture,
            'total_ht': total_ht,
            'taux_reduction': taux_reduction,
            'montant_reduction': montant_reduction,
            'total_ht_apres_reduction': total_ht_apres_reduction,
            'taux_tva': self.taux_tva * 100,  # Convertir en pourcentage
            'montant_tva': montant_tva,
            'total_ttc': total_ttc
        }
        
        # Afficher un résumé
        print(f"Total HT: {total_ht:,.0f} FCFA")
        if montant_reduction > 0:
            print(f"Réduction ({taux_reduction}%): -{montant_reduction:,.0f} FCFA")
            print(f"Total HT après réduction: {total_ht_apres_reduction:,.0f} FCFA")
        print(f"TVA ({self.taux_tva*100}%): {montant_tva:,.0f} FCFA")
        print(f"Total TTC: {total_ttc:,.0f} FCFA")
        
        return facture
    
    def verifier_creation_carte_reduction(self, client_info, facture):
        """Vérifie si une carte de réduction doit être créée"""
        code_client = client_info['code_client']
        
        # Vérifier si le client a déjà une carte
        if self.gestion_fichiers.client_a_carte_reduction(code_client):
            return
        
        # Vérifier si le montant justifie une carte de réduction
        total_ttc = facture['total_ttc']
        
        for plage in self.plages_remise:
            if plage['min'] <= total_ttc <= plage['max']:
                # Créer la carte de réduction
                numero_carte = self.generer_numero_carte()
                
                carte_info = {
                    'numero_carte': numero_carte,
                    'code_client': code_client,
                    'taux_reduction': plage['taux']
                }
                
                self.gestion_fichiers.ajouter_carte_reduction(carte_info)
                
                print(f"\n🎫 CARTE DE RÉDUCTION CRÉÉE")
                print(f"Numéro: {numero_carte}")
                print(f"Taux de réduction: {plage['taux']}%")
                print("Cette carte sera applicable aux prochaines factures.")
                break
    
    def generer_numero_carte(self):
        """Génère un numéro de carte de réduction unique"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"CARD{timestamp}"
    
    def saisir_nouveau_produit(self):
        """Saisit les informations d'un nouveau produit"""
        print("\n📦 AJOUT D'UN NOUVEAU PRODUIT")
        print("-" * 40)
        
        try:
            # Générer automatiquement le code produit
            code_produit = self.gestion_fichiers.generer_prochain_code_produit()
            print(f"Code produit généré: {code_produit}")
            
            # Saisir le libellé
            while True:
                libelle = input("Libellé du produit: ").strip()
                if libelle:
                    break
                print("❌ Le libellé ne peut pas être vide.")
            
            # Saisir le prix unitaire
            while True:
                try:
                    prix_unitaire = float(input("Prix unitaire (FCFA): "))
                    if prix_unitaire > 0:
                        break
                    else:
                        print("❌ Le prix doit être positif.")
                except ValueError:
                    print("❌ Veuillez entrer un nombre valide.")
            
            produit_info = {
                'code_produit': code_produit,
                'libelle': libelle,
                'prix_unitaire': prix_unitaire
            }
            
            print(f"✅ Produit {libelle} ajouté avec le code {code_produit}")
            return produit_info
            
        except Exception as e:
            print(f"❌ Erreur lors de la saisie du produit: {e}")
            return None
    
    def convertir_nombre_en_lettres(self, nombre):
        """Convertit un nombre en lettres (version simplifiée)"""
        # Version simplifiée - peut être étendue pour une conversion complète
        if nombre < 1000:
            return f"{nombre:.0f}"
        elif nombre < 1000000:
            return f"{nombre/1000:.0f} mille"
        elif nombre < 1000000000:
            return f"{nombre/1000000:.0f} millions"
        else:
            return f"{nombre/1000000000:.0f} milliards"

# Test du module
if __name__ == "__main__":
    facturation = Facturation()
    
    print("Test du module de facturation:")
    print("Plages de remise configurées:")
    for i, plage in enumerate(facturation.plages_remise, 1):
        print(f"{i}. {plage['min']:,} - {plage['max']:,} FCFA: {plage['taux']}%")