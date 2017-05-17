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
		self.gpsFrequency = 0.5
		self.gps = gps.GPS(self.gpsFrequency)
		self.gps.start()
		self.logger = logger.FileLogger()
		
		self.checkPoint = Point(None, None)
		self.positionQueue = deque()
		self.maxPositions = 5
		self.distanceEpsilon = 3.0
		
		self.lastPosition = Point(None, None)
		self.lastAngle = float("inf")
		self.lastDistance = float("inf")
		self.lastAngleToCheckpoint = float("inf")
		
		self.currentPosition = Point(None, None)
		self.currentAngle = float("inf")
		self.currentDistance = float("inf")
		self.currentAngleToCheckpoint = float("inf")
		
		time.sleep(1.5*self.gpsFrequency)
		self.collectPositions()
		
	def setNextPoint(self, checkPoint):
		self.checkPoint = checkPoint
		self.logger.logAction("setNextPoint", checkPoint)
		
	def getLocation(self):
		delta = self.gps.get()
		self.logger.logAction("getLocation", delta[0])
		
		if len(self.positionQueue) == self.maxPositions:
			self.positionQueue.popleft()
		self.positionQueue.append(delta[0])
		
	def getAverageDistanceFromCheckpoint(self):
		if not self.checkPoint.isNone() and len(self.positionQueue) != 0:
			distance = 0.0
			for position in self.positionQueue:
				try:
					distance += position.getDistanceFrom(self.checkPoint)
				except:
					self.logger.logWarning("None Distance")
			return distance / len(self.positionQueue)
		else:
			return float("inf")
			
	def getAverageAngleToCheckpoint(self):
		if not self.checkPoint.isNone() and len(self.positionQueue) != 0:
			angle = 0.0
			for position in self.positionQueue:
				try:
					angle += position.getAngleTo(self.checkPoint)
				except:
					self.logger.logWarning("None Checkpoint Angle")
			return angle / len(self.positionQueue)
		else:
			return float("inf")
			
	def getAveragePosition(self):
		if len(self.positionQueue) != 0:
			x = 0.0
			y = 0.0
			for position in self.positionQueue:
				try:
					x += position.x
					y += position.y
				except:
					self.logger.logWarning("None Position")
			n = len(self.positionQueue)
			return Point(x / n, y / n)
		else:
			return Point(None, None)
		
	def getAverageAngle(self):
		if not self.lastPosition.isNone() and len(self.positionQueue) != 0:
			angle = 0.0
			for position in self.positionQueue:
				try:
						angle += self.lastPosition.getAngleTo(position)
				except:
					self.logger.logWarning("None Angle")
			return angle / len(self.positionQueue)
		else:
			return float("inf")
			
	def collectPositions(self):
		self.lastPosition = self.currentPosition
		self.lastDistance = self.currentDistance
		self.lastAngle = self.currentAngle
		self.lastAngleToCheckpoint = self.currentAngleToCheckpoint
		
		self.resetQueue()
		while len(self.positionQueue) != self.maxPositions:
			self.getLocation()
			time.sleep(1.5*self.gpsFrequency)
		
		self.currentPosition = self.getAveragePosition()
		self.currentDistance = self.getAverageDistanceFromCheckpoint()
		self.currentAngle = self.getAverageAngle()
		self.currentAngleToCheckpoint = self.getAverageAngleToCheckpoint()
		
		#print "angle: {ang} distance: {dist}".format(ang=self.lastAngle, dist=self.lastDistance)
		self.logger.logState(self.currentPosition, self.currentAngle, 
			self.currentAngleToCheckpoint, self.currentDistance)
			
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
		self.collectPositions()
		
	def test(self):
		self.moveForward()
		while self.currentDistance > self.distanceEpsilon:		
			if self.lastDistance != None and self.lastDistance < self.currentDistance:
				self.logger.logWarning("Wrong way!")
			angle = self.currentAngleToCheckpoint - self.currentAngle
			if angle < -140.0 or 140.0 < angle:
				self.engine.stop()
				self.turn180degrees()
			elif angle < -20.0:
				self.engine.stop()
				self.turnLeftABit()
			elif 20.0 < angle:
				self.engine.stop()
				self.turnRightABit()
			self.moveForward()
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
	traceback.print_exc()
finally:
	mind.killAll()
