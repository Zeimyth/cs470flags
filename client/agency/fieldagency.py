from agent.fieldagent import FieldAgent
from fields.attractive import AttractiveField
from fields.repulsive import RepulsiveField
from math import sqrt

class FieldAgency:

	def __init__(self, server, enemy):
		self.flagRadius = 1
		self.flagSpread = 500

		self.server = server
		self.enemy = enemy
		self.color = self.server.listConstants().get('team')

		self.agents = []
		self.staticFields = []
		self.dynamicFields = []

		self._init()
		self._run()


	def _init(self):
		self._initializeStaticFields()
		self._initializeTankAgents()


	def _initializeStaticFields(self):
		self._calculateBase()
		self._calculateObstacles()


	def _calculateBase(self):
		base = self._findFriendlyBase()
		x, y = self._findCenterOfPoints(base._points)

		self.baseField = AttractiveField(x, y, self.flagRadius, self.flagSpread)


	def _findFriendlyBase(self):
		bases = self.server.listBases()
		return [base for base in bases if base.color == self.color][0]


	def _calculateObstacles(self):
		obstacles = self.server.listObstacles()

		for obstacle in obstacles:
			x, y = self._findCenterOfPoints(obstacle._points)

			radiusx = obstacle._points[0].x - obstacle._points[3].x
			radiusy = obstacle._points[0].y - obstacle._points[3].y
			radius = sqrt(pow(radiusx, 2) + pow(radiusy, 2)) / 2
			spread = 30

			repulsiveField = RepulsiveField(x, y, radius, spread)
			self.staticFields.append(repulsiveField)


	def _initializeTankAgents(self):
		for tank in self.server.listFriendlyTanks():
			self.agents.append(FieldAgent())


	def _run(self):
		while True:
			self._takeAction()


	def _takeAction(self):
		tankStatuses = self.server.listFriendlyTanks()
		self._calculateDynamicFields(tankStatuses)

		fields = self.staticFields + self.dynamicFields

		for i in range(len(self.agents)):
			action = self.agents[i].getAction(fields, tankStatuses[i])
			if action[0] == "speed":
				self.server.setVelocity(i, action[1])
			elif action[0] == "turn":
				self.server.setTurnRate(i, action[1])


	def _calculateDynamicFields(self, friendlyTanks):
		self.dynamicFields = []
		self._calculateFlagFields()
		self._calculateFriendlyTanks(friendlyTanks)
		# self._calculateEnemyTanks()


	def _calculateFlagFields(self):
		for flag in self.server.listFlags():
			if flag.color == self.enemy:
				flagField = None

				if flag.possessingTeam == self.color:
					flagField = self.baseField
				else:
					flagField = AttractiveField(flag.x, flag.y, self.flagRadius, self.flagSpread)

				self.dynamicFields.append(flagField)


	def _calculateFriendlyTanks(self, friendlyTanks):
		for tank in friendlyTanks:
			tankField = RepulsiveField(tank.x, tank.y, 3, 10)
			self.dynamicFields.append(tankField)


	def _findCenterOfPoints(self, points):
		x = 0
		y = 0

		for point in points:
			x += point.x
			y += point.y
		x = x / len(points)
		y = y / len(points)

		return x, y
