
#!/usr/bin/env python

#green/data0 is pin 22
#white/data1 is pin 7
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(17, GPIO.IN)
GPIO.setup(27, GPIO.IN)

bits = ''
timeout = 5
def one(channel):
	global bits
	bits = bits + '1'
	#timeout = 5
   
def zero(channel):
	global bits
	bits = bits + '0'
	#timeout = 5

GPIO.add_event_detect(17, GPIO.FALLING, callback=one)
GPIO.add_event_detect(27, GPIO.FALLING, callback=zero)

print ("Present Card")
while 1:
	if len(bits) == 32:
		print (25 * "-")
		print ("32 Bit Mifare Card")
		print ("Binary:",bits)
		print ("Decimal:",int(str(bits),2))
		print ("Hex:",hex(int(str(bits),2)))
		bits = '0'
		print (25 * "-")
		print ()
		print ("Present Card")
