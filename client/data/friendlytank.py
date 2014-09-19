import re

class FriendlyTank(object):
	@staticmethod
	def parseList(tankList):

		def _parseTank(tankString):
			cleanedString = re.sub(' +', ' ', tankString)
			parts = cleanedString.split(' ')
			if (parts[0] == 'mytank'):
				return FriendlyTank(parts[1:])
			else:
				print 'Unable to parse {0} as FriendlyTank'.format(cleanedString)
				return None

		return [_parseTank(tank) for tank in tankList]


	def __init__(self, tankList):
		self.index = int(tankList[0])
		self.callsign = tankList[1]
		self.status = tankList[2]
		self.shotsAvailable = int(tankList[3])
		self.reloadTime = float(tankList[4])
		self.flag = tankList[5]
		self.x = int(tankList[6])
		self.y = int(tankList[7])
		self.angle = float(tankList[8])
		self.vx = float(tankList[9])
		self.vy = float(tankList[10])
		self.angVel = float(tankList[11])

	def __str__(self):
		return 'FriendlyTank({0} {1} {2} {3} {4} {5} {6} {7} {8} {9} {10} {11})'.format(
			self.index,
			self.callsign,
			self.status,
			self.shotsAvailable,
			self.reloadTime,
			self.flag,
			self.x,
			self.y,
			self.angle,
			self.vx,
			self.vy,
			self.angVel
		)
