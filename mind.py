import time
import engine
import gps
from point import Point
from collections import deque
import logger
import traceback
import threading
import sqlcontroller

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
		self.distanceEpsilon = 3
		
		self.lastPosition = Point(None, None)
		self.lastAngle = float("inf")
		self.lastDistance = float("inf")
		self.lastAngleToCheckpoint = float("inf")
		
		self.currentPosition = Point(None, None)
		self.currentAngle = float("inf")
		self.currentDistance = float("inf")
		self.currentAngleToCheckpoint = float("inf")
		
		self.turnAngle = Point(None, None)
		self.isMoving = False
		self.isTurning = False
		self.isStopped = False
		self.sqlFrequency = 0.5
		self.waitFrequency = 0.1
		
		time.sleep(1.5*self.gpsFrequency)
		self.collectPositions()
		
		self.sqlcontroller = sqlcontroller.SQLController()
		self.sqlThread = threading.Thread(target=self.sqlWorker)
		self.sqlThread.start()
		
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
		self.isTurning = True
		self.engine.turnLeft(60)
		self.wait(0.3)
		self.engine.hardStop()
		self.isTurning = False
	
	def turnRightABit(self):
		self.logger.logAction("turnRightABit")
		self.isTurning = True
		self.engine.turnRight(100)
		self.wait(0.3)
		self.engine.hardStop()
		self.isTurning = False
	
	def turn180degrees(self):
		self.logger.logAction("turn180degrees")
		self.isTurning = True
		self.engine.turnLeft(100)
		self.wait(1)
		self.engine.hardStop()
		self.isTurning = False
		
	def moveForward(self):
		self.logger.logAction("moveForward")
		self.isMoving = True
		self.engine.moveForward(100)
		self.wait(3)
		self.engine.stop()
		self.isMoving = False
		self.collectPositions()
		
	def serialQueue(self):
		tmp = "["
		for id, position in enumerate(self.positionQueue):
			tmp += position.toJSON()
			if id < len(self.positionQueue)-1:
				tmp += ", "
		tmp += "]"
		return tmp
		
	def test(self):
		self.moveForward()
		while self.currentDistance > self.distanceEpsilon:		
			if self.lastDistance != None and self.lastDistance < self.currentDistance:
				self.logger.logWarning("Wrong way!")
			angle = - self.currentAngleToCheckpoint + self.currentAngle
			if angle < -180.0:
				angle += 360
			elif angle > 180.0:
				angle -= 360
			self.turnAngle = angle
			self.logger.log(str(angle))
			if angle < -140.0 or 140.0 < angle:
				self.turn180degrees()
			elif angle > 20.0:
				self.turnRightABit()
			elif -20.0 > angle:
				self.turnLeftABit()
			self.moveForward()
			
			# self.sqlcontroller.logState(self.currentPosition, "[]", self.serialQueue(), self.currentDistance, self.currentAngleToCheckpoint, self.currentAngle, self.turnAngle, self.isMoving, self.isTurning)
			
		self.engine.cleanUp()
		self.logger.log("Robot is at the checkpoint!")
		self.killAll()
		
	def sqlWorker(self):
		while not self.isStopped:
			self.sqlcontroller.logState(self.currentPosition, "[]", self.serialQueue(), self.currentDistance, self.currentAngleToCheckpoint, self.currentAngle, self.turnAngle, self.isMoving, self.isTurning)
			self.isStopped = self.sqlcontroller.isStopped()
			time.sleep(self.sqlFrequency);
	
	def wait(self, waitTime):
		while not self.isStopped and waitTime > 0:
			time.sleep(self.waitFrequency)
			waitTime -= self.waitFrequency
		
	def killAll(self):
		self.isStopped = True
		self.gps.kill()
	

mind = Mind()
try:
	mind.setNextPoint(Point(19.034780, 47.284399))
	mind.test()
except Exception as ex:
	traceback.print_exc()
finally:
	mind.killAll()
