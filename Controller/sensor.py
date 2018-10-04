#!/usr/bin/python3
#https://sites.google.com/site/ev3python/learn_ev3_python/using-sensors/sensor-modes
#http://docs.ev3dev.org/projects/lego-linux-drivers/en/ev3dev-jessie/sensor_data.html

import ev3dev.ev3 as ev3

sensorLeft = ev3.ColorSensor('in1')
sensorRight = ev3.ColorSensor('in4')


AMBIENT = 0
REFLECT = 1
COLOR = 2
TOTALBLACK = 10
HALFBLACKWHITE = 60
BLACKLINE = 0
ADJUSTSPEED = 1
ONLINE = 2
arrayofcolors = ('unknown','black','blue','green','yellow','red','white','brown')

def setmodeSensorsLR(mode):
    if mode == 0:
        sensorLeft.mode = 'COL-AMBIENT' # measures lux
        sensorRight.mode = 'COL-AMBIENT' # measures lux
        print("sensor mode set to ambient")
    elif mode == 1:
        sensorLeft.mode = 'COL-REFLECT' # measures light intensity
        sensorRight.mode = 'COL-REFLECT' # measures light intensity
        print("sensor mode set to reflect")
    else:
        sensorLeft.mode = 'COL-COLOR' # measures color corresponting to arrayofcolors
        sensorRight.mode = 'COL-COLOR' # measures color corresponting to arrayofcolors
        print("sensor mode set to color")
 # should be dynamic to the amount of background light

def binarize(sensorValue): # use with sensor on'COL-REFLECT' mode
    if sensorValue < TOTALBLACK:
        return BLACKLINE
    if sensorValue < HALFBLACKWHITE:
        return ADJUSTSPEED
    return ONLINE


def readLineSensors():
    left = binarize(sensorLeft.value())
    right = binarize(sensorRight.value())
    #print('left',sensorLeft.value(),'right',sensorRight.value())
    return left, right
