import os
import json

# Write, Get , create , delete (TO DO LIST)

#	Beginning -> create and write list onto the file 	//	Logger
#	Destination reached -> Remember second to last tag and request new path // rfid_reader 
#	OR on startup request on the parkingspot request new path // or when destination reached // validation on the rfid_reader

#	When end reached -> delete file // In rfid_reader file

class LocalLogger:
	def __init__(self, name = 'log'):
			self.name = (name+'.txt')
			self.log = {}
			self.log['parking_lot'] = []

	def create_file(self):
		if os.path.isfile(self.name):
			open(self.name,'w')
		else:
			print("File doesn't exist.\n','File will be created")
			open(self.name,'w+')

	def write_file(self, id ,coordinates):
		for i in range(len(id)):
			self.log['parking_lot'].append({
				'rfid_tag': id[i] ,
				'coordinates' :coordinates[i]
			})
			with open(self.name,'w') as outfile:
				json.dump(self.log,outfile, indent= 2)

	def get_content(self):
		with open(self.name) as json_file:
			self.log = json.load(json_file)
			return self.log['parking_lot']

	def delete_file(self):
		os.remove(self.name)
