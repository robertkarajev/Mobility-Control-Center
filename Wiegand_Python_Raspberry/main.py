#import wiegand_read_v3 as wg
import client as cl
import wiegand_read_experimental as wg

class Main:
	
	def __init__(self, mqtt, path = ''):
		self.mqtt = cl.MQTTClient("145.24.222.194", True) #boolean is localhost // ip local host, host port 1883 
		self.verifier = wg.ParkingVerifier([])
	def run():
		while True:
			# receive_tag_id = wg.Wiegand.run()
			receive_tag_id = str(input())
			if not self.verifier.verify_path(receive_tag_id):
				path = mqtt.getPath(receive_tag_id,'get') # Returns a list
				self.verifier.change_path(path)
			

main = Main()

main.run()
