import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.relpath('..'))))
import config

import time
from math import atan2, degrees, copysign

class ArtemisAgent:

	def __init__(self):
		self.degreesToTurn = 0
		self.startAngle = 999


	def aim(self, target, status):
		if config.debugLevelEnabled(config.DEBUG):
			print "ArtemisAgent: my angle"
			print degrees(status.angle)
		if self.startAngle == 999:
			self.startAngle = degrees(status.angle)
		newAngle = self._calculateAngle((status.x, status.y), target)
		turnRate = self._calcTurn(newAngle, degrees(status.angle))
		if turnRate != 0:
			return tuple(["turn", turnRate])
		else:
			self.degreesToTurn = 0
			self.startAngle = 999
			return tuple(["shoot"])


	def _calculateAngle(self, fromLoc, toLoc):
		deltaX = toLoc[0] - fromLoc[0]
		deltaY = toLoc[1] - fromLoc[1]

		return degrees(atan2(deltaY, deltaX))


	def _calcTurn(self, newAngle, myAngle):
		if self.degreesToTurn == 0:
			self.degreesToTurn = newAngle - myAngle
		angle = newAngle - myAngle
		if angle > 180:
			angle -= 360
		elif angle < -180:
			angle += 360

		if self.degreesToTurn / angle > .5:
			rate = copysign(1, angle)
		else:
			rate = 0

		if config.debugLevelEnabled(config.DEBUG):
			print self.degreesToTurn / angle
			print "ArtemisAgent: Desired angle = {0:.2f}, Angle = {1:.2f}, Rate = {2:.2f}".format(
				newAngle, angle, rate)

		return rate
