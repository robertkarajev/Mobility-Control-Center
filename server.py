import paho.mqtt.client as mqttClient
import json
import configparser as cp

read_file = cp.ConfigParser()
read_file.read('read_file.ini')
port = read_file['port']['MQTT']
ip = read_file['serverinformation']['IP']

class MQTTServer:
    def dummyPathfinding(self, carInfo):
        path = ['tag1', 'tag2', 'tag3', 'tag4', 'tag5', 'tag6', 'tag7']
        #path = carInfo[1]
        return path

    def checkAuthorization(self, carId):
        if carId in self.checkArr:
            return False
        self.checkArr.append(carId)
        print('known carIds: ', self.checkArr)
        return True

    def addTag(self, tag):
        database = []
        if tag in database:
            return tag + ' already in database'
        else:
            return tag + ' added to database'

    def on_connect(self, client, userdata, flags, rc):
        self.client.subscribe('GP', 1)  # GetPath
        self.client.subscribe('PA', 1)  # ParkArrived
        self.client.subscribe('AU', 1)  # AUthorize
        self.client.subscribe('RT', 1)  # Read Tag
        if rc == 0:
            print("Connected to broker")
            global Connected                # Use global variable
            Connected = True                # Signal connection
        else:
            print("Connection failed")

    def sendPublish(self, topic, message, qos):
        self.client.publish(topic, json.dumps(message), qos)

    def on_message(self, client, userdata, message):
        msg = json.loads(str(message.payload.decode('utf-8')))
        if message.topic == "GP":
            carInfo = msg.split(',')
            print(carInfo)
            self.sendPublish(carInfo[0], self.dummyPathfinding(carInfo), 1)
        elif message.topic == 'PA':
            print('car ' + msg + ' has arrived succesfully')
        elif message.topic == 'AU':
            self.sendPublish(msg, self.checkAuthorization(msg), 1)
        elif message.topic == 'RT':
            carInfo = msg.split(',')
            print(carInfo)
            self.sendPublish(carInfo[0], self.addTag(carInfo[1]), 1)
        else:
            print('yayeeeeeettt')

    def __init__(self):
        Connected = False   #global variable for the state of the connection

        broker_address = ip #Broker address
        broker_address = '127.0.0.1'
        port = port                         #Broker port
        user = "server"                    #Connection username
        password = "lololololniemanddieditraadhahaha"            #Connection password

        self.checkArr = []
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


MQTTServer()
while True:
    pass
