from client import MQTTClient
import rfid_reader as wg
import configparser as cp

read_file = cp.ConfigParser()
read_file.read('read_file.ini')
user = read_file['serverinformation']['User']
pw = read_file['serverinformation']['PW']
ip = read_file['serverinformation']['IP']
port = int(read_file['serverport']['MySQl'])

# Leaving it blank will use local host, host port 1883 
#mqtt = MQTTClient(ip, port) # host adress, port 
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
