import time
import engine
import gps
from point import Point
from collections import deque
import logger
import traceback

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
		self.checkPoint = Point(None, None)
		self.positionQueue = deque()
		self.maxPositions = 5
		self.lastPosition = Point(None, None)
		self.lastDistance = float("inf")
		self.lastAngle = float("inf")
		#self.distanceEpsilon = 3.0
		self.distanceEpsilon = 0.0
		self.logger = logger.FileLogger()
		
	def setNextPoint(self, checkPoint):
		self.checkPoint = checkPoint
		self.logger.logAction("setNextPoint", checkPoint)
		
	def getLocation(self):
		self.lastDistance = self.getAverageDistanceFromCheckpoint()
		self.lastAngle = self.getAverageAngleToCheckpoint()
		
		delta = self.gps.get()
		self.lastPosition = delta[0]
		self.logger.logAction("getLocation", self.lastPosition)
		
		if len(self.positionQueue) == self.maxPositions:
			self.positionQueue.popleft()
		self.positionQueue.append(self.lastPosition)
		
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
					self.logger.log("LOL")
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
					self.logger.log("LOL angle")
			return distance / len(self.positionQueue)
		else:
			return float("inf")
			
	def resetQueue(self):
		self.positionQueue = deque()
	
	def turnLeftABit(self):
		self.logger.logAction("turnLeftABit")
		self.engine.turnLeft(100)
		time.sleep(0.3)
		self.engine.hardStop()
	
	def turnRightABit(self):
		self.logger.logAction("turnRightABit")
		self.engine.turnRight(100)
		time.sleep(0.3)
		self.engine.hardStop()
	
	def turn180degrees(self):
		self.logger.logAction("turn180degrees")
		self.engine.turnLeft(100)
		time.sleep(1)
		self.engine.hardStop()
		
	def moveForward(self):
		self.logger.logAction("moveForward")
		self.engine.moveForward(60)
		self.resetQueue()
		
	def test(self):
		self.engine.moveForward(60)
		while self.getAverageDistanceFromCheckpoint() > self.distanceEpsilon:
			self.getLocation()
		
			if len(self.positionQueue) == self.maxPositions:			
				if self.lastDistance < self.getAverageDistanceFromCheckpoint():
					self.logger.log("WARNING: Wrong way!")
				angle = self.getAverageAngleToCheckpoint()
				if angle < -140.0 or 140.0 < angle:
					self.engine.stop()
					self.turn180degrees()
					self.moveForward()
				elif angle < -20.0:
					self.engine.stop()
					self.turnLeftABit()
					self.moveForward()
				elif 20.0 < angle:
					self.engine.stop()
					self.turnRightABit()
					self.moveForward
					
				#print "angle: {ang} distance: {dist}".format(ang=self.lastAngle, dist=self.lastDistance)
				self.logger.logState(self.lastPosition, self.lastAngle, self.lastDistance)
			time.sleep(1)
		self.engine.cleanUp()
		self.logger.log("Robot is at the checkpoint!")
		
	def killAll(self):
		self.gps.kill()

mind = Mind()
try:
	mind.setNextPoint(Point(19.034780, 47.284399))
	mind.test()
except Exception as ex:
	#print type(ex)
	traceback.print_exc()
finally:
	mind.killAll()
