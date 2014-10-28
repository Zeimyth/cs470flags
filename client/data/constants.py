class Constants:
	@staticmethod
	def parseList(constantsList):

		def _parseConstant(constantString):
			parts = constantString.split(' ')
			if (parts[0] == 'constant'):
				return (parts[1], parts[2])
			else:
				print 'Unable to parse {0} as constant'.format(constantsString)
				return None

		return Constants([_parseConstant(constant) for constant in constantsList])


	def __init__(self, constantsList):
		self.dictionary = {}
		for constantTuple in constantsList:
			self.dictionary[constantTuple[0]] = constantTuple[1]


	def isDefined(self, key):
		return key in self.dictionary


	def get(self, key):
		return self.dictionary[key]


	def getInt(self, key):
		return int(self.get(key))


	def getFloat(self, key):
		return float(self.get(key))


	# examples:
	# constant team blue
	# constant worldsize 800
	# constant tankangvel 0.785398163397
	# constant tanklength 6
	# constant tankradius 4.32
	# constant tankspeed 25
	# constant tankalive alive
	# constant tankdead dead
	# constant linearaccel 0.5
	# constant angularaccel 0.5
	# constant tankwidth 2.8
	# constant shotradius 0.5
	# constant shotrange 350
	# constant shotspeed 100
	# constant flagradius 2.5
	# constant explodetime 5
	# constant truepositive 1
	# constant truenegative 1


	def __str__(self):
		return 'Constants({0})'.format(', '.join(['{0} -> {1}'.format(key, self.dictionary[key]) for key in self.dictionary]))
