import time
import datetime
import os

class Logger(object):
	console = True
	
	def __init__(self, console = True):
		self.console = console
		
	def log(self, msg):
		if self.console:
			print msg
		
	def logAction(self, action, param = None):
		tmp = "[" + action + "]"
		if param != None:
			tmp += ": " + str(param)
		self.log(tmp)
	
	def logState(self, position, angle, angleToCheckpoint, distance):
		self.log("position: {pos} angle: {ang} angleToCheckpoint: {acheck} distance: {dist}".format(pos=str(position),
							ang=angle, acheck = angleToCheckpoint, dist=distance))

	def logWarning(self, msg):
		self.log("WARNING: " + msg)

class FileLogger(Logger):
	directory = "logs"
	filename = None
	file = None
	
	def __init__(self, console = True):
		super(FileLogger, self).__init__(console)
		if not os.path.exists(self.directory):
			os.makedirs(self.directory)
		self.filename = self.directory + "/log" \
				+ datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d_%H%M%S') \
				+ ".txt"
		self.file = open(self.filename, "w")
	
	def log(self, msg):
		super(FileLogger, self).log(msg)
		self.file.write(msg + "\n")
	
	def __del__(self):
		self.file.close()