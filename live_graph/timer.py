import time as tm
class Sleep:
	def sleep(self, sleep_time = 1): # default is on 1 sec
		start = tm.time()
		end_time =  0
		while (sleep_time > end_time):
			end_time = tm.time() - start
			
