import paho.mqtt.client as mqttClient
import random
import string
import json

class MQTTClient:
    #create a random string containing letters and numbers with a variable length
    def randomString(self, stringLength):
        letters = string.ascii_letters + '0123456789'
        return ''.join(random.choice(letters) for i in range(stringLength))

    #callback function for when the script get a CONNACK from the broker
    #subscribes to own name so it can receive personal messages from the server-client
    def on_connect(self, client, userdata, flags, rc):
        client.subscribe(self.name, 1)
        if rc == 0:
            print("Connected to broker")
            global Connected                #Use global variable
            Connected = True                #Signal connection
        else:
            print("Connection failed")

    #callback function for when a message is received from the broker
    def on_message(self, client, userdata, message):
        if message.topic == self.name:
            msg = str(message.payload.decode('utf-8'))
            msg = json.loads(msg)
            if not isinstance(msg, list):
                print('[ERROR] message received not a list')
            print(msg)
        else:
            print('message that was not intended for you has been received')

    #general sending method
    def sendPublish(self, topic, message, qos):
        self.client.publish(topic, json.dumps(message), qos)

    #get a path by sending the name of the car as well as the RFID tag just read(GetPath)
    def getPath(self, tagId):
        self.sendPublish('GP', self.name + ',' + str(tagId), 1)

    #confirm that you have arrived at the destination (ParkArrived)
    def arrived(self):
        self.sendPublish('PA', self.name, 1)

    def __init__(self, broker_address, localTesting, password='', broker_port=1883):
        self.name = self.randomString(69)
        Connected = False   #global variable for the state of the connection

        self.broker_address = broker_address        #Broker address
        if localTesting:
            self.broker_address = "127.0.0.1"       #Broker address
        self.port = broker_port                     #Broker port
        self.user = self.name                       #Connection username
        self.password = self.randomString(69)       #Connection password

        self.client = mqttClient.Client(self.name)                    #create new instance
        self.client.username_pw_set(self.user, password=self.password)#set username and password
        self.client.on_connect = self.on_connect                      #attach function to callback
        self.client.on_message = self.on_message                      #attach function to callback

        print(self.broker_address)

        try:
            self.client.connect(self.broker_address, port=self.port)  # connect to broker
        except:
            print('could not connect, continue trying')

        self.client.loop_start()  # start the loop

#(broker_ip localTesting, password='', broker_port='1833')
mqttclient = MQTTClient("145.24.222.194", True)
while True:
    print('Enter new RFID tag: ')
    tagRead = str(input())
    mqttclient.getPath(tagRead)
