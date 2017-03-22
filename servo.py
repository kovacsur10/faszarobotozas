#
# demo program a Raspberry PI 20 és 21 lápára/pinjére kötött szervó (RC, PWM) meghajtására
# a két szervó (20,21) a robot motorvezérlőjét irányítja 21 előre-hátra, 20 fordulás
#
#

import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM) # Raspberry pinkiosztása

GPIO.setup(21, GPIO.OUT) # 20-21 kimenetek
GPIO.setup(20, GPIO.OUT)

# a szervó jel nek 50Hz, azaz 20ms-enként kell ismétlődnie
# akkor van középső", "neutrális" helyzetben ha 1,5ms a kitöltés 1,5/20 = 0,075 azaz 7,5%
# a két végkitérés 1ms és 2ms azaz 0,05-től 0,1-ig azaz 5%-tól 10%-ig

drive=GPIO.PWM(21,50) # 21 port 50 Hz (20 ms)
drive.start(7.5) # neutrális
turn=GPIO.PWM(20,50)
turn.start(7.5)

turn.ChangeDutyCycle(7.5)

# az egszerűség és a fokozatosság miatt (float)10-el osztunk
# előre egyre gyorsabban
for speed in range(75,100):
	drive.ChangeDutyCycle(speed/10.0)
	print speed/10.0
	time.sleep(0.2)

# középállás - állj
drive.ChangeDutyCycle(7.5)

time.sleep(5)

# forgás egyre gyorsabban
for steer in range(75, 100):
	turn.ChangeDutyCycle(steer/10.0)
	print steer/10.0
	time.sleep(0.2)

# középállás - állj
turn.ChangeDutyCycle(7.5)
time.sleep(5)

print "stop"
drive.stop()
turn.stop()
time.sleep(3)
print "cleanup"
GPIO.cleanup()
time.sleep(3)




