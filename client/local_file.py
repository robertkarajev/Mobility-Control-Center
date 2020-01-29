import os
import json
import datetime as dt

class LocalFile:
	def __init__(self, name = "localinformation"):
			self.name = (name+'.txt')
			self.file = {}
			self.create_file()

	# create txt file if there's a file overwrite else create a new file
	def create_file(self):
		if os.path.isfile(self.name):
			self.info("file already created",self.name)
		else:
			self.info("is created", self.name)
			open(self.name,'w+')

	def write_tags(self, state , rfid_id, directions):
		self.file[state] = []
		self.file[state].append({'date & time': str(dt.datetime.now().strftime('%d/%m/%y ---- %H:%M:%S'))}) # Get current time of register
		self.file[state].append({
			'rfid_tag': rfid_id ,
			'directions':directions
		})
		with open(self.name,'w') as outfile:
			json.dump(self.file,outfile, indent= 2) 

	def car_state(self,state, msg):
		self.file[state].append({
			'state': msg
		})
		with open(self.name,'w') as outfile:
			json.dump(self.file,outfile, indent= 2) 

	def get_content(self, content):
		with open(self.name) as json_file:
			try:
				self.file = json.load(json_file)
				return self.file[str(content)]
			except:
				self.warning(' does not exists', content)

	def clear_content(self):
		f = open(self.name, "w+") # Overwrites the whole file
		f.write('')
		f.close()

	def update(self, info, topic =''):
		print('[UPDATE]  ', topic, info)

	def info(self, info, topic =''):
		print('[INFO]    ', topic, info)

	def warning(self, info, topic =''):
		print('[WARNING] ', topic, info)

	def error(self, info, topic =''):
		print('[ERROR]   ', topic, info)