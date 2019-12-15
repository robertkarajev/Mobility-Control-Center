from client import MQTTClient
import rfid_reader as wg
import configparser as cp
import mqttBrokerinfo as mbi

class Main:
	
	def __init__(self, path = ''):
		self.mqtt = MQTTClient("145.24.222.194", False) #boolean is localhost // ip local host, host port 1883 
		self.verifier = wg.ParkingVerifier([])
		print('hello there')
	
	def run(self):
		while True:
			receive_tag_id, previous_tag = wg.Wiegand.run()
			#receive_tag_id = str(input())
			if not self.verifier.verify_path(receive_tag_id):
				path = self.mqtt.getPath(receive_tag_id,'get') # Returns a list
				self.verifier.change_path(path)
				self.verifier.verify_path(receive_tag_id)

# Leaving it blank will use local host, host port 1883 
mqtt = MQTTClient(mbi[0], mbi[1], mbi[2], mbi[3]) # host adress, port, brokername,brokerpass
verifier = wg.ParkingVerifier([])
	
def main():
	receive_data = wg.Wiegand()
	while True:
		receive_tag_id = receive_data.run()
		if receive_tag_id != None:
			print("Card ID: ", receive_tag_id)
		if not verifier.verify_path(receive_tag_id):
			path = mqtt.getPath(receive_tag_id,'get') # Returns a list
			verifier.change_path(path)
			verifier.verify_path(receive_tag_id)
main()
