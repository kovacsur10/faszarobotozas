import time
import datetime
import os

class Logger(object):
	console = True
	
	def __init__(self, console = True):
		self.console = console
		
	def log(self, str):
		if self.console:
			print str
		
	def logAction(self, action, param = None):
		tmp = "[" + action + "]"
		if param != None:
			tmp += ": " + str(param)
		self.log(tmp)
	
	def logState(self, position, angle, distance):
		self.log("position: {pos} angle: {ang} distance: {dist}".format(pos=str(position), ang=angle, dist=distance))

class FileLogger(Logger):
	directory = "logs"
	filename = None
	file = None
	
	def __init__(self, console = True):
		super(FileLogger, self).__init__(console)
		if not os.path.exists(self.directory):
			os.makedirs(self.directory)
		self.filename = self.directory + "/log" + datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d_%H%M%S') + ".txt"
		self.file = open(self.filename, "w")
	
	def log(self, str):
		super(FileLogger, self).log(str)
		self.file.write(str + "\n")
	
	def __del__(self):
		self.file.close()