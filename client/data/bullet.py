class Bullet:
	@staticmethod
	def parseList(bulletList):

		def _parseBullet(bulletString):
			parts = bulletString.split(' ')
			if (parts[0] == 'shot'):
				return Bullet(float(parts[1]), float(parts[2]), float(parts[3]), float(parts[4]))
			else:
				print 'Unable to parse {0} as bullet'.format(bulletString)
				return None

		return [_parseBullet(bullet) for bullet in bulletList]


	def __init__(self, x, y, vx, vy):
		self.x = x
		self.y = y
		self.vx = vx
		self.vy = vy


	def __str__(self):
		return 'Bullet(({0}, {1}), ({2}, {3}))'.format(self.x, self.y, self.vx, self.vy)
