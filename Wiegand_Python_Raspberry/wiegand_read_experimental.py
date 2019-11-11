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
		self.channel()
	
	def setup (self):
		GPIO.setmode(GPIO.BOARD) #BCM or BOARD
		GPIO.setup (self.data0, GPIO.IN, pull_up_down = GPIO.PUD_UP)
		GPIO.setup (self.data1, GPIO.IN, pull_up_down = GPIO.PUD_UP)
	
	def channel (self):
		GPIO.add_event_detect (self.data0, GPIO.FALLING, callback = self.channel_zero)
		GPIO.add_event_detect (self.data1, GPIO.FALLING, callback = self.channel_one)

	def channel_zero (self, channel):
		self.bits +='0'
	
	def channel_one (self, channel):
		self.bits +='1'

	def reset(self):
		self.bits = ''	
	
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
			print("Frame of length (" + str(len(self.tag)) + "): " + self.tag + " (" + str(self.binaryToInt(self.tag)) + ") - PARITY CHECK FAILED")
			return False
		return True
			
	def process_tag(self):
		if self.tag == '':
			return
		elif (len(self.tag) < 10):
			print("[" + self.name + "] Frame of length (" + str(len(self.tag)) + "):" + self.tag + " DROPPED")
		elif self.verify(self.bits):
			print("Frame of length (" + str(len(self.tag)) + "): " + self.tag + " (" + str(self.binaryToInt(self.tag)) + ") OK KOI" )
	
	@staticmethod
	def binaryToInt(binary_string):
		print(binary_string)
		binary_string = binary_string[1:-1] #Removing the first and last bit (Non-data bits)
		print(binary_string)
		result = int(binary_string, 2)
		return result
		
	def read(self):
		if len(self.bits) > 1:
			if len(self.bits) >= 32 and len(self.bits) <= 34:
					result = self.bits
					hex_string = str(hex(int(str(result),2)))
					#print(type(str(hex(int(str(result),2)))))# binary -> string -> decimal , hex , string 
					n , string = hex_string.split('0x')
					self.reset()
					return string
			else:
				print("Bad reading")
				self.reset()
		else:
			self.reset()
			tm.sleep(0.4)
	def run(self):
		try:
			while True:
				#print(wg.read())
				self.verify(self.bits)
				tm.sleep(0.1)
			
		except KeyboardInterrupt:
			GPIO.cleanup()
			print("Clean exit by user")
	
print("Read card")
Wiegand.run()
