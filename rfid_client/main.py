from client import MQTTClient
import rfid_reader as wg
import configparser as cp
import mqttBrokerInfo as mbi
import local_logger as ll
import logger

logger = logger.Logger(1)

# Leaving it blank will use local host, host port 1883
mbi = mbi.getmqttinfo()
mqtt = MQTTClient(mbi[0], mbi[1], mbi[2], mbi[3], logger) # host adress, port, brokername,brokerpass
verifier = wg.ParkingVerifier([])
	
def main():
	receive_data = wg.Wiegand()
	log = ll.LocalLogger()
	while True:
		receive_tag_id, previous_tag = receive_data.run()
		if receive_tag_id != None:
			print("Card ID: ", receive_tag_id)

		if not verifier.verify_path(receive_tag_id):
			if receive_tag_id:
				path = mqtt.getPath(receive_tag_id, previous_tag) # Returns a list
				log.write_file("arrival",path,"x")
				verifier.change_path(path)
				verifier.verify_path(receive_tag_id)
main()

'''
# If last rfid_tag has been read, get new path 
if log.getcontent("arrival")[-1]["rfid_tag"] == receive_data:
	path = mqtt.getPath(receive_tag_id,'get') # Returns a list
	log.write_file("depature",path,"x")

#If second to last rfid_tag has been read, get new path
if log.getcontent("arrival")[-2]["rfid_tag"] == receive_data:
	path = mqtt.getPath(receive_tag_id,'get') # Returns a list
	log.write_file("depature",path,"x")

if log.getcontent("depature")[-1]["rfid_tag"] == receive_data: # When leaving parkinglot, delete log file
	log.delete_file()
'''