import socket
from datetime import datetime
import json 
import time

HOST = "77.249.179.218"   #"145.24.222.194"
PORT = 5000

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

"""
dit script is de client die simuleert dat gebruikers achter elkaar inlogt. 
de server behandeld deze logins als een thread die slaapt.(gebruiker logt in-> thread aanmaken en laten slapen(ingelogd)->thread is klaar gebruiker uitgelogd. )
er worden JSON strings verstuurd.
de dictionaries zijn bedoeld om informatie van de gebruiker te simuleren
verbinding wordt tot stant gebracht door middel van sockets
informatie van de gebruikers worden willekeurig gekozen op basis van een random generator.
"""
counter=0

while counter<5:

    now= datetime.now()

    logPackage = {
        "RFID-ID":"PAAAAAAAAAAAAAAAAAAAGGGGGGGGGGGGGGGAAAAAAAAAAAAAAAAAAAA",
        "date"   : str(now.time())
    }

    package = json.dumps(logPackage)
    package = package + '\n'
    sock.sendall(package.encode())
    time.sleep(1)
    counter+=1


sock.close()