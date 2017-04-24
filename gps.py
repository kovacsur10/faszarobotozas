import threading
import time
from point import Point
import gpsbase

threadLock = threading.Lock() # mutex for GPS shared data

# GPS thread for querying the GPSbase class (device) for data
class gpsQueryThread (threading.Thread):
	def __init__(self, gps, queryTime, parent):
		threading.Thread.__init__(self)
		self.gps = gps
		self.queryTime = queryTime
		self.parent = parent
				
	def run(self):
		print "GPS query thread starts"
		while True:
			self.gps.update()
			self.parent.updateData(self.gps.longitude, self.gps.latitude)
			time.sleep(self.queryTime)
		print "GPS query thread ends"
		
class GPS:
	gps = None
	seen = False
	previous = (None, None, None)
	actual = (None, None, None)

	def __init__(self):
		self.gps = gpsbase.GPSBase()
		self.seen = False
		self.queryThread = gpsQueryThread(self.gps, 0.5, self)
		self.previous = (None, None, None)
		self.actual = (None, None, None)
				
	def start(self):
		self.queryThread.start()
	
	def updateData(self, lon, lat):
		threadLock.acquire()
		if self.seen:
			self.seen = False
			self.previous = self.actual
		p1 = Point(self.actual[0], self.actual[1])
		p2 = Point(lon, lat)
		dist = p1.getDistanceFrom(p2)
		orientation = p1.getAngleTo(p2)
		self.actual = (p2, dist, orientation)
		threadLock.release()
				
	def get(self):
		threadLock.acquire()
		self.seen = True
		retVal = self.actual
		pt = Point(self.actual[0], self.actual[1])
		self.actual = (pt, None, None)
		threadLock.release()
		return retVal