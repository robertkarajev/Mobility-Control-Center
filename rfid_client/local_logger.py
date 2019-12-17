import os
import json
import datetime as dt

# Write, Get , create , delete (TO DO LIST)

#	Beginning -> create and write list onto the file 	//	Logger
#	Destination reached -> Remember second to last tag and request new path // rfid_reader 
#	OR on startup request on the parkingspot request new path // or when destination reached // validation on the rfid_reader

#	When end reached -> delete file // In rfid_reader file

class LocalLogger:
	def __init__(self, name = "log"):
			self.name = (name+'.txt')
			self.log = {}
			self.create_file()


	def create_file(self):
		if os.path.isfile(self.name):
			open(self.name,'w')
		else:
			print("File doesn't exist.\nFile: "+ self.name +" will be created")
			open(self.name,'w+')

	def write_file(self, state , rfid_id):
		self.log[state] = []
		self.log[state].append({'date & time': str(dt.datetime.now().strftime('%d/%m/%y ---- %H:%M:%S'))})
		for i in range(len(rfid_id)):
			self.log[state].append({
				'rfid_tag': rfid_id[i] ,
			})
			with open(self.name,'w') as outfile:
				json.dump(self.log,outfile, indent= 2)

	def get_content(self, content):
		with open(self.name) as json_file:
			try:
				self.log = json.load(json_file)
				return self.log[str(content)]
			except:
				print("Value: "+content+" doesn't exist!")

	def delete_file(self):
		os.remove(self.name)
