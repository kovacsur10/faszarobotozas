BCM = "BCM"
OUT = "OUT"

def setmode(mode):
	print "GPIO setmode with param {m}".format(m=mode)
	
def cleanup():
	print "GPIO cleanup"
	
def setup(port, type):
	print "GPIO setup with params {p} {t}".format(p=port, t=type)

class PWM:
	def __init__(self, port, power):
		self.port = port
		print "GPIO setup with params {pt} {pw}".format(pt=port, pw=power)
		
	def start(self, speed):
		print "{pt} starts with speed {s}".format(pt=self.port, s=speed)
	
	def stop(self):
		print "{pt} stops".format(pt=self.port)
		
	def ChangeDutyCycle(self, speed):
		print "{pt} speed {s}".format(pt=self.port, s=speed)