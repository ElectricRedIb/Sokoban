#!/usr/bin/python3
#https://sites.google.com/site/ev3python/learn_ev3_python/using-sensors/sensor-modes
#http://docs.ev3dev.org/projects/lego-linux-drivers/en/ev3dev-jessie/sensor_data.html

#import ev3dev.ev3 as ev3

sensorLeft = 10#ev3.ColorSensor('in1')
sensorRight = 70#ev3.ColorSensor('in2')

AMBIENT = 0
REFLECT = 1
COLOR = 2
arrayofcolors = ('unknown','black','blue','green','yellow','red','white','brown')

def setmodeSensorsLR(mode):
    if mode == 0:
        #sensorLeft.mode = 'COL-AMBIENT' # measures lux
        #sensorRight.mode = 'COL-AMBIENT' # measures lux
        print("sensor mode set to ambient")
    elif mode == 1:
        #sensorLeft.mode = 'COL-REFLECT' # measures light intensity
        #sensorRight.mode = 'COL-REFLECT' # measures light intensity
        print("sensor mode set to reflect")
    else:
        #sensorLeft.mode = 'COL-COLOR' # measures color corresponting to arrayofcolors
        #sensorRight.mode = COL-COLOR' # measures color corresponting to arrayofcolors
        print("sensor mode set to color")

backgroundValue = 50 # should be dynamic to the amount of background light
def binarize(sensorValue): # use with sensor on'COL-REFLECT' mode
    if sensorValue > backgroundValue:
        binary = 1
    else:
        binary = 0
    return binary


def readFunction():
    #left = binarize(sensorLeft.value())
    #right = binarize(sensorRight.value())
    #print("Left",sensorLeft.value(),"Right", sensorRight.value())
    left = binarize(sensorLeft)
    right = binarize(sensorRight)
    print("Left",sensorLeft,"Right", sensorRight)


    return left, right


def detectLine():
    left, right = readFunction()
    if left != right:
        if left:
            print("decrease speed on left")
            return 1
        else:
            print("decrease speed on right")
            return 2


    print("on the line")
    return 0
