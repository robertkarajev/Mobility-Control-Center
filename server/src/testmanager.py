import lib.modules.credentials as cr
import lib.modules.services as sv
import lib.testmodules.testservices as tsv
import lib.modules.timer as tm

class ParkingManager:
	def __init__(self):
		mqttBrokerCredentials = cr.getMqttBrokerCredentials()
		self.mqttServerClient = sv.MqttServerClient(mqttBrokerCredentials[0],
													mqttBrokerCredentials[1],
													mqttBrokerCredentials[3],
													brokerAddress = mqttBrokerCredentials[2])
		self.mqttServerClient.createClient()
		self.mqttServerClient.startConnection()

		mySqlDbCredentials = cr.getMySqlDatabaseCredentials()
		self.mySqlConnector = sv.MySQLConnector(mySqlDbCredentials[0], 
												mySqlDbCredentials[1],
												mySqlDbCredentials[2],
												'localhost',
												self.sshTestEnvironment())
		self.mySqlConnector.startConnection()

	def carAuthentication(self, carId):
		carInDb = self.mySqlConnector.checkCarId(carId)
		if carInDb:
			return False  # carId already in db so new car needs to get new id: return false
		else:
			self.mySqlConnector.registerCar(carId)
			return True

	def spaceAssignment(self, carId):	#prefered assignemnet???
		pass
	
	def getPath(self, startTag, endTag):
		return ['tag1', 'tag2', 'tag3', endTag]

	def generatePath(self, carId, startTag):
		carState = self.mySqlConnector.getCarState(carId)
		if carState == 'arriving':
			endTag = self.mySqlConnector.getAssignedCarToSpace(carId)
			print(endTag)
			if endTag:
				endTag = endTag[0][2]
			else:
				endTag = self.mySqlConnector.getRandomParkingSpace()[2]
				self.mySqlConnector.assignCarToSpace(carId, endTag)
		else:
			if carState == 'parked':
				self.mySqlConnector.setCarState(carId, 'leaving')
				self.mySqlConnector.unassignCarFromSpace(carId)
			endTag = self.mySqlConnector.getExit()[2]
		return self.getPath(startTag, endTag)

	def registerArrival(self, carId):
		carState = self.mySqlConnector.getCarState(carId)
		if carState == 'arriving':
			self.mySqlConnector.setCarState(carId, 'parked')
			return 'parked'
		else:
			self.mySqlConnector.deleteCar(carId)
			return 'clearName'

	def processMessage(self):
		genericMessage = self.mqttServerClient.getMsg()
		print(genericMessage)
		topic = genericMessage[0]
		message = genericMessage[1]

		# AUthorization (to authorize cars to make sure no car has the same ID)
		if topic == 'AU':
			self.mqttServerClient.sendPublish(message, self.carAuthentication(message), 1)

		# Get Path (a car wants a path (either to parking space or the exit))
		elif topic == "GP":
			carInfo = message.split(',')
			self.mqttServerClient.sendPublish(carInfo[0], self.generatePath(carInfo[0], carInfo[1]), 1)

		# Last Tag (the car has arrived at the destination)
		elif topic == 'LT':
			print('car ' + message + ' has arrived succesfully')
			self.mqttServerClient.sendPublish(message, self.registerArrival(message), 1)

		# MIGRATE THIS PEACE TO TEST/PREPERATION
		# # Read Tag (to add to database (voor opzet))
		# elif topic == 'RT':
		# 	carInfo = message.split(',')
		# 	print(carInfo)
		# 	self.mqttServerClient.sendPublish(carInfo[0], self.addTag(carInfo[1]), 1)
		else:
			print('[ERROR]: topic of message not recognised')

	def addTag(self, tagId):
		pass

	#TEST PURPOSES
	def sshTestEnvironment(self):
		var = cr.getMySqlDatabaseCredentials()
		sshConn = tsv.SSHTunnel(var[3], 22, var[0], var[1], 'localhost', var[4])
		sshConn.createSSHTunnelForwarder()
		sshConn.startTunnel()
		timer = tm.Timer()
		timer.postpone(5, f'ssh connection status: {sshConn.tunnelForwarder.local_is_up((var[3], 22))} ')
		return sshConn.tunnelForwarder.local_bind_port

manager = ParkingManager()
while True:
	manager.processMessage()
#manager.registerArrival('java')
#print(manager.registerArrival('lada'))