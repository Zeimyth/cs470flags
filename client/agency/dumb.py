#!/usr/bin/env python
from agent.dumbagent import DumbAgent

class DumbAgency:

	def __init__(self, server):
		self.server = server
		self.agents = []

		for tank in self.server.listFriendlyTanks():
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
			elif action == "stopMove":
				self.server.setVelocity(i, 0)
			elif action == "turn":
				self.server.setTurnRate(i, 1)
			elif action == "stopTurn":
				self.server.setTurnRate(i, 0)
			elif action == "shoot":
				self.server.shoot(i)

