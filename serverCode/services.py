import mysql.connector as mysqlconn
import time as tm
import paho.mqtt.client as paho
import threading
import json
# import RPi.GPIO as GPIO

topDatabase = 'SQLDatabase'
topMqtt = 'MQTTServerClient'


class MqttServerClient:
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

    def createClient(self):
        self.client = paho.Client("ServerClient")                   # create new instance
        self.client.username_pw_set(self.user, password=self.password)  # set username and password
        self.client.on_connect = self.on_connect              # attach function to callback
        self.client.on_message = self.setMsg                  # attach function to callback
        self.logger.info('client created.', topic=topMqtt)

    def startConnection(self):
        try:
            self.client.connect(self.brokerAddress, port=self.port)

            # create new thread to process network traffic
            self.client.loop_start()
            self.logger.info('connection established.', topic=topMqtt)
        except:
            self.logger.warning('connection failed, retrying...', topic=topMqtt)

    def stopConnection(self):
        self.client.disconnect()
        self.client.loop_stop()
        self.logger.info('connection closed.', topic=topMqtt)

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

    def sendPublish(self, topic, message, qos):
        self.logger.info('sent message:', '(topic: '+topic+', message: '+str(message)+', qos: '+str(qos)+')',
                         topic=topMqtt)
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
        self.logger.info('received message from car:', msg, topic=topMqtt)
        return msg


class MySqlConnector:
    def __init__(self, username, password, databaseName, databaseAddress, databasePort, logger=None):
        self.username = username
        self.password = password
        self.databaseName = databaseName
        self.databaseAddress = databaseAddress
        self.databasePort = databasePort
        
        self.logger = logger
        self.logger.debug('connection arguments:',
                          self.username, self.password, self.databaseAddress, self.databasePort,
                          topic=topDatabase)

    def startConnection(self):
        self.connection = mysqlconn.MySQLConnection(username=self.username,
                                                    password=self.password,
                                                    database=self.databaseName,
                                                    host=self.databaseAddress,
                                                    port=self.databasePort)
        self.logger.info('connection established.', topic=topDatabase)

    def closeConnection(self):
        self.connection.close()
        self.logger.info('connection closed.', topic=topDatabase)

    def executeQuery(self, query, values = None):
        self.logger.debug('executing query:', query, 'values:', values, topic=topDatabase)
        cursor = self.connection.cursor()
        if 'SELECT' in query.upper():
            cursor.execute(query, values)
            result = cursor.fetchall()
            cursor.close()
            self.logger.debug('end result:', result, topic=topDatabase)
            return result
        else:
            cursor.execute(query, values)
            self.connection.commit()
            cursor.close()
            self.logger.debug('end result:', True, topic=topDatabase)
            return True

    def checkCarId(self, carId):
        query = "SELECT IF(id_car = '"+carId+"', True, False) FROM cars"
        result = self.executeQuery(query)
        return (1,) in result

    def registerCar(self, carId):
        query = "INSERT INTO cars VALUES ('"+carId+"', 'arriving')"
        self.executeQuery(query)
        return True

    def deleteCar(self, carId):
        query = "DELETE FROM cars WHERE id_car = '"+carId+"'"
        self.executeQuery(query)

    def getCarState(self, carId):
        query = "SELECT state FROM cars WHERE id_car = '"+carId+"'"
        result = self.executeQuery(query)
        return result[0][0]

    def setCarState(self, carId, state):
        query = "UPDATE cars SET state = '"+state+"' WHERE id_car = '"+carId+"'"
        self.executeQuery(query)

    def getAssignedCarToSpace(self, carId):
        query = "SELECT * FROM parking_spaces WHERE assigned_car = '"+carId+"'"
        result = self.executeQuery(query)
        return result

    def getRandomParkingSpace(self):
        query = "SELECT * FROM parking_spaces WHERE assigned_car IS NULL ORDER BY RAND() LIMIT 1"
        result = self.executeQuery(query)
        return result[0]

    def assignCarToSpace(self, carId, rfid_tag):
        query = "UPDATE parking_spaces SET assigned_car = '"+carId+"' WHERE rfid_tag = '"+rfid_tag+"'"
        self.executeQuery(query)   

    def unassignCarFromSpace(self, car_id):
        query = "UPDATE parking_spaces SET assigned_car = NULL WHERE assigned_car = '"+car_id+"'"
        self.executeQuery(query)

    def isEntryPoint(self, rfid_tag):
        query = "SELECT IF(rfid_tag = '"+rfid_tag+"', True, False) FROM parking_roads WHERE id_unit >= 100000 AND id_unit < 101000"
        result = self.executeQuery(query)
        return (1,) in result

    def getExit(self):
        query = "SELECT * FROM parking_roads WHERE id_unit >= 101000 AND id_unit < 102000"
        result = self.executeQuery(query)
        return result

    def getParkingRoads(self):
        query = "SELECT rfid_tag, coordinates FROM parking_roads"
        result = self.executeQuery(query)
        return result

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

#!/usr/bin/env python
#green/data0 is pin 11
#white/data1 is pin 13
#For Example Use pin 22 not GPIO 22 and use pin 7 not GPIO 7
# class Wiegand:
# 	def __init__ (self, proc_name = 'wiegand', data0 = 11, data1 = 13, bits = ''):
# 		self.proc_name = proc_name
# 		self.data0 = data0
# 		self.data1 = data1
# 		self.bits = bits
# 		self.setup()
	
# 	def setup (self):
# 		GPIO.setmode(GPIO.BOARD) #BCM or BOARD
# 		GPIO.setup (self.data0, GPIO.IN, pull_up_down = GPIO.PUD_UP)
# 		GPIO.setup (self.data1, GPIO.IN, pull_up_down = GPIO.PUD_UP)
# 		GPIO.add_event_detect (self.data0, GPIO.FALLING, callback = self.channel_zero)
# 		GPIO.add_event_detect (self.data1, GPIO.FALLING, callback = self.channel_one)

# 	def channel_zero (self, channel):
# 		self.bits +='0'
	
# 	def channel_one (self, channel):
# 		self.bits +='1'
	
# 	def set_procname(self):
# 		from ctypes import cdll, byref, create_string_buffer
# 		libc = cdll.LoadLibrary('libc.so.6')    #Loading a 3rd party library C
# 		buff = create_string_buffer(len(self.proc_name)+1) #Note: One larger than the name (man prctl says that)
# 		buff.value = self.proc_name                 #Null terminated string as it should be
# 		libc.prctl(15, byref(buff), 0, 0, 0) #Refer to "#define" of "/usr/include/linux/prctl.h" for the misterious
	
# 	def retrieve_id(self, binary_string = ''):
# 		first_part = binary_string[0:13]
# 		second_part = binary_string[13:0]
# 		parts = [first_part, second_part]
# 		bitsTo1 = [0, 0]
# 		index = 0	
	
# 		for part in parts:
# 			bitsTo1[index] = part.count('1')
# 			index += 1
		
# 		if bitsTo1[0] % 2 != 0 or bitsTo1[1] % 2 != 1:
# 			bin = binary_string[1:-1] # Leaving out the first and last bit
# 			if len(bin) == 32:
# 				hex_string = str(hex(int(bin,2)))
# 				#n, hex_compressed = hex_string.split('0x')
# 				hex_compressed = hex_string[2:10] # Removing 0x from each incoming card
#  				#print('binary: ' + bin)
# 				#print('decimal: ' , int(bin,2)) 
# 				print('hex: ' , hex(int(bin,2)))  
# 				self.bits = ''
# 				return hex_compressed
	
# 	def run(self):
# 		data = self.retrieve_id(self.bits)
# 		tm.sleep(0.01)
# 		return data