import paho.mqtt.client as paho
import random
import string
import json
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
        else:
            print("Connection failed")

    def setNameFile(self):
        f = open("carName.txt", "w+")
        f.write(self.name)
        f.close()

    def getNameFile(self):
        f = open("carName.txt", "r+")
        self.name = f.read()

    def clearNameFile(self):
        f = open("carName.txt", "w+")
        f.write('')
        f.close()

    # callback function for when a message is received from the broker
    def on_message(self, client, userdata, message):
        if message.topic == self.name:
            msg = json.loads(str(message.payload.decode('utf-8')))
            if not isinstance(msg, list):  # if msg is a path or not
                if not self.authorized:
                    self.authLogic(msg)
                elif msg == 'clearName':
                    self.clearNameFile()
                    self.authorized = False
                else:
                    print('[ERROR] message received not a list')
            else:
                print(self.authorized)
                self.msg = msg
        else:
            print('message that was not intended for you has been received')

    def authLogic(self, msg):
        if msg:  # msg == True
            self.setNameFile()
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

    # get a path by sending the name of the car as well as the RFID tag just read(GetPath)
    def getPath(self, tagId):
        self.msg = 'get'
        self.sendPublish('GP', self.name + ',' + str(tagId), 1)
        start = time.time()
        counter = 0
        while self.msg == 'get':
            if time.time() - start > self.retrySendingAfterSeconds:
                if counter >= self.maxAmountRetriesSending:
                    return 'took too long try sending new tag'
                print('retry sending getPath')
                self.sendPublish('GP', self.name + ',' + str(tagId), 1)
                counter += 1
                start = time.time()
        return self.msg

    # confirm that you have arrived at the destination (arrivedAtLastTag)
    def arrivedAtLastTag(self):
        self.sendPublish('LT', self.name, 1)

    def __init__(self, brokerAddress, brokerPort, brokerUser, brokerPassword, localTesting):
        # variables that can be changed
        self.retrySendingAfterSeconds = 5
        self.maxAmountRetriesSending = 5
        self.carIdLength = 4

        self.getNameFile()
        self.authorized = True
        if not self.name:
            self.authorized = False
            self.name = self.randomString(self.carIdLength)
        print(self.name)

        # variables that should not be changed
        self.brokerAddress = brokerAddress   # Broker address
        self.port = brokerPort               # Broker port
        self.user = brokerUser               # Connection username
        self.password = brokerPassword       # Connection password

        if localTesting:
            self.brokerAddress = "127.0.0.1"  # Broker address

        self.client = paho.Client(self.name)                            # create new instance
        self.client.username_pw_set(self.user, password=self.password)  # set username and password
        self.client.on_connect = self.on_connect                        # attach function to callback
        self.client.on_message = self.on_message                        # attach function to callback
        self.msg = 'get'

        print('broker address: ' + self.brokerAddress, ' port: ', self.port)

        try:
            self.client.connect(self.brokerAddress, port=self.port)  # connect to broker
        except:
            print('could not connect, continue trying')

        self.client.loop_start()  # start the loop
        if self.authorized:
            print('id was authorized before already')
        else:
            self.getAuth()
