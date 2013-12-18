#!/usr/bin/python

import RPi.GPIO as GPIO, Image, time
import sys
import random

# Configurable values
dev       = "/dev/spidev0.0"
pixels    = 160
pixelsOn  = 3

# Create a bit bytearray for the entire LED strip
buff = bytearray(pixels * 3 + 1)
blankPixel = bytearray(3)
dwellTime = 5 # sec

def getPixel(r,g,b):
	pixel = bytearray(3)
	pixel[0] = r
	pixel[1] = g
	pixel[2] = b
	return pixel

def getRandomPixel():
	pixel = bytearray(3)
	pixel[0] = random.randrange(0,255)
	pixel[1] = random.randrange(0,255)
	pixel[2] = random.randrange(0,255)
	return pixel

def setPixels(startPos,count,rgb,brightness=1):
	for p in range(startPos,count):
		setPixel(p,rgb,brightness)

def setPixel(pos,rgb,brightness=1):
	offset = pos * 3
	# pixels need to be sent in GRB order
	buff[offset] = gamma[int(rgb[1]*brightness)]
	buff[offset+1] = gamma[int(rgb[0]*brightness)]
	buff[offset+2] = gamma[int(rgb[2]*brightness)]

def setPixelTrail(pos,rgb,length):
	dimmingFactor = 0.5
	for i in range(length):
		actualPos = pos - i
		brightness = 1/(i+1) * dimmingFactor + 1-dimmingFactor
		if(actualPos >= 0):
			setPixel(actualPos,rgb,brightness)

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

def glow(rgb,pixelList):
	for i in range(-10,10):
		# convert to 0 -> 10 -> 0
		j = 10 - abs(i)
		brightness = j / 10.0
		for p in pixelList:
			setPixel(p,rgb,brightness)
		paint()
		if(i == 0):
			time.sleep(dwellTime)
		else:
			time.sleep(0.05)

while True:
	setPixels(0,pixels,[0,0,0])
	onpixels = [random.randrange(0,pixels) for i in range(pixelsOn)]
	print onpixels
	glow(getRandomPixel(),onpixels)
