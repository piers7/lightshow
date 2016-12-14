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


print "Setting up for %d pixels" % pixels

currentPos = 0
buff = bytearray(pixels * 3 + 1)
while True:
        # print currentPos
        
        # Create a bit bytearray for the entire LED strip
        # need to explicitly zero out the blank pixels using the gamma conversion
        # because of the high bit set
        for x in range(pixels):
                offset = x * 3
                buff[offset] = gamma[0]
                buff[offset+1] = gamma[0]
                buff[offset+2] = gamma[0]

        # Set pixel on in the *current* active position
        # print offset
        offset = currentPos * 3
        buff[offset] = gamma[displayPixel[1]]
        buff[offset+1] = gamma[displayPixel[0]]
        buff[offset+2] = gamma[displayPixel[2]]

        # Show the display
        spidev.write(buff)
        spidev.flush()

        # time.sleep(.01)
        currentPos = (currentPos + 1)
        if(currentPos > pixels -1):
                currentPos = 0
                displayPixel[0] = random.randrange(0,255)
                displayPixel[1] = random.randrange(0,255)
                displayPixel[2] = random.randrange(0,255)


