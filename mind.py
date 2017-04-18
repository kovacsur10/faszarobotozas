import time
import engine
import gps

class Mind:
		def __init__(self):
				self.engine = engine.Engine()
				self.gps = gps.GPS()
				self.gps.start()
				
		def getLocation(self):
				print self.gps.get()

		def test(self):
				self.engine.moveForward(60)
				time.sleep(1)
				self.engine.stop()
				time.sleep(2)
				for i in range(1,100):
					self.getLocation()
					time.sleep(1)
				self.engine.cleanUp()
				
mind = Mind()
mind.test()
