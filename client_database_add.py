import paho.mqtt.client as paho
import random
import string
import json
import mqttBrokerInfo
import time


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
            self.connected = True
        else:
            print("Connection failed")

    # callback function for when a message is received from the broker
    def on_message(self, client, userdata, message):
        if message.topic == self.name:
            msg = json.loads(str(message.payload.decode('utf-8')))
            if not self.authorized:
                self.authLogic(msg)
            else:
                self.msg = msg
        else:
            print('message that was not intended for you has been received')

    def authLogic(self, msg):
        if msg:  # msg == True
            self.authorized = True
            print('ID authorized by server')
        else:
            print('ID not authorized by server')
            self.client.unsubscribe(self.name)
            self.name = self.randomString(self.carIdLength)
            self.client.subscribe(self.name, 1)
            self.getAuth()

    # general sending method
    def sendPublish(self, topic, message, qos):
        if not self.authorized and not topic == 'AU':
            self.getAuth()
        self.client.publish(topic, json.dumps(message), qos)

    def getAuth(self):
        self.sendPublish('AU', self.name, 1)

    # send a tag to the server which it will put in the database if it isn't there yet
    def sendTag(self, tagId, msg):
        self.msg = msg
        self.sendPublish('RT', self.name + ',' + str(tagId), 1)  # ReadTag
        start = time.time()
        counter = 0
        while self.msg == 'get':
            if time.time() - start > self.retrySendingAfterSeconds:
                if counter >= self.maxAmountRetriesSending:
                    return 'took too long try sending new tag'
                print('retry sending ReadTag')
                self.sendPublish('RT', self.name + ',' + str(tagId), 1)  # ReadTag
                counter += 1
                start = time.time()
        return self.msg

    def __init__(self, brokerAddress, brokerPort, brokerUser, brokerPassword, localTesting):
        self.retrySendingAfterSeconds = 5
        self.maxAmountRetriesSending = 5
        self.carIdLength = 4

        self.authorized = False
        self.connected = False

        self.name = self.randomString(self.carIdLength)

        self.brokerAddress = brokerAddress  # Broker address
        self.port = brokerPort              # Broker port
        self.user = brokerUser              # Connection username
        self.password = brokerPassword      # Connection password

        if localTesting:
            self.broker_address = "127.0.0.1"  # Broker address

        self.client = paho.Client(self.name)                      # create new instance
        self.client.username_pw_set(self.user, password=self.password)  # set username and password
        self.client.on_connect = self.on_connect                        # attach function to callback
        self.client.on_message = self.on_message                        # attach function to callback
        self.msg = ''

        print('broker address: ' + self.brokerAddress, ' port: ', self.port)

        try:
            self.client.connect(self.brokerAddress, port=self.port)  # connect to broker
        except:
            print('could not connect, continue trying')

        self.client.loop_start()  # start the loop
        self.getAuth()


# (broker_ip, localTesting, password='', broker_port='1833')
brokerInfo = mqttBrokerInfo.getmqttinfo()
mqttClient = MQTTClient(brokerInfo[0], brokerInfo[1], brokerInfo[2], brokerInfo[3], False)
while True:
    print('Enter new RFID tag: ')
    tagRead = str(input())
    print(mqttClient.sendTag(tagRead, 'get'))
