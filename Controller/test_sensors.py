#!/usr/bin/python3
print("\n------------------------ Program start ------------------------\n")
import controller
import motors
import signal
from time import sleep
from datetime import datetime as dt
#exit control
def signal_handler(sig, frame):
	print('Shutting down gracefully')
	motors.stopMotors()
	exit(0)

# Install the signal handler for CTRL+C
signal.signal(signal.SIGINT, signal_handler)
#print('Press Ctrl+C to exit')

RIP = False

FORWARD = 'F'
TURNRIGHT = 'R'
TURNLEFT = 'L'
REVERSE = 'B'
DELIVER_CAN = 'D'
GOAL = 'G'



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
	actionList.append(actionState('G',1))
	return actionList
print("\n------------------------- Choose path! ------------------------\n")
print("\"map\" will read the map file!")
print("Otherwise enter only valid chars F,R,L,B and D!")
filename = input("What to do then ?: ")
path = ""
if filename == "map":
	with open(filename) as map:
		path = map.read()
	map.close()
else:
	path = filename

complete = False
#inf program need RIP = True
#makeActions([DRIVE,TURNRIGHT,DRIVE,PUSH,REVERSE,TURNLEFT,DRIVE,TURNRIGHT,DRIVE,DRIVE,TURNRIGHT,DRIVE,TURNRIGHT,DRIVE,PUSH,REVERSE,TURNLEFT,DRIVE,TURNRIGHT,DRIVE,DRIVE,TURNRIGHT,GOAL])
DOTHIS = makeActions(path)
print("\n" + path)
if filename == "map": # only for cosmetics
	print("------------------------ Run the robot! -----------------------\n")
else:
	print("\n------------------------ Run the robot! -----------------------\n")
pointer = 0
startTime = dt.now()
while not complete:
	if pointer%10:
		controller.batteryState()
	state = DOTHIS[pointer].action
	stateRepeate = DOTHIS[pointer].repeateAction
	print(state, end='')
	if state == FORWARD:
		if controller.drive(stateRepeate):
			pointer = pointer + 1
			if DOTHIS[pointer].action == TURNLEFT or DOTHIS[pointer].action == TURNRIGHT:
				#print("here!")
				motors.moveRel(110)
			#print("change state",DOTHIS[pointer])
	elif state == TURNRIGHT:
		if (controller.turn('right',stateRepeate)):
			pointer = pointer + 1
			#print("change state",DOTHIS[pointer])
	elif state == TURNLEFT:
		if (controller.turn('left',stateRepeate)):
			pointer = pointer + 1
			#print("change state",DOTHIS[pointer])
	elif state == REVERSE:
		if controller.rev():
			pointer = pointer + 1
	elif state == DELIVER_CAN:
		if controller.push():
			if controller.rev():
				pointer = pointer + 1
	elif state == GOAL:
		if RIP:
			pointer = 0
		else:
			complete = True

motors.stopMotors()
endTime = dt.now()

print("\n\n------------------------ The End " + str(endTime.minute - startTime.minute) + ":" + str(abs(endTime.second - startTime.second)) + "------------------------\n")
