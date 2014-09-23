from agent.fieldagent import FieldAgent
from fields.attractive import AttractiveField
from fields.repulsive import RepulsiveField
from math import sqrt

class FieldAgency:

	flagRadius = 1
	flagSpread = 300

	def __init__(self, server, enemy):
		self.flagRadius = 1
		self.flagSpread = 500
		self.server = server
		self.enemy = enemy
		self.color = self.server.listConstants().get('team')
		self.agents = []
		self.fields = []
		self._calculateBase()
		self._initializeFields()

		for tank in self.server.listFriendlyTanks():
			self.agents.append(FieldAgent())

		while True:
			self._takeAction()

	def _initializeFields(self):		
		self.fields.append(self._findFlag())
		obstacles = self.server.listObstacles()
		for obstacle in obstacles:
			x = 0
			y = 0
			for point in obstacle._points:
				x += point.x
				y += point.y
			x = x / len(obstacle._points)
			y = y / len(obstacle._points)
			radiusx = obstacle._points[0].x - obstacle._points[3].x
			radiusy = obstacle._points[0].y - obstacle._points[3].y
			radius = sqrt(pow(radiusx, 2) + pow(radiusy, 2)) / 2
			spread = 30
			repulsiveField = RepulsiveField(x, y, radius, spread)
			self.fields.append(repulsiveField)

	def _calculateBase(self):
		bases = self.server.listBases()
		base = [base for base in bases if base.color == self.color][0]
		x = 0
		y = 0
		for point in base._points:
			x += point.x
			y += point.y
		x = x / len(base._points)
		y = y / len(base._points)
		self.baseField = AttractiveField(x, y, self.flagRadius, self.flagSpread)

	def _findFlag(self):
		flags = self.server.listFlags()
		for flag in flags:
			if flag.color == self.enemy:
				return AttractiveField(flag.x, flag.y, self.flagRadius, self.flagSpread)

	def _checkFlag(self):
		flags = self.server.listFlags()
		for flag in flags:
			if flag.color == self.enemy:
				if flag.possessingTeam == self.color:
					self.fields[0] = self.baseField
				else:
					self.fields[0] = self._findFlag()

	def _takeAction(self):
		tankStatuses = self.server.listFriendlyTanks()
		self._checkFlag()
		for i in range(len(self.agents)):
			action = self.agents[i].getAction(self.fields, tankStatuses[i])
			if action[0] == "speed":
				self.server.setVelocity(i, action[1])
			elif action[0] == "turn":
				self.server.setTurnRate(i, action[1])
			
