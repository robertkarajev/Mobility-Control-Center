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

def give_directions(path):
	length = ''
	destination = []
	directions = []
	direct = ['V', 'R', 'B', 'L'] # Directions/ Forward, Right, Reverse, left
	for i in path:
		for j in direct:
			if j in i:
				length = i.split(j)
				destination.append(length[0]) 
				directions.append(j)
	return length, directions

def get_rfid_tag():
	next_tag, previous_tag = receive_data.run() # Get current and previous tag in a tuple
	if next_tag:
		local_file.info(next_tag, "Card id: ")
		return next_tag, previous_tag
	return next_tag, previous_tag

def commands(command, angle): # This function is still in WIP, it can be used for commanding the vehicle
	if command == 'left':
		print('turning left')
	if command == 'right':
		print('turning right')
	if command == 'reverse':
		print('turning reverse')

# Whenever the vehicle starts up it will check if the vehicle already have a given path/is leaving.
def start_up(): 
	local_list = []
	local_path = [] 
	if local_file.get_content('Depature'):
		local_list = local_file.get_content("Depature")[1].get("rfid_tag") # Give saved path to the vehicle 
		local_path = local_file.get_content("Depature")[1].get("directions")

	elif local_file.get_content('Arrival'): # if arrival return this path
		local_list = local_file.get_content("Arrival")[1].get("rfid_tag")
		local_path = local_file.get_content("Arrival")[1].get("directions")
	return local_list, local_path

def end_reached():
	try:
		if local_file.get_content("Arrival")[2].get("state") == "True":
			local_file.info(local_file.get_content("Depature")[1].get("rfid_tag")[-1],'End reached, last known rfid: ')
			local_file.clear_content() # Wipes out localinformation.txt about the path
	except:
		pass

def main():
	local_save = start_up()
	verifier.change_path(local_save)
	state = 'Depature' if local_file.get_content("Depature") else 'Arrival'

	while True:
		receive_tag, previous_tag = get_rfid_tag()
		if not receive_tag.startswith('5c'):
			continue
		result = verifier.verify_path(receive_tag)

		if result == 'lastTag':
			verifier.change_path([])  # Requires a blank list returned else expection will occur
			mqtt.arrivedAtLastTag()  # Changes state from arrival to parked or departure to left the parkinglot
			state = 'Depature'
			local_file.write_tags(state, [], [])
			end_reached()
			local_file.car_state(state, "True")

		if not result:
			if receive_tag:
				path, directions = mqtt.getPath(receive_tag, previous_tag) # Returns a path from the server side with directions
				local_file.write_tags(state,path, directions) # Writes the path and state of the vehicle in the localinformation.txt.
				verifier.change_path(path) # Updates current path
				verifier.verify_path(receive_tag) # Check if the vehicle is riding accordingly in comparison with generated path 
			
				#if state == "Depature" and receive_tag == local_file.get_content("Arrival")[1].get("rfid_tag")[-2]:
				#	print('stop reverse, try rotating') 
				try:
					if receive_tag == local_file.get_content("Arrival")[1].get("rfid_tag")[-1]:
						local_file.info(receive_tag, 'Card id: ')
						state = "Depature"

					if state == "Depature" and receive_tag == local_file.get_content("Arrival")[1].get("rfid_tag")[-1]: # get new path when the vehicle starts up
						local_file.write_tags(state,path, directions)
						verifier.change_path(path) 	
						local_file.info(directions,"Directions given: ")

				except:
					local_file.warning(state, "doesn't exist.")
				local_file.update(verifier.retrieved_path,(state+" path: "))
				local_file.info(directions,"Directions given: ")
				give_directions(directions)
			
		else:
			local_file.info(verifier.retrieved_path, (state+" path: "))
main()
