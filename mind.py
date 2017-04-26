import time
import engine
import gps
from point import Point

class Mind:
	checkPoint = None
	currentPosition = None

	def __init__(self):
		self.engine = engine.Engine()
		self.gps = gps.GPS()
		self.gps.start()
		self.setNextPoint(Point(None, None))
		self.currentPosition = None
		
	def setNextPoint(self, checkPoint):
		self.checkPoint = checkPoint
		
	def getLocation(self):
		delta = self.gps.get()
		print delta
		self.currentPosition = delta[0]
		if self.currentPosition != None:
			self.currentPosition.print_()

	def test(self):
		# self.engine.moveForward(60)
		# time.sleep(1)
		# self.engine.stop()
		# time.sleep(2)
		for i in range(1,100):
			self.getLocation()
			time.sleep(1)
		self.engine.cleanUp()

mind = Mind()
mind.test()
