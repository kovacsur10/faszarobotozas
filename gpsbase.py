#!/usr/bin/env python

# mkdir /media/usb
# mount /dev/sda1 /media/usb

import time
import serial
import string

class GPSBase:
	"""$GPGGA,hhmmss.ss,llll.ll,a,yyyyy.yy,a,x,xx,x.x,x.x,M,x.x,M,x.x,xxxx*hh
	1    = UTC of Position
	2    = Latitude
	3    = N or S
	4    = Longitude
	5    = E or W
	6    = GPS quality indicator (0=invalid; 1=GPS fix; 2=Diff. GPS fix)
	7    = Number of satellites in use [not those in view]
	8    = Horizontal dilution of position
	9    = Antenna altitude above/below mean sea level (geoid)
	10   = Meters  (Antenna height unit)
	11   = Geoidal separation (Diff. between WGS-84 earth ellipsoid and
				 mean sea level.  -=geoid is below WGS-84 ellipsoid)
	12   = Meters  (Units of geoidal separation)
	13   = Age in seconds since last update from diff. reference station
	14   = Diff. reference station ID#
	15   = Checksum
	"""
	utc = None
	latitude = None
	lat_dir = None
	longitude = None
	lon_dir = None
	quality = None
	satelites = None
	hdop = None
	altitude = None
	alt_unit = None
	geoidal = None
	geo_unit = None
	age = None
	diff = None
	checksum = None
	
	gps = None
	data = None
	changed = False
	
	def __init__(self):			
		self.gps = serial.Serial(
			port='/dev/ttyAMA0',
			baudrate = 9600,
			parity= serial.PARITY_NONE,
			stopbits=serial.STOPBITS_ONE,
			bytesize=serial.EIGHTBITS,
			timeout=1
		)
		self.update()
	
	def update(self):
		self.changed = False
		self.data = self.gps.readline()
		if self.data[0:6] == '$GPGGA':
			self.changed = True
			tmp = self.data[7:].split(',')
			self.utc = tmp[0]
			if (tmp[1] != ""):
				self.latitude = float(tmp[1]) / 100
			else:
				self.latitude = 0.0
			self.lat_dir = tmp[2]
			if (tmp[3] != ""):
				self.longitude = float(tmp[3]) / 100
			else:
				self.longitude = 0.0
			self.lon_dir = tmp[4]
			self.quality = tmp[5]
			self.satelites = tmp[6]
			self.hdop = tmp[7]
			self.altitude = tmp[8]
			self.alt_unit = tmp[9]
			self.geoidal = tmp[10]
			self.geo_unit = tmp[11]
			self.age = tmp[12]
			tmp2 = tmp[13].split('*')
			self.diff = tmp2[0]
			self.checksum = tmp2[1]