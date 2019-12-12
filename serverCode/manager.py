import lib.modules.credentials as cr
import lib.modules.services as sv
import lib.testmodules.testservices as tsv
import lib.modules.timer as tm
import lib.modules.logger as logger
import lib.modules.pathfinding as pf

logger = logger.Logger(1)
topMan = 'ParkingManager'
topCar = 'Car'
topMsg = 'Messanger'
topAdd = 'addTag'


class ParkingManager:
	def __init__(self):
		mqttBrokerCredentials = cr.getMqttBrokerCredentials()
		self.mqttServerClient = sv.MqttServerClient(mqttBrokerCredentials[0],
													mqttBrokerCredentials[1],
													mqttBrokerCredentials[3],
													brokerAddress=mqttBrokerCredentials[2],
													logger=logger)
		self.mqttServerClient.createClient()
		self.mqttServerClient.startConnection()
		mySqlDbCredentials = cr.getMySqlDatabaseCredentials()
		self.mySqlConnector = sv.MySqlConnector(mySqlDbCredentials[0], 
												mySqlDbCredentials[1],
												mySqlDbCredentials[2],
												'localhost',
												self.getSshLocalBindPort(),
												logger=logger)
		self.mySqlConnector.startConnection()
		logger.info('connections established.', topic=topMan)
		
		spaces = self.stringToTuple(self.mySqlConnector.getParkingSpaces())
		self.spaces = spaces[0]
		self.spacesWithEntry = spaces[1]
		self.roads = self.stringToTuple(self.mySqlConnector.getParkingRoads())[0]
		self.spacesAndRoads = self.spaces + self.roads
		self.pathFinder = pf.PathFinder(self.spaces, self.roads)

	def stringToTuple(self, array):
		newArr = []
		arrWithEntry = []
		try:
			for (tag, coord) in array:
				newArr.append((tag, (int(coord[1]), int(coord[3]))))
		except:
			for (tag, coord, coord2) in array:
				newArr.append((tag, (int(coord[1]), int(coord[3]))))
				arrWithEntry.append((tag, (int(coord[1]), int(coord[3])), (int(coord2[1]), int(coord2[3]))))
		return [newArr, arrWithEntry]

	def getCoordinates(self, tag):
		for x in self.spacesAndRoads:
			if tag in x:
				return x[1]
	
	def getTag(self, cor):
		for x in self.spacesAndRoads:
			if cor in x:
				return x[0]

	def replaceCoordinatesInPathWithTagIds(self, corPath):
		for y in range(len(corPath)):
			for x in self.spacesAndRoads:
				if corPath[y] in x:
					corPath[y] = x[0]
					break
		return corPath

	def carAuthentication(self, carId):
		result = None
		carInDb = self.mySqlConnector.checkCarId(carId)
		if carInDb:
			result = False  # carId already in db so new car needs to get new id: return false
		else:
			self.mySqlConnector.registerCar(carId)
			logger.info('registered car', carId, 'state as ==arriving==.', topic=topMan)
			result = True
		logger.info('car authentication result:', result, topic=topMan)
		return result
	
	def generatePath(self, beginCoordinates, endCoordinates, prevCoordinates, entryCoordinates):
		path = self.pathFinder.getPath(beginCoordinates, endCoordinates, prevCoordinates, entryCoordinates)
		path[0] = self.replaceCoordinatesInPathWithTagIds(path[0])
		logger.info('path generation successful.', topic=topMan)
		logger.info('generated path :', path, topic=topMan)
		return path

	def getSpecificPath(self, carId, startTag, prevTag):
		beginCoordintates = self.getCoordinates(startTag)
		entryCoordinates = None

		prevCor = ''
		if prevTag:
			prevCor = self.getCoordinates(prevTag)

		carState = self.mySqlConnector.getCarState(carId)
		if carState == 'arriving':
			endTag = self.mySqlConnector.getAssignedCarToSpace(carId)
			if endTag:
				endCoordinates = self.getCoordinates(endTag[0][2])
			else:
				newParkingSpaceTag = self.mySqlConnector.getRandomParkingSpace()[2]
				self.mySqlConnector.assignCarToSpace(carId, newParkingSpaceTag)
				endCoordinates = self.getCoordinates(newParkingSpaceTag)
			logger.debug('generating arriving path..', topic=topMan)
		else:
			if carState == 'parked':
				self.mySqlConnector.setCarState(carId, 'leaving')
				logger.info('registered car', carId, 'state as ==leaving==.', topic=topMan)
				self.mySqlConnector.unassignCarFromSpace(carId)
			endTag = self.mySqlConnector.getExit()[0][1]
			endCoordinates = self.getCoordinates(endTag)
			logger.debug('generating leaving path..', topic=topMan)

		for _, a, b in self.spacesWithEntry:
			if a == endCoordinates:
				entryCoordinates = b
		return self.generatePath(beginCoordintates, endCoordinates, prevCor, entryCoordinates)

	#this method is called when the car has arrived to its set(parking_space OR exit) destination
	def registerArrival(self, carId):
		carState = self.mySqlConnector.getCarState(carId)
		if carState == 'arriving':
			self.mySqlConnector.setCarState(carId, 'parked')
			logger.info('registered car', carId, 'state as ==parked==.', topic=topMan)
			return 'parked'
		else:
			self.mySqlConnector.deleteCar(carId)
			logger.info('unregistered car', carId, 'from parking lot.', topic=topMan)
			return 'clearName'

	def processMessage(self):
		logger.info('listening for messages...', topic=topMsg)
		genericMessage = self.mqttServerClient.getMsg()
		topic = genericMessage[0]
		message = genericMessage[1]

		#[!!!] #TEST THIS LOGGING CONTENT !!!
		# AUthorization (to authorize cars to make sure no car has the same ID)
		if topic == 'AU':
			logger.info(message, 'requests authentication...', topic=topCar)
			self.mqttServerClient.sendPublish(message, self.carAuthentication(message), 1)

		# Get Path (a car wants a path (either to parking space or the exit))
		elif topic == "GP":
			logger.info(message, 'requests path...', topic=topCar)
			carInfo = message.split(',')
			self.mqttServerClient.sendPublish(carInfo[0], self.getSpecificPath(carInfo[0], carInfo[1], carInfo[2]), 1)

		# Last Tag (the car has arrived at the destination)
		elif topic == 'LT':
			logger.info(message, 'requests to register arrival...', topic=topCar)
			self.mqttServerClient.sendPublish(message, self.registerArrival(message), 1)

		# MIGRATE THIS PEACE TO TEST/PREPERATION
		# # Read Tag (to add to database (voor opzet))
		# elif topic == 'RT':
		# logger.info('tagId being added to database', topic=topAdd)
		# 	carInfo = message.split(',')
		# 	print(carInfo)
		# 	self.mqttServerClient.sendPublish(carInfo[0], self.addTag(carInfo[1]), 1)
		else:
			print('[ERROR]: topic of message not recognised')
		print()

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
while True:
	manager.processMessage()
#manager.carAuthentication('rata')
#manager.registerArrival('java')
#print(manager.registerArrival('lada'))