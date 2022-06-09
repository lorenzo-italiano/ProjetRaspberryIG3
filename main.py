# On importe le driver LCD afin de pouvoir indiquer a l'utilisateur le début et la fin du chargement et montrer
# que le dispositif est bien allumé
from drivers.LCD import *
# On allume l'écran en mettant le fond blanc
setWhite()
setText("Chargement")

################################################### IMPORTS DE FICHIERS #############################################################

# On importe tous les drivers / bibliothèques dont nous avons besoins dans le programme
from drivers.button import *
from drivers.pn532.pn532 import *
from drivers.read_mifare import *
from drivers.write_mifare import *
from drivers.grove_ultrasonic import *
from drivers.LED import *
from os import *
import sys
from threading import *
from signal import *
from drivers.grovepi import *
from time import *
import re
#from picamera import PiCamera
#camera = PiCamera()
import requests

################################################### FONCTIONS DU MAIN ########################################################

# Fonction pour selectionner la valeur de base des capteurs a ultrason (ex : 200 si l'objet le plus proche est a 2m), pour cela on
# selectionne la valeur la plus réccurrente parmis 30 essais, car le capteur n'est pas précis et effectue des sauts tous les 
# 4 ou 5 captages en moyenne. Prend en paramètre le pin sur lequel se trouve le capteur ultrason (7 ou 8)

def selectValeurBase(pinEntree):
	tab = []
	for i in range(30):
		tab.append(ultrasonic(pinEntree))
		sleep(0.1)
	#print(tab)
	#print(getUniqueValueTab(tab))
	dico = {}
	for i in getUniqueValueTab(tab):
		dico.setdefault(i, getNBOccurences(tab,i))
	#print(dico)
	max = 0
	indexmax = 0
	for i in dico:
		if max < dico.get(i):
			max = dico.get(i)
			indexmax = i
	#print(max)
	return indexmax

# Sert a récuperer le nombre d'occurence du parametre nb dans le tableau tab passé en paramètre

def getNBOccurences(tab,nb):
	compteur = 0
	for i in tab:
		if i == nb:
			compteur += 1
	return compteur

# Renvoie un tableau sans doublons sur les valeurs contenues dans celui-ci

def getUniqueValueTab(tab):
	tableau = []
	for i in tab:
		if i not in tableau:
			tableau.append(i)
	return tableau

# Prend une photo, en nommant l'image selon le numéro actuel de photo (voir dans le fichier imagenb)
# ecrit la valeur actuelle + 1 dans le fichier imagenb pour que la prochaine photo ait son nom unique

def prendrePhoto():
	with open("imagenb",'r') as file:
    	data = file.read()

	name = "image" + data + ".jpg"

	#camera.start_preview()
	#sleep(0.1)
	#camera.capture(name)
	#camera.stop_preview()

	with open("imagenb",'w') as file:
    	file.write(str(int(data)+1))
	return name

# Crée une nouvelle session en ajoutant + 1 au numéro de la session dans le fichier sessionnb afin de passer a la session suivante

def newSession():
	with open("sessionnb",'r') as file:
    	data = file.read()
	with open("sessionnb",'w') as file:
    	file.write(str(int(data)+1))

# Réccupère dans le fichier sessionnb le numéro courrant de la session et le retourne

def getNbSession():
	with open("sessionnb",'r') as file:
    	nbSession = int(file.read())
	return nbSession

# Renvoie la date actuelle (heure:minute:seconde)

def getCurrentTime():
	t = localtime()
	current_time = strftime("%H:%M:%S", t)
	return current_time

# Permet d'envoyer les informations actuelles vers le google sheet contenant toutes les informations en temps réel et 
# traçant des graphiques automatiques

def sendInfos(session,date,nbPersonne,image):
	idform = "1I0Hu22776JB3CvGPM9Q2fhkcts4K9fhkelXTxehLlhE"
	session = "entry.1318486255"
	date = "entry.789742660"
	nbPersonne = "entry.893312314"
	image = "entry.1189917965"

	str = "https://docs.google.com/forms/d/" + idform +"/formResponse?ifq&" + session +"=" + str(session) + "&" + date +"=" + str(date) + "&" + nbPersonne + "=" + str(nbPersonne) + "&" + image + "=" + str(image) + "&submit=Submit"

	requests.post(str)

##################################################INITIALISATION DES VARIABLES########################################################

# On crée une nouvelle session
newSession()

# On initialise quelques variables

nbPersonne = 0

pinEntree = 7
pinSortie = 8

valeurBaseCapteurEntree = selectValeurBase(7)
valeurBaseCapteurSortie = selectValeurBase(8)

dejacapteentre = False
dejacaptesortie = False

# Chargement terminé, on l'affiche sur l'écran
setText("Chargement\ntermine !")
#print("chargé")

############################################### PROGRAMME PRINCIPAL ##################################################################

# On crée un thread pour la lecture de carte car c'est une fonction bloquante
x = Thread(target=readCardOnLoop)
# On le paramètre de façon a ce que lorsque ce programme se ferme le Thread est kill également
x.daemon = True
# On lance le thread
x.start()
# C'est ici que le runner commence :
while (True):
	# On detecte si quelqu'un appuie sur le bouton, auquel cas on éteint le dispositif jusqu'à que quelqu'un réappuie sur le bouton
	# (ce second appui sera capté par le fichier launcher que nous lançons)
	if(readButton(2)==1):
		newpid = fork()
		if newpid == 0:
			system('python3 launcher.py')
			break
		else:
			sys.exit()
			break
	else:
		# Si le bouton n'a pas été pressé, alors on detecte ce qu'il se passe au niveau des capteurs ultrasons pour voir s'il y a des passages
		dist = ultrasonic(pinEntree) 
		if(dist < (valeurBaseCapteurEntree-30) and dejacapteentre==False): 
			if (ultrasonic(pinEntree) < (valeurBaseCapteurEntree-30)):
				if(ultrasonic(pinEntree) < (valeurBaseCapteurEntree-30)):
					nbPersonne += 1
					dejacapteentre = True
					writeNb(nbPersonne)
					image = prendrePhoto()
					session = getNbSession()
					time = getCurrentTime()
					# On envoie les infos au google sheet
					sendInfos(session,time,nbPersonne,image)
					# On bloque avec un sleep pour ne pas activer le second ultrason
					sleep(1)
		elif (dist >= (valeurBaseCapteurEntree-30) and dejacapteentre == True): 
			dejacapteentre = False
		dist2 = ultrasonic(pinSortie) 
		if (dist2 < (valeurBaseCapteurSortie-30) and dejacaptesortie==False): 
			if (ultrasonic(pinSortie) < (valeurBaseCapteurSortie-30)): 
				if(ultrasonic(pinSortie) < (valeurBaseCapteurSortie-30)):
					nbPersonne -= 1
					dejacaptesortie = True
					writeNb(nbPersonne)
					image = prendrePhoto()
					session = getNbSession()
					time = getCurrentTime()
					# On envoie les infos au google sheet
					sendInfos(session,time,nbPersonne,image)
					# On bloque avec un sleep pour ne pas activer le second ultrason
					sleep(1)
		elif (dist2 >= (valeurBaseCapteurSortie-30) and dejacaptesortie == True): 
			dejacaptesortie = False
		sleep(0.2)


##------------------------------------------------------------------------------------------------------------------------------------##
#|																																	  |#		
#|											CODE PAR : AMZERT INES	 ET  ITALIANO LORENZO											  |#
#|																																	  |#
##------------------------------------------------------------------------------------------------------------------------------------##
