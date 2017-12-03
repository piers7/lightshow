# Arches 
# NeoPixel light show for 'leaping arches'
# 
# Based on NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
# itself based on Arduino NeoPixel library strandtest example.
import time
import sys
import random

from neopixel import *


# LED strip configuration:
LED_COUNT   = 60      # Number of LED pixels.
LED_PIN     = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA     = 5       # DMA channel to use for generating signal (try 5)
LED_INVERT  = False   # True to invert the signal (when using NPN transistor level shift)

ARCH_COUNT = 2 # Nuober of arches within LED_COUNT. Each arch will animate slightly differently

# Override some defaults from the command line
if sys.argv[1]:
	LED_COUNT = int(sys.argv[1])
if sys.argv[2]:
	ARCH_COUNT = int(sys.argv[2])

ARCH_SIZE = LED_COUNT / ARCH_COUNT

# Define functions which animate LEDs in various ways.
def clear():
	for i in range(strip.numPixels()):
		strip.setPixelColor(i,0)

def colorWipe(strip, color, wait_ms=50):
	"""Wipe color across display a pixel at a time."""
	for i in range(strip.numPixels()):
		strip.setPixelColor(i, color)
		strip.show()
		time.sleep(wait_ms/1000.0)

def theaterChase(strip, color, wait_ms=50, iterations=10):
	"""Movie theater light style chaser animation."""
	for j in range(iterations):
		for q in range(3):
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, color)
			strip.show()
			time.sleep(wait_ms/1000.0)
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, 0)

def wheel(pos):
	"""Generate rainbow colors across 0-255 positions."""
	if pos < 85:
		return Color(pos * 3, 255 - pos * 3, 0)
	elif pos < 170:
		pos -= 85
		return Color(255 - pos * 3, 0, pos * 3)
	else:
		pos -= 170
		return Color(0, pos * 3, 255 - pos * 3)

def rainbow(strip, wait_ms=20, iterations=1):
	"""Draw rainbow that fades across all pixels at once."""
	for j in range(256*iterations):
		for i in range(strip.numPixels()):
			strip.setPixelColor(i, wheel((i+j) & 255))
		strip.show()
		time.sleep(wait_ms/1000.0)

def rainbowCycle(strip, wait_ms=20, iterations=5):
	"""Draw rainbow that uniformly distributes itself across all pixels."""
	for j in range(256*iterations):
		for i in range(strip.numPixels()):
			strip.setPixelColor(i, wheel(((i * 256 / strip.numPixels()) + j) & 255))
		strip.show()
		time.sleep(wait_ms/1000.0)

def theaterChaseRainbow(strip, wait_ms=50):
	"""Rainbow movie theater light style chaser animation."""
	for j in range(256):
		for q in range(3):
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, wheel((i+j) % 255))
			strip.show()
			time.sleep(wait_ms/1000.0)
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, 0)

def basicArchCross(strip, rgb, wait_ms=20):
	# fire across
	for i in range(ARCH_SIZE):
		for a in range(ARCH_COUNT):
			offset = i + a*ARCH_SIZE
			strip.setPixelColor(offset, rgb)	
		strip.show()
		time.sleep(wait_ms/1000.0)
		for a in range(ARCH_COUNT):
			offset = i + a*ARCH_SIZE
			strip.setPixelColor(offset, 0)	

	# fire back again
	for i in reversed(range(ARCH_SIZE)):
		for a in range(ARCH_COUNT):
			offset = i + a*ARCH_SIZE
			strip.setPixelColor(offset, rgb)	
		strip.show()
		time.sleep(wait_ms/1000.0)
		for a in range(ARCH_COUNT):
			offset = i + a*ARCH_SIZE
			strip.setPixelColor(offset, 0)	

def delay(ms):
	time.sleep(ms/1000)

class Projectile:
	gravity = -9.8 * 2 # in m/sec
	
	def __init__ (self, id = 0, velocity = 9.8, height = 0):
		self.id = id
		self.height = height
		self.velocity = velocity
		self.effectiveGravity = Projectile.gravity
		
	def update(self, ms = 1):
		self.height += self.velocity * ms / 1000
		self.velocity += self.effectiveGravity * ms / 1000

def fireProjectiles(numProjectiles = 1, wait_ms = 10):
	projectiles = [Projectile(p, random.uniform(25,40)) for p in range(numProjectiles)]
	running = numProjectiles
		
	while running > 0:
		for i in range(numProjectiles):
			p = projectiles[i]
			if(p.height >= 0 and p.height < ARCH_SIZE):
				pixelIndex = int(p.height + ARCH_SIZE * p.id)
				#print pixelIndex

				# blank where it was
				strip.setPixelColor(pixelIndex, 0)
				p.update(wait_ms)
				pixelIndex = int(p.height + ARCH_SIZE * p.id)

				# if we get over the middle of the arch we have to fall down the far sise
				if(p.height > ARCH_SIZE / 2):
					p.effectiveGravity = abs(p.effectiveGravity)
					
				strip.setPixelColorRGB(pixelIndex, 170, 0, 0)
		strip.show()
		delay(wait_ms)
		running = sum(1 for p in projectiles if p.height >= 0 and p.height < ARCH_SIZE)
	delay(wait_ms * 2)

# Main program logic follows:
if __name__ == '__main__':
	# Create NeoPixel object with appropriate configuration.
	strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT)
	# Intialize the library (must be called once before other functions).
	strip.begin()
	clear()
	strip.show()
	
	print 'Running with %d' % LED_COUNT
	print 'Press Ctrl-C to quit.'
	while True:
		fireProjectiles(2)
		#basicArchCross(strip, Color(100,100,100))
		# Color wipe animations.
		#colorWipe(strip, Color(255, 0, 0))  # Red wipe
		#colorWipe(strip, Color(0, 255, 0))  # Blue wipe
		#colorWipe(strip, Color(0, 0, 255))  # Green wipe
		# Theater chase animations.
		
		##theaterChase(strip, Color(127, 127, 127))  # White theater chase
		#theaterChase(strip, Color(127,   0,   0))  # Red theater chase
		#theaterChase(strip, Color(  0,   0, 127))  # Blue theater chase
		
		# Rainbow animations.
		#rainbow(strip)
		#rainbowCycle(strip)
		#theaterChaseRainbow(strip)
