
import sensor
import motors
import lineFollow
import difreg



sensor.setmodeSensorsLR(sensor.REFLECT)

TURNSPEED = 200
DRIVESPEED = 800


#rightReg = lineFollow.lineFollow(DRIVESPEED,sensor.readRight())
#leftReg = lineFollow.lineFollow(DRIVESPEED,sensor.readLeft())

reg = difreg.difreg()


def drive(direction):
    '''
    speed = DRIVESPEED * direction
    #if sensor.readGripSensor() == sensor.BLACKLINE:
    #    speed = TURNSPEED * direction
    #    DRIVESPEED = speed
    #    print("change speed")
    #print("DRIVESPEED", DRIVESPEED)
    left, right = sensor.readLineSensors()
    errorR = rightReg.regPID(sensor.readRight())
    errorL = leftReg.regPID(sensor.readLeft())
    rr = speed- errorR* direction
    rl = speed- errorL * direction
    motors.driveRightOnly(rr)
    motors.driveLeftOnly(rl)
    #motorRight.run_forever(speed_sp=rr)
    #motorLeft.run_forever(speed_sp=rl)
    #print("speed right",rr,errorR,right, "left",rl,errorL,left)
    '''
    speed = DRIVESPEED * direction
    errR, errL = reg.regulate(sensor.readLeft(), sensor.readRight())
    motors.driveRightOnly(speed - errL)
    motors.driveLeftOnly(speed - errR)
    left, right = sensor.readLineSensors()
    print("err right",errR, "left",errL)
    if not (left + right):
        #motors.stopMotors();
        return 1
    return 0

'''
def turn(direction,turns):
    motors.moveRel(115)
    while True:
        motors.driveRightOnly(TURNSPEED)
        motors.driveLeftOnly(-TURNSPEED)
        pass
    return 1
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
