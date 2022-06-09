import drivers.write_mifare as wr

print("Bienvenue dans le menu de création de carte")
print("Appuyer sur le bouton pour créer une nouvelle carte")
nom = input("Ecrivez le nom de la personne : ")
prenom = input("Ecrivez le prenom de la personne : ")
access = "init"
i = 0
while i == 0:
    if access == "total" or access == "restricted" or access == "none":
        i = 1
    else:
        access = input("Ecrivez l'accès que possederas cette personne (total, restricted ou none) : ")

print("Bienvenue " + prenom)

wr.readCard()
wr.createNewCard(nom,prenom,access)

