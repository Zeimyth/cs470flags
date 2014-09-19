import re

class EnemyTank(object):
	@staticmethod
	def parseList(tankList):

		def _parseTank(tankString):
			cleanedString = re.sub(' +', ' ', tankString)
			parts = cleanedString.split(' ')
			if (parts[0] == 'othertank'):
				return EnemyTank(parts[1:])
			else:
				print 'Unable to parse {0} as EnemyTank'.format(cleanedString)
				return None

		return [_parseTank(tank) for tank in tankList]


	def __init__(self, tankList):
		self.callsign = tankList[0]
		self.color = tankList[1]
		self.status = tankList[2]
		self.flag = tankList[3]
		self.x = float(tankList[4])
		self.y = float(tankList[5])
		self.angle = float(tankList[6])

	def __str__(self):
		return 'EnemyTank({0} {1} {2} {3} ({4}, {5}) {6})'.format(
			self.callsign,
			self.color,
			self.status,
			self.flag,
			self.x,
			self.y,
			self.angle,
		)
