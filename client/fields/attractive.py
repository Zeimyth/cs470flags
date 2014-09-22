from math import sqrt, atan2, degrees, cos, sin

class AttractiveField:
	
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
			deltaX = 0
			deltaY  = 0
		elif distance > self.spread:
			deltaX = self.spread * degrees(cos(theta)) * .01
			deltaY = self.spread * degrees(sin(theta)) * .01
		else:
			deltaX = (distance - self.radius) * degrees(cos(theta)) * .01
			deltaY = (distance - self.radius) * degrees(sin(theta)) * .01
		print "Xs"
		print xdiff
		print deltaX
		print "Ys"
		print ydiff
		print deltaY
		return tuple([deltaX, deltaY])
		
		
