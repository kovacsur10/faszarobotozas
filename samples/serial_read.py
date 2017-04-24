#!/usr/bin/env python

#
# demo program a Raspberry PI soros portjára csatlakoztatott GPS vevő jeleinek a kiolvasására
# a soros port felkonfigurálása (9600 baud, stb...) és olvasása...
#

import time
import serial
ser = serial.Serial(
	port='/dev/ttyAMA0',
	baudrate = 9600,
	parity= serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS,
	timeout=1
)
counter=0

while 1:
	x=ser.readline()
	print x
