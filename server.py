import paho.mqtt.client as mqttClient
import json
import test
import time

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
        self.client.subscribe('GP', 1)  # Get Path
        self.client.subscribe('PA', 1)  # Park Arrived
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

    def __init__(self, broker_address, port, user, password, test):
        Connected = False   # global variable for the state of the connection

        self.broker_address = broker_address            # Broker address
        if test:
            self.broker_address = '127.0.0.1'
        self.port = port                                     # Broker port
        self.user = user                                 # Connection username
        self.password = password   # Connection password

        self.checkArr = []
        self.client = mqttClient.Client("Server")             # create new instance
        self.client.username_pw_set(self.user, password=self.password)  # set username and password
        self.client.on_connect = self.on_connect              # attach function to callback
        self.client.on_message = self.on_message              # attach function to callback

        print(self.broker_address, self.port)

        try:
            self.client.connect(self.broker_address, port=port)  # connect to broker
        except:
            print('could not connect, continue trying')

        self.client.loop_start()  # start the loop


brokerInfo = test.getmqttinfo()
mqttClient = MQTTServer(brokerInfo[0], brokerInfo[1], brokerInfo[2], brokerInfo[3], False)
while True:
    pass
