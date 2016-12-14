#!/usr/bin/python

import RPi.GPIO as GPIO, Image, time
import sys
import random

# Configurable values
dev       = "/dev/spidev0.0"
pixelCount = 160
pixelsOn  = 3

# Create a bit bytearray for the entire LED strip
buff = bytearray(pixelCount * 3 + 1)
blankPixel = bytearray(3)
dwellTime = .1 # sec

def getPixel(r,g,b):
	pixel = bytearray(3)
	pixel[0] = r
	pixel[1] = g
	pixel[2] = b
	return pixel

def setPixel(pos,rgb,brightness=1):
	offset = pos * 3
	# pixels need to be sent in GRB order
	buff[offset] = gamma[int(rgb[1]*brightness)]
	buff[offset+1] = gamma[int(rgb[0]*brightness)]
	buff[offset+2] = gamma[int(rgb[2]*brightness)]

def paint():
	spidev.write(buff)
        spidev.flush()


# Open SPI device
spidev    = file(dev, "wb")

# Calculate gamma correction table.  This includes
# LPD8806-specific conversion (7-bit color w/high bit set).
gamma = bytearray(256)
for i in range(256):
        gamma[i] = 0x80 | int(pow(float(i) / 255.0, 2.5) * 127.0 + 0.5)

def twinkle():
	lightStates = [0 for i in range(pixelCount)]
	brightness = [0 for i in range(pixelCount)]

	while(True):
	    # activate a new random cell
	    on = random.randrange(0,pixelCount)
	    while(lightStates[on] > 0):
	        on = random.randrange(0,pixelCount)
	    lightStates[on] = 1

	    # progress all the active cells
	    for i in range(pixelCount):
	        state = lightStates[i];
	        if(state >= 10):
	            state = 0
	        elif state > 0:
	            state += 1
	        lightStates[i] = state

	        j = 5 - abs(state -5)
	        brightness[i] = j / 5.0
		setPixel(i, [0xff,0xff,0xff], brightness[i])
	    
	    #print(brightness)
	    paint()
	    time.sleep(dwellTime)

twinkle()
