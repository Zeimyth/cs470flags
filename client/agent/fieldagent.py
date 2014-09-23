import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.relpath('..'))))
import config

import time
from math import atan2, degrees, copysign

class FieldAgent:

	def __init__(self):
		self.moveTimes = []
		self.moveList = {}

	def _calcVector(self, vectorList):
		deltaX = 0
		deltaY = 0
		for vector in vectorList:
			deltaX += vector[0]
			deltaY += vector[1]

		if config.debugLevelEnabled(config.TRACE):
			print "DeltaX"
			print deltaX
			print "DeltaY"
			print deltaY

		angle, magnitude = self._deltaToVelocity(deltaX, deltaY)
		return angle, magnitude

	def _deltaToVelocity(self, deltaX, deltaY):
		angle = degrees(atan2(deltaY, deltaX))
		'''if deltaX < 0 and deltaY > 0:
			angle = angle + 180
		elif deltaX < 0 and deltaY < 0:
			angle = angle - 180'''
		magnitude = .5
		return angle, magnitude

	def _createVectors(self, fieldList, x, y):
		vectorList = []
		for field in fieldList:
			vector = field.getVector(x, y)
			vectorList.append(vector)
		return vectorList

	def _calcTurn(self, newAngle, myAngle):
		angle = newAngle - myAngle
		if angle > 180:
			angle -= 360
		elif angle < -180:
			angle += 360
		now = time.time()
		duration = .2
		stop = now + duration
		if abs(angle) < 5:
			speed = 0
		elif abs(angle) > 90:
			speed = copysign(1, angle)
		else:		
			#speed = (angle/18) * .1 + .2
			speed = copysign(.5, angle)

		if config.debugLevelEnabled(config.TRACE):
			print "Desired angle"
			print newAngle
			print "Angle"
			print angle
			print "Speed"
			print speed

		self.moveTimes.append(now)
		self.moveList[now] = tuple(["turn", speed])
		#self.moveTimes.append(stop)
		#self.moveList[stop] = tuple(["turn", 0])
		

	def getAction(self, fieldList, status):
		now = time.time()

		if config.debugLevelEnabled(config.TRACE):
			print "my angle"
			print degrees(status.angle)

		if len(self.moveTimes) == 0:
			vectorList = self._createVectors(fieldList, status.x, status.y)
			newAngle, newVelocity = self._calcVector(vectorList)
			if newAngle != 0:
				self._calcTurn(newAngle, degrees(status.angle))
			return tuple(["speed", newVelocity])
		elif self.moveTimes[0] < now:
			action = self.moveList[self.moveTimes[0]]
			del self.moveList[self.moveTimes[0]]
			del self.moveTimes[0]
			return action
		else:
			return tuple([""])
