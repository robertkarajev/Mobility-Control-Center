import paho.mqtt.client as mqttClient
import random
import string
import json
import test

idLength = 4

class MQTTClient:
    # create a random string containing letters and numbers with a variable length
    def randomString(self, stringLength):
        letters = string.ascii_letters + '0123456789'
        return ''.join(random.choice(letters) for i in range(stringLength))

    # callback function for when the script get a CONNACK from the broker
    # subscribes to own name so it can receive personal messages from the server-client
    def on_connect(self, client, userdata, flags, rc):
        client.subscribe(self.name, 1)
        if rc == 0:
            print("Connected to broker")
            global Connected                # Use global variable
            Connected = True                # Signal connection
        else:
            print("Connection failed")

    # callback function for when a message is received from the broker
    def on_message(self, client, userdata, message):
        if message.topic == self.name:
            msg = json.loads(str(message.payload.decode('utf-8')))
            if not self.authorized:
                if msg:  # msg == True
                    self.authorized = True
                    print('ID authorized by server')
                else:
                    print('ID not authorized by server')
                    self.client.unsubscribe(self.name)
                    self.name = self.randomString(idLength)
                    self.client.subscribe(self.name, 1)
                    self.getAuth()
            else:
                self.msg = msg
        else:
            print('message that was not intended for you has been received')

    # general sending method
    def sendPublish(self, topic, message, qos):
        self.client.publish(topic, json.dumps(message), qos)

    def getAuth(self):
        self.sendPublish('AU', self.name, 1)

    # send a tag to the server which it will put in the database if it isn't there yet
    def sendTag(self, tagId, msg):
        self.msg = msg
        self.sendPublish('RT', self.name + ',' + str(tagId), 1)  # RT
        while self.msg == 'get':
            pass
        return self.msg

    def __init__(self, broker_address, localTesting, password='', broker_port=1883):
        self.name = self.randomString(idLength)
        self.authorized = False
        Connected = False  # global variable for the state of the connection

        self.broker_address = broker_address   # Broker address
        if localTesting:
            self.broker_address = "127.0.0.1"  # Broker address
        self.port = broker_port                # Broker port
        self.user = self.name                  # Connection username
        self.password = self.randomString(8)   # Connection password

        self.client = mqttClient.Client(self.name)                      # create new instance
        self.client.username_pw_set(self.user, password=self.password)  # set username and password
        self.client.on_connect = self.on_connect                        # attach function to callback
        self.client.on_message = self.on_message                        # attach function to callback
        self.msg = ''

        print('broker address: ' + self.broker_address)

        try:
            self.client.connect(self.broker_address, port=self.port)  # connect to broker
        except:
            print('could not connect, continue trying')

        self.client.loop_start()  # start the loop
        self.getAuth()


# (broker_ip, localTesting, password='', broker_port='1833')
brokerInfo = test.getmqttinfo()
mqttClient = MQTTClient(brokerInfo[0], brokerInfo[1], brokerInfo[2], brokerInfo[3], False)
while True:
    print('Enter new RFID tag: ')
    tagRead = str(input())
    print(mqttClient.sendTag(tagRead, 'get'))
