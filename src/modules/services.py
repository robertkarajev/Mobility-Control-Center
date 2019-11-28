import mysql.connector as mysqlconn
import time as tm
import paho.mqtt.client as mqttClient
#import RPi.GPIO as GPIO

class MQTTServerClient:
    def __init__(self, broker_address, broker_password, broker_port = 1883, broker_username = 'server'):
        self.broker_address = broker_address
        self.broker_port = broker_port
        self.broker_username = broker_username
        self.broker_password = broker_password

    def createClient(self):
        self.client = mqttClient.Client("Server")
        self.client.username_pw_set(self.broker_username, password = self.broker_password)
        
        #attach function to callback
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        
    def startConnection(self):
        try:    
            self.client.connect(broker_address, port=self.broker_port)
            
            #create new thread to process network traffic
            self.client.loop_start()
        except:
            print('[INFO] Connection failed...')

    def stopConnection(self):
            self.client.disconnect()
            self.client.loop_stop()

    def on_connect(self, client, userdata, flags, connectionResult):
        if connectionResult == 0:
            print('[INFO] Connection to broker successful')
            self.client.subscribe('GP', 1)#GetPath
            self.client.subscribe('PA', 1)#ParkArrived
            self.client.subscribe('AU', 1)#AUthorize
        elif connectionResult == 1:
            print('[ERROR] Connection refused - incorrect protocol version')
        elif connectionResult == 2:
            print('[ERROR] Connection refused - invalid client identifier')
        elif connectionResult == 3:
            print('[ERROR] Connection refused - server unavailable')
        elif connectionResult == 4:
            print('[ERROR] Connection refused - bad username or password')
        elif connectionResult == 5:
            print('[ERROR] Connection refused - not authorised')

    def on_message(self, client, userdata, message):
        if message.topic == 'GP':
            carInfo = str(message.payload.decode('utf-8')).split(',')
            self.client.publish(carInfo[0], "random", 1)
        elif message.topic == 'PA':
            carId = str(message.payload.decode('utf-8'))

    #def sendPublish(self, topic, message, qos):
    #    self.client.publish(topic, json.dumps(message), qos)


class MySQLConnector:
    def __init__(self, db_username, db_password, db_name, db_local_address, db_local_port):
        self.db_username = db_username
        self.db_password = db_password
        self.db_name = db_name
        self.db_host = db_local_address
        self.db_port = db_local_port

    def startConnection(self):
        self.connection = mysqlconn.MySQLConnection(username = self.db_username,
                                         password = self.db_password,
                                         database = self.db_name,
                                         host = self.db_host,
                                         port = self.db_port)

    def closeConnection(self):
        self.connection.close()

    def executeQuery(self, query, values = None):
        cursor = self.connection.cursor()
        if 'SELECT' in query.upper():
            cursor.execute(query, values)
            result = cursor.fetchall()
            cursor.close()
            return result
        else:
            cursor.execute(query, values)
            self.connection.commit()
            cursor.close()
            return True

    def checkCarId(self, carId):
        query = "SELECT IF(id_car = '"+carId+"', True, False) FROM cars"
        result = self.executeQuery(query)
        return (1,) in result

    def registerCar(self, carId):
        if not self.checkCarId(carId):
            query = "INSERT INTO cars VALUES ('"+carId+"', 'arriving')"
            self.executeQuery(query)
            return True
        else:
            return False

    #if lwaving or parked: return path to exit
    #else assign parking space and return path to said parking space
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
        return result[0]

    def getRandomParkingSpace(self):
        query = "SELECT * FROM parking_spaces WHERE assigned_car IS NULL ORDER BY RAND() LIMIT 1"
        result = self.executeQuery(query)
        return result[0]

    def assignCarToSpace(self, carId, rfid_tag):
        query = "UPDATE parking_spaces SET assigned_car = '"+carId+"' WHERE rfid_tag = '"+rfid_tag+"'"
        self.executeQuery(query)

    def unassignCarFromSpace(self, rfid_tag):
        query = "DELETE assigned_car FROM parking_spaces WHERE rfid_tag = '"+rfid_tag+"'"
        self.executeQuery(query)

    def isEntryPoint(self, rfid_tag):
        query = "SELECT IF(rfid_tag = '"+rfid_tag+"', True, False) FROM parking_roads WHERE id_unit >= 100000 AND id_unit < 101000"
        result = self.executeQuery(query)
        return (1,) in result

    def getExit(self):
        query = "SELECT * FROM parking_roads WHERE id_unit >= 101000 AND id_unit < 102000"
        result = self.executeQuery(query)
        return result

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

#!/usr/bin/env python
#green/data0 is pin 11
#white/data1 is pin 13
#For Example Use pin 22 not GPIO 22 and use pin 7 not GPIO 7
class Wiegand:
	def __init__ (self, proc_name = 'wiegand', data0 = 11, data1 = 13, bits = ''):
		self.proc_name = proc_name
		self.data0 = data0
		self.data1 = data1
		self.bits = bits
		self.setup()
	
	def setup (self):
		GPIO.setmode(GPIO.BOARD) #BCM or BOARD
		GPIO.setup (self.data0, GPIO.IN, pull_up_down = GPIO.PUD_UP)
		GPIO.setup (self.data1, GPIO.IN, pull_up_down = GPIO.PUD_UP)
		GPIO.add_event_detect (self.data0, GPIO.FALLING, callback = self.channel_zero)
		GPIO.add_event_detect (self.data1, GPIO.FALLING, callback = self.channel_one)

	def channel_zero (self, channel):
		self.bits +='0'
	
	def channel_one (self, channel):
		self.bits +='1'
	
	def set_procname(self):
		from ctypes import cdll, byref, create_string_buffer
		libc = cdll.LoadLibrary('libc.so.6')    #Loading a 3rd party library C
		buff = create_string_buffer(len(self.proc_name)+1) #Note: One larger than the name (man prctl says that)
		buff.value = self.proc_name                 #Null terminated string as it should be
		libc.prctl(15, byref(buff), 0, 0, 0) #Refer to "#define" of "/usr/include/linux/prctl.h" for the misterious
	
	def retrieve_id(self, binary_string = ''):
		first_part = binary_string[0:13]
		second_part = binary_string[13:0]
		parts = [first_part, second_part]
		bitsTo1 = [0, 0]
		index = 0	
	
		for part in parts:
			bitsTo1[index] = part.count('1')
			index += 1
		
		if bitsTo1[0] % 2 != 0 or bitsTo1[1] % 2 != 1:
			bin = binary_string[1:-1] # Leaving out the first and last bit
			if len(bin) == 32:
				hex_string = str(hex(int(bin,2)))
				#n, hex_compressed = hex_string.split('0x')
				hex_compressed = hex_string[2:10] # Removing 0x from each incoming card
 				#print('binary: ' + bin)
				#print('decimal: ' , int(bin,2)) 
				print('hex: ' , hex(int(bin,2)))  
				self.bits = ''
				return hex_compressed
	
	def run(self):
		data = self.retrieve_id(self.bits)
		tm.sleep(0.01)
		return data