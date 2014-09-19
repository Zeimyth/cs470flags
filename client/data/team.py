class Team:
	@staticmethod
	def parseList(teamList):

		def _parseTeam(teamString):
			parts = teamString.split(' ')
			if (parts[0] == 'team'):
				return Team(parts[1], int(parts[2]))
			else:
				print 'Unable to parse {0} as team'.format(teamString)
				return None

		return [_parseTeam(team) for team in teamList]


	def __init__(self, color, playercount):
		self.color = color
		self.playercount = playercount


	def __str__(self):
		return 'Team({0}, {1})'.format(self.color, self.playercount)
