#!/usr/bin/env python

#green/data0 is pin 11
#white/data1 is pin 13
#For Example Use pin 22 not GPIO 22 and use pin 7 not GPIO 7
import time as tm
import RPi.GPIO as GPIO

class Wiegand:
	def __init__ (self, proc_name = 'wiegand' ,data0 = 11, data1 = 13, bits = ''):
		self.proc_name = proc_name
		self.data0 = data0
		self.data1 = data1
		self.bits = bits
		self.setup()
	
	def setup (self):
		GPIO.setmode(GPIO.BOARD) #BCM or BOARD
		GPIO.setup (self.data0, GPIO.IN, pull_up_down = GPIO.PUD_UP)
		GPIO.setup (self.data1, GPIO.IN, pull_up_down = GPIO.PUD_UP)
		GPIO.add_event_detect (self.data0, GPIO.FALLING, callback = self.channel_zero)
		GPIO.add_event_detect (self.data1, GPIO.FALLING, callback = self.channel_one)

	def channel_zero (self, channel):
		self.bits +='0'
	
	def channel_one (self, channel):
		self.bits +='1'
	
	def set_procname(self):
		from ctypes import cdll, byref, create_string_buffer
		libc = cdll.LoadLibrary('libc.so.6')    #Loading a 3rd party library C
		buff = create_string_buffer(len(self.proc_name)+1) #Note: One larger than the name (man prctl says that)
		buff.value = self.proc_name                 #Null terminated string as it should be
		libc.prctl(15, byref(buff), 0, 0, 0) #Refer to "#define" of "/usr/include/linux/prctl.h" for the misterious
	
	def verify(self, binary_string):
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
				#n, hex_compressed = hex_string.split('0x')
				hex_compressed = hex_string[2:10] # Removing 0x from each incoming card
 				#print('binary: ' + bin)
				#print('decimal: ' , int(bin,2)) 
				#print('hex: ' , hex(int(bin,2)))  
				self.bits = ''
				return hex_compressed
	
	def run (self):
		try:			
			data = self.verify (self.bits)
			print ('Card id: ', data)
			tm.sleep (0.1)
			return data
			
		except KeyboardInterrupt:
			GPIO.cleanup ()
			print ("Clean exit by user")

class ParkingAuthenticator:
	def __init__ (self, scanned_id = [], uid = '' , retrieved_id = [])
		self.scanned_id = scanned_id
		self.uid = uid
		self.retrieved_id = retrieved_id
		
	def select_next_card (self):
		pass
	
	def get_new_path(self):
		pass
	
	def verify_path (self):
		pass
	
print ("Read card")
wg = Wiegand ('wiegand', 11, 13)
while True:
	wg.run()
