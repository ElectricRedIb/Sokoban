#!/usr/bin/python3

import sensor
import signal
from time import sleep



#exit control
def signal_handler(sig, frame):
	print('Shutting down gracefully')
	exit(0)

# Install the signal handler for CTRL+C
signal.signal(signal.SIGINT, signal_handler)
print('Press Ctrl+C to exit')


sensor.setmodeSensorsLR(sensor.COLOR)
while True:
    sensor.detectLine()

    sleep(0.5)
