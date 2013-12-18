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

# internal state
buff = bytearray(pixels * 3 + 1)
# Open SPI device
spidev    = file(dev, "wb")

def setColor(r,g,b):
	displayPixel[0] = gamma[r]
	displayPixel[1] = gamma[g]
	displayPixel[2] = gamma[b]

def changeColor():
	setColor(random.randrange(0,255),random.randrange(0,255),random.randrange(0,255))

def setPixel(index,rgb):
	offset = index * 3
	if(offset < len(buff) -1):
	        buff[offset] = gamma[rgb[1]]
        	buff[offset+1] = gamma[rgb[0]]
        	buff[offset+1] = gamma[rgb[2]]

def clearPixel(index): 
	offset = index * 3
	if(offset < len(buff)-1):
		buff[offset] = buff[offset+1] = buff[offset+2] = gamma[0]

def chase(startIndex,length,rgb):
	currentPos = startIndex
	endIndex = startIndex + length -1
	print "Chasing between %d and %d" % (startIndex,endIndex)
	while(currentPos < endIndex):
		# print currentPos
		for i in range(startIndex,endIndex):
			# For each iteration of the loop, move the current position along one
			# and repaint all pixels between start and finish
			if(i == currentPos):
				setPixel(i,displayPixel)
			else:
				clearPixel(i)
		spidev.write(buff)
		spidev.flush()
		currentPos+=1
			
# Calculate gamma correction table.  This includes
# LPD8806-specific conversion (7-bit color w/high bit set).
gamma = bytearray(256)
for i in range(256):
        gamma[i] = 0x80 | int(pow(float(i) / 255.0, 2.5) * 127.0 + 0.5)


print "Setting up for %d pixels" % pixels

# Start with the buffer all empty
for i in range(pixels):
	clearPixel(i)

#for i in range(pixels):
#	setPixel(i, displayPixel)
#	for j in range(pixels - i):
#		setPixel(j, displayPixel)
	
spidev.write(buff)
spidev.flush()

for p in range(pixels):
	changeColor()
	chase(0,pixels -p,displayPixel)
