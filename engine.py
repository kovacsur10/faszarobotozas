import RPi.GPIO as GPIO
import time

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
	
	idleSpeed = 75
	idleSteer = 75
	smoothStopRate = 1
	smoothSpeedChangeRate = 1
	smoothSteerChangeRate = 1
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
		self.drive.start( self.actualSpeed / 10.0 )
		self.turn=GPIO.PWM( self.turnPort, 50 )
		self.turn.start( self.actualSteer / 10.0 )
	
	def cleanUp(self):
		self.drive.stop()
		self.turn.stop()
		GPIO.cleanup()
	
	# movement functions
	def stop(self):
		self.drive.ChangeDutyCycle( self.idleSpeed / 10.0 )
		self.turn.ChangeDutyCycle( self.idleSteer / 10.0 )
	
	def smoothStop(self):
		if moving:
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
				self.drive.ChangeDutyCycle(speed / 10.0)
				time.sleep(self.refreshRate)
			self.drive.ChangeDutyCycle( self.idleSpeed / 10.0 )
		else:
			for steer in r:
				self.turn.ChangeDutyCycle(steer / 10.0)
				time.sleep(self.refreshRate)
			self.turn.ChangeDutyCycle( self.idleSteer / 10.0 )
	
	def smoothSetSpeed(self, speed):
		if not self.rotating:
			# check the input value
			if speed < 50:
				speed = 50
			elif 100 < speed:
				speed = 100
			
			# smooth speed modification
			if self.actualSpeed < speed:
				changeRate = self.smoothSpeedChangeRate
			else:
				changeRate = -1 * self.smoothSpeedChangeRate
			r = range(self.actualSpeed, speed, changeRate)
			for sp in r:
				self.drive.ChangeDutyCycle(sp / 10.0)
				time.sleep(self.refreshRate)
		else:
			raise MutualLockout("Cannot move during rotating!")
	
	def smoothSetSteer(self, steer):
		if not self.moving:
			# check the input value
			if steer < 50:
				steer = 50
			elif 100 < steer:
				steer = 100
			# smooth steer modification
			if self.actualSteer < steer:
				changeRate = self.smoothSteerChangeRate
			else:
				changeRate = -1 * self.smoothSteerChangeRate
			r = range(self.actualSteer, steer, changeRate)
			for sp in r:
				self.turn.ChangeDutyCycle(sp / 10.0)
				time.sleep(self.refreshRate)
		else:
			raise MutualLockout("Cannot rotate during moving!")
		
e = Engine()
e.smoothSetSpeed(100)
time.sleep(10)
e.stop()

e.cleanUp()