#r : read
#w: wright a new one
#a : add at the then of the file
#r+ : read + wright
#b : for binary file eg. rb (read binary file)

import pandas as pd

contenu1 = pd.read_excel('../Clients.xlsx')
contenu2 = pd.read_excel('../Produits.xlsx')

produits = pd.DataFrame(contenu2)
clients = pd.DataFrame(contenu1)

print(clients, "\n\n\n", produits)

#clients (code_client, nom, contact, IFU)
#produits (code_produit, libelle, prix_unitaire)


