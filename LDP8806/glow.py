#!/usr/bin/python

import RPi.GPIO as GPIO, Image, time
import sys
import random

# Configurable values
dev       = "/dev/spidev0.0"
pixels    = 160

def getRandomPixel():
	pixel = bytearray(3)
	pixel[0] = random.randrange(0,255)
	pixel[1] = random.randrange(0,255)
	pixel[2] = random.randrange(0,255)
	return pixel

def setPixels(startPos,count,rgb):
	for p in range(startPos,count):
		offset = p * 3
		buff[offset] = gamma[rgb[1]]
		buff[offset+1] = gamma[rgb[0]]
		buff[offset+2] = gamma[rgb[2]]

def updateStrip():
	spidev.write(buff)
        spidev.flush()


# Open SPI device
spidev    = file(dev, "wb")

# Calculate gamma correction table.  This includes
# LPD8806-specific conversion (7-bit color w/high bit set).
gamma = bytearray(256)
for i in range(256):
        gamma[i] = 0x80 | int(pow(float(i) / 255.0, 2.5) * 127.0 + 0.5)


print "Setting up for %d pixels" % pixels

# Create a bit bytearray for the entire LED strip
buff = bytearray(pixels * 3 + 1)
dimmedPixel = bytearray(3)

while True:
	displayPixel = getRandomPixel()
	for i in range(-10,10):
		# convert to 0->10->0
		j = 10 - abs(i)
		brightness = j / 10.0
		print brightness
		dimmedPixel[0] = int(displayPixel[0] * brightness)
		dimmedPixel[1] = int(displayPixel[1] * brightness)
		dimmedPixel[2] = int(displayPixel[2] * brightness)

		setPixels(0,pixels,dimmedPixel)
		updateStrip()
		if(i==0):
			time.sleep(0.75)
		else:
			time.sleep(0.25)
	time.sleep(1)
