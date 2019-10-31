import paho.mqtt.client as mqttClient
import time
#from pathfinding import getPath

'''
todo:
connectie met pathfinding
hoe de informatie doorgeven aan pathfinding
hoe de informatie van het pad doorsturen
'''


def dummyPathfinding(carInfo, firstTagRead=False):
    path = carInfo[1]
    return path


def on_connect(client, userdata, flags, rc):
    client.subscribe("newCar", 1)
    client.subscribe('carDisconnect', 1)
    if rc == 0:
        print("Connected to broker")
        global Connected                #Use global variable
        Connected = True                #Signal connection
    else:
        print("Connection failed")


def on_message(client, userdata, message):
    if message.topic == "newCar":
        carInfo = str(message.payload.decode('utf-8')).split(',')
        print(carInfo)
        client.subscribe(carInfo[0] + '/newTag', 1)
        client.publish(carInfo[0], dummyPathfinding(carInfo, True), 1)
    elif "/newTag" in message.topic:
        rfid = str(message.payload.decode('utf-8'))
        autoId = message.topic.split('/newTag')[0]
        print([autoId, rfid])
        client.publish(autoId, dummyPathfinding([autoId, rfid]), False, 1)
    elif message.topic == 'carDisconnect':
        client.unsubscribe(str(message.payload.decode('utf-8')) + '/newTag')
    else:
        print('yayeeeeeettt')


Connected = False   #global variable for the state of the connection

#broker_address = "145.24.222.194"  #Broker address
broker_address = '127.0.0.1'
port = 1883                         #Broker port
user = "server"                    #Connection username
password = "lololololniemanddieditraadhahaha"            #Connection password

client = mqttClient.Client("Server")               #create new instance
client.username_pw_set(user, password=password)    #set username and password
client.on_connect = on_connect                      #attach function to callback
client.on_message = on_message                      #attach function to callback

print(broker_address)

try:
    client.connect(broker_address, port=port)          #connect to broker
except:
    print('could not connect, continue trying')

client.loop_start()        #start the loop

while not Connected:    #Wait for connection
    time.sleep(0.1)

try:
    while(True):
        time.sleep(10000)


except KeyboardInterrupt:
    print("exiting")
    client.disconnect()
    client.loop_stop()
