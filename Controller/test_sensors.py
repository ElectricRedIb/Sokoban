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
TURN = 1
REVERSE = 2
PUSH = 3
GOAL = 4

FORWARD = 1
BACKWARDS = -1

state = DRIVE
b = 1
DOTHIS = [DRIVE,DRIVE,TURN,GOAL]
pointer = 0
while b:
	state = DOTHIS[pointer]
	if state == DRIVE:
		if controller.drive(FORWARD):
			pointer = pointer + 1
			print("change state",DOTHIS[pointer])
	elif state == TURN:
		if (controller.turn('right',1)):
			pointer = pointer + 1
			print("change state",DOTHIS[pointer])
	elif state == REVERSE:
		if controller.drive(BACKWARDS):
			state = GOAL
	elif state == PUSH:
		pass
	elif state == GOAL:
		pointer = 0


print('Program ended')
motors.stopMotors()
