import random
import time

PARITY_NONE = "PARITY_NONE"
STOPBITS_ONE = "STOPBITS_ONE"
EIGHTBITS = "EIGHTBITS"

class Serial:
	def __init__(self, port, baudrate, parity, stopbits, bytesize, timeout):
		self.time = random.randint(1,2200)
		print "Serial init"
		
	def readline(self):
		north = random.randint(80,99)
		east = random.randint(60, 80)
		time.sleep(0.8)
		self.time = self.time + 1
		return "$GPGGA,{t}.000,4728.43{no},N,01903.47{ea},E,1,5,1.69,73.8,M,41.1,M,,*60".format(t=self.time, no=north, ea=east)