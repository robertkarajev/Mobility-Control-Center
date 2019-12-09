import lib.modules.credentials as cr
import lib.modules.services as sv
import lib.testmodules.testservices as tsv
import lib.modules.timer as tm
import lib.modules.logger as logger

logger = logger.Logger(1)
topMan = 'Manager'

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
		self.mySqlConnector = sv.MySqlConnector(mySqlDbCredentials[0], 
												mySqlDbCredentials[1],
												mySqlDbCredentials[2],
												'localhost',
												self.getSshLocalBindPort(),
												logger = logger)
		self.mySqlConnector.startConnection()
		logger.info('connections established.', topic=topMan)

	def carAuthentication(self, carId):
		result = None
		carInDb = self.mySqlConnector.checkCarId(carId)
		if carInDb:
			result = False  # carId already in db so new car needs to get new id: return false
		else:
			self.mySqlConnector.registerCar(carId)
			result = True
		logger.info('car authentication result:', result, topic=topMan)
		return result

	def spaceAssignment(self, carId):	#prefered assignemnet???
		pass
	
	def getPath(self, startTag, endTag):
		logger.debug('path: ', '...', topic=topMan)
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
			logger.debug('generating arriving path..', topic=topMan)
		else:
			if carState == 'parked':
				self.mySqlConnector.setCarState(carId, 'leaving')
				self.mySqlConnector.unassignCarFromSpace(carId)
			endTag = self.mySqlConnector.getExit()
			logger.info('generating leaving path..', topic=topMan)
		return self.getPath(startTag, endTag)

	#this method is called when the car has arrived to its set(parking_space OR exit) destination
	def registerArrival(self, carId):
		carState = self.mySqlConnector.getCarState(carId)
		if carState == 'arriving':
			self.mySqlConnector.setCarState(carId, 'parked')
			logger.info('car:', carId, 'registered as parked', topic=topMan)
			return 'parked'
		else:
			self.mySqlConnector.deleteCar(carId)
			logger.info('car:', carId, 'unregistered from parking lot', topic=topMan)
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
		print()

	def addTag(self, tagId):
		pass

	#TEST PURPOSES
	def getSshLocalBindPort(self):
		var = cr.getMySqlDatabaseCredentials()
		sshConn = tsv.SSHTunnel(var[3], 22, var[0], var[1], 'localhost', var[4])
		sshConn.createSSHTunnelForwarder()
		sshConn.startTunnel()
		timer = tm.Timer()
		timer.postpone(5, f'ssh connection status: {sshConn.tunnelForwarder.local_is_up((var[3], 22))} ')
		logger.debug('Created ssh tunnel with connection to port:', sshConn.tunnelForwarder.local_bind_port, topic=topMan)
		return sshConn.tunnelForwarder.local_bind_port

manager = ParkingManager()
#while True:
	#manager.processMessage()
manager.carAuthentication('rata')
#manager.registerArrival('java')
#print(manager.registerArrival('lada'))