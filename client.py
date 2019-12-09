import paho.mqtt.client as paho
import random
import string
import json
import time
import logger

logger = logger.Logger(0)


class MQTTClient:
    def __init__(self, user, password, port, brokerAddress='127.0.0.1'):
        # variables that can be changed
        self.retrySendingAfterSeconds = 5
        self.maxAmountRetriesSending = 5
        self.carIdLength = 4

        # variables that should not be changed
        self.brokerAddress = brokerAddress   # Broker address
        self.port = port               # Broker port
        self.user = user               # Connection username
        self.password = password       # Connection password

        # init here to prevent warnings
        self.authorized = None
        self.client = None
        self.name = None

        self.msg = 'get'

        logger.info('broker address:', self.brokerAddress, 'port:', self.port, topic='connection')

    def createClient(self):
        self.getNameFile()
        if self.name:
            self.authorized = True
        else:
            self.authorized = False
            self.name = self.generateName(self.carIdLength)
        self.client = paho.Client(self.name + self.generateName(self.carIdLength))  # create new instance
        self.client.username_pw_set(self.user, password=self.password)  # set username and password
        self.client.on_connect = self.on_connect  # attach function to callback
        self.client.on_message = self.on_message  # attach function to callback
        if self.authorized:
            logger.info('id was authorized before already', topic='connection')
            self.getAuth()
        else:
            logger.info('requested authorization', topic='connection')
            self.getAuth()

    def startConnection(self):
        try:
            self.client.connect(self.brokerAddress, port=self.port)  # connect to broker
            self.client.loop_start()  # start the loop
        except:
            logger.error('could not connect, continue trying', topic='connection')

    def stopConnection(self):
        self.client.disconnect()
        self.client.loop_stop()

    # callback function for when the script get a CONNACK from the broker
    # subscribes to own name so it can receive personal messages from the server-client
    def on_connect(self, client, userdata, flags, rc):
        client.subscribe(self.name, 1)
        if rc == 0:
            logger.info("Connected to broker", topic='connection')
        else:
            logger.error("Connection failed", topic='connection')

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
        self.authorized = False
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
                elif msg == 'parked':
                    logger.info('confirmation for parking received', topic='message')
                elif str(msg) == 'False':
                    logger.info('id was indeed already in database', topic='message')
                elif str(msg) == 'True':
                    logger.error('id not in database while it should have been', topic='message')
                else:
                    logger.error('message received not a list:', msg, topic='message')
            else:
                self.msg = msg
        else:
            logger.error('message that was not intended for you has been received:', message, topic='message')

    def authLogic(self, msg):
        if msg:  # msg == True
            self.setNameFile()
            self.authorized = True
            logger.info('ID authorized by server', topic='message')
        else:
            logger.info('ID not authorized by server', topic='message')
            self.client.unsubscribe(self.name)
            self.name = self.generateName(self.carIdLength)
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
                logger.warning('retry sending getPath')
                self.sendPublish('GP', self.name + ',' + str(tagId), 1)
                counter += 1
                start = time.time()
        return self.msg

    # confirm that you have arrived at the destination (arrivedAtLastTag)
    def arrivedAtLastTag(self):
        self.sendPublish('LT', self.name, 1)

    # create a random string containing letters and numbers with a variable length
    def generateName(self, stringLength):
        letters = string.ascii_letters + '0123456789'
        return ''.join(random.choice(letters) for i in range(stringLength))