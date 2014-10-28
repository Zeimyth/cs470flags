import os
import sys
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.relpath('../data'))))
from point import Point

class BlindAgent:

	def __init__(self):
		self._moveTimes = []
		self._moveList = {}

		self.goal = None
		self._pushMove('choose', 0)


	def _pushMove(self, move, offset):
		now = time.time()

		self._moveTimes.append(now + offset)
		self._moveList[now + offset] = move


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
			elif nextMove == 'repath':
				# calculate the best path to the destination
				self._calculatePath(status.x, status.y, grid)
			elif nextMove == 'setSpeed':
				# set the new forward speed
				pass
			elif nextMove == 'setTurn':
				# set the new turning speed
				pass
			else:
				return None


	def _getNextMove(self):
		move = self._moveList[self._moveTimes[0]]
		del self._moveList[self._moveTimes[0]]
		del self._moveTimes[0]

		return move


	def _chooseNewGoal(self, grid):
		return Point(*grid.findNextPoint())


	def _calculatePath(self, x, y, grid):
		pass
