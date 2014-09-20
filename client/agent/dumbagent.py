import time
import random

class DumbAgent:

	def __init__(self):
		self.moveTimes = []
		self.moveList = {}
		self._dumbCycle("start")
		self._shoot()

	def _dumbCycle(self, lastMove):
		now = time.time()
		self.moveTimes.append(now)
		if lastMove == "move":
			self.moveList[now] = "turn"
			self.moveTimes.append(now+2)
			self.moveList[now+2] = "stopTurn"
		else:
			self.moveList[now] = "move"
			moveLength = now + random.randint(3,8)
			self.moveTimes.append(moveLength)
			self.moveList[moveLength] = "stopMove"
		self.moveTimes.sort()

	def _shoot(self):
		now = time.time()
		shootTime = now + random.randint(1,4)
		self.moveTimes.append(shootTime)
		self.moveList[shootTime] = "shoot"
		self.moveTimes.sort()

	def getAction(self):
		now = time.time()
		if self.moveTimes[0] > now:
			return ""
		else:
			action = self.moveList[self.moveTimes[0]]
			del self.moveList[self.moveTimes[0]]
			del self.moveTimes[0]
			if action == "stopTurn":
				self._dumbCycle("turn")
			elif action == "stopMove":
				self._dumbCycle("move")
			elif action == "shoot":
				self._shoot()
			return action
