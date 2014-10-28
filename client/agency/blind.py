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
		self.server = server

		serverConstants = server.listConstants()
		size = serverConstants.getInt('worldsize') + 100
		truePositive = serverConstants.getFloat('truepositive')
		trueNegative = serverConstants.getFloat('truenegative')

		self.grid = ProbabilityGrid(size, size, prior, truePositive, trueNegative)
		self.agents = []

		# self.agents.append(BlindAgent())
		self.agents.append(DumbAgent())
		self.agents.append(DumbAgent())
		self.agents.append(DumbAgent())

		while True:
			self._takeAction()

	def _takeAction(self):
		tankData = self.server.listFriendlyTanks()

		for i in range(len(self.agents)):
			data = self.server.getSurroundings(i)
			if data != None:
				self.grid.batchUpdate(data.getTopLeftCorner().x, data.getTopLeftCorner().y, data.getGrid())
			
			# action = self.agents[i].getAction(tankData[i], GridWrapper(self.grid))

			# if action is not None:
			# 	if action[0] == "speed":
			# 		self.server.setVelocity(i, action[1])
			# 	elif action[1] == "turn":
			# 		self.server.setTurnRate(i, action[1])

			action = self.agents[i].getAction()
			if action != "":
				if config.debugLevelEnabled(config.TRACE):
					print "Action" + action + str(i)

				if action == "move":
					self.server.setVelocity(i, 1)
				elif action == "stopMove":
					self.server.setVelocity(i, 0)
				elif action == "turn":
					self.server.setTurnRate(i, 1)
				elif action == "stopTurn":
					self.server.setTurnRate(i, 0)
				elif action == "shoot":
					self.server.shoot(i)



class GridWrapper:

	def __init__(self, grid):
		self.grid = grid


	def findNextPoint(self):
		width = self.grid.getWidth()
		height = self.grid.getHeight()

		allPoints = [(self.grid.getCoverage(x, y), (x**2 + y**2)**0.5, x - 400, 400 - y) for y in xrange(height) for x in xrange(width)]
		goal = sorted(allPoints, key=itemgetter(0, 1))[0]
		return (goal[2], goal[3])


	def calculatePathToPoint(self, start, goal):
		# http://en.wikipedia.org/wiki/A*_search_algorithm#Pseudocode
		closedSet = None # TODO
		openSet = PriorityQueue(0)
		openSet.put((self._heuristic(start, goal), start))
		cameFrom = {}
		gScore = {}
		fScore = {}

		gScore[start] = 0
		fScore[start] = gScore[start] + self._heuristic(start, goal)

		while not openSet.empty():
			current = openSet.get()
			if current.x == goal.x and current.y == goal.y:
				return self._reconstructPath(cameFrom, goal)

			closedSet.add(current) # TODO
			for neighbor in self._getNeighborNodes(current):
				if neighbor in closedSet: # TODO
					continue

				tentativeScore = gScore[current] + 1


	# function A*(start,goal)
	#     closedset := the empty set    // The set of nodes already evaluated.
	#     openset := {start}    // The set of tentative nodes to be evaluated, initially containing the start node
	#     came_from := the empty map    // The map of navigated nodes.
	 
	#     g_score[start] := 0    // Cost from start along best known path.
	#     // Estimated total cost from start to goal through y.
	#     f_score[start] := g_score[start] + heuristic_cost_estimate(start, goal)
	 
	#     while openset is not empty
	#         current := the node in openset having the lowest f_score[] value
	#         if current = goal
	#             return reconstruct_path(came_from, goal)
	 
	#         remove current from openset
	#         add current to closedset
	#         for each neighbor in neighbor_nodes(current)
	#             if neighbor in closedset
	#                 continue
	#             tentative_g_score := g_score[current] + dist_between(current,neighbor)
	 
	#             if neighbor not in openset or tentative_g_score < g_score[neighbor] 
	#                 came_from[neighbor] := current
	#                 g_score[neighbor] := tentative_g_score
	#                 f_score[neighbor] := g_score[neighbor] + heuristic_cost_estimate(neighbor, goal)
	#                 if neighbor not in openset
	#                     add neighbor to openset
	 
	#     return failure

	def _heuristic(self, point, goal):
		return (point.x**2 + point.y**2)**0.5


	def _getNeighborNodes(self, node):
		pass


	def _reconstructPath(self, cameFrom, currentNode):
		pass
	# function reconstruct_path(came_from, current_node)
	#     if current_node in came_from
	#         p := reconstruct_path(came_from, came_from[current_node])
	#         return (p + current_node)
	#     else
	#         return current_node