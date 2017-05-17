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
			
	def logState(self, position, checkpoints, positions, angle, angleToCheckpoint, distance, time, moving, turning):
		try:
			self.cursor.execute("""INSERT INTO state (longitude, latitude, checkpoints, positions, cpAngle, distance, faceAngle, turnAngle, moving, turning) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
					(position.x, position.y, checkpoints, positions, angleToCheckpoint, distance, angle, time, moving, turning))
			self.db.commit()
			print "yaaay"
		except Exception as ex:
			traceback.print_exc()
			self.db.rollback()
				
	#def actionToID(self, action):
	#	return 0
		
	def __del__(self):
		self.db.close()