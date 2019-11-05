import paho.mqtt.client as mqttClient
import time
#from pathfinding import getPath
class MQTTServer:
    '''
    todo:
    connectie met pathfinding
    hoe de informatie doorgeven aan pathfinding
    hoe de informatie van het pad doorsturen
    '''


    def dummyPathfinding(carInfo, firstTagRead=False):
        path = carInfo[1]
        return path

    def on_connect(self, client, userdata, flags, rc):
        self.client.subscribe("newCar", 1)
        self.client.subscribe('carDisconnect', 1)
        if rc == 0:
            print("Connected to broker")
            global Connected                #Use global variable
            Connected = True                #Signal connection
        else:
            print("Connection failed")

    def on_message(self, client, userdata, message):
        if message.topic == "newCar":
            carInfo = str(message.payload.decode('utf-8')).split(',')
            print(carInfo)
            self.client.subscribe(carInfo[0] + '/newTag', 1)
            self.client.publish(carInfo[0], self.dummyPathfinding(carInfo, True), 1)
        elif "/newTag" in message.topic:
            rfid = str(message.payload.decode('utf-8'))
            autoId = message.topic.split('/newTag')[0]
            print([autoId, rfid])
            self.client.publish(autoId, self.dummyPathfinding([autoId, rfid]), False, 1)
        elif message.topic == 'carDisconnect':
            self.client.unsubscribe(str(message.payload.decode('utf-8')) + '/newTag')
        else:
            print('yayeeeeeettt')

    def __init__(self):
        Connected = False   #global variable for the state of the connection

        broker_address = "145.24.222.194"  #Broker address
        #broker_address = '127.0.0.1'
        port = 1883                         #Broker port
        user = "server"                    #Connection username
        password = "lololololniemanddieditraadhahaha"            #Connection password

        self.client = mqttClient.Client("Server")               #create new instance
        self.client.username_pw_set(user, password=password)    #set username and password
        self.client.on_connect = self.on_connect                      #attach function to callback
        self.client.on_message = self.on_message                      #attach function to callback

        print(broker_address)

        try:
            self.client.connect(broker_address, port=port)          #connect to broker
        except:
            print('could not connect, continue trying')

        self.client.loop_start()        #start the loop

        while not Connected:    #Wait for connection
            time.sleep(0.1)

        try:
            while True:
                time.sleep(10000)

        except KeyboardInterrupt:
            print("exiting")
            self.client.disconnect()
            self.client.loop_stop()


MQTTServer()
