from point import Point

class Obstacle:
	@staticmethod
	def parseList(obstacleList):

		def _parseObstacle(obstacleString):
			parts = obstacleString.split(' ')
			if (parts[0] == 'obstacle'):
				return Obstacle(parts[1:])
			else:
				print 'Unable to parse {0} as obstacle'.format(obstacleString)
				return None

		return [_parseObstacle(obstacle) for obstacle in obstacleList]


	def __init__(self, obstacleList):
		coordinateTupleList = zip(obstacleList[0::2], obstacleList[1::2])
		self._points = [Point(float(coord[0]), float(coord[1])) for coord in coordinateTupleList]


	def __str__(self):
		return 'Obstacle({0})'.format(['{0}'.format(point) for point in self._points])
