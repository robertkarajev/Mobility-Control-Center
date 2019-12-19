from client import MQTTClient
import rfid_reader as wg
import configparser as cp
import mqttBrokerInfo as mbi
import local_file as ll
import logger
import os

logger = logger.Logger(1)

# Leaving it blank will use local host, host port 1883
mbi = mbi.getmqttinfo()
mqtt = MQTTClient(mbi[0], mbi[1], mbi[2], mbi[3], logger) # host adress, port, brokername,brokerpass
mqtt.createClient()
mqtt.startConnection()
verifier = wg.ParkingVerifier([])
local_file = ll.LocalFile()
receive_data = wg.Wiegand()

def give_directions(directions):
	command, direction = directions
	# something with messaging
	pass

def main():
	# check_log_on_start_up()
	state = "arrival"
	while True:
		receive_tag_id, previous_tag = receive_data.run()
		if receive_tag_id != None:
			local_file.info(receive_tag_id, " Card id: ")

		result = verifier.verify_path(receive_tag_id)
		if result == 'lastTag':
			verifier.change_path([])
			mqtt.arrivedAtLastTag()
			state = "depature"
			if state == "depature" and receive_tag_id == local_file.get_content("depature")[-1]:
				local_file.info(receive_tag_id, 'Card id: ')
				local_file.delete_file()
				local_file.info('', 'End reached')

		if not result:						# Check if the rfid reader is receiving the correct path
			if receive_tag_id:												
				path, directions = mqtt.getPath(receive_tag_id, previous_tag) # Returns a list
				local_file.write_file(state,path)
				verifier.change_path(path)
				verifier.verify_path(receive_tag_id)
					
				if receive_tag_id == local_file.get_content("arrival")[-1]:
					local_file.info(receive_tag_id, 'Card id: ')
					state = "depature"

				if state == "depature" and receive_tag_id == local_file.get_content("arrival")[-1]: # get new path when the vehicle starts up
					local_file.write_file(state,path)
					verifier.change_path(path)
					# go in reverse
					print(verifier.retrieved_path,"depature")

				if state == "depature" and receive_tag_id == local_file.get_content("arrival")[-2]:
					# stop going in reverse
					pass 

				print(verifier.retrieved_path)
				print(directions)
				give_directions(directions)
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
