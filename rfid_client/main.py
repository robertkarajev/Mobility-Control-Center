from client import MQTTClient
import rfid_reader as wg
import configparser as cp
import mqttBrokerInfo as mbi
import local_logger as ll
import logger
import os

logger = logger.Logger(1)

# Leaving it blank will use local host, host port 1883
mbi = mbi.getmqttinfo()
mqtt = MQTTClient(mbi[0], mbi[1], mbi[2], mbi[3], logger) # host adress, port, brokername,brokerpass
mqtt.createClient()
mqtt.startConnection()
verifier = wg.ParkingVerifier([])

def main():
	receive_data = wg.Wiegand()
	log = ll.LocalLogger()
	while True:
		receive_tag_id, previous_tag = receive_data.run()
		if receive_tag_id != None:
			print("Card ID: ", receive_tag_id)

		result = verifier.verify_path(receive_tag_id)
		print(result)
		if result == 'lastTag':
			mqtt.arrivedAtLastTag()


		if not result:						# Check if the rfid reader is receiving the correct path
			if receive_tag_id:												
				path, directions = mqtt.getPath(receive_tag_id, previous_tag) # Returns a list
				log.write_file("arrival",path)
				verifier.change_path(path)
				verifier.verify_path(receive_tag_id)
				print(verifier.retrieved_path)
				# geef door: directions
		else:
			print(verifier.retrieved_path)

main()

'''
currently have verify, logger, get previous and current rfid, 
Something with following the road direction //checker
Give directions to the vehicle x/direction
On arrival go backwards or get new path

on depature delete log



'''
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