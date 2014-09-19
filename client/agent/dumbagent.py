import time
import random

class DumbAgent:

	def __init__(self):
		self.moveTimes = []
		self.moveList = {}
		self._dumbCycle("start")
	
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
			return action
