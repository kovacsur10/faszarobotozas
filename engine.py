import RPi.GPIO as GPIO 
#import mygpio as GPIO
import time
import math

class Angle:	
	def __init__(self):
		self.radian = 0.0
	
	# normalize :: radian -> radian
	def normalize(self, value):
		ct = math.trunc(value / math.pi)
		return value - (ct * math.pi)
	
	# radian :: radian -> ()
	def radian(self, value):
		self.radian = normalize(value)
	
	# degree :: degree -> ()
	def degree(self, value):
		self.radian = normalize(math.radians(value))
		
	# getRadian :: -> radian
	def getRadian(self):
		return self.radian
	
	# getDegree :: -> degree
	def getDegree(self):
		return math.degrees(self.radian)

class MutualLockout(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

class Engine:
	moving = None
	rotating = None
	actualSpeed = None
	actualSteer = None
	
	idleSpeed = 7500
	idleSteer = 7500
	smoothStopRate = 25
	smoothSpeedChangeRate = 100
	smoothSteerChangeRate = 100
	refreshRate = 0.1
	
	drivePort = 21
	turnPort = 20
	drive = None
	turn = None
	
	# init and cleanup functions
	def __init__(self):
		self.actualSpeed = self.idleSpeed
		self.actualSteer = self.idleSteer
		self.moving = False
		self.rotating = False
		GPIO.setmode( GPIO.BCM )
		GPIO.setup( self.drivePort, GPIO.OUT )
		GPIO.setup( self.turnPort, GPIO.OUT )
		self.drive=GPIO.PWM( self.drivePort, 50 )
		self.drive.start( self.actualSpeed / 1000.0 )
		self.turn=GPIO.PWM( self.turnPort, 50 )
		self.turn.start( self.actualSteer / 1000.0 )
	
	def cleanUp(self):
		self.hardStop()
		self.drive.stop()
		self.turn.stop()
		GPIO.cleanup()
	
	### movement functions ###
	
	# hardStop :: -> ()
	def hardStop(self):
		self.drive.ChangeDutyCycle( self.idleSpeed / 1000.0 )
		self.turn.ChangeDutyCycle( self.idleSteer / 1000.0 )
		self.actualSpeed = self.idleSpeed
		self.actualSteer = self.idleSteer
		self.moving = False
		self.rotating = False
	
	#stop :: -> ()
	def stop(self):
		if self.moving:
			actual = self.actualSpeed
			idle = self.idleSpeed
		else:
			actual = self.actualSteer
			idle = self.idleSteer
			
		# set the range
		if actual > idle:
			r = range(actual, idle, -1 * self.smoothStopRate)
		else:
			r = range(actual, idle, self.smoothStopRate)
		#smooth stop
		if self.moving:
			for speed in r:
				self.drive.ChangeDutyCycle(speed / 1000.0)
				time.sleep(self.refreshRate)
			self.drive.ChangeDutyCycle( self.idleSpeed / 1000.0 )
		else:
			for steer in r:
				self.turn.ChangeDutyCycle(steer / 1000.0)
				time.sleep(self.refreshRate)
			self.turn.ChangeDutyCycle( self.idleSteer / 1000.0 )
		self.actualSpeed = self.idleSpeed
		self.actualSteer = self.idleSteer
		self.moving = False
		self.rotating = False
	
	# moveForward :: [1..100] -> () raises MutualLockout exception 
	def moveForward(self, speed):
		if not self.rotating:
			self.moving = True
			# check input value
			if speed > 100:
				speed = 10000
			elif speed < 1:
				speed = 7525
			else:
				speed = 7500 + (speed * 25)
			self.smoothSetSpeed(speed)
		else:
			raise MutualLockout("Cannot move during rotation!")
	
	# moveBackward :: [1..100] -> () raises MutualLockout exception 
	def moveBackward(self, speed):
		if not self.rotating:
			self.moving = True
			# check input value
			if speed > 100:
				speed = 5000
			elif speed < 1:
				speed = 7475
			else:
				speed = 7500 - speed * 25
			self.smoothSetSpeed(speed)
		else:
			raise MutualLockout("Cannot move during rotation!")
	
	# private
	# smoothSetSpeed :: [5000..10000] -> ()
	def smoothSetSpeed(self, speed):
		# smooth speed modification
		if self.actualSpeed < speed:
			changeRate = self.smoothSpeedChangeRate
		else:
			changeRate = -1 * self.smoothSpeedChangeRate
		r = range(self.actualSpeed, speed, changeRate)
		for sp in r:
			self.drive.ChangeDutyCycle(sp / 1000.0)
			time.sleep(self.refreshRate)
		self.drive.ChangeDutyCycle(speed / 1000.0)
		self.actualSpeed = speed
	
	# private
	# smoothSetSteer :: [5000..10000] -> ()
	def smoothSetSteer(self, steer):
		# smooth steer modification
		if self.actualSteer < steer:
			changeRate = self.smoothSteerChangeRate
		else:
			changeRate = -1 * self.smoothSteerChangeRate
		r = range(self.actualSteer, steer, changeRate)
		for sp in r:
			self.turn.ChangeDutyCycle(sp / 1000.0)
			time.sleep(self.refreshRate)
		self.turn.ChangeDutyCycle(steer / 1000.0)
		self.actualSteer = steer
	
	# turnLeft :: [1..100] -> ()
	def turnLeft(self, steer): # TODO: test directions!
		if not self.moving:
			self.rotating = True
			# check input value
			if steer > 100:
				steer = 10000
			elif steer < 1:
				steer = 7525
			else:
				steer = 7500 + (steer * 25)
			self.smoothSetSteer(steer)
		else:
			raise MutualLockout("Cannot turn left during moving forward or backward!");
	
	# turnRight :: [1..100] -> ()
	def turnRight(self, steer): # TODO: test directions!
		if not self.moving:
			self.rotating = True
			# check input value
			if steer > 100:
				steer = 5000
			elif steer < 1:
				steer = 7475
			else:
				steer = 7500 - steer * 25
			self.smoothSetSteer(steer)
		else:
			raise MutualLockout("Cannot turn left during moving forward or backward!");
	
#	# turn :: Angle -> ()
#	def turn(self, angle):
#		if not self.moving and not self.rotating:
#			self.rotating = True
#			if angle < 0.0: # left
#				
#			else: # right
#				
#		else:
#			raise MutualLockout("Cannot turn left or right during doing any movement!")
	
e = Engine()

e.moveForward(60)
time.sleep(1)

e.stop()
time.sleep(2)

e.cleanUp()