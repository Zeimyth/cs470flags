import numpy as np
import Image

class ProbabilityGrid:

	#Constuctor
	#width: the width of the grid
	#height: the height og the grid
	#prior: the initial probability in the grid
	#truePositive: the True Positive Rate
	#trueNegative: the True Negative Rate
	def __init__(self, width, height, prior, truePositive, trueNegative):
		self.grid = np.zeros((width, height))
		self.coverage = np.zeros((width, height))
		self.grid.fill(prior)
		self.truePositive = truePositive
		self.trueNegative = trueNegative
		self.falsePositive = 1 - truePositive
		self.falseNegative = 1 - trueNegative
		self.inputCount = 0

	def batchUpdate(self, x, y, filterGrid):
		x = x + 400
		y = 400 - y
		width = len(filterGrid)
		height = len(filterGrid[0])
		for dx in range(width):
			for dy in range(height):
				self._update(x+dx, y+dy, filterGrid[dx][dy])
		self.inputCount += 0
		if(self.inputCount % 10 is 0):
			#self.showImages()

	def showImages(self):
		self.showProbability()
		self.showCoverage()

	def showProbability(self):
		image = Image.fromarray((self.grid * 255).astype(np.int32))
		image.show()

	def showCoverage(self):
		imageArray = (self.coverage * 255) / self.coverage.max()
		coverageImage = Image.fromarray(imageArray.astype(np.int32))
		coverageImage.show()

	#The x and y of where we are updating
	#obstacle: a boolean indicating whether the position is reported to be a obstace
	#Updates the probability that a pixel is an obstacle
	def _update(self, x, y, obstacle):
		current = self.grid[x,y]
		notCurrent = 1 - current
		if obstacle:
			new = (self.truePositive * current) / ((self.truePositive * current) + (self.falsePositive * notCurrent))
		else:
			notNew = (self.trueNegative * notCurrent) / ((self.trueNegative * notCurrent) + (self.falseNegative * current))
			new = 1 - notNew
		self.grid[y,x] = new
		self.coverage[y,x] = self.coverage[y,x] + 1

	#returns the probability that a point is n obstacle
	def getProbability(self, x, y):
		return self.grid[x,y]

	#returns the number of times a point as been observed
	def getCoverage(self, x, y):
		return self.coverage[x,y]

	#creates the probability map image
	def createImage(self, path):
		image = Image.fromarray((self.grid * 255).astype(np.int32))
		image.save(path)

	#creates the coverage map image
	def createCoverageImage(self, path):
		imageArray = (self.coverage * 255) / self.coverage.max()
		coverageImage = Image.fromarray(imageArray.astype(np.int32))
		coverageImage.save(path)

	#saves a csv of of the probabilities
	def saveCSV(self, path):
		np.savetxt(path, self.grid, delimiter=",")