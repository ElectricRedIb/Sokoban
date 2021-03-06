
import sensor
import motors
import lineFollow
from difreg import difreg
from time import sleep
import ev3dev.ev3 as ev


sensor.setmodeSensorsLR(sensor.REFLECT)

power = ev.PowerSupply()
MAXTURNSPEED = 0
MINTURNSPEED = 0
DRIVESPEED = 0
def batteryState():
    global MAXTURNSPEED
    global MINTURNSPEED
    global DRIVESPEED
    voltage = power.measured_voltage/1000000
    if voltage < 8.0:
        print("State of battery: ")
        print("     Under 8.0. Voltage at " + str(voltage))
        MAXTURNSPEED = 300
        MINTURNSPEED = 100
        DRIVESPEED = 800
    else:
        print("State of battery: ")
        print("     Over 8.0. Voltage at " + str(voltage))
        MAXTURNSPEED = 300*0.7
        MINTURNSPEED = 100
        DRIVESPEED = 800*0.9
batteryState()


#rightReg = lineFollow.lineFollow(DRIVESPEED,sensor.readRight())
#leftReg = lineFollow.lineFollow(DRIVESPEED,sensor.readLeft())

reg = difreg()


f = open('sensor_speed_values', 'w')
def lineFollowDrive():
    speed = DRIVESPEED
    left, right = sensor.readLineSensors()
    errR, errL = reg.regulate(left,right)
    #f.write(str(left)+ " : ")
    #f.write(str(right)+ " : ")
    #f.write(str(speed-errL)+ " : ")
    #f.write(str(speed - errR)+ " \n")
    motors.driveRightOnly(speed - errR)
    motors.driveLeftOnly(speed - errL)

def drive(crossSections):
    crossSectionsPasted = 0
    blackLinePasted = True
    while True:
        lineFollowDrive()
        left, right = sensor.readLineSensors()
        #print("err right",errR, "left",errL)
        sensorSum = left + right
        onBlackLine = sensorSum <= 20
        if not(onBlackLine):
            blackLinePasted = True
        if onBlackLine and blackLinePasted:
            #motors.stopMotors();
            crossSectionsPasted = crossSectionsPasted + 1
            blackLinePasted = False
            if crossSectionsPasted >= crossSections:
                reg.reset()
                return 1



'''
def turn(direction):
    """returns 1 when turning is done"""
    state = 0
    turnsteps = 110
    while True:
        left, right = sensor.readLineSensors()
        err = left - right

        if state == 0:
            #motors.moveRel(115)
            state = 1
        elif state == 1:
            if direction == 'right':
                motors.moveRelT(turnsteps,'right')
            else:
                motors.moveRelT(turnsteps,'left')
            if direction == 'right':
                motors.driveRightOnly(-TURNSPEED)
                motors.driveLeftOnly(TURNSPEED)
            else:
                motors.driveRightOnly(TURNSPEED)
                motors.driveLeftOnly(-TURNSPEED)
            state = 2
        elif state == 2:
            if abs(err) > 25:
                state = 3
        elif state == 3:
            if abs(err) < 15:
                motors.stopMotors()
                return 1
'''
def turn(direction,repState):
    """returns 1 when turning is done"""
    state = 0
    turnsteps = 90
    initRight = motors.getPositionRight()
    initLeft = motors.getPositionLeft()
    amountOfturns = 0
    while amountOfturns < repState:
        left, right = sensor.readLineSensors()
        err = left - right

        if err < 0:
            err = err *-1
        #print(err)
        if state == 0:
            if direction == 'right':
                posRight = motors.getPositionRight()
                if abs(initRight-posRight) < turnsteps:
                    speed = MAXTURNSPEED
                else:
                    speed = MINTURNSPEED
                    state = 1
                motors.driveRightOnly(-speed)
                motors.driveLeftOnly(speed)
            else:
                posLeft = motors.getPositionLeft()
                if abs(initLeft-posLeft) < turnsteps:
                    speed = MAXTURNSPEED
                else:
                    speed = MINTURNSPEED
                    state = 1
                motors.driveRightOnly(speed)
                motors.driveLeftOnly(-speed)
        elif state == 1:
            if direction == 'right':
                motors.driveRightOnly(-speed)
                motors.driveLeftOnly(speed)
            else:
                motors.driveRightOnly(speed)
                motors.driveLeftOnly(-speed)
            if err > 35:
                state = 2
        elif state == 2:
            if err < 20:
                motors.stopMotors()
                amountOfturns = amountOfturns + 1
                initRight = motors.getPositionRight()
                initLeft = motors.getPositionLeft()
                state = 0
    return 1

def rev():
    motors.moveRel(-265) #550 #260 ved 7.30 strøm!
    return 1

def push():
    gripperInitValue = sensor.readGripSensor()
    while True:
        lineFollowDrive()
        gripperDifValue = abs(gripperInitValue - sensor.readGripSensor())
        #print("diff", gripperDifValue)
        if gripperDifValue > 200:# and blackLinePasted :
            #crossSectionsPasted = crossSectionsPasted + 1
            #blackLinePasted = False
            #if crossSectionsPasted >= crossSections:
            reg.reset()
            return 1
