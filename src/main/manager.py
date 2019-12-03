import main.modules.credentials as credentials
import main.modules.services as sv

class ParkingManager:
	def __init__(self):
		mqttBrokerCredentials = credentials.getMqttBrokerCredentials()
		self.mqttServerClient = sv.MqttServerClient(mqttBrokerCredentials[0],
													mqttBrokerCredentials[1],
													mqttBrokerCredentials[2],
													mqttBrokerCredentials[3])
		self.mqttServerClient.createClient()
		self.mqttServerClient.startConnection()

		mySqlDbCredentials = credentials.getMySqlDatabaseCredentials()
		self.mySqlConnector = sv.MySQLConnector(mySqlDbCredentials[0], 
												mySqlDbCredentials[1],
												mySqlDbCredentials[2],
												mySqlDbCredentials[3],
												mySqlDbCredentials[4])
		self.mySqlConnector.startConnection()
		

	def carAuthentication(self, carId):
		pass

	def spaceAssignment(self, carId):	#prefered assignemnet???
		pass
	
	def generatePath(self, carId, rfidTag):
		pass

	def registerArrival(self, carId):
		pass

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

