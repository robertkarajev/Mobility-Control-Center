#green/data0 is pin 11
#white/data1 is pin 13
#For Example Use pin 22 not GPIO 22 and use pin 7 not GPIO 7
import time as tm
import sys
import RPi.GPIO as GPIO

class Wiegand:
	def __init__ (self, proc_name = 'wiegand' ,data0 = 11, data1 = 13, bits = ''):
		self.proc_name = proc_name			# Process for wiegand protocol
		self.data0 = data0					# pin for Data 0 
		self.data1 = data1					# pin for Data 1 
		self.bits = bits
		
		self.previous_id = ""
		
		self.setup()
	
	def setup (self):
		GPIO.setmode(GPIO.BOARD) 														 #BCM or BOARD
		GPIO.setup (self.data0, GPIO.IN, pull_up_down = GPIO.PUD_UP)					 # Retrieve data 0
		GPIO.setup (self.data1, GPIO.IN, pull_up_down = GPIO.PUD_UP) 					 # Retrieve data 1
		GPIO.add_event_detect (self.data0, GPIO.FALLING, callback = self.channel_zero) 	 # Checks incoming data from data 0
		GPIO.add_event_detect (self.data1, GPIO.FALLING, callback = self.channel_one)	 # Checks incoming data from data 1

	def channel_zero (self, channel):
		self.bits +='0'
	
	def channel_one (self, channel):
		self.bits +='1'
	
	def set_procname(self):
		from ctypes import cdll, byref, create_string_buffer
		libc = cdll.LoadLibrary('libc.so.6')   				 #Loading a 3rd party library C
		buff = create_string_buffer(len(self.proc_name)+1) 	 #Note: One larger than the name (man prctl says that)
		buff.value = self.proc_name                			 #Null terminated string as it should be
		libc.prctl(15, byref(buff), 0, 0, 0) 				 #Refer to "#define" of "/usr/include/linux/prctl.h" for the misterious
	
	def retrieve_id(self, binary_string = ''):
		first_part = binary_string[0:13]
		second_part = binary_string[13:0]
		parts = [first_part, second_part]
		bitsTo1 = [0, 0]
		index = 0	
	
		for part in parts:
			bitsTo1[index] = part.count('1')
			index += 1
		
		if bitsTo1[0] % 2 != 0 or bitsTo1[1] % 2 != 1:
			bin = binary_string[1:-1] # Leaving out the first and last bit
			
			if len(bin) == 32:
				hex_string = str(hex(int(bin,2)))
				hex_compressed = hex_string[2:10] # Removing 0x from each incoming card
				
				print('hex: ' , hex(int(bin,2)))  
				
				self.bits = ''
				return hex_compressed
	
	def get_previous_id(self, id):
		
		if id:	
			print("here", id)
			if self.previous_id != id:
				return_old_id = self.previous_id
				self.previous_id = id
				return return_old_id	

	def run(self):
		new_id = self.retrieve_id(self.bits)
		previous_id = self.get_previous_id(new_id)
		tm.sleep(0.01)
		return new_id, previous_id	

class ParkingVerifier:
	def __init__ (self, retrieved_path):
		self.retrieved_path = retrieved_path 			# Retrieve path from server
		
	def verify_path (self, msg):
# If retrieved_path contains any incoming msg from the RFID, remove msg from retrieve_id
		if msg is self.retrieved_path[-1]:
			return 'lastTag'
		if msg in self.retrieved_path:
			self.retrieved_path.remove(msg)
			return True
	
	def change_path (self, path):
		self.retrieved_path = path
		
'''
print ("Read card")
wg = Wiegand ()
while True:
	try:
		data, old_data = wg.run()
		if data:
			print("New: ",data, " Old: ", old_data)
	except KeyboardInterrupt:
		GPIO.cleanup ()
		print ("Clean exit by user")
		sys.exit()
'''
