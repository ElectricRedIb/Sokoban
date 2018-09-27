#!/usr/bin/python3

#import ev3dev.ev3 as ev3
import signal
import numpy as np
import time as t

# Connect two motors and two (different) light sensors
#mA = ev3.LargeMotor('outA')
#mB = ev3.LargeMotor('outB')

#lightSensorLeft = ev3.ColorSensor('in1')
#lightSensorRight = ev3.LightSensor('in2')

# Use constants to later acces motor speeds and sensor thresholds
#THRESHOLD_LEFT = 30
#THRESHOLD_RIGHT = 350

#BASE_SPEED = 30
#TURN_SPEED = 80

# Check if the motors are connected

#assert lightSensorLeft.connected, "LightSensorLeft(ColorSensor) is not connected"
#assert lightSensorRight.connected, "LightSensorRight(LightSensor) is not conected"


# Set the motor mode
#mB.run_direct()
#mA.run_direct()

#mA.polarity = "inversed"
#mB.polarity = "normal"
#'''
# The example doesn't end on its own.
# Use CTRL-C to exit it (needs command line).
# This is a generic way to be informed
# of this event and then take action.
def signal_handler(sig, frame):
	print('Shutting down gracefully')
	#mA.duty_cycle_sp = 0
	#mB.duty_cycle_sp = 0

	exit(0)


# Install the signal handler for CTRL+C
signal.signal(signal.SIGINT, signal_handler)
print('Press Ctrl+C to exit')

# Endless loop reading sensors and controlling motors.
'''
while True:

	sensorLeft = lightSensorLeft.value()
	sensorRight = lightSensorRight.value()

	print("sensorLeft: ", sensorLeft, " sensorRight: ", sensorRight)
	mA.duty_cycle_sp = BASE_SPEED

	motorC.duty_cycle_sp =BASE_SPEED
	mB.duty_cycle_sp = BASE_SPEED
'''

'''
alpha_a = -0.02
theta_a = 50
sensorRight = 1/(1+ np.exp(alpha_a*(theta_a - lightSensorRight )))
'''
'''
w00 = 1
out0 = np.tanh(w00*sensorRight)
'''
class neuronInput:
	"""docstring for neuronInput."""
	alpha = -0.02
	theta = 50
	def __init__(self):
		pass
	def caloutput(self, input):
		return 1/(1+ np.exp(self.alpha*(self.theta - input )))

jj = neuronInput()

lightSensorRight = 0
sensorRight = 0
while True:
	sensorRight = jj.caloutput(lightSensorRight)
	print('sensor neuron',sensorRight, 'raw sensor output', lightSensorRight)
	out0 = np.tanh(sensorRight)
	lightSensorRight  = lightSensorRight +1
	t.sleep(0.25)
