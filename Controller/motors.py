#!/usr/bin/python3
#https://sites.google.com/site/ev3python/learn_ev3_python/using-motors
#http://docs.ev3dev.org/projects/lego-linux-drivers/en/ev3dev-jessie/motor_data.html

import ev3dev.ev3 as ev3


motorLeft = ev3.LargeMotor('outA')
motorRight = ev3.LargeMotor('outB')
#motorTurn = ev3.MediumMotor('outC')



#def turnBackWheel(position):
#    motorTurn.run_to_rel_pos(position_sp=position, speed_sp=900, stop_action="hold")
def stopMotors():
    motorLeft.stop(stop_action="brake")
    motorRight.stop(stop_action="brake")
#    motorTurn.stop()
def driveLeft(speed): # speed -1000 to 1000 uses inbuild speed control
    motorLeft.run_forever(speed_sp=speed)
def driveRight(speed): # speed -1000 to 1000 uses inbuild speed control
    motorRight.run_forever(speed_sp=speed)
