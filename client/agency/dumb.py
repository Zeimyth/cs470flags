#!/usr/bin/env python
from agent.dumbagent import DumbAgent

class DumbAgency:

	def __init__(self, server):
		self.server = server
		self.agents = []
		self.agents.append(DumbAgent())
		self.agents.append(DumbAgent())
		while True:
			self._takeAction()

	def _takeAction(self):
		for i in range(len(self.agents)):
			action = self.agents[i].getAction()
			if action != "":
				print "Action" + action + str(i)
			if action == "move":
				self.server.setVelocity(i, 1)
			if action == "stopMove":
				self.server.setVelocity(i, 0)
			if action == "turn":
				self.server.setTurnRate(i, 1)
			if action == "stopTurn":
				self.server.setTurnRate(i, 0)
		
