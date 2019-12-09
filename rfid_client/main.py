from client import MQTTClient
import rfid_reader as wg
import configparser as cp
import mqttBrokerinfo as mbi

#read_file = cp.ConfigParser()
#read_file.read('read_file.ini')
#user = read_file['broker']['user']
#pw = read_file['broker']['PW']
#ip = read_file['broker']['brokerAddress']
#port = int(read_file['broker']['port'])
#read_file = cp.ConfigParser()
#read_file.read('read_file.ini')

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
