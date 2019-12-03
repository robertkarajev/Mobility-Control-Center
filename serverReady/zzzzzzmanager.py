import src.modules.services as services
import mqttBrokerInfo

class ParkingManager:
    def __init__(self):
        self.counter = 0
        brokerInfo = mqttBrokerInfo.getmqttinfo()
        self.mqtt = services.MQTTServer(brokerInfo[0], brokerInfo[1], brokerInfo[2], brokerInfo[3], False)
        self.mqtt.createClient()
        self.mqtt.startConnection()

    # this includes create all the resources for parking manager

    def carAuthentication(self, carId):
        pass

    def spaceAssignment(self, carId):  # prefered assignemnet???
        pass

    def generatePath(self, carId, rfidTag):
        pass

    def registerArrival(self, carId):
        pass

    def processMessage(self):
        pass

    def addTag(self, tagId):
        pass

    def processMsg(self):
        msgInfo = self.mqtt.getMsg()
        print(msgInfo)
        topic = msgInfo[0]
        msg = msgInfo[1]

        # Get Path (a car wants a path (either to parking space or the exit))
        if topic == "GP":
            carInfo = msg.split(',')
            self.mqtt.sendPublish(carInfo[0], self.generatePath(carInfo[0], carInfo[1]), 1)

        # Last Tag (the car has arrived at the destination)
        elif topic == 'LT':
            print('car ' + msg + ' has arrived succesfully')
            self.mqtt.sendPublish(msg, self.registerArrival(msg), 1)

        # AUthorization (to authorize cars to make sure no car has the same ID)
        elif topic == 'AU':
            self.mqtt.sendPublish(msg, self.carAuthentication(msg), 1)

        # Read Tag (to add to database (voor opzet))
        elif topic == 'RT':
            carInfo = msg.split(',')
            print(carInfo)
            self.mqtt.sendPublish(carInfo[0], self.addTag(carInfo[1]), 1)

        else:
            print('[ERROR]: topic of message not recognised')

    while True:
        processMsg()
