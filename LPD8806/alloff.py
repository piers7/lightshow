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
blankPixel = bytearray(3)

# Open SPI device
spidev    = file(dev, "wb")

# Calculate gamma correction table.  This includes
# LPD8806-specific conversion (7-bit color w/high bit set).
gamma = bytearray(256)
for i in range(256):
        gamma[i] = 0x80 | int(pow(float(i) / 255.0, 2.5) * 127.0 + 0.5)

# Create a bit bytearray for the entire LED strip
buff = bytearray(pixels * 3 + 1)

for i in range(pixels):
	offset = i * 3
        buff[offset] = gamma[0]
        buff[offset+1] = gamma[0]
        buff[offset+2] = gamma[0]

        spidev.write(buff)
        spidev.flush()

