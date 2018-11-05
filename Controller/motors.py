#!/usr/bin/python3
#https://sites.google.com/site/ev3python/learn_ev3_python/using-motors
#http://docs.ev3dev.org/projects/lego-linux-drivers/en/ev3dev-jessie/motor_data.html

import ev3dev.ev3 as ev3
from time import sleep

motorRight = ev3.LargeMotor('outA')
motorLeft = ev3.LargeMotor('outD')
#motorTurn = ev3.MediumMotor('outC')
motorRight.polarity = "normal"#"inversed"#
motorLeft.polarity = "normal"#"inversed"#


#def turnBackWheel(position):
#    motorTurn.run_to_rel_pos(position_sp=position, speed_sp=900, stop_action="hold")
def moveRel(position):
    motorRight.run_to_rel_pos(position_sp=position, speed_sp=600, stop_action="brake")
    motorLeft.run_to_rel_pos(position_sp=position, speed_sp=600, stop_action="brake")
    motorRight.wait_while('running')
'''
def turnRight(position):
    motorRight.run_to_rel_pos(position_sp=position, speed_sp=600, stop_action="brake")
    sleep(0.3)
def turnLeft(position):
    motorLeft.run_to_rel_pos(position_sp=position, speed_sp=600, stop_action="brake")
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
