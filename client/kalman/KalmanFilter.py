
import time

class KalmanFilter:

	def __init__(self, server, enemy, comQueue):
		self.flagRadius = 1
		self.flagSpread = 500

		self.server = server
		self.enemy = enemy
		self.color = self.server.listConstants().get('team')

		self.comQueue = comQueue

		self._run()

	def _run(self):
		while True:
			enemy = [e for e in self.server.listEnemyTanks() if e.color == self.enemy][0]
			self.comQueue.put(enemy)
			time.sleep(3)
