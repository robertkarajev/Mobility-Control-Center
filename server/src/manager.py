import lib.modules.credentials as cr
import lib.modules.services as sv
import lib.testmodules.testservices as tsv
import lib.modules.timer as tm
import lib.modules.logger as logger
import lib.modules.pathfinding as pf
import lib.modules.grid as sim

# initialized Logger to log all debug, info, warning, critical and error information
logger = logger.Logger(1)

# topics used to seperatly log different events
topMan = 'ParkingManager'
topCar = 'Car'
topMsg = 'Messanger'
topAdd = 'addTag'

class ParkingManager:
	# initialize all the services Mqtt client, MySql client and Pathfinder object that generates paths
	# this method also queries parking spaces and roads to store them in self.spaces and self.roads
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
		self.pathFinder = pf.PathFinder(self.spaces, self.roads, logger)

		self.pathFinder.generateGrid()
		squareHeight = 100
		squareWidth = 100

		self.simulator = sim.Simulator(self.pathFinder.grid, squareHeight, squareWidth)

	# help method that converts string to tuples 
	# (this is used because coordinates are stored as string inside the database 
	# but are used as tuples while communicating between server and client)
	def stringToTuple(self, array):
		newArr = []
		arrWithEntry = []
		try:
			for (tag, coord) in array:
				newArr.append((tag, (int(coord[1]), int(coord[3]))))
		except ValueError:
			for (tag, coord, coord2) in array:
				newArr.append((tag, (int(coord[1]), int(coord[3]))))
				arrWithEntry.append((tag, (int(coord[1]), int(coord[3])), (int(coord2[1]), int(coord2[3]))))
		return [newArr, arrWithEntry]

	# filter the initialized spaces and roads records only to get the coordinates
	def getCoordinates(self, tag):
		for x in self.spacesAndRoads:
			if tag in x:
				return x[1]
	
	# filter the initialized spaces and roads records only to get the tags
	def getTag(self, cor):
		for x in self.spacesAndRoads:
			if cor in x:
				return x[0]

	# takes generated path with coordinates to convert the coordinates to their respective tags
	def replaceCoordinatesInPathWithTagIds(self, corPath):
		for y in range(len(corPath)):
			for x in self.spacesAndRoads:
				if corPath[y] in x:
					corPath[y] = x[0]
					break
		return corPath

	# this method is called when car/client makes contact with server/parking manager,
	# it registers a car as arriving to the parking lot
	def carAuthentication(self, carId):
		carInDb = self.mySqlConnector.checkCarId(carId)
		if carInDb:
			result = False  # carId already in db so new car needs to get new id: return false
		else:
			self.mySqlConnector.registerCar(carId)
			logger.info('registered car', carId, 'state as ==arriving==.', topic=topMan)
			result = True
		logger.info('car authentication result:', result, topic=topMan)
		return result
	
	# this method is called when a path needs to be generated, 
	# and it depending on which state the car happens to be arriving, parked, leaving
	def generatePath(self, beginCoordinates, endCoordinates, prevCoordinates, entryCoordinates, entryAtEnd):
		path = self.pathFinder.getPath(beginCoordinates, endCoordinates, prevCoordinates, entryCoordinates, entryAtEnd)
		self.simulator.setPath(path[0].copy())
		self.simulator.setPathColor()
		self.simulator.simulateCarMovement()
		path[0] = self.replaceCoordinatesInPathWithTagIds(path[0])
		logger.info('path generation successful.', topic=topMan)
		logger.info('generated path :', path, topic=topMan)
		return path

	# this method takes carId, startTag and prevTag and depending on these it generates needed path
	# the scanned startTag determines in what state the car is
	def getSpecificPath(self, carId, startTag, prevTag):
		beginCoordintates = self.getCoordinates(startTag)
		entryCoordinates = None
		entryAtEnd = None

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
				entryAtEnd = True
			if a == beginCoordintates:
				entryCoordinates = b
				entryAtEnd = False
		return self.generatePath(beginCoordintates, endCoordinates, prevCor, entryCoordinates, entryAtEnd)

	# this method is called when the car has arrived to its set(parking_space OR exit) destination
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

	# main method that is constantly running waiting for messages to be processed
	def processMessage(self):
		logger.info('listening for messages...', topic=topMsg)
		genericMessage = self.mqttServerClient.getMsg()
		topic = genericMessage[0]
		message = genericMessage[1]

		# Authentication (messages sent to this topic are meant to make sure car registered are unique)
		if topic == 'AU':
			logger.info(message, 'requests authentication...', topic=topCar)
			self.mqttServerClient.sendPublish(message, self.carAuthentication(message), 1)

		# Get Path (messages sent to this topic are to whether generate path to the parking space OR exit)
		elif topic == "GP":
			logger.info(message, 'requests path...', topic=topCar)
			carInfo = message.split(',')
			self.mqttServerClient.sendPublish(carInfo[0], self.getSpecificPath(carInfo[0], carInfo[1], carInfo[2]), 1)

		# Last Tag (messages sent to this topic are to let the parking manager know that the car is arrived at their destination)
		elif topic == 'LT':
			logger.info(message, 'requests to register arrival...', topic=topCar)
			self.mqttServerClient.sendPublish(message, self.registerArrival(message), 1)

		elif topic == 'ST':
			splitMsg = message.split(',')
			carId = splitMsg[0]
			tagId = splitMsg[1]
			tagCoordinates = self.getCoordinates(tagId)
			self.simulator.simulateCarMovement()
			print('received tag')
		else:
			logger.error('topic of message not recognised', topic=topMsg)
		print()

	# TEST PURPOSES
	# this is used because the school network doesn't allow direct connection the server
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
