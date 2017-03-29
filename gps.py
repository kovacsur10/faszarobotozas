#!/usr/bin/env python

# mkdir /media/usb
# mount /dev/sda1 /media/usb

import time
import serial
import string

ser = serial.Serial(
	port='/dev/ttyAMA0',
	baudrate = 9600,
	parity= serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS,
	timeout=1
)
counter=0

class GPS:
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
	def __init__(self, data):
		if data[0:6] == '$GPGGA':
			tmp = data[7:].split(',')
			self.utc = tmp[0]
			self.latitude = tmp[1]
			self.lat_dir = tmp[2]
			self.longitude = tmp[3]
			self.lon_dir = tmp[4]
			self.quality = tmp[5]
			self.satelites = tmp[6]
			self.hdop = tmp[7]
			self.altitude = tmp[8]
			self.alt_unit = tmp[9]
			self.geoidal = tmp[10]
			self.geo_unit = tmp[11]
			self.age = tmp[12]
			self.diff = tmp[13]
			self.checksum = tmp[14]
	

while 1:
	data = ser.readline()
	if data[0:6] == '$GPGGA':
		ga = GPS(data)
		print (ga.utc)
	
	# print data
