from point import Point

def _parseOccGridAt(atString):
	xyPart = atString.split(' ')[1]
	xyPartSplit = xyPart.split(',')

	x = int(xyPartSplit[0].strip())
	y = int(xyPartSplit[1].strip())

	return Point(x, y)


def _parseOccGridDimensions(dimString):
	whPart = dimString.split(' ')[1]
	whPartSplit = whPart.split('x')

	w = int(whPartSplit[0].strip())
	h = int(whPartSplit[1].strip())

	return Point(w, h)


def _parseOccGridList(gridList):
	return [[int(num) == 1 for num in line.strip()] for line in gridList]



class OccGrid:
	@staticmethod
	def parseList(occGridList):
		topLeftCorner = _parseOccGridAt(occGridList[0])
		dimensions = _parseOccGridDimensions(occGridList[1])
		grid = _parseOccGridList(occGridList[2:])

		return OccGrid(topLeftCorner, dimensions, grid)


	def __init__(self, topLeftCorner, dimensions, grid):
		self.topLeftCorner = topLeftCorner
		self.dimensions = dimensions
		self.grid = grid


	def getTopLeftCorner(self):
		return self.topLeftCorner


	def getDimensions(self):
		return self.dimensions


	def getGrid(self):
		return self.grid


	def __str__(self):
		return 'OccGrid(at {0}, dim {1}, {2})'.format(self.topLeftCorner, self.dimensions, self.grid)
