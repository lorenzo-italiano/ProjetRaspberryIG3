from drivers.button import *
from drivers.LCD import *
from time import *

initButton(2)

setText("Appuyer bouton pour demarrer")

while(1):
    if(readButton(2)==1):
        from main import *
        break