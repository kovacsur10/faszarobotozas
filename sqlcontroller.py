import MySQLdb
import traceback

class SQLController:
	def __init__(self):
		self.db = MySQLdb.connect(host= "localhost",
															user="robot",
															passwd="robot",
															db="robotics")
		self.cursor = self.db.cursor()

	#def logAction(self, action, param = None):
	#	if param = None:
	#		param = ""
	#	try:
	#		cursor.execute("""INSERT INTO useractions (action, params) VALUES (%s, %s)""", self.actionToID(action), param)
	#		db.commit()
	#	except:
	#		db.rollback()
			
	def logState(self, position, checkpoints, positions, distance, checkpointAngle, faceAngle, turnAngle, moving, turning):
		"""
			position : Point(x, y)
			checkpoints : json string
			positions : json string
			distance : double
			checkpointAngle : double
			faceAngle : double
			turnAngle : double
			moving : boolean
			turning : boolean
		"""
		try:
			self.cursor.execute("""
				INSERT INTO state (longitude, latitude, checkpoints, positions, cpAngle, distance, faceAngle, turnAngle, moving, turning) 
				VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
			""", (position.x, position.y, checkpoints, positions, checkpointAngle, distance, faceAngle, turnAngle, moving, turning))
			self.db.commit()
			# print "yaaay"
		except Exception as ex:
			traceback.print_exc()
			self.db.rollback()
		
	def isStarted(self):
		result = self.getAction(1)
		return result is not None
		
	def isStopped(self):
		result = self.getAction(2)
		return result is not None
	
	def getNewCheckpoint(self):
		result = self.getAction(3)
		if result is None:
			return None
		return result[1]
		
	def getRemovedCheckpoint(self):
		result = self.getAction(4)
		if result is None:
			return None
		return result[1]
			
	def getAction(self, actionID):
		row = None
		try:
			self.cursor.execute("""
				SELECT id, params
				FROM useractions 
				WHERE action = %s AND state = 0
			""", actionID)
			row = self.cursor.fetchone()
			if row is not None:
				print row
				self.cursor.execute("""
					UPDATE useractions 
					SET state = 1 
					WHERE id = %s
				""", row)
				self.db.commit()
		except Exception as ex:
			traceback.print_exc()
			self.db.rollback()
		return row
			
	#def actionToID(self, action):
	#	return 0
		
	def __del__(self):
		self.db.close()