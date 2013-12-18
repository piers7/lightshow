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

# Create a bit bytearray for the entire LED strip
buff = bytearray(pixels * 3 + 1)

while True:
        displayPixel[0] = (displayPixel[0] + 1) % 255
        displayPixel[1] = (displayPixel[1] + 5) % 255
        displayPixel[2] = (displayPixel[2] + 10) % 255

        for p in range(pixels):
                offset = p * 3
                buff[offset] = gamma[displayPixel[1]]
                buff[offset+1] = gamma[displayPixel[0]]
                buff[offset+2] = gamma[displayPixel[2]]

        spidev.write(buff)
        spidev.flush()

        time.sleep(0.5)
