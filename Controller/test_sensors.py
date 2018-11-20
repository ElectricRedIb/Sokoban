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

RIP = True

DRIVE = "Drive"
TURNRIGHT = "Turn right"
TURNLEFT = "Turn left"
REVERSE = "Reverse"
PUSH = "Push can"
GOAL = "GOAL!"

class actionState(object):
	"""docstring for state."""
	def __init__(self, action,repeateAction):
		self.action = action
		self.repeateAction = repeateAction

def makeActions(listOfactions):
    actionList = []
    repeate = 1
    lengthOfList = len(listOfactions)
    for i in range(0,lengthOfList):
        if (i < lengthOfList-1):
            if (listOfactions[i] == listOfactions[i+1]):
                repeate = repeate + 1
            else:
                actionList.append(actionState(listOfactions[i],repeate))
                repeate = 1
        else:
            actionList.append(actionState(listOfactions[i],repeate))
    return actionList

state = DRIVE
complete = False
#inf program need RIP = True
#makeActions([DRIVE,TURNRIGHT,DRIVE,PUSH,REVERSE,TURNLEFT,DRIVE,TURNRIGHT,DRIVE,DRIVE,TURNRIGHT,DRIVE,TURNRIGHT,DRIVE,PUSH,REVERSE,TURNLEFT,DRIVE,TURNRIGHT,DRIVE,DRIVE,TURNRIGHT,GOAL])
DOTHIS = makeActions([DRIVE,TURNRIGHT,DRIVE,PUSH,REVERSE,TURNLEFT,DRIVE,TURNRIGHT,DRIVE,DRIVE,TURNRIGHT,DRIVE,TURNRIGHT,DRIVE,PUSH,REVERSE,TURNLEFT,DRIVE,TURNRIGHT,DRIVE,DRIVE,TURNRIGHT,GOAL])##[PUSH,REVERSE,TURNRIGHT,DRIVE,TURNLEFT,DRIVE,TURNLEFT,DRIVE,TURNLEFT,GOAL]#[DRIVE,REVERSE,TURNRIGHT,GOAL]#[DRIVE,TURNLEFT,DRIVE,TURNLEFT,DRIVE,TURNLEFT,DRIVE,TURNLEFT,DRIVE,TURNRIGHT,DRIVE,TURNRIGHT,DRIVE,TURNRIGHT,DRIVE,TURNRIGHT,GOAL]
pointer = 0
while not complete:
	state = DOTHIS[pointer].action
	stateRepeate = DOTHIS[pointer].repeateAction
	print(state)
	if state == DRIVE:
		if controller.drive(stateRepeate):
			pointer = pointer + 1
			if DOTHIS[pointer].action == TURNLEFT or DOTHIS[pointer].action == TURNRIGHT:
				#print("here!")
				motors.moveRel(115)
			#print("change state",DOTHIS[pointer])
	elif state == TURNRIGHT:
		if (controller.turn('right')):
			pointer = pointer + 1
			#print("change state",DOTHIS[pointer])
	elif state == TURNLEFT:
		if (controller.turn('left')):
			pointer = pointer + 1
			#print("change state",DOTHIS[pointer])
	elif state == REVERSE:
		if controller.rev():
			pointer = pointer + 1
	elif state == PUSH:
		if controller.push():
			pointer = pointer + 1
	elif state == GOAL:
		if RIP:
			pointer = 0
		else:
			complete = True


print('Program ended')
motors.stopMotors()
