import sys
import os.path

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

import config

from agent.fieldagent import FieldAgent
from fields.attractive import AttractiveField
from fields.repulsive import RepulsiveField
from math import sqrt
import time

class ArtemisAgency:

	def __init__(self, server, enemy, obsQueue, predQueue, interval):
		self.flagRadius = 1
		self.flagSpread = 500

		self.server = server
		self.enemy = enemy
		self.color = self.server.listConstants().get('team')

		self.obsQueue = obsQueue
		self.predQueue = predQueue

		self.interval = interval

		self.agents = []
		self.staticFields = []
		self.dynamicFields = []
		self.lastOpponent = ""

		self._init()
		self._run()


	def _init(self):
		if config.debugLevelEnabled(config.INFO):
			print "ArtemisAgency: Initializing"

	def _run(self):
		while True:
			self._addToObservations()
			self._takeAction()

	def _takeAction(self):
		predictions = ""
		while not self.predQueue.empty():
			predictions = self.predQueue.get()
		if predictions != "":
			if config.debugLevelEnabled(config.DEBUG):
				print "ArtemisAgency: {}".format(predictions[0])

	def _addToObservations(self):
		now = time.time()

		if config.debugLevelEnabled(config.DEBUG):
			print 'ArtemisAgency: observing'

		next_wakeup = now + self.interval
		observations = self.server.listEnemyTanks()
		self.obsQueue.put(observations)
		sleepLength = next_wakeup - time.time()

		time.sleep(sleepLength)
	