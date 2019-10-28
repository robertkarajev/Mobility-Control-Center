
#weigand.py - read card IDs from a wiegand card reader
#(C) 2017 Paul Jimenez - released under LGPLv3+

import time as tm
from time import sleep
import RPi.GPIO as GPIO

CARD_MASK = 0b11111111111111110 # 16 ones
FACILITY_MASK = 0b1111111100000000000000000 # 8 ones
start = tm.time()
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
# Max pulse interval: 2ms
# pulse width: 50us

class Wiegand:
	def __init__(self, pin0, pin1, callback):
		self.pin0 = GPIO.setup(pin0, GPIO.OUT)
		self.pin1 = GPIO.setup(pin1, GPIO.OUT)
		self.last_card = None
		self.next_card = 0
		self._bits = 0
		self.last_bit_read = None
		self.callback = callback
		#self.pin0.irq(trigger=Pin.IRQ_FALLING, handler=self._on_pin0)
		#self.pin1.irq(trigger=Pin.IRQ_FALLING, handler=self._on_pin1)
		#self.timer = Timer(-1)
		#self.timer.init(period=50, mode=Timer.PERIODIC, callback=self._cardcheck)
		self.timer(0.05, callback= self._cardcheck)
		self.cards_read = 0

	def _on_pin0(self, newstate): self._on_pin(0, newstate)
	def _on_pin1(self, newstate): self._on_pin(1, newstate)
	
	def timer(self, given_time= 1, callback= None):
		sleep(given_time)
		
	def _on_pin(self, is_one, newstate):
		now = tm.time()-start
		if self.last_bit_read is not None and now - self.last_bit_read < 2:
		# too fast
			return
		self.last_bit_read = now
		self.next_card <<= 1
		if is_one: self.next_card |= 1
		self._bits += 1
	def get_card(self):
		if self.last_card is None:
			return None
		return ( self.last_card & CARD_MASK ) >> 1
        
	def get_facility_code(self):
		if self.last_card is None:
			return None
		# Specific to standard 26bit wiegand
		return ( self.last_card & FACILITY_MASK ) >> 17

	def _cardcheck(self, t):
		if self.last_bit_read is None: return
		now = tm.time()-start
		if now - self.last_bit_read > 50:
			# too slow - new start!
			self.last_bit_read = None
			self.last_card = self.next_card
			self.next_card = 0
			self._bits = 0
			self.cards_read += 1
			self.callback(self.get_card(), self.get_facility_code(), self.cards_read)