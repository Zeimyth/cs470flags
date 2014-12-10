import os
import sys
import time
from math import atan2, degrees, pi

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.relpath('../data'))))
from point import Point

class BlindPigeon:

	def __init__(self):
		self._clearMoves()

		self.PATH_THRESHOLD = 10
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


	def getAction(self, status):
		now = time.time()

		if len(self._moveTimes) == 0:
			self._pushMove('choose', 0)
		elif self._moveTimes[0] > now:
			return None
		else:
			nextMove = self._getNextMove()

			if nextMove == 'choose':
				# choose new goal point and calculate path
				self.goal = self._chooseNewGoal()
				print 'New goal: {0}'.format(self.goal)
				self._pushMove('repath', 0)
				return {'speed': 0, 'angle': 0}
			elif nextMove == 'repath':
				# calculate the best path to the destination
				print 'Recalculating path...'
				self._path = self._calculatePath(status.x, status.y)
				self._nextStep = 0
				self._pushMove('track', 0)
				self._pushMove('repath', 10)
				return {'shoot': True}
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


	def _chooseNewGoal(self):
		return Point(-200, 200)


	def _calculatePath(self, x, y):
		fullPath = [self.goal]

		# print 'full path',
		# for p in fullPath:
		# 	print str(p)

		corners = []
		twoAgo = None
		previous = None

		for point in fullPath:
			if len(corners) == 0:
				# Special case to keep starting point out of the path
				if previous is not None and twoAgo is not None and \
				previous.x - point.x != twoAgo.x - previous.x and \
				previous.y - point.y != twoAgo.y - previous.y:
					corners.append(previous)
			elif len(corners) == 1:
				if previous.x - point.x != corners[-1].x - previous.x and \
				previous.y - point.y != corners[-1].y - previous.y:
					corners.append(previous)
			else:
				if corners[-1].x - point.x != corners[-2].x - corners[-1].x and \
				corners[-1].y - point.y != corners[-2].y - corners[-1].y:
					corners.append(previous)

			twoAgo = previous
			previous = point

		if len(fullPath) > 0:
			corners.append(fullPath[-1])

		# print 'path',
		# for p in corners:
		# 	print str(p),

		# print ''

		return corners


	def _getNextPointInPath(self, myLoc):
		if self._nextStep >= len(self._path):
			return None
		elif self._distance(myLoc, self.goal) > self.GOAL_THRESHOLD:
			currentPoint = self._path[self._nextStep]
			if self._distance(currentPoint, myLoc) > self.PATH_THRESHOLD:
				return currentPoint
			else:
				# print 'reached {0}'.format(str(currentPoint))
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
		# print point, Point(status.x, status.y)
		desiredAngle = self._getAngleOfLineBetweenTwoPoints(Point(status.x, status.y), point)
		myAngle = degrees(status.angle)

		if desiredAngle > 90 and myAngle < -90:
			myAngle += 360
		elif myAngle > 90 and desiredAngle < -90:
			desiredAngle += 360

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
