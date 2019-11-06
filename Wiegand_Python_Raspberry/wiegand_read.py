#!/usr/bin/env python

#green/data0 is pin 22
#white/data1 is pin 7
#Note! Use pin 22 not GPIO 22 and use pin 7 not GPIO 7
import time as tm
import RPi.GPIO as GPIO

class Wiegand:
	def __init__ (self, data0 = 11, data1 = 13, bits = '', time_out = 15):
		self.data0 = data0
		self.data1 = data1
		self.bits = bits
		self.time_out = time_out
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

	def read(self):
		if len(self.bits) > 1:
			if len(self.bits) > 32:
					result = self.bits
					#print("Binary: ", bits)
					#print ("Decimal:",int(str(result),2))
					print ("Hex:",hex(int(str(result),2)))
					self.reset()
					return hex(int(str(result),2))
			else:
				print("length is smaller than 32 bits")
				self.reset()
				return 0
		else:
			self.reset()
			#print("received bits: ", len(bits))
			tm.sleep(0.4)
			return 0 
			
class Sleep:
	def sleep(self, sleep_time = 1): # default is on 1 sec
		start = tm.time()
		end_time =  0
		while (sleep_time > end_time):
			end_time = tm.time() - start
			
	
def set_procname(newname):
    from ctypes import cdll, byref, create_string_buffer
    libc = cdll.LoadLibrary('libc.so.6')    #Loading a 3rd party library C
    buff = create_string_buffer(len(newname)+1) #Note: One larger than the name (man prctl says that)
    buff.value = newname                 #Null terminated string as it should be
    libc.prctl(15, byref(buff), 0, 0, 0) #Refer to "#define" of "/usr/include/linux/prctl.h" for the misterious value 16 & arg[3..5] are zero as the man page says.

print("Read card")
wg = Wiegand()
sp = Sleep()
try:
	while True:
		print(wg.read())
		
except KeyboardInterrupt:
	GPIO.cleanup()
	print("Clean exit by user")