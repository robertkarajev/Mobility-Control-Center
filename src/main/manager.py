import modules.details as details
import modules.services as sv

class ParkingManager:
	def __init__(self):
		self.mySqlConnector = sv.MySQLConnector(details.username, 
												details.password,
												details.databaseName,
												details.databaseHost,
												details.databasePort)
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
		pass