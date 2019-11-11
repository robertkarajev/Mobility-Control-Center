#!/usr/bin/env python

#green/data0 is pin 11
#white/data1 is pin 13
#For Example Use pin 22 not GPIO 22 and use pin 7 not GPIO 7
import time as tm
import RPi.GPIO as GPIO

class Wiegand:
	def __init__ (self, proc_name = 'wiegand' ,data0 = 11, data1 = 13, bits = '', stored_bits = '', timeout = 5):
		self.proc_name = proc_name
		self.data0 = data0
		self.data1 = data1
		self.stored_bits = stored_bits
		self.bits = bits
		self.timeout = timeout
		self.setup()
		self.channel()
	
	def setup (self):
		GPIO.setmode(GPIO.BOARD) #BCM or BOARD
		GPIO.setup (self.data0, GPIO.IN, pull_up_down = GPIO.PUD_UP)
		GPIO.setup (self.data1, GPIO.IN, pull_up_down = GPIO.PUD_UP)
	
	def channel (self):
		GPIO.add_event_detect (self.data0, GPIO.FALLING, callback = self.channel_zero)
		GPIO.add_event_detect (self.data1, GPIO.FALLING, callback = self.channel_one)

	def channel_zero (self, channel):
		self.bits = self.bits + '0'
	
	def channel_one (self, channel):
		self.bits = self.bits + '1'

	def reset(self):
		self.bits = ''
		self.timeout = 5
	
	def set_procname(self):
		from ctypes import cdll, byref, create_string_buffer
		libc = cdll.LoadLibrary('libc.so.6')    #Loading a 3rd party library C
		buff = create_string_buffer(len(self.proc_name)+1) #Note: One larger than the name (man prctl says that)
		buff.value = self.proc_name                 #Null terminated string as it should be
		libc.prctl(15, byref(buff), 0, 0, 0) #Refer to "#define" of "/usr/include/linux/prctl.h" for the misterious

	def store_bits(self, incoming_bits):
		self.stored_bits = incoming_bits
	
	def read(self):
		if self.bits:
			self.timeout = self.timeout - 1
			tm.sleep(0.001)
			
			if len(self.bits) >= 1 and self.timeout == 0:
					print(len(self.bits))
					result = int(str(self.bits),2)
					if result > 1:
						print('dec: ',result)
						print('hex: ',hex(result))
						#hex_string = str(hex(result))
						#print(type(str(hex(int(str(result),2)))))# binary -> string -> decimal , hex , string 
						#n , string = hex_string.split('0x')
						#print(string)
						self.reset()
					else:
						self.reset()
					#return string
			#else:
				#print("Bad reading")
				#self.reset()
		else:
			#self.reset()
			tm.sleep(0.001)

print("Read card")
wg = Wiegand()

try:
	while True:
		#print(wg.read())
		wg.read()
		
except KeyboardInterrupt:
	GPIO.cleanup()
	print("Clean exit by user")