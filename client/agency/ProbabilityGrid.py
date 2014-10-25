import numpy as np
import Image

class ProbabilityGrid:

	def __init__(self, width, height, prior, truePositive, trueNegative):
		self.grid = np.zeros(width, height)
		self.grid.fill(prior)
		self.truePositive = truePositive
		self.trueNegative = trueNegative
		self.falsePositive = 1 - truePositive
		self.falseNegative = 1 - trueNegative

	def update(self, x, y, obstacle):
		current = self.grid[y,x]
		new = 0 #result of bayes math
		self.grid[y,x] = new

	def createImage(self, path):
		image = Image.fromarray(self.grid)
		image.save(path)

	def saveCSV(self, path):
		np.savetxt(path, self.grid, delimiter=",")