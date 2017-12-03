# Arches 
# NeoPixel light show for 'leaping arches'
# 
# Based on NeoPixel library strandtest example by Tony DiCola (tony@tonydicola.com)
# itself based on Arduino NeoPixel library strandtest example.
import time
import sys
import random
import math

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

def getRandomColor():
	#r = random() * 255
	#g = random() * 255
	#b = random() * 255
	#return strip.Color(r,g,b)
	return wheel(int(random.random() * 255))

class Projectile:
	def __init__ (self, id = 0, velocity = 9.8, height = 0, offset = 0, trailLength = 4):
		self.id = id
		self.height = height
		self.velocity = velocity
		self.color = getRandomColor()
		self.offset = offset
		self.trailLength = 4
		self.trail = [height]
		
	def update(self, gravity, ms = 1):
		self.height += self.velocity * ms / 1000
		self.velocity += gravity * ms / 1000
		self.trail.append(self.height)
		while(len(self.trail) > self.trailLength):
			self.trail = self.trail[1:]
		#self.velocity *= dragCoeff	
		
	def inRange(self):
		return self.height >= 0 and self.height < ARCH_SIZE
		
	def getPosition(self):
		return int(self.height)
		
#	def getTrail(self):
#		pos = self.getPosition()
#		if(self.velocity >= 0):
#			return range(pos, pos + self.trailLength + 1)
#		else:
#			return range(pos -self.trailLength, pos+1)

def fireProjectiles(numArches, wait_ms = 10):
	gravity = -9.8 * 2 # in m/sec
	bounceFactor = -.95
	
	# first create some projectiles
	# was a bit messy as a list comprehension, so
	projectiles = []
	for i in range(1):
		# one at the start
		velocity = random.uniform(25,40)
		height = 0
		projectiles.append(Projectile(i, velocity, height))
		
		# one at the end
		#velocity = -random.uniform(25,40)
		#height = ARCH_SIZE - 1
		#projectiles.append(Projectile(i, velocity, height))

	running = 1
	while running > 0:
		clear() # simplest just to re-paint everything
		for p in projectiles:
			# projectiles 0 and 1 are on ARCH 0
			# projectiles 1 and 2 are on ARCH 1

			# gravity has to change once we get over the middle of the arch
			if(p.height > ARCH_SIZE / 2):
				effectiveGravity = abs(gravity)
			else:
				effectiveGravity = gravity
			
			# also, we need to bounce at the ends
			if(p.height < 0):
				p.velocity = abs(p.velocity) * bounce
			elif(p.height > ARCH_SIZE):
				p.velocity = -abs(p.velocity) * bounce

			p.update(effectiveGravity, wait_ms)
				
			pixelIndex = p.getPosition()

			#print pixelIndex
			# need to do this differently depending on the direction
			#if(p.velocity > 0):
			#	showTrail(pixelIndex, pixelIndex+4, p.color)
			#else:
			#	showTrail(pixelIndex-4, pixelIndex, p.color)
			
			for i in [int(x) for x in p.trail if x > 0 and x < ARCH_SIZE]:
				pos = i + p.offset
				strip.setPixelColor(pos, p.color)

		strip.show()
		delay(wait_ms)
		running = sum(1 for p in projectiles if p.inRange())
		
		#print [x.height for x in projectiles]
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
	print 'Using %d arches of %d each' % (ARCH_COUNT, ARCH_SIZE)
	print 'Press Ctrl-C to quit.'
	while True:
		fireProjectiles(ARCH_COUNT)
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
