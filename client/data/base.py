from point import Point

class Base(object):
	@staticmethod
	def parseList(baseList):

		def _parseBase(baseString):
			parts = baseString.split(' ')
			if (parts[0] == 'base'):
				return Base(parts[1], parts[2:])
			else:
				print 'Unable to parse {0} as base'.format(baseString)
				return None

		return [_parseBase(base) for base in baseList]


	def __init__(self, color, baseList):
		coordinateTupleList = zip(baseList[0::2], baseList[1::2])
		self._points = [Point(float(coord[0]), float(coord[1])) for coord in coordinateTupleList]

		self.color = color


	def __str__(self):
		return 'Base({0}, {1})'.format(self.color, ['{0}'.format(point) for point in self._points])
