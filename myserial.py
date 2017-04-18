import random
import time

PARITY_NONE = "PARITY_NONE"
STOPBITS_ONE = "STOPBITS_ONE"
EIGHTBITS = "EIGHTBITS"

class Serial:
	def __init__(self, port, baudrate, parity, stopbits, bytesize, timeout):
		self.time = random.randint(1,2200)
		self.lastNorth = 90
		self.lastEast = 70
		print "Serial init"
		
	# 1/100 esellyel lehet nagyon rossz
	# 1/8 esellyel lehet rossz a hatarokon belul
	# amugy pedig viszonylag pontos eredmenyt ad
	def readline(self):
		bad = random.randint(1,100)
		if bad == 1:
			north = random.randint(1,99)
			east = random.randint(1, 99)
		else:
			bad = random.randint(1,8)
			if bad == 1:
				north = random.randint(80,99)
				east = random.randint(60, 80)
			else:
				minNorth = self.lastNorth - 3
				maxNorth = self.lastNorth + 3
				minEast = self.lastEast - 3
				maxEast = self.lastEast + 3
				if minNorth < 80:
					minNorth = 80
				if maxNorth > 99:
					maxNorth = 99
				if minEast < 60:
					minEast = 60
				if maxEast > 80:
					maxEast = 80
				north = random.randint(minNorth, maxNorth)
				east = random.randint(minEast, maxEast)
		time.sleep(0.5)
		self.time = self.time + 1
		self.lastNorth = north
		self.lastEast = east
		return "$GPGGA,{t}.000,4728.43{no},N,01903.47{ea},E,1,5,1.69,73.8,M,41.1,M,,*60".format(t=self.time, no=north, ea=east)