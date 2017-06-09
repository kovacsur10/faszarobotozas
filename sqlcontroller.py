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
			self.cursor.execute("""INSERT INTO state (longitude, latitude, checkpoints, positions, cpAngle, distance, faceAngle, turnAngle, moving, turning) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
					(position.x, position.y, checkpoints, positions, checkpointAngle, distance, faceAngle, turnAngle, moving, turning))
			self.db.commit()
			# print "yaaay"
		except Exception as ex:
			traceback.print_exc()
			self.db.rollback()
				
	#def actionToID(self, action):
	#	return 0
		
	def __del__(self):
		self.db.close()