from agent.fieldagent import FieldAgent
from fields.attractive import AttractiveField
from fields.repulsive import RepulsiveField
from math import sqrt
import time

class ArtemisAgency:

	def __init__(self, server, enemy, obsQueue, predQueue):
		self.flagRadius = 1
		self.flagSpread = 500

		self.server = server
		self.enemy = enemy
		self.color = self.server.listConstants().get('team')

		self.obsQueue = obsQueue
		self.predQueue = predQueue

		self.agents = []
		self.staticFields = []
		self.dynamicFields = []
		self.lastOpponent = ""

		self._init()
		self._run()


	def _init(self):
		print "initializing"

	def _run(self):
		while True:
			self._addToObservations()
			self._takeAction()

	def _takeAction(self):
		predictions = ""
		while not self.predQueue.empty():
			predictions = self.predQueue.get()
		if predictions != "":
			print predictions[0]

	def _addToObservations(self):
		observations = self.server.listEnemyTanks()
		self.obsQueue.put(observations)
		time.sleep(3)
		


	