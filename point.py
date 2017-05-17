from math import radians, degrees, cos, sin, asin, sqrt, atan2

class Point:
	x = 0.0 # longitude
	y = 0.0 # latitude
	
	def __init__(self, x_init, y_init):
		self.set(x_init, y_init)

	def set(self, x_init, y_init):
		self.x = x_init
		self.y = y_init
		
	def getAngleTo(self, point):
		if point.isNone() or self.isNone():
			return None
		y = sin(point.x - self.x) * cos(point.y)
		x = cos(self.y) * sin(point.y) - sin(self.y) * cos(point.y) * cos(point.x - self.x)
		return degrees(atan2(y, x))
		
	def getDistanceFrom(self, point): #previously this was 'haversine'
		if point.isNone() or self.isNone():
			return None
	
		# convert decimal degrees to radians 
		lon1, lat1, lon2, lat2 = map(radians, [self.x, self.y, point.x, point.y])

		# haversine formula 
		dlon = lon2 - lon1 
		dlat = lat2 - lat1 
		a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
		c = 2 * asin(sqrt(a)) 
		r = 6371
		return c * r * 1000
		
	def __str__(self):
		return "{x} {y}".format(x=self.x, y=self.y)
		
	def isNone(self):
		return self.x == None or self.y == None