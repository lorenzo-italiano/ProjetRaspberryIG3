Pas de bibliothèques externes nécessaires.

Branchements :
Le dispositif est paramétré de sorte a ce que si vous suiviez les branchements suivants, 
vous ne rencontrerez aucun soucis de fonctionnement
caméra : sur l'emplacement prévu a cet effet
bouton : port D2
led : port D4
lcd : I2C-3
NFC : I2C quelconque
ultrasons : un sur le port D7 un sur le D8

La caméra que nous avons ne fonctionne pas et génére l'erreur "no data received from camera" lorsque
nous executons le code pour prendre une photo, le code concernant la caméra est donc présent dans les
fichiers mais est en commentaire afin d'éviter les erreurs de python et pour que le système puisse quand même tourner.

Il est a noter que les programmes sont écris de façon a ce que la raspberry execute le fichier launcher.py a son lancement.