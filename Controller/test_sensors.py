#!/usr/bin/python3

import controller
import motors
import signal
from time import sleep



#exit control
def signal_handler(sig, frame):
	print('Shutting down gracefully')
	motors.stopMotors()
	exit(0)

# Install the signal handler for CTRL+C
signal.signal(signal.SIGINT, signal_handler)
print('Press Ctrl+C to exit')

DRIVE = 0
TURNRIGHT = 1
TURNLEFT = 2
REVERSE = 3
PUSH = 4
GOAL = 5

FORWARD = 1
BACKWARDS = -1

state = DRIVE
complete = 1
DOTHIS = [DRIVE,GOAL]##[PUSH,REVERSE,TURNRIGHT,DRIVE,TURNLEFT,DRIVE,TURNLEFT,DRIVE,TURNLEFT,GOAL]#[DRIVE,REVERSE,TURNRIGHT,GOAL]#[DRIVE,TURNLEFT,DRIVE,TURNLEFT,DRIVE,TURNLEFT,DRIVE,TURNLEFT,DRIVE,TURNRIGHT,DRIVE,TURNRIGHT,DRIVE,TURNRIGHT,DRIVE,TURNRIGHT,GOAL]
pointer = 0
while complete:
	state = DOTHIS[pointer]
	if state == DRIVE:
		if controller.drive(FORWARD):
			pointer = pointer + 1
			motors.moveRel(115)
			#print("change state",DOTHIS[pointer])
	elif state == TURNRIGHT:
		if (controller.turn('right',1)):
			pointer = pointer + 1
			#print("change state",DOTHIS[pointer])
	elif state == TURNLEFT:
		if (controller.turn('left',1)):
			pointer = pointer + 1
			#print("change state",DOTHIS[pointer])
	elif state == REVERSE:
		if controller.rev():
			pointer = pointer + 1
	elif state == PUSH:
		if controller.drive(FORWARD):
			pointer = pointer + 1
	elif state == GOAL:
		pointer = 0


print('Program ended')
motors.stopMotors()
