# from https://raspberrypihq.com/making-a-led-blink-using-the-raspberry-pi-and-python/
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import sys
from time import sleep # Import the sleep function from the time module

pin = int(sys.argv[1]) if len(sys.argv) > 1 else 8
print str(pin)
GPIO.setwarnings(False) # Ignore warning for now
#GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setmode(GPIO.BCM) # Use logical pin numbering
GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW) # Set pin 8 to be an output pin and set initial value to low (off)

while True: # Run forever
	print "On"
	GPIO.output(pin, GPIO.HIGH) # Turn on
	sleep(1) # Sleep for 1 second

	print "Off"
	GPIO.output(pin, GPIO.LOW) # Turn off
	sleep(1) # Sleep for 1 second
