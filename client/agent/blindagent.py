import os
import sys
import time
from math import atan2, degrees, pi

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.relpath('../data'))))
from point import Point

class BlindAgent:

	def __init__(self):
		self._clearMoves()

		self.PATH_THRESHOLD = 20
		self.GOAL_THRESHOLD = 50

		self.goal = None
		self._pushMove('choose', 0)


	def _clearMoves(self):
		self._moveTimes = []
		self._moveList = {}


	def _pushMove(self, move, offset):
		now = time.time()

		self._moveTimes.append(now + offset)
		self._moveTimes.sort()
		self._moveList[now + offset] = move


	def _getNextMove(self):
		move = self._moveList[self._moveTimes[0]]
		del self._moveList[self._moveTimes[0]]
		del self._moveTimes[0]

		return move


	def getAction(self, status, grid):
		now = time.time()

		if len(self._moveTimes) == 0:
			self._pushMove('choose', 0)
		elif self._moveTimes[0] > now:
			return None
		else:
			nextMove = self._getNextMove()

			if nextMove == 'choose':
				# choose new goal point and calculate path
				self.goal = self._chooseNewGoal(grid)
				print 'New goal: {0}'.format(self.goal)
				self._pushMove('repath', 0)
				return {'speed': 1}
			elif nextMove == 'repath':
				# calculate the best path to the destination
				self._path = self._calculatePath(status.x, status.y, grid)
				self._nextStep = 0
				self._pushMove('track', 0)
				self._pushMove('repath', 5)
				return None
			elif nextMove == 'track':
				targetPoint = self._getNextPointInPath(Point(status.x, status.y))
				# print targetPoint
				if targetPoint is not None:
					action = self._trackToPoint(targetPoint, status)
					# print action
					self._pushMove('track', 0)
					return action
				else:
					self._clearMoves()
					self._pushMove('choose', 0)
			else:
				return None


	def _chooseNewGoal(self, grid):
		return Point(*grid.findNextPoint())


	def _calculatePath(self, x, y, grid):
		return grid.calculatePathToPoint(Point(x, y), self.goal)


	def _getNextPointInPath(self, myLoc):
		if self._distance(myLoc, self.goal) > self.GOAL_THRESHOLD:
			currentPoint = self._path[self._nextStep]
			if self._distance(currentPoint, myLoc) > self.PATH_THRESHOLD:
				return currentPoint
			else:
				while self._nextStep < len(self._path) and self._distance(self._path[self._nextStep], myLoc) <= self.PATH_THRESHOLD:
					self._nextStep += 1

				if self._nextStep >= len(self._path):
					return None
				else:
					return self._path[self._nextStep]
		else:
			return None


	def _distance(self, a, b):
		return ((a.x - b.x)**2 + (a.y - b.y)**2)**0.5


	def _trackToPoint(self, point, status):
		desiredAngle = self._getAngleOfLineBetweenTwoPoints(Point(status.x, status.y), point)
		myAngle = degrees(status.angle)

		# print desiredAngle, myAngle

		angleSpeed = self._calculateAngleSpeed(desiredAngle, myAngle)
		forwardSpeed = 1 if angleSpeed == 0 else 0.25 if angleSpeed**2 == 1 else 0.33

		return {'speed': forwardSpeed, 'angle': angleSpeed}


	def _getAngleOfLineBetweenTwoPoints(self, p1, p2):
		xDiff = p2.x - p1.x
		yDiff = p2.y - p1.y
		return degrees(atan2(yDiff, xDiff))


	def _calculateAngleSpeed(self, desiredAngle, myAngle):
		# if myAngle < 0:
		# 	myAngle += 360
		# 	desiredangle += 360
		# if desiredAngle < 0:
		# 	desiredAngle += 360
		# 	myAngle += 360

		normalizedAngle = desiredAngle - myAngle

		if normalizedAngle > 45:
			return 1
		elif normalizedAngle > 15:
			return 0.5
		elif normalizedAngle > 5:
			return 0.1
		elif normalizedAngle < -45:
			return -1
		elif normalizedAngle < -15:
			return -0.5
		elif normalizedAngle < -5:
			return -0.1
		else:
			return 0
