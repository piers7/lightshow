#!/usr/bin/python

import RPi.GPIO as GPIO, Image, time
import sys
import random

# Configurable values
dev       = "/dev/spidev0.0"
pixels    = 160
spacing   = 10
traillength = 4

# Create a bit bytearray for the entire LED strip
buff = bytearray(pixels * 3 + 1)
blankPixel = bytearray(3)

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

def upwardsSpiral(displayPixel, repeatCount):
	for repeats in range(repeatCount):
		for i in range(0,spacing):
			for p in range(pixels - 1):
				if p % spacing == i:
					setPixelTrail(p,displayPixel,traillength)
				else:
					setPixel(p,blankPixel)
			setPixel(pixels-1,displayPixel)
			paint()
			time.sleep(0.05)

def flash(displayPixel,repeatCount):
	for repeats in range(repeatCount):
		for i in range(0, pixels):
			setPixel(i,displayPixel)
		paint()
		time.sleep(0.5)
		for i in range(0, pixels):
			setPixel(i,blankPixel)
		paint()
		time.sleep(0.5)

def multiColored(repeatCount, palette):
	for repeats in range(repeatCount):
		for i in range(0, pixels):
			setPixel(i, palette[(i+repeats) % len(palette)])

		paint()
		time.sleep(0.05)

def glow(rgb):
	for i in range(-10,10):
		# convert to 0 -> 10 -> 0
		j = 10 - abs(i)
		brightness = j / 10.0
		setPixels(0,pixels,rgb,brightness)
		paint()
		if(i == 0):
			time.sleep(3)
		else:
			time.sleep(0.05)



redAndGreen = [
	getPixel(255,0,0),
	getPixel(255,0,0),
	getPixel(0,0,0),
	getPixel(0,255,0),
	getPixel(0,255,0),
	getPixel(0,0,0)
]
blueAndYellow = [
	getPixel(0,0,255),
	getPixel(0,0,0),
	getPixel(0xFF,0xAA,0)
]
while True:
	displayPixel = getRandomPixel()
	for i in range(5):
		glow(displayPixel)
		time.sleep(0.5)
		displayPixel = getRandomPixel()
	for i in range(10):
		multiColored(16-1, redAndGreen)
		multiColored(16-1, blueAndYellow)
	flash(displayPixel,2)
	for i in range(5):
		upwardsSpiral(displayPixel, 10)
		displayPixel = getRandomPixel()
