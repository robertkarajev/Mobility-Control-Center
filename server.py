import paho.mqtt.client as mqttClient
import json
import mqttBrokerInfo

database = []


class mySQLconnector:
    def __init__(self):
        self.checkArr = []

    def dummyPathfinding(self, carInfo):
        path = ['tag1', 'tag2', 'tag3', 'tag4', 'tag5', 'tag6', 'tag7']
        #path = carInfo[1]
        return path

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


class MQTTServer:
    def on_connect(self, client, userdata, flags, rc):
        self.client.subscribe('GP', 1)  # Get Path
        self.client.subscribe('PA', 1)  # Park Arrived
        self.client.subscribe('AU', 1)  # AUthorize
        self.client.subscribe('RT', 1)  # Read Tag
        if rc == 0:
            print("Connected to broker")
            self.connected = True                # Signal connection
        else:
            print("Connection failed")

    def sendPublish(self, topic, message, qos):
        self.client.publish(topic, json.dumps(message), qos)

    def setMsg(self, client, userdata, msg):
        self.msg = json.loads(str(msg.payload.decode('utf-8')))
        self.topic = msg.topic

    def getMsg(self):
        return [self.topic, self.msg]

    '''def on_message(self, client, userdata, message):
        msg = json.loads(str(message.payload.decode('utf-8')))
        # Get Path (a car wants a path (either to parking space or the exit))
        if message.topic == "GP":
            carInfo = msg.split(',')
            print(carInfo)
            self.sendPublish(carInfo[0], connector.dummyPathfinding(carInfo), 1)
        # Park Arrived (the car has arrived at the destination)
        elif message.topic == 'PA':
            print('car ' + msg + ' has arrived succesfully')
        # AUthorization (to authorize cars to make sure no car has the same ID)
        elif message.topic == 'AU':
            self.sendPublish(msg, connector.registerCar(msg), 1)
        # Read Tag (to add to database (voor opzet))
        elif message.topic == 'RT':
            carInfo = msg.split(',')
            print(carInfo)
            self.sendPublish(carInfo[0], connector.addTag(carInfo[1]), 1)
        else:
            print('[ERROR]: topic of message not recognised')'''

    def __init__(self, broker_address, port, user, password, test):
        self.connected = False   # global variable for the state of the connection
        self.msg = ''
        self.topic = ''

        self.broker_address = broker_address            # Broker address
        if test:
            self.broker_address = '127.0.0.1'
        self.port = port                                     # Broker port
        self.user = user                                 # Connection username
        self.password = password   # Connection password

        self.client = mqttClient.Client("Server")             # create new instance
        self.client.username_pw_set(self.user, password=self.password)  # set username and password
        self.client.on_connect = self.on_connect              # attach function to callback
        self.client.on_message = self.on_message              # attach function to callback
        self.client.on_message = self.setMsg                  # attach function to callback

        print(self.broker_address, self.port)

        try:
            self.client.connect(self.broker_address, port=port)  # connect to broker
        except:
            print('could not connect, continue trying')

        self.client.loop_start()  # start the loop

'''
brokerInfo = mqttBrokerInfo.getmqttinfo()
mqttClient = MQTTServer(brokerInfo[0], brokerInfo[1], brokerInfo[2], brokerInfo[3], False)
connector = mySQLconnector()
while True:
    pass
'''