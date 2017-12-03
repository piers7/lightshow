class Projectile:
	gravity = -9.8; # in m/sec
	def __init__ (self, velocity = 9.8):
		self.height = 0
		self.velocity = velocity
	def update(self, ms = 1):
		self.height += self.velocity * ms / 1000;
		self.velocity -= gravity * ms / 1000;
