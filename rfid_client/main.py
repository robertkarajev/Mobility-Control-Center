from client import MQTTClient
import rfid_reader as wg
import configparser as cp
import mqttBrokerInfo as mbi
import local_file as ll
import logger
import os

logger = logger.Logger(1)

example_cards = ["5c6e522e","5c79af3e","5c75a37e","5c716c9e","5c7313de"]
example_direction = ["here left","here right"]
# Leaving it blank will use local host, host port 1883
mbi = mbi.getmqttinfo()
mqtt = MQTTClient(mbi[0], mbi[1], mbi[2], mbi[3], logger) # host adress, port, brokername,brokerpass
mqtt.createClient()
mqtt.startConnection()
verifier = wg.ParkingVerifier([])
local_file = ll.LocalFile()
receive_data = wg.Wiegand()

def give_directions(path):
	message = path[-1]
	destination = []
	directions = []
	direct = ['V', 'R', 'B', 'L']
	for i in path:
		for j in direct:
			if j in i:
				length = i.split(j)
				destination.append(length[0]) 
				directions.append(j)
	# something with messaging
	return length, directions

def get_rfid_tag():
	next_tag, previous_tag = receive_data.run()
	if next_tag:
		local_file.info(next_tag, " Card id: ")
		return next_tag, previous_tag

def commands(command, angle):
	if command == 'left':
		print('turning left')
	if command == 'right':
		print('turning right')
	if command == 'reverse':
		print('turning reverse')
			
def start_up():
	local_list = []
	if local_file.get_content('depature'):
		for i in (local_file.get_content('depature')[1:]):
			local_list = local_list.append(i['rfid_tag'])

	elif local_file.get_content('arrival'): # if arrival return this path
		for i in (local_file.get_content('arrival')[1:]):
			local_list = local_list.append(i['rfid_tag'])
	return local_list

def end_reached(state):
	if state == 'depature':
		local_file.clear_content()
		local_file.info(local_file.get_content("depature")[-1],'End reached, last known rfid: ')

def main():
	local_save = start_up()
	verifier.change_path(local_save)
	state = 'depature' if local_file.get_content('depature') else 'arrival'
	while True:
		receive_tag, previous_tag = get_rfid_tag()
		result = verifier.verify_path(receive_tag)

		if result == 'lastTag':
			verifier.change_path([])
			# mqtt.arrivedAtLastTag()
			end_reached(state)
			state = 'arrival' if local_file.get_content('depature')[-1] == receive_tag else 'depature'

		if not result and receive_tag:
			#path, directions = mqtt.getPath(receive_tag_id, previous_tag) # Returns a list
			path = example_cards
			directions = example_direction
			local_file.write_file(state,path)
			verifier.change_path(path)
			verifier.verify_path(receive_tag)
			
			if state == "depature" and receive_tag == local_file.get_content("arrival")[-2]:
				# stop going in reverse
				print('stop reverse, try rotating')
				pass 

			if receive_tag == local_file.get_content("arrival")[-1]:
				local_file.info(receive_tag, 'Card id: ')
				state = "depature"
				if state == "depature":
					local_file.write_file(state,path)
					verifier.change_path(path)
					# go in reverse till the previous tag has been read
					local_file.update(verifier.retrieved_path,"Depature path: ")

			local_file.update(verifier.retrieved_path,"Arrival path: ")
			local_file.info(directions,"Directions given: ")
			give_directions(directions)
			
		else:
			local_file.info(verifier.retrieved_path, "Arrival path: ")
		
'''
def main():
	state = "arrival"
	while True:
		receive_tag_id, previous_tag = receive_data.run()
		if receive_tag_id != None:
			local_file.info(receive_tag_id, " Card id: ")

		result = verifier.verify_path(receive_tag_id)
		if result == 'lastTag':
			verifier.change_path([])
			mqtt.arrivedAtLastTag()
			end_reached(state)
			state = "depature"

		if not result:						# Check if the rfid reader is receiving the correct path
			if receive_tag_id:												
				#path, directions = mqtt.getPath(receive_tag_id, previous_tag) # Returns a list
				path = example_cards
				directions = example_direction
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
				if state == "depature" and receive_tag_id == local_file.get_content("depature")[-1]:
					local_file.info(receive_tag_id, 'Card id: ')
					local_file.clear_content()
					local_file.info('', 'End reached')
				print(verifier.retrieved_path)
				print(directions)
				give_directions(directions)
				# geef door: directions

		else:
			print(verifier.retrieved_path)
'''
main()
