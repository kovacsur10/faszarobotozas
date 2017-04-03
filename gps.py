import threading
import time
from math import radians, cos, sin, asin, sqrt

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
            
            lon = self.gps.longitude
            lat = self.gps.latitude
            self.parent.updateData(lon, lat)
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
    
    #private - DO NOT CALL FROM OUTSIDE!
    def __getDistance(self, lon1, lat1, lon2, lat2): #previously this was 'haversine'
        """
        Calculate the great circle distance between two points 
        on the earth (specified in decimal degrees)
        """
        if lon1 == None or lat1 == None or lon2 == None or lat2 == None:
            return None
            
        # convert decimal degrees to radians 
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

        # haversine formula 
        dlon = lon2 - lon1 
        dlat = lat2 - lat1 
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a)) 
        r = 6371 # Radius of earth in kilometers. Use 3956 for miles
        return c * r
        
    def updateData(self, lon, lat):
        threadLock.acquire()
        if self.seen:
            self.seen = False
            self.previous = self.actual
        dist = self.__getDistance(self.actual[0], self.actual[1], lon, lat);
        self.actual = (lon, lat, dist)
        threadLock.release()
        
    def get(self):
        threadLock.acquire()
        self.seen = True
        retVal = self.actual
        self.actual = (self.actual[0], self.actual[1], None)
        threadLock.release()
        return retVal