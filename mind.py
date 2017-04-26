import time
import engine
import gps
from point import Point
from collections import deque

class Mind:
	checkPoint = None
	positionQueue = None # for average counting and movement towards the check point
	maxPositions = 5

	def __init__(self):
		self.engine = engine.Engine()
		self.gps = gps.GPS()
		self.gps.start()
		self.setNextPoint(Point(None, None))
		self.positionQueue = deque()
		self.maxPositions = 5
		
	def setNextPoint(self, checkPoint):
		self.checkPoint = checkPoint
		
	def getLocation(self):
		delta = self.gps.get()
		print delta
		if len(self.positionQueue) == self.maxPositions:
			self.positionQueue.popleft()
		self.positionQueue.append(delta[0])
		
		if len(self.positionQueue) != 0:
			self.positionQueue[-1].print_()
			if self.checkPoint != None:
				self.positionQueue[-1].getAngleTo(self.checkPoint)

	def test(self):
		self.engine.moveForward(60)
		time.sleep(1)
		self.engine.stop()
		time.sleep(2)
		for i in range(1,100):
			self.getLocation()
			time.sleep(1)
		self.engine.cleanUp()

mind = Mind()
mind.setNextPoint(Point(19.034780, 47.284399))
mind.test()
