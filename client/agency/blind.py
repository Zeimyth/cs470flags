#!/usr/bin/env python

import os
import sys
from operator import itemgetter
from Queue import PriorityQueue

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.relpath('../..'))))
import config

from ProbabilityGrid import ProbabilityGrid
from agent.blindagent import BlindAgent
from agent.dumbagent import DumbAgent
from point import Point

class BlindAgency:

	def __init__(self, server, prior):
		self._server = server
		self._serverConstants = server.listConstants()

		size = self._serverConstants.getInt('worldsize')
		truePositive = self._serverConstants.getFloat('truepositive')
		trueNegative = self._serverConstants.getFloat('truenegative')

		self.grid = ProbabilityGrid(size, size, prior, truePositive, trueNegative)
		self.agents = []

		self.agents.append(BlindAgent())
		# self.agents.append(DumbAgent())
		# self.agents.append(DumbAgent())
		# self.agents.append(DumbAgent())

		while True:
			self._takeAction()

	def _takeAction(self):
		tankData = self._server.listFriendlyTanks()

		for i in range(len(self.agents)):
			data = self._server.getSurroundings(i)
			if data != None:
				self.grid.batchUpdate(data.getTopLeftCorner().x, data.getTopLeftCorner().y, data.getGrid())
			
			action = self.agents[i].getAction(tankData[i], GridWrapper(self.grid))

			if action is not None:
				if 'speed' in action:
					self._server.setVelocity(i, action['speed'])
				if 'angle' in action:
					self._server.setTurnRate(i, action['angle'])
				if 'shoot' in action:
					self._server.shoot(i)

			# action = self.agents[i].getAction()
			# if action != "":
			# 	if config.debugLevelEnabled(config.TRACE):
			# 		print "Action" + action + str(i)

			# 	if action == "move":
			# 		self.server.setVelocity(i, 1)
			# 	elif action == "stopMove":
			# 		self.server.setVelocity(i, 0)
			# 	elif action == "turn":
			# 		self.server.setTurnRate(i, 1)
			# 	elif action == "stopTurn":
			# 		self.server.setTurnRate(i, 0)
			# 	elif action == "shoot":
			# 		self.server.shoot(i)



class GridWrapper:

	def __init__(self, grid):
		self._grid = grid
		self._THRESHOLD = .97


	def findNextPoint(self):
		width = self._grid.getWidth()
		height = self._grid.getHeight()

		allPoints = [(self._grid.getCoverage(x, y), (x**2 + y**2)**0.5, x - 400, 399 - y) for y in xrange(height) for x in xrange(width)]
		goal = sorted(allPoints, key=itemgetter(0, 1))[0]
		return (goal[2], goal[3])


	def calculatePathToPoint(self, start, goal):
		# http://en.wikipedia.org/wiki/A*_search_algorithm#Pseudocode
		closedSet = set()
		queue = PriorityQueue(0)
		queue.put((self._heuristic(start, goal), start))
		cameFrom = {}
		score = {}

		score[start] = 0

		while not queue.empty():
			_, current = queue.get()
			if current.x == goal.x and current.y == goal.y:
				return self._reconstructPath(cameFrom, goal)

			if current.flatten(800) in closedSet:
				continue
			closedSet.add(current.flatten(800))
			for neighbor in self._getNeighborNodes(current):
				if neighbor.flatten(800) in closedSet:
					continue

				turnPenalty = 0.5

				if current.flatten(800) in cameFrom and \
				current.x - neighbor.x == cameFrom[current.flatten(800)].x - current.x and \
				current.y - neighbor.y == cameFrom[current.flatten(800)].y - current.y:
					turnPenalty = 0 

				neighborScore = score[current] + 1 + turnPenalty
				cameFrom[neighbor.flatten(800)] = current
				score[neighbor] = neighborScore
				queue.put((neighborScore + self._heuristic(neighbor, goal), neighbor))

		return []


	def _heuristic(self, point, goal):
		return ((point.x - goal.x)**2 + (point.y - goal.y)**2)**0.5


	def _getNeighborNodes(self, node):
		neighbors = []

		leftNeighbor = Point(node.x - 1, node.y)
		rightNeighbor = Point(node.x + 1, node.y)
		topNeighbor = Point(node.x, node.y + 1)
		bottomNeighbor = Point(node.x, node.y - 1)

		if self._isValidPoint(leftNeighbor):
			neighbors.append(leftNeighbor)
		if self._isValidPoint(rightNeighbor):
			neighbors.append(rightNeighbor)
		if self._isValidPoint(topNeighbor):
			neighbors.append(topNeighbor)
		if self._isValidPoint(bottomNeighbor):
			neighbors.append(bottomNeighbor)

		return neighbors


	def _isValidPoint(self, point):
		return point.x >= -400 and point.x <= 399 and point.y >= -400 and point.y <= 399 and self._grid.getProbability(point.x + 400, 399 - point.y) < self._THRESHOLD


	def _reconstructPath(self, cameFrom, currentNode):
		if currentNode.flatten(800) in cameFrom:
			path = self._reconstructPath(cameFrom, cameFrom[currentNode.flatten(800)])
			path.append(currentNode) # correct? reverse order?
			return path
		else:
			return [currentNode]
