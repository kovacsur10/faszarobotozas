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
		self.distanceEpsilon = 3.0
		
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
				try:
					distance += position.getDistanceFrom(self.checkPoint)
				except:
					print "LOL"
			return distance / len(self.positionQueue)
		else:
			return float("inf")
			
	def getAverageAngleToCheckpoint(self):
		if self.checkPoint != None and len(self.positionQueue) != 0:
			distance = 0.0
			for position in self.positionQueue:
				try:
					distance += position.getAngleTo(self.checkPoint)
				except:
					print "LOL angle"
			return distance / len(self.positionQueue)
		else:
			return float("inf")
			
	def resetQueue(self):
		self.positionQueue = deque()
	
	def turnLeftABit(self):
		self.engine.turnLeft(100)
		time.sleep(0.3)
		self.engine.hardStop()
	
	def turnRightABit(self):
		self.engine.turnRight(100)
		time.sleep(0.3)
		self.engine.hardStop()
	
	def turn180degrees(self):
		self.engine.turnLeft(100)
		time.sleep(1)
		self.engine.hardStop()
		
	def test(self):
		self.engine.moveForward(60)
		while self.getAverageDistanceFromCheckpoint() > self.distanceEpsilon:
			self.getLocation()
		
			if len(self.positionQueue) == self.maxPositions:			
				if self.lastDistance < self.getAverageDistanceFromCheckpoint():
					print "WARNING!"
				angle = self.getAverageAngleToCheckpoint()
				if angle < -140.0 or 140.0 < angle:
					self.engine.stop()
					self.turn180degrees()
					self.engine.moveForward(60)
					self.resetQueue()
				elif angle < -20.0:
					self.engine.stop()
					self.turnLeftABit()
					self.engine.moveForward(60)
					self.resetQueue()
				elif 20.0 < angle:
					self.engine.stop()
					self.turnRightABit()
					self.engine.moveForward(60)
					self.resetQueue()
					
				print "angle: {ang} distance: {dist}".format(ang=self.lastAngle, dist=self.lastDistance)
			time.sleep(1)
		self.engine.cleanUp()
		print "Robot is at the checkpoint!"
		
	def killAll(self):
		self.gps.kill()

mind = Mind()
try:
	mind.setNextPoint(Point(19.034780, 47.284399))
	mind.test()
except Exception as ex:
	print type(ex)
finally:
	mind.killAll()
