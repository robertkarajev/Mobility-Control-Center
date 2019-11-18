#import wiegand_read_v3 as wg
from client import MQTTClient
import rfid_reader as wg

class Main:
	def __init__(self, path = ''):
		# Leaving it blank will use local host, host port 1883 
		self.mqtt = MQTTClient("145.24.222.194", 1883) # host adress, port 
		self.verifier = wg.ParkingVerifier([])
	
	def run(self):
		receive_data = wg.Wiegand()
		while True:
			receive_tag_id = receive_data.run()
			if not self.verifier.verify_path(receive_tag_id):
				path = self.mqtt.getPath(receive_tag_id,'get') # Returns a list
				self.verifier.change_path(path)
				self.verifier.verify_path(receive_tag_id)

main = Main()

main.run()
