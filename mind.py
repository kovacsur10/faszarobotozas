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
	checkPoints = None
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
		
		self.checkPoints = deque()
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
		
		self.turnAngle = float("inf")
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
		
	def setNextCheckpoint(self, checkPoint):
		self.checkPoints.append(checkPoint)
		self.logger.logAction("setNextCheckpoint", checkPoint)
	
	def removeCheckpoint(self, checkPoint):
		# TODO: mark element to skip
		self.logger.logAction("removeCheckpoint", checkPoint)
		
	def getLocation(self):
		delta = self.gps.get()
		self.logger.logAction("getLocation", delta[0])
		
		if len(self.positionQueue) == self.maxPositions:
			self.positionQueue.popleft()
		self.positionQueue.append(delta[0])
		
	def getAverageDistanceFromCheckpoint(self):
		if len(self.checkPoints) > 0 and len(self.positionQueue) != 0:
			distance = 0.0
			for position in self.positionQueue:
				try:
					distance += position.getDistanceFrom(self.checkPoints[0])
				except:
					self.logger.logWarning("None Distance")
			return distance / len(self.positionQueue)
		else:
			return float("inf")
			
	def getAverageAngleToCheckpoint(self):
		if len(self.checkPoints) > 0 and len(self.positionQueue) != 0:
			angle = 0.0
			for position in self.positionQueue:
				try:
					angle += position.getAngleTo(self.checkPoints[0])
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
		
	def serialQueue(self, queue):
		tmp = "["
		for id, position in enumerate(queue):
			if position is not None:
				tmp += position.toJSON()
				if id < len(queue)-1:
					tmp += ", "
		tmp += "]"
		return tmp
		
	def test(self):
		#while self.isStopped and len(self.checkPoints) == 0:
		#	time.sleep(sqlFrequency)
		self.isStopped = False
			
		self.moveForward()
		while len(self.checkPoints) > 0:
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
				# self.sqlcontroller.logState(self.currentPosition, serialQueue(self.checkPoints), serialQueue(self.positionQueue), self.currentDistance, self.currentAngleToCheckpoint, self.currentAngle, self.turnAngle, self.isMoving, self.isTurning)			
			self.logger.log("Robot is at the checkpoint!")
			self.checkPoints.popleft()
			
		self.engine.cleanUp()
		self.killAll()
		
	def sqlWorker(self):
		while not self.isStopped:
			if not self.isStopped:
				#print self.currentPosition
				#print self.serialQueue(self.checkPoints)
				#print self.serialQueue(self.positionQueue)
				#print self.currentDistance
				#print self.currentAngleToCheckpoint
				#print self.currentAngle
				#print self.turnAngle
				#print self.isMoving
				#print self.isTurning
				if (self.currentDistance != float("inf")) and (self.currentAngle != float("inf")) and (self.currentAngleToCheckpoint != float("inf")) and (self.turnAngle != float("inf")):
					#print "OKS"
					self.sqlcontroller.logState(self.currentPosition, self.serialQueue(self.checkPoints), self.serialQueue(self.positionQueue), self.currentDistance, self.currentAngleToCheckpoint, self.currentAngle, self.turnAngle, self.isMoving, self.isTurning)
				# newCheckpoint = self.sqlcontroller.getNewCheckpoint()
				# if newCheckpoint is not None:
					# self.setNextCheckpoint(newCheckpoint)
				# removedCheckpoint = self.sqlcontroller.getRemovedCheckpoint()
				# if removedCheckpoint is not None:
					# self.removeCheckpoint(removedCheckpoint)
				self.isStopped = self.sqlcontroller.isStopped()
			else:
				self.isStopped = not self.sqlcontroller.isStarted()
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
	mind.setNextCheckpoint(Point(19.03414, 47.284501))
	#mind.setNextCheckpoint(Point(19.034780, 47.284399))
	mind.test()
except Exception as ex:
	traceback.print_exc()
finally:
	mind.killAll()
