import threading
import paho.mqtt.client as paho
import json

database = []

# mockservices eg database connection
class mySQLconnector:
    def __init__(self):
        self.checkArr = []

    def dummyPathfinding(self, carInfo):
        path = ['tag1', 'tag2', 'tag3', 'tag4', 'tag5', 'tag6', 'tag7']
        return path

    def carArrivedLogic(self, carId):
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
        print('known carIds: ', self.checkArr)
        return True

    def addTag(self, tag):
        if tag in database:
            return tag + ' already in database'
        else:
            database.append(tag)
            print(database)
            return tag + ' added to database'

    def deleteCar(self, carId):
        if carId in database:
            database.remove(carId)

class MQTTServer:
    def on_connect(self, client, userdata, flags, rc):
        self.client.subscribe('GP', 1)  # Get Path
        self.client.subscribe('LT', 1)  # arrived at Last Tag
        self.client.subscribe('AU', 1)  # AUthorize
        self.client.subscribe('RT', 1)  # Read Tag
        if rc == 0:
            print("Connected to broker")
        else:
            print("Connection failed")

    def sendPublish(self, topic, message, qos):
        self.client.publish(topic, json.dumps(message), qos)

    def setMsg(self, client, userdata, msg):
        self.topic = msg.topic
        self.msg = json.loads(str(msg.payload.decode('utf-8')))
        self.returnMsg.set()

    def getMsg(self):
        self.returnMsg.wait()
        self.returnMsg.clear()
        return [self.topic, self.msg]

    def __init__(self, broker_address, port, user, password, test):
        self.returnMsg = threading.Event()
        self.msg = ''
        self.topic = ''

        self.broker_address = broker_address            # Broker address
        if test:
            self.broker_address = '127.0.0.1'
        self.port = port                                     # Broker port
        self.user = user                                 # Connection username
        self.password = password   # Connection password

        self.client = paho.Client("Server")             # create new instance
        self.client.username_pw_set(self.user, password=self.password)  # set username and password
        self.client.on_connect = self.on_connect              # attach function to callback
        self.client.on_message = self.setMsg                  # attach function to callback

        print(self.broker_address, self.port)

        try:
            self.client.connect(self.broker_address, port=port)  # connect to broker
        except:
            print('could not connect, continue trying')

        self.client.loop_start()  # start the loop
