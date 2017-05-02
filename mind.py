import time
import engine
import gps
from point import Point
from collections import deque

class Mind:
	checkPoint = None
	positionQueue = None # for average counting and movement towards the check point
	maxPositions = 5
	
	lastDistance = float("inf")
	lastAngle = float("inf")

	def __init__(self):
		self.engine = engine.Engine()
		self.gps = gps.GPS()
		self.gps.start()
		self.setNextPoint(Point(None, None))
		self.positionQueue = deque()
		self.maxPositions = 5
		self.lastDistance = float("inf")
		self.lastAngle = float("inf")
		
	def setNextPoint(self, checkPoint):
		self.checkPoint = checkPoint
		
	def getLocation(self):
		self.lastDistance = self.getAverageDistanceFromCheckpoint()
		self.lastAngle = self.getAverageAngleToCheckpoint()
		
		delta = self.gps.get()
		if len(self.positionQueue) == self.maxPositions:
			self.positionQueue.popleft()
		self.positionQueue.append(delta[0])
		
		if len(self.positionQueue) != 0:
			self.positionQueue[-1].print_()
			if self.checkPoint != None:
				self.positionQueue[-1].getAngleTo(self.checkPoint)
				
	def getAverageDistanceFromCheckpoint(self):
		if self.checkPoint != None and len(self.positionQueue) != 0:
			distance = 0.0
			for position in self.positionQueue:
				distance += position.getDistanceFrom(self.checkPoint)
			return distance / len(self.positionQueue)
		else:
			return float("inf")
			
	def getAverageAngleToCheckpoint(self):
		if self.checkPoint != None and len(self.positionQueue) != 0:
			distance = 0.0
			for position in self.positionQueue:
				distance += position.getAngleTo(self.checkPoint)
			return distance / len(self.positionQueue)
		else:
			return float("inf")
	
	def turnLeftABit(self):
		self.engine.turnLeft(100)
		time.sleep(1)
		self.engine.hardStop()
	
	def turnRightABit(self):
		self.engine.turnRight(100)
		time.sleep(1)
		self.engine.hardStop()
	
	def turn180degrees(self):
		self.engine.turnLeft(100)
		time.sleep(3)
		self.engine.hardStop()
		
	def test(self):
		self.engine.moveForward(60)
		time.sleep(1)
		self.engine.stop()
		time.sleep(2)
		for i in range(1,100):
			self.getLocation()
			if self.lastDistance < self.getAverageDistanceFromCheckpoint():
				print "WARNING!"
			angle = self.getAverageAngleToCheckpoint()
			if angle < -160.0 or 160.0 < angle:
				self.turn180degrees()
			elif angle < -20.0:
				self.turnLeftABit()
			elif 20.0 < angle:
				self.turnRightABit()
				
			print "{ang} {dist}".format(ang=self.lastAngle, dist=self.lastDistance)
			time.sleep(1)
		self.engine.cleanUp()

mind = Mind()
mind.setNextPoint(Point(19.034780, 47.284399))
mind.test()
