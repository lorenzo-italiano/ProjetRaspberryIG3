"""
This example shows connecting to the PN532 and reading an M1
type RFID tag
"""

import RPi.GPIO as GPIO

import drivers.pn532.pn532 as nfc
from drivers.pn532 import *
from time import *
from drivers.LCD import *
from drivers.LED import *

def read_hexa(hexa):
    return chr(int(hexa))

#pn532 = PN532_SPI(cs=4, reset=20, debug=False)
pn532 = PN532_I2C(debug=False, reset=20, req=16)
#pn532 = PN532_UART(debug=False, reset=20)

ic, ver, rev, support = pn532.get_firmware_version()
print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))

# Configure PN532 to communicate with MiFare cards
pn532.SAM_configuration()

uid = []
def testThread():
    while True:
        print("test")
        sleep(1)

def readCard():
    global uid
    print('Waiting for RFID/NFC card to write to!')
    while True:
        # Check if a card is available to read
        uid = pn532.read_passive_target(timeout=0.5)
        print('.', end="")
        # Try again if no card is available.
        if uid is not None:
            break
    print('Found card with UID:', [hex(i) for i in uid])

def readCardOnLoop():
    initLED(4)
    global uid
    read = False
    print('Waiting for RFID/NFC card to write to!')
    while True:
        # Check if a card is available to read
        uid = pn532.read_passive_target(timeout=0.5)
        #print('.', end="")
        # Try again if no card is available.
        if uid is not None and read == False:
            print('Found card with UID:', [hex(i) for i in uid])
            read = True
            if(authentification()):
                #print("authentification reussi")
                onLED(4)
                sleep(0.1)
                offLED(4)
                prenom = ""
                prenom = str(readLineWithReturn(5))
                if str(readLineWithReturn(6)) != None:
                    prenom += str(readLineWithReturn(6))
                pr2 = ""
                for i in prenom:
                    if ord(i) != 0:
                        pr2 += i
                setText("Bonjour " + pr2)
                
            else:
                onLED(4)
                sleep(0.1)
                offLED(4)
                sleep(0.2)
                onLED(4)
                sleep(0.1)
                offLED(4)
                setText("Vous n'etes pas du staff")
                
        if uid is None:
            read = False
    


key_a = b'\xFF\xFF\xFF\xFF\xFF\xFF'

secret = "96e28113b50ff25621e63730785ad0c9"
# Now we try to go through all 16 sectors (each having 4 blocks)
# each of them having a heading line of data which must not be altered, which is why we don't read it and don't write on it
readableData = [1,2,4,5,6,8,9,10,12,13,14,16,17,18,20,21,22,24,25,26,28,29,30,32,33,34,36,37,38,40,41,42,44,45,46,48,49,50,52,53,54,56,57,58,60,61,62]
# 16 blocks
blocks = [[1,2],[4,5,6],[8,9,10],[12,13,14],[16,17,18],[20,21,22],[24,25,26],[28,29,30],[32,33,34],[36,37,38],[40,41,42],[44,45,46],[48,49,50],[52,53,54],[56,57,58],[60,61,62]]

def readAllReadableData():
    for i in readableData:
        try:
            pn532.mifare_classic_authenticate_block(
                uid, block_number=i, key_number=nfc.MIFARE_CMD_AUTH_A, key=key_a)
            #print(i, ':', ' '.join(['%02X' % read_hexa(str(x))
            #    for x in pn532.mifare_classic_read_block(i)]))
            print(i, end='')
            for x in pn532.mifare_classic_read_block(i):
                print("|",read_hexa(str(x)), end = '')
                #print("|",x, end = '')
                print(" ", end='')
            print("|\n")
            #for x in pn532.mifare_classic_read_block(i):
            #    print(chr(x))
            
        except nfc.PN532Error as e:
            print(e.errmsg)
            break
    GPIO.cleanup()


def readLine(i):
    try:
        pn532.mifare_classic_authenticate_block(
            uid, block_number=i, key_number=nfc.MIFARE_CMD_AUTH_A, key=key_a)
        #print(i, ':', ' '.join(['%02X' % read_hexa(str(x))
        #    for x in pn532.mifare_classic_read_block(i)]))
        print(i, end='')
        for x in pn532.mifare_classic_read_block(i):
            print("|",read_hexa(str(x)), end = '')
            print(" ", end='')
        print("|\n")
        #for x in pn532.mifare_classic_read_block(i):
        #    print(chr(x))
        
    except nfc.PN532Error as e:
        print(e.errmsg)
    GPIO.cleanup()

# Indiquer le num du block à lire (ex : le premier block est le block 1)
# A noter qu'il y a 16 blocks
def readBlock(block):
    for i in blocks[block-1]:
        readLine(i)

def readLineWithReturn(i):
    string = ""
    try:
        pn532.mifare_classic_authenticate_block(
            uid, block_number=i, key_number=nfc.MIFARE_CMD_AUTH_A, key=key_a)
        #print(i, ':', ' '.join(['%02X' % read_hexa(str(x))
        #    for x in pn532.mifare_classic_read_block(i)]))
        #print(i, end='')
        for x in pn532.mifare_classic_read_block(i):
            string += read_hexa(str(x))
        return string
        #for x in pn532.mifare_classic_read_block(i):
        #    print(chr(x))
        
    except nfc.PN532Error as e:
        print(e.errmsg)
    GPIO.cleanup()



#readBlock(1)
#readBlock(2)
#readBlock(3)
#readBlock(4)

def authentification():
    secret = "96e28113b50ff25621e63730785ad0c9"
    if((str(readLineWithReturn(1))+str(readLineWithReturn(2))) == secret):
        return True
    else:
        return False

#readAllReadableData()

