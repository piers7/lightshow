#!/usr/bin/python

import RPi.GPIO as GPIO, Image, time
import sys
import random
import datetime

# Configurable values
dev        = "/dev/spidev0.0"
pixelCount = 160
spacing    = 10
traillength = 4
dwellTime = .1 # sec
hourFrom = 19
hourTo = 23

# Create a bit bytearray for the entire LED strip
buff = bytearray(pixelCount * 3 + 1)
blankPixel = bytearray(3)

def getRandomPixel():
	pixel = bytearray(3)
	pixel[0] = random.randrange(0,255)
	pixel[1] = random.randrange(0,255)
	pixel[2] = random.randrange(0,255)
	return pixel

def setAllOff():
	setPixels(0,pixelCount,[0,0,0])

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
			for p in range(pixelCount - 1):
				if p % spacing == i:
					setPixelTrail(p,displayPixel,traillength)
				else:
					setPixel(p,blankPixel)
			setPixel(pixelCount-1,displayPixel)
			paint()
			time.sleep(0.05)

def flash(displayPixel,repeatCount):
	for repeats in range(repeatCount):
		for i in range(0, pixelCount):
			setPixel(i,displayPixel)
		paint()
		time.sleep(0.5)
		for i in range(0, pixelCount):
			setPixel(i,blankPixel)
		paint()
		time.sleep(0.5)

def multiColored(repeatCount, palette):
	for repeats in range(repeatCount):
		for i in range(0, pixelCount):
			setPixel(i, palette[(i+repeats) % len(palette)])

		paint()
		time.sleep(0.05)

def glow(rgb):
	for i in range(-10,10):
		# convert to 0 -> 10 -> 0
		j = 10 - abs(i)
		brightness = j / 10.0
		setPixels(0,pixelCount,rgb,brightness)
		paint()
		if(i == 0):
			time.sleep(3)
		else:
			time.sleep(0.05)

def twinkle(delays):
	lightStates = [0 for i in range(pixelCount)]
	brightness = [0 for i in range(pixelCount)]

	for delay in delays:
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

		paint()
		print delay
		time.sleep( delay )

redAndGreen = [
	[255,0,0],
	[255,0,0],
	[0,0,0],
	[0,255,0],
	[0,255,0],
	[0,0,0]
]
blueAndYellow = [
	[0,0,255],
	[0,0,0],
	[0xFF,0xAA,0]
]

def startup():
	print "Startup"
	startDelayMs = 1000
	endDelayMs = 10
	steps = 250
	delayRange = (startDelayMs - endDelayMs) / (steps * 1.0)
	delays = [(steps-i)/1000.0 for i in range(steps)]
	twinkle(delays)

def run():
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

def shutdown():
	print "shutdown"	
	for i in range(pixelCount):
		setPixel(i, [0,0,0])
		paint()
		time.sleep(0.01)

setAllOff()
paint()
while True:
	hour = datetime.datetime.now().hour
	if hour < hourFrom or hour >= hourTo:
		print "Waiting %d" % hour
		setAllOff()
		setPixel(hour,[255,0,0])
		paint()
		time.sleep(10*60)
	else:
		startup()
		while(datetime.datetime.now().hour < hourTo):
			run()
		shutdown()
