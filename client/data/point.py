class Point(object):
	def __init__(self, x, y):
		self.x = x
		self.y = y


	def toTuple(self):
		return tuple([self.x, self.y])


	def flatten(self, mult):
		return self.x + self.y * mult


	def __str__(self):
		return '({0}, {1})'.format(self.x, self.y)



class WorldPoint(Point):

	def getWorldX(self):
		return x


	def getWorldY(self):
		return y


	def getGridX(self):
		return x + 400


	def getGridY(self):
		return 399 - y


	def toWorldTuple(self):
		return tuple([x, y])



class GridPoint(Point):

	def getWorldX(self):
		return x - 400


	def getWorldY(self):
		return 399 - y


	def getGridX(self):
		return x


	def getGridY(self):
		return y
