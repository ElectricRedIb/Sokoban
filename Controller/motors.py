#!/usr/bin/python3
#https://sites.google.com/site/ev3python/learn_ev3_python/using-motors
#http://docs.ev3dev.org/projects/lego-linux-drivers/en/ev3dev-jessie/motor_data.html

import ev3dev.ev3 as ev3
import sensor
from time import sleep



motorRight = ev3.LargeMotor('outA')
motorLeft = ev3.LargeMotor('outD')
#motorTurn = ev3.MediumMotor('outC')
motorRight.polarity = "normal"#"inversed"
motorLeft.polarity = "normal"#"inversed"
sensor.setmodeSensorsLR(sensor.REFLECT)

TURNSPEED = 400
STANDARTDRIVESPEED = 700

DRIVESPEED = STANDARTDRIVESPEED

#def turnBackWheel(position):
#    motorTurn.run_to_rel_pos(position_sp=position, speed_sp=900, stop_action="hold")
'''
def turnRight(position):
    motorRight.run_to_rel_pos(position_sp=position, speed_sp=600, stop_action="brake")
    sleep(0.3)
'''
def coastMotors():
    motorRight.stop(stop_action="coast")
    motorLeft.stop(stop_action="coast")
def stopMotors():
    motorRight.stop(stop_action="brake")
    motorLeft.stop(stop_action="brake")
#    motorTurn.stop()
def driveRightOnly(speed): # speed -1000 to 1000 uses inbuild speed control
    motorRight.run_forever(speed_sp=speed)
def driveLeftOnly(speed): # speed -1000 to 1000 uses inbuild speed control
    motorLeft.run_forever(speed_sp=speed)

def driveRight(state, speed):
    if state == sensor.BLACKLINE:
        motorRight.stop(stop_action="brake")
    elif state == sensor.ADJUSTSPEED:
        newspeed = speed * 0.8
        motorRight.run_forever(speed_sp=newspeed)
    elif state == sensor.ONLINE:
        motorRight.run_forever(speed_sp=speed)

def driveLeft(state, speed):
    if state == sensor.BLACKLINE:
        motorLeft.stop(stop_action="brake")
    elif state == sensor.ADJUSTSPEED:
        newspeed = speed * 0.8
        motorLeft.run_forever(speed_sp=newspeed)
    elif state == sensor.ONLINE:
        motorLeft.run_forever(speed_sp=speed)

def drive(direction):
    global DRIVESPEED
    speed = DRIVESPEED * direction
    if sensor.readGripSensor() == sensor.BLACKLINE:
        speed = TURNSPEED * direction
        DRIVESPEED = speed
        print("change speed")
    #print("DRIVESPEED", DRIVESPEED)
    left, right = sensor.readLineSensors()
    driveRight(right, speed)
    driveLeft(left, speed)
    if not (left + right):
        return 1
    return 0


def turn(direction,turns):
    global DRIVESPEED
    DRIVESPEED = STANDARTDRIVESPEED
    done = 0
    state = 0
    amountOfTurns = turns
    while not done:
        left, right = sensor.readLineSensors()
        if state == 0:
            if left + right == 4:
                state = 1
        elif state == 1:  # ------------------------- State 1
            if direction == 'right':
                driveLeftOnly(TURNSPEED)
                if left == sensor.BLACKLINE:
                    state = 2
            else:
                driveRightOnly(TURNSPEED)
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
                driveRightOnly(-TURNSPEED)
                driveLeftOnly(TURNSPEED)
            else:
                driveRightOnly(TURNSPEED)
                driveLeftOnly(-TURNSPEED)
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
            stopMotors()
            done = 1
    return 1
