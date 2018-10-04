#!/usr/bin/python3
#https://sites.google.com/site/ev3python/learn_ev3_python/using-motors
#http://docs.ev3dev.org/projects/lego-linux-drivers/en/ev3dev-jessie/motor_data.html

import ev3dev.ev3 as ev3
import sensor
from time import sleep



motorLeft = ev3.LargeMotor('outA')
motorRight = ev3.LargeMotor('outD')
#motorTurn = ev3.MediumMotor('outC')
motorLeft.polarity = "normal"#"inversed"
motorRight.polarity = "normal"#"inversed"
sensor.setmodeSensorsLR(sensor.REFLECT)
#def turnBackWheel(position):
#    motorTurn.run_to_rel_pos(position_sp=position, speed_sp=900, stop_action="hold")
def turnRight(position):
    motorRight.run_to_rel_pos(position_sp=position, speed_sp=600, stop_action="brake")
    sleep(0.3)
def turnLeft(position):
    motorLeft.run_to_rel_pos(position_sp=position, speed_sp=600, stop_action="brake")
    sleep(0.3)
def stopMotors():
    motorLeft.stop(stop_action="brake")
    motorRight.stop(stop_action="brake")
#    motorTurn.stop()
def driveLeftOnly(speed): # speed -1000 to 1000 uses inbuild speed control
    motorLeft.run_forever(speed_sp=speed)
def driveRightOnly(speed): # speed -1000 to 1000 uses inbuild speed control
    motorRight.run_forever(speed_sp=speed)

def driveLeft(state, speed):
    if state == sensor.BLACKLINE:
        motorLeft.stop(stop_action="brake")
    elif state == sensor.ADJUSTSPEED:
        newspeed = speed * 0.8
        motorLeft.run_forever(speed_sp=newspeed)
    elif state == sensor.ONLINE:
        motorLeft.run_forever(speed_sp=speed)


def driveRight(state, speed):
    if state == sensor.BLACKLINE:
        motorRight.stop(stop_action="brake")
    elif state == sensor.ADJUSTSPEED:
        newspeed = speed * 0.8
        motorRight.run_forever(speed_sp=newspeed)
    elif state == sensor.ONLINE:
        motorRight.run_forever(speed_sp=speed)


def drive(speed):
    left, right = sensor.readLineSensors()
    driveLeft(left, speed)
    driveRight(right, speed)
    if not (left + right):
        return 1
    return 0

TURNSPEED = 400
def turn(direction,turns):
    done = 0
    state = 0
    amountOfTurns = turns
    while not done:
        left, right = sensor.readLineSensors()
        if state == 0:
            if left + right == 4:
                state = 1
        elif state == 1:
            if direction == 'right':
                driveRightOnly(TURNSPEED)
            else:
                driveLeftOnly(TURNSPEED)
            if right == sensor.BLACKLINE:
                state = 2
        elif state == 2:
            if right == sensor.ONLINE:
                state = 3
        elif state == 3:
            if direction == 'right':
                driveLeftOnly(-TURNSPEED)
                driveRightOnly(TURNSPEED)
            else:
                driveLeftOnly(TURNSPEED)
                driveRightOnly(-TURNSPEED)
            state = 4
        elif state == 4:
            if left == sensor.BLACKLINE:
                amountOfTurns = amountOfTurns - 1
                if amountOfTurns:
                    state = 5
                else:
                    state = 10
        elif state  == 5:
            if left == sensor.ONLINE:
                state = 4
        elif state == 10:
            stopMotors()
            done = 1
    return 1
