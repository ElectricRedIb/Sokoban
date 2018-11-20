
import sensor
import motors
import lineFollow
from difreg import difreg
from time import sleep


sensor.setmodeSensorsLR(sensor.REFLECT)

TURNSPEED = 100
DRIVESPEED = 700


#rightReg = lineFollow.lineFollow(DRIVESPEED,sensor.readRight())
#leftReg = lineFollow.lineFollow(DRIVESPEED,sensor.readLeft())

reg = difreg()

def lineFollowDrive():
    speed = DRIVESPEED
    errR, errL = reg.regulate(sensor.readLeft(), sensor.readRight())
    motors.driveRightOnly(speed - errL)
    motors.driveLeftOnly(speed - errR)

def drive(crossSections):
    crossSectionsPasted = 0
    blackLinePasted = True
    while True:
        lineFollowDrive()
        left, right = sensor.readLineSensors()
        #print("err right",errR, "left",errL)
        if left + right:
            blackLinePasted = True
        if not(left + right) and blackLinePasted:
            #motors.stopMotors();
            crossSectionsPasted = crossSectionsPasted + 1
            blackLinePasted = False
            if crossSectionsPasted >= crossSections:
                return 1




def turn(direction):
    """returns 1 when turning is done"""
    state = 0
    turnsteps = 100
    while True:
        err = sensor.readLeft() - sensor.readRight()

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
            if abs(err) > 20:
                state = 3
        elif state == 3:
            if abs(err) < 5:
                motors.stopMotors()
                return 1


def rev():
    motors.moveRel(-260) #550 #260 ved 7.30 strøm!
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
            return 1


'''
def turn(direction,turns):
    motors.moveRel(115)
    while True:
        motors.driveRightOnly(TURNSPEED)
        motors.driveLeftOnly(-TURNSPEED)
        pass
    return 1
'''
'''
def turn(direction,t):
    """returns 1 when turning is done"""
    state = 0
    turnsteps = 145
    while True:
        err = sensor.readLeft() - sensor.readRight()

        if state == 0:
            motors.moveRel(115)
            state = 1
        elif state == 1:
            if direction == 'right':
                motors.moveRelT(turnsteps,'right')

            else:
                motors.moveRelT(turnsteps,'left')
            return 1
'''











'''
def turn(direction,turns):
    done = 0
    state = 0
    amountOfTurns = turns

    while not done:
        left, right = sensor.readLineSensors()
        if state == 0:
            motors.moveRel(115)
            #while True:
            #    pass
            state = 3
            if left + right == 4:
                pass
                #state = 1
        elif state == 1:  # ------------------------- State 1
            if direction == 'right':
                motors.driveLeftOnly(TURNSPEED)
                motors.driveRightOnly(0)
                if left == sensor.BLACKLINE:
                    state = 2
            else:
                motors.driveRightOnly(TURNSPEED)
                motors.driveLeftOnly(0)
                if right == sensor.BLACKLINE:
                    state = 2
        elif state == 2:  # ------------------------- State 2
            if direction == "right":
                if left == sensor.ONLINE:
                    state = 3
            else:
                if right == sensor.ONLINE:
                    state = 3
        elif state == 3:  # ------------------------- State 3
            if direction == 'right':
                motors.driveRightOnly(-TURNSPEED)
                motors.driveLeftOnly(TURNSPEED)
            else:
                motors.driveRightOnly(TURNSPEED)
                motors.driveLeftOnly(-TURNSPEED)
            state = 4
        elif state == 4: # ------------------------- State 4
            if direction == "right":
                if right == sensor.BLACKLINE:
                    amountOfTurns = amountOfTurns - 1
                    if amountOfTurns:
                        state = 5
                    else:
                        state = 10
            else:
                if left == sensor.BLACKLINE:
                    amountOfTurns = amountOfTurns - 1
                    if amountOfTurns:
                        state = 5
                    else:
                        state = 10
        elif state  == 5:  # ------------------------- State 5
            if direction == "right":
                if right == sensor.ONLINE:
                    state = 4
            else:
                if left == sensor.ONLINE:
                    state = 4
        elif state == 10:  # ------------------------- State 10 end state
            motors.stopMotors()
            done = 1
    return 1
'''
