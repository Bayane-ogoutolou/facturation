import pandas as pd

contenu1 = pd.read_excel("../Clients.xlsx")
contenu2 = pd.read_excel("../Produits.xlsx")

clients = pd.DataFrame(contenu1)
produits = pd.DataFrame(contenu2)

print(clients,"\n\n",produits)

