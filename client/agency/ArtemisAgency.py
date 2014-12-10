import sys
import os.path

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

import config

import time

from agent.artemisagent import ArtemisAgent

class ArtemisAgency:

	def __init__(self, server, obsQueue, predQueue, interval):
		self.server = server

		self.obsQueue = obsQueue
		self.predQueue = predQueue

		self.interval = interval

		self.agents = []

		self._init()
		self._run()


	def _init(self):
		if config.debugLevelEnabled(config.INFO):
			print "ArtemisAgency: Initializing"

		for tank in self.server.listFriendlyTanks():
			self.agents.append(ArtemisAgent())


	def _run(self):
		nextObserve = time.time()
		prediction = ""

		while True:
			nextObserve += self.interval
			self._addToObservations()

			while time.time() < nextObserve:
				while not self.predQueue.empty():
					prediction = self.predQueue.get()[0]
				self._takeAction(prediction)


	def _takeAction(self, prediction):
		if prediction != "":
			if config.debugLevelEnabled(config.DEBUG):
				print "ArtemisAgency: Enemy predicted at {}".format(prediction)

			tanks = self.server.listFriendlyTanks()
			for i in xrange(len(self.agents)):
				action = self.agents[i].aim(prediction, tanks[i])
				if action[0] == "turn":
					self.server.setTurnRate(i, action[1])
				elif action[0] == "shoot":
					self.server.shoot(i)


	def _addToObservations(self):
		if config.debugLevelEnabled(config.DEBUG):
			print 'ArtemisAgency: observing'

		observations = self.server.listEnemyTanks()
		self.obsQueue.put(observations)
