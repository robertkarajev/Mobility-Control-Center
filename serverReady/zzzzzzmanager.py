import src.modules.services as services
import mqttBrokerInfo

class ParkingManager:
    def __init__(self):
        self.counter = 0
        brokerInfo = mqttBrokerInfo.getmqttinfo()
        self.mqtt = services.MqttServerClient(brokerInfo[0], brokerInfo[1], brokerInfo[2], brokerInfo[3], False)
        self.mqtt.createClient()
        self.mqtt.startConnection()
        self.db = services.MySQLConnector()

    # this includes create all the resources for parking manager

    def carAuthentication(self, carId):
        carInDb = self.db.checkCarId(carId)
        if carInDb:
            return False  # carId already in db so new car needs to get new id: return false
        else:
            self.db.registerCar(carId)
            return True

    def spaceAssignment(self, carId):  # prefered assignemnet???
        pass

    def generatePath(self, carId, startTag):
        carState = self.db.getCarState(carId)
        if carState == 'arriving':
            endTag = self.db.getAssignedCarToSpace()
            if not endTag:
                endTag = self.db.getRandomParkingSpace()[2]
                self.db.assignCarToSpace(endTag)
        else:
            if carState == 'parked':
                self.db.setCarState(carId, 'leaving')
                self.db.unassignCarFromSpace(carId)
            endTag = self.db.getExit()

        return self.getPath(startTag, endTag)

    def registerArrival(self, carId):
        carState = self.db.getCarState(carId)
        if carState == 'arriving':
            self.db.setCarState(carId, 'parked')
            return 'parked'
        else:
            self.db.deleteCarFromDb(carId)
            return 'clearName'

    def addTag(self, tagId):
        pass

    def getPath(self, startTag, endTag):
        return ['tag1', 'tag2', 'tag3', endTag]

    def processMessage(self):
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
        processMessage()
