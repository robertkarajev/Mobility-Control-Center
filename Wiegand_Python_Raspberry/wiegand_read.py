#!/usr/bin/env python

#green/data0 is pin 22
#white/data1 is pin 7
#Note! Use pin 22 not GPIO 22 and use pin 7 not GPIO 7
import time
import RPi.GPIO as GPIO

class Wiegand:
	def __init__ (self, data0 = 22, data1 = 7, bits = ''):
		self.data0 = data0
		self.data1 = data1
		self.bits = bits
		GPIO.setmode(GPIO.BOARD) #BCM or BOARD
		self.setup()
		self.channel()
	
	def setup (self):
		GPIO.setup (self.data0, GPIO.IN, pull_up_down = GPIO.PUD_UP)
		GPIO.setup (self.data1, GPIO.IN, pull_up_down = GPIO.PUD_UP)
	
	def channel (self):
		GPIO.add_event_detect (self.data0, GPIO.FALLING, callback = self.channel_zero)
		GPIO.add_event_detect (self.data1, GPIO.FALLING, callback = self.channel_one)

	def channel_zero (self, channel):
		self.bits = self.bits + '0'
	
	def channel_one (self, channel):
		self.bits = self.bits + '1'
	
	def __str__(self):
		return str(self.bits)

def set_procname(newname):
    from ctypes import cdll, byref, create_string_buffer
    libc = cdll.LoadLibrary('libc.so.6')    #Loading a 3rd party library C
    buff = create_string_buffer(len(newname)+1) #Note: One larger than the name (man prctl says that)
    buff.value = newname                 #Null terminated string as it should be
    libc.prctl(15, byref(buff), 0, 0, 0) #Refer to "#define" of "/usr/include/linux/prctl.h" for the misterious value 16 & arg[3..5] are zero as the man page says.
    	
print("Read card")
wg = Wiegand()
print(wg)
while True:
	bits = int(wg)
	
	if bits > 1:
		print(hex(bits))
