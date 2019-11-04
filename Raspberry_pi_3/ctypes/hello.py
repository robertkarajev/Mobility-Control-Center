import ctypes

wg = ctypes.CDLL('Wiegand.so')

class Wiegand:
	def __init__(self):
		wg.begin()
		
	def run():
		while True:
			if(wg.available()):
				print(ctypes.c_ulong(wg.getCode()))
			else:
				print("Waiting")
Wiegand.run()