#!/usr/bin/python3

import motors
import sensor
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

while b:
	if state == DRIVE:
		if motors.drive(FORWARD):
			state = TURN
	elif state == TURN:
		if (motors.turn('left',1)):
			state = DRIVE
	elif state == REVERSE:
		pass
	elif state == PUSH:
		pass
	elif state == GOAL:
		b = 0


print('Program ended')
motors.stopMotors()
