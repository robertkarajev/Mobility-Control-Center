import os
import json
import datetime as dt

class LocalFile:
	def __init__(self, name = "localinformation"):
			self.name = (name+'.txt')
			self.file = {}
			self.create_file()

	def create_file(self):
		if os.path.isfile(self.name):
			open(self.name,'w')
		else:
			self.info("is created", self.name)
			open(self.name,'w+')

	def write_file(self, state , rfid_id):
		self.file[state] = []
		self.file[state].append({'date & time': str(dt.datetime.now().strftime('%d/%m/%y ---- %H:%M:%S'))})
		for i in range(len(rfid_id)):
			self.file[state].append({
				'rfid_tag': rfid_id[i] ,
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
		f = open(self.name, "w+")
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