from math import sqrt, atan2, degrees, sin, cos

class RepulsiveField:
	
	def __init__(self, x, y, radius, spread):
		self.x = x
		self.y = y
		self.radius = radius
		self.spread = spread

	#here x and y are the x and y of the tank
	def getVector(self, x, y):
		xdiff = self.x - x
		ydiff = self.y - y
		distance = sqrt(pow(xdiff,2) + pow(ydiff,2))
		theta = atan2(ydiff, xdiff) 
		if distance < self.radius:
			'''deltaX = degrees(sin(theta)) * -1
			deltaY = degrees(sin(theta)) * -1'''
			deltaX = 0
			deltaY = 0
		elif distance > self.spread + self.radius:
			deltaX = 0
			deltaY = 0
		else:
			deltaX = (self.spread + self.radius - distance) * degrees(cos(theta)) * -1
			deltaY = (self.spread + self.radius - distance) * degrees(sin(theta)) * -1
		return tuple([deltaX, deltaY])
		
