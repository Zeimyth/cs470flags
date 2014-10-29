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
