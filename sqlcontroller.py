import MySQLdb

class SQLController:
	def __init__(self):
		self.db = MySQLdb.connect(host= "localhost",
															user="root",
															passwd="root",
															db="robotics")
		self.cursor = db.cursor()

	#def logAction(self, action, param = None):
	#	if param = None:
	#		param = ""
	#	try:
	#		cursor.execute("""INSERT INTO useractions (action, params) VALUES (%s, %s)""", self.actionToID(action), param)
	#		db.commit()
	#	except:
	#		db.rollback()
			
	def logState(self, position, checkpoints, positions, angle, angleToCheckpoint, distance, time, moving, turning):
		try:
			self.cursor.execute("""INSERT INTO state (longitude, latitude, checkpoints, positions, cpAngle, distance, faceAngle, turnAngle, moving, turning) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
					position.x, position.y, checkpoints, positions, angleToCheckpoint, distance, angle, time, moving, turning)
			self.db.commit()
		except:
			self.db.rollback()
				
	#def actionToID(self, action):
	#	return 0
		
	def __del__(self):
		self.db.close()