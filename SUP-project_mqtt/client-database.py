import paho.mqtt.client as mqttClient
import time
import random
import string

'''
on messgae: sent data received to other script
'''


def randomString(stringLength=169):
    """Generate a random string of fixed length """
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(stringLength))


name = randomString(169)
#name = 'test'


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        global Connected                #Use global variable
        Connected = True                #Signal connection
    else:
        print("Connection failed")


def on_message(client, userdata, message):
    print(message)


Connected = False   #global variable for the state of the connection

#broker_address = "145.24.222.194"   #Broker address
broker_address = "127.0.0.1"   #Broker address
port = 1883                         #Broker port
user = name                         #Connection username
password = randomString(169)        #Connection password

client = mqttClient.Client(name)                    #create new instance
client.username_pw_set(user, password=password)     #set username and password
client.will_set('carDisconnect', name, 1)
client.on_connect = on_connect                      #attach function to callback
client.on_message = on_message                      #attach function to callback

if not Connected:
    try:
        client.connect(broker_address, port=port)
    except:
        print('could not connect, continue trying')

    client.loop_start()

    while not Connected:
        time.sleep(0.1)

def newTagRead(tagId):
        client.publish('addTagToDatabase', tagId, 1)


try:
    while True:
        print('Enter new RFID tag: ')
        tagRead = input()
        newTagRead(tagRead)


except KeyboardInterrupt:
    print("exiting")
    client.publish('carDisconnect', name, 1)
    client.disconnect()
    client.loop_stop()
