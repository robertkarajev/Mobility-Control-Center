#import wiegand_read_v3 as wg
from client import MQTTClient
import wiegand_read_experimental as wg

class Main:
	
	def __init__(self, path = ''):
		self.mqtt = MQTTClient("145.24.222.194", True) #boolean is localhost // ip local host, host port 1883 
		self.verifier = wg.ParkingVerifier([])
	
	def run(self):
		while True:
			# receive_tag_id = wg.Wiegand.run()
			receive_tag_id = str(input())
			if not self.verifier.verify_path(receive_tag_id):
				path = self.mqtt.getPath(receive_tag_id,'get') # Returns a list
				self.verifier.change_path(path)
				self.verifier.verify_path(receive_tag_id)

main = Main()

main.run()
