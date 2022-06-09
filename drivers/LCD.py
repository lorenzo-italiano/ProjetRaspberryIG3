# coding: utf-8
import smbus
from time import *
from re import *
from drivers.LED import *
from random import *

bus = smbus.SMBus(1)  # pour I2C-1 (0 pour I2C-0)

# Indiquez ici les deux adresses de l'ecran LCD
# celle pour les couleurs du fond d'ecran 
# et celle pour afficher des caracteres
DISPLAY_RGB_ADDR = 0x62
DISPLAY_TEXT_ADDR = 0x3e

color={
	'red' : [255,0,0],
	'green' : [0,255,0],
	'blue' : [0,0,255],
	'white' : [200,200,200],
	'mangenta' : [255,0,255],
	'black' : [0,0,0]
}

# Completez le code de la fonction permettant de choisir la couleur
# du fond d'ecran, n'oubliez pas d'initialiser l'ecran
def setRGB(rouge,vert,bleu):
	# rouge, vert et bleu sont les composantes de la couleur qu'on vous demande
	bus.write_byte_data(DISPLAY_RGB_ADDR,0x00,0x00)
	bus.write_byte_data(DISPLAY_RGB_ADDR,0x01,0x00)
	bus.write_byte_data(DISPLAY_RGB_ADDR,0x02,bleu)
	bus.write_byte_data(DISPLAY_RGB_ADDR,0x03,vert)
	bus.write_byte_data(DISPLAY_RGB_ADDR,0x04,rouge)
	bus.write_byte_data(DISPLAY_RGB_ADDR,0x08,0xAA)
	print("Couleur écran changée")

def setColor(color):
	setRGB(color[0],color[1],color[2])

def setWhite():
	setColor(color['white'])

def setRed():
	setColor(color['red'])

def Alert(text):
	#initLED(7)
	while(1):
		setRed()
		#onLED(7)
		setText(text)
		sleep(2)
		#offLED(7)
		textCmd(0x01)
		textCmd(0x0F)
		textCmd(0x38)
# Envoie  a l'ecran une commande concerant l'affichage des caracteres
# (cette fonction vous est donnes gratuitement si vous
# l'utilisez dans la fonction suivante, sinon donnez 2000€
# a la banque et allez dictement en prison :)
def textCmd(cmd):
    bus.write_byte_data(DISPLAY_TEXT_ADDR,0x80,cmd)

def writeText(text):
	for i in text:
		sleep(uniform(0.1,0.3))
		bus.write_byte_data(DISPLAY_TEXT_ADDR,0x40,ord(i))	

def directWriteText(text):
	for i in range (len(text)):
		bus.write_byte_data(DISPLAY_TEXT_ADDR,0x40,ord(text[i]))

def resetLCD():
	textCmd(0x01)
	sleep(0.1)
	textCmd(0x0F)
	sleep(0.1)
	textCmd(0x38)
	sleep(0.1)

def writeNb(text):
	resetLCD()
	directWriteText(str(text))
# Completez le code de la fonction permettant d'ecrire le texte recu en parametre
# Si le texte contient un \n ou plus de 16 caracteres pensez a gerer
# le retour a la ligne
def setText(texte):
	resetLCD()

	textecut = findall('.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?',texte)# a corriger
	textecut.pop()
	for i in textecut:
		if(len(i) == 0):
			textecut.remove(i)
	print(textecut)

	
	if(len(textecut) > 2):
		i = 0
		alreadyWritten = ""
		while i < (len(textecut)):
			if(textecut[i]==alreadyWritten):
				directWriteText(textecut[i])
			else:
				writeText(textecut[i])
			if(i+1 < len(textecut) and textecut[i+1]!= ''):
				textCmd(0xc0)
				writeText(textecut[i+1])
				alreadyWritten =textecut[i+1]
			sleep(2)
			resetLCD()
			i += 1
		sleep(2)
		resetLCD()
	else:
		writeText(textecut[0])
		textCmd(0xc0)
		if(len(textecut)>1):
			writeText(textecut[1])
	#if ....:  # si on rencontre \n ou si on depasse 16 caracteres
	#	textCommand(0xc0) # pour passer a la ligne
	print("texte ecrit")

def authentificationRequest():
	textOnLoop(1,"Veuillez scannervotre badge pourauthentification")

def textOnLoop(condition,texte):
	while(condition):
		setText(texte)

#def erreurBadge():

#limites de personnes
def limiteAtteinte(compteur):
	#implémenter le saut de ligne
	setText(str(compteur) + " " + "limite atteinte")

def erreurRecoFacialeStaff():
	Alert("Erreur de reconnaissance faciale Staff")
