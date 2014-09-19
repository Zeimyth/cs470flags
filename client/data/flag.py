class Flag:
	@staticmethod
	def parseList(flagList):

		def _parseFlag(flagString):
			parts = flagString.split(' ')
			if (parts[0] == 'flag'):
				return Flag(parts[1], parts[2], float(parts[3]), float(parts[4]))
			else:
				print 'Unable to parse {0} as flag'.format(flagString)
				return None

		return [_parseFlag(flag) for flag in flagList]


	def __init__(self, color, possessingTeam, x, y):
		self.color = color
		self.possessingTeam = possessingTeam
		self.x = x
		self.y = y


	def __str__(self):
		return 'Flag({0}, {1}, ({2}, {3}))'.format(self.color, self.possessingTeam, self.x, self.y)
