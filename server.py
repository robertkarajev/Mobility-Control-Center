import threading
import paho.mqtt.client as paho
import json

topCarCall = 'carCall'
topCon = 'connection'


# mockservices eg database connection
class MySQLConnector:
    def __init__(self, logger=None):
        self.logger = logger
        self.database = []
        self.checkArr = []

    def dummyPathfinding(self, carInfo):
        path = ['tag1', 'tag2', 'tag3', 'tag4', 'tag5', 'tag6', 'tag7']
        return path

    def registerArrival(self, carId):
        # if carId.state == 1||2
        if carId:
            self.deleteCar(carId)
            return 'clearName'
        # if carId.state == 0
        else:
            carId.state = 1

    def registerCar(self, carId):
        if carId in self.checkArr:
            return False
        self.checkArr.append(carId)
        self.logger.debug(self.checkArr, topic=topCarCall)
        return True

    def addTag(self, tag):
        if tag in self.database:
            return tag + ' already in database'
        else:
            self.database.append(tag)
            self.logger.info(self.database, topic=topCarCall)
            return tag + ' added to database'

    def deleteCar(self, carId):
        if str(carId) in self.checkArr:
            self.checkArr.remove(carId)


class MqttServerClient:
    def __init__(self, user, password, port, brokerAddress='127.0.0.1', logger=None):
        self.logger = logger
        self.event = threading.Event()
        self.msgArr = []
        self.client = None

        self.brokerAddress = brokerAddress  # Broker address
        self.port = port                    # Broker port
        self.user = user                    # Connection username
        self.password = password            # Connection password

        logger.info(self.brokerAddress, self.port, topic=topCon)

    def createClient(self):
        self.client = paho.Client("testServer")                   # create new instance
        self.client.username_pw_set(self.user, password=self.password)  # set username and password
        self.client.on_connect = self.on_connect              # attach function to callback
        self.client.on_message = self.setMsg                  # attach function to callback

    def startConnection(self):
        try:
            self.client.connect(self.brokerAddress, port=self.port)

            # create new thread to process network traffic
            self.client.loop_start()
        except:
            self.logger.warning('could not connect, continue trying', topic=topCon)

    def stopConnection(self):
        self.client.disconnect()
        self.client.loop_stop()

    def on_connect(self, client, userdata, flags, connectionResult):
        if connectionResult == 0:
            self.logger.info('Connection to broker successful', topic=topCon)
            self.client.subscribe('GP', 1)  # Get Path
            self.client.subscribe('LT', 1)  # arrived at Last Tag
            self.client.subscribe('AU', 1)  # AUthorize
            self.client.subscribe('RT', 1)  # Read Tag
        elif connectionResult == 1:
            self.logger.error('incorrect protocol version', topic=topCon)
        elif connectionResult == 2:
            self.logger.error('invalid client identifier', topic=topCon)
        elif connectionResult == 3:
            self.logger.error('server unavailable', topic=topCon)
        elif connectionResult == 4:
            self.logger.error('bad username or password', topic=topCon)
        elif connectionResult == 5:
            self.logger.error('not authorised', topic=topCon)

    def sendPublish(self, topic, message, qos):
        self.client.publish(topic, json.dumps(message), qos)

    def setMsg(self, client, userdata, msg):
        topic = msg.topic
        msg = json.loads(str(msg.payload.decode('utf-8')))
        self.msgArr.append([topic, msg])
        self.event.set()

    def getMsg(self):
        self.event.wait()
        msg = self.msgArr.pop(0)
        if not len(self.msgArr) > 0:
            self.event.clear()
        return msg
