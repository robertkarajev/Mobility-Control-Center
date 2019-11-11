#!/usr/bin/env python

#green/data0 is pin 22
#white/data1 is pin 7
import time
import RPi.GPIO as GPIO

D0 = 11
D1 = 13
bits = ''
t = 15
timeout = t

GPIO.setmode(GPIO.BOARD)
GPIO.setup(D0, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(D1,GPIO.IN, pull_up_down=GPIO.PUD_UP)

def set_procname(newname):
	from ctypes import cdll, byref, create_string_buffer
	libc = cdll.LoadLibrary('libc.so.6')    #Loading a 3rd party library C
	buff = create_string_buffer(len(newname)+1) #Note: One larger than the name (man prctl says that)
	buff.value = newname                 #Null terminated string as it should be
	libc.prctl(15, byref(buff), 0, 0, 0) #Refer to "#define" of "/usr/include/linux/prctl.h" for the misterious value 16 & arg[3..5] are zero as the man page says.
    
def one(channel):
	global bits
	#print("one: ", one)
	global timeout
	bits = bits + '1'
	timeout = t
    
def zero(channel):
	global bits
	#print("zero: ",bits)
	global timeout
	bits = bits + '0'
	timeout = t

def main():
	global bits
	#print("main: ",bits)
	global timeout
	GPIO.add_event_detect(D0, GPIO.FALLING, callback=zero)
	GPIO.add_event_detect(D1, GPIO.FALLING, callback=one)
	while 1:
		#print("before while: ", bits)
		if bits:
			#print("after while: ", bits)
			timeout = timeout -1
			time.sleep(0.001)
			if len(bits) > 1 and timeout == 0:
				#print "Binary:",bits
				result = int(str(bits),2)
				#print("after len: ", bits)
				if result > 1: # the number of my test badge
					#print("after results: ", bits)
					bits = '0'
					print (result)
					print (hex(result))
				else:
					bits = '0'
					timeout = t
					print ("Bad Read")
		else:
			time.sleep(0.001)



if __name__ == '__main__':
	main()