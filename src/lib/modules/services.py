import mysql.connector as mysqlconn
import time as tm
import paho.mqtt.client as paho
import threading
import json

#topic for logger
topDatabase = 'SQLDatabase'
topMqtt = 'MQTTServerClient'

class MqttServerClient:
    #initialize MqttServerClient for communication with Client side
    def __init__(self, user, password, port, brokerAddress='127.0.0.1', logger=None):
        self.user = user                    # Connection username
        self.password = password            # Connection password
        self.brokerAddress = brokerAddress  # Broker address
        self.port = port                    # Broker port

        self.logger = logger
        logger.debug('connection arguments', self.user, self.password, self.brokerAddress, self.port, topic=topMqtt)

        self.event = threading.Event()
        self.msgArr = []
        self.client = None

    #create new instace that will communicate with Client side
    def createClient(self):
        self.client = paho.Client("ServerClient")                   # create new instance
        self.client.username_pw_set(self.user, password=self.password)  # set username and password
        self.client.on_connect = self.on_connect              # attach function to callback
        self.client.on_message = self.setMsg                  # attach function to callback
        self.logger.info('client created.', topic=topMqtt)

    #start connection of MqttServerClient
    def startConnection(self):
        try:
            self.client.connect(self.brokerAddress, port=self.port)

            # create new thread to process network traffic
            self.client.loop_start()
            self.logger.info('connection established.', topic=topMqtt)
        except:
            self.logger.warning('connection failed, retrying...', topic=topMqtt)

    #method which stops all initialized object to properly close the MqttServerClient connection
    def stopConnection(self):
        self.client.disconnect()
        self.client.loop_stop()
        self.logger.info('connection closed.', topic=topMqtt)

    #callback method which is used on connect to subscribed to perticular channels found within this method
    def on_connect(self, client, userdata, flags, connectionResult):
        errorMessage = 'connection refused'
        if connectionResult == 0:
            self.client.subscribe('GP', 1)  # Get Path
            self.client.subscribe('LT', 1)  # arrived at Last Tag
            self.client.subscribe('AU', 1)  # AUthorize
            self.client.subscribe('RT', 1)  # Read Tag
        elif connectionResult == 1:
            self.logger.error(errorMessage, 'incorrect protocol version', topic=topMqtt)
        elif connectionResult == 2:
            self.logger.error(errorMessage, 'invalid client identifier', topic=topMqtt)
        elif connectionResult == 3:
            self.logger.error(errorMessage, 'server unavailable', topic=topMqtt)
        elif connectionResult == 4:
            self.logger.error(errorMessage, 'bad username or password', topic=topMqtt)
        elif connectionResult == 5:
            self.logger.error(errorMessage, 'not authorised', topic=topMqtt)

    #method which publishes a created message to Mqtt Broker
    def sendPublish(self, topic, message, qos):
        self.logger.info('sent message:', '(topic: '+topic+', message: '+str(message)+', qos: '+str(qos)+')', topic=topMqtt)
        self.client.publish(topic, json.dumps(message), qos)

    #set a msg that for publishing
    def setMsg(self, client, userdata, msg):
        topic = msg.topic
        msg = json.loads(str(msg.payload.decode('utf-8')))
        self.msgArr.append([topic, msg])
        self.event.set()

    #read messages that are written to the subscribed topic, this waits for an event
    # in this case a message that is written to the topic to which this client is subscribed to
    def getMsg(self):
        self.event.wait()
        msg = self.msgArr.pop(0)
        if not len(self.msgArr) > 0:
            self.event.clear()
        self.logger.info('received message from car:', msg, topic=topMqtt)
        return msg

class MySqlConnector:
    #sets all needed credential information for MySqlConnector
    def __init__(self, username, password, databaseName, databaseAddress, databasePort, logger = None):
        self.username = username
        self.password = password
        self.databaseName = databaseName
        self.databaseAddress = databaseAddress
        self.databasePort = databasePort
        
        self.logger = logger
        self.logger.debug('connection arguments:', self.username, self.password, self.databaseAddress, self.databasePort, topic = topDatabase)

    #creates an instance of MySqlConnector which can be used by this class
    def startConnection(self):
        self.connection = mysqlconn.MySQLConnection(username = self.username,
                                         password = self.password,
                                         database = self.databaseName,
                                         host = self.databaseAddress,
                                         port = self.databasePort)
        self.logger.info('connection established.', topic = topDatabase)

    #close the connection
    def closeConnection(self):
        self.connection.close()
        self.logger.info('connection closed.', topic = topDatabase)

    #used for executing a query
    def executeQuery(self, query, values = None):
        self.logger.debug('executing query:', query, 'values:', values, topic = topDatabase)
        cursor = self.connection.cursor()
        if 'SELECT' in query.upper():
            cursor.execute(query, values)
            result = cursor.fetchall()
            cursor.close()
            self.logger.debug('end result:', result, topic = topDatabase)
            return result
        else:
            cursor.execute(query, values)
            self.connection.commit()
            cursor.close()
            self.logger.debug('end result:', True, topic = topDatabase)
            return True

    #checks if a car with given carId exists and return 'True' or 'False' result
    def checkCarId(self, carId):
        query = "SELECT IF(id_car = '"+carId+"', True, False) FROM cars"
        result = self.executeQuery(query)
        return (1,) in result

    #inserts an unregisterd a car into cars table
    def registerCar(self, carId):
        query = "INSERT INTO cars VALUES ('"+carId+"', 'arriving')"
        self.executeQuery(query)
        return True

    #delete car from cars table
    def deleteCar(self, carId):
        query = "DELETE FROM cars WHERE id_car = '"+carId+"'"
        self.executeQuery(query)

    #checks what the state of the car is with given carId
    def getCarState(self, carId):
        query = "SELECT state FROM cars WHERE id_car = '"+carId+"'"
        result = self.executeQuery(query)
        return result[0][0]

    #sets a state for a car
    def setCarState(self, carId, state):
        query = "UPDATE cars SET state = '"+state+"' WHERE id_car = '"+carId+"'"
        self.executeQuery(query)

    #checks whether and which car with given carId is assigend to a parking space
    def getAssignedCarToSpace(self, carId):
        query = "SELECT * FROM parking_spaces WHERE assigned_car = '"+carId+"'"
        result = self.executeQuery(query)
        return result

    #generates a random parking space
    def getRandomParkingSpace(self):
        query = "SELECT * FROM parking_spaces WHERE assigned_car IS NULL ORDER BY RAND() LIMIT 1"
        result = self.executeQuery(query)
        return result[0]

    #assings a car with given carId to parking space with given rfidTag
    def assignCarToSpace(self, carId, rfidTag):
        query = "UPDATE parking_spaces SET assigned_car = '"+carId+"' WHERE rfid_tag = '"+rfidTag+"'"
        self.executeQuery(query)

    #delete car with given carId from parking space
    def unassignCarFromSpace(self, carId):
        query = "UPDATE parking_spaces SET assigned_car = NULL WHERE assigned_car = '"+carId+"'"
        self.executeQuery(query)

    #checks whether rfid tag with given rfidTag is an entry point returns 'True' or 'False'
    def isEntryPoint(self, rfidTag):
        query = "SELECT IF(rfid_tag = '"+rfidTag+"', True, False) FROM parking_roads WHERE id_unit >= 100000 AND id_unit < 101000"
        result = self.executeQuery(query)
        return (1,) in result

    #get exit where cars leave the parking space (exit tiles are configured between the range of 101000 and 102000)
    def getExit(self):
        query = "SELECT * FROM parking_roads WHERE id_unit >= 101000 AND id_unit < 102000"
        result = self.executeQuery(query)
        return result

    #returns list of all roads with their rfid_tag and coordinates
    def getParkingRoads(self):
        query = "SELECT rfid_tag, coordinates FROM parking_roads"
        result = self.executeQuery(query)
        return result

    #returns list of all parking_spaces with their rfid_tag, coordinates and entry_coordinates
    def getParkingSpaces(self):
        query = "SELECT rfid_tag, coordinates, entry_coordinates FROM parking_spaces"
        result = self.executeQuery(query)
        return result

'''
    def insertLot(self, id_parking_lot, is_space_available, available_spaces):
        query = ("INSERT INTO parking_lots "
                   "(id_parking_lot, is_space_available, available_spaces) "
                   "VALUES (%s, %s, %s)")
        values = (id_parking_lot, is_space_available, available_spaces)
        self.executeQuery(query, values)

    def insertWing(self, id_parking_wing, available_spaces, number_of_spaces, is_wing_full, id_parking_lot):
        query = ("INSERT INTO parking_wings "
                   "(id_parking_wing, available_spaces, number_of_spaces, is_wing_full, id_parking_lot) "
                   "VALUES (%s, %s, %s, %s, %s)")
        values = (id_parking_wing, available_spaces, number_of_spaces, is_wing_full, id_parking_lot)
        self.executeQuery(query, values)

    def insertSpace(self, id_parking_space, rfid_tag, location, availability, id_parking_wing):
        query = ("INSERT INTO parking_spaces "
                   "(id_parking_space, rfid_tag, location, availability, id_parking_wing) "
                   "VALUES (%s, %s, %s, %s, %s)")
        values = (id_parking_space, rfid_tag, location, availability, id_parking_wing)
        self.executeQuery(query, values)

    def insertRoad(self, id_unit, rfid_tag, location, id_parking_lot):
        query = ("INSERT INTO parking_roads "
                   "(id_unit, rfid_tag, location, id_parking_wing) "
                   "VALUES (%s, %s, %s, %s)")
        values = (id_unit, rfid_tag, location, id_parking_lot)
        self.executeQuery(query, values)
'''