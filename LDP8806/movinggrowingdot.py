#!/usr/bin/python

# Light painting / POV demo for Raspberry Pi using
# Adafruit Digital Addressable RGB LED flex strip.
# ----> http://adafruit.com/products/306

import RPi.GPIO as GPIO, Image, time
import sys
import random

# Configurable values
dev       = "/dev/spidev0.0"
pixels    = 160
displayPixel = bytearray(3)
displayPixel[0] = random.randrange(0,255)
displayPixel[1] = random.randrange(0,255)
displayPixel[2] = random.randrange(0,255)

# Open SPI device
spidev    = file(dev, "wb")

# Calculate gamma correction table.  This includes
# LPD8806-specific conversion (7-bit color w/high bit set).
gamma = bytearray(256)
for i in range(256):
        gamma[i] = 0x80 | int(pow(float(i) / 255.0, 2.5) * 127.0 + 0.5)

def setPixels(range, rgb, brightness=1):
	for x in range:
		setPixel(x, rgb, brightness)
		
def setPixel(pos,rgb,brightness=1):
	offset = pos * 3

	# pixels need to be sent in GRB order
	buff[offset] = gamma[int(rgb[1]*brightness)]
	buff[offset+1] = gamma[int(rgb[0]*brightness)]
	buff[offset+2] = gamma[int(rgb[2]*brightness)]

print "Setting up for %d pixels" % pixels

currentPos = 0
numOfLights = 1

# Create a bit bytearray for the entire LED strip
# need to explicitly zero out the blank pixels using the gamma conversion
# because of the high bit set
buff = bytearray(pixels * 3 + 1)
setPixels(range(pixels),[0xff,0xff,0xff],0)

colors = bytearray(pixels * 3)
for x in range(pixels):
	colors[x*3] = random.randrange(0,255)
	colors[x*3+1] = random.randrange(0,255)
	colors[x*3+2] = random.randrange(0,255)

print "Running main loop"
while True:
	print "Number of lights %d" % numOfLights
	while currentPos < 160 -1:
		# blank the strip
		setPixels(range(pixels),[0xff,0xff,0xff],0)

        # Set pixel on in the *current* active position
        # print offset
		for x in range(numOfLights):
			if(currentPos + x < pixels):
				color = [colors[x*3],colors[x*3+1],colors[x*3+2]]
				setPixel(currentPos + x, color)

        # Show the display
		spidev.write(buff)
		spidev.flush()
		currentPos = (currentPos + 1)

	while currentPos >= 0:
		# blank the strip
		setPixels(range(pixels),[0xff,0xff,0xff],0)

        # Set pixel on in the *current* active position
        # print offset
		for x in range(numOfLights):
			if(currentPos + x < pixels):
				color = [colors[x*3],colors[x*3+1],colors[x*3+2]]
				setPixel(currentPos + x, color)

        # Show the display
		spidev.write(buff)
		spidev.flush()

        # time.sleep(.01)
		currentPos = (currentPos - 1)

	currentPos = 0
	numOfLights +=1
	displayPixel[0] = random.randrange(0,255)
	displayPixel[1] = random.randrange(0,255)
	displayPixel[2] = random.randrange(0,255)
