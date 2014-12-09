import sys
import os.path

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

import config

import time
import numpy

class KalmanFilter:

	def __init__(self, enemy, obsQueue, predQueue, interval):
		self.iteration_count = 15

		self.enemy = enemy

		self.obsQueue = obsQueue
		self.predQueue = predQueue

		if config.debugLevelEnabled(config.INFO):
			print "KalmanFilter: Initializing"

		self._setConstants(interval)

		self._run()

	def _setConstants(self, interval):
		self.state_not = numpy.matrix('400;0;0;0;0;0')
		self.epsilon_not = numpy.matrix(
			'100   0   0   0   0   0;'+
			'  0   .1  0   0   0   0;'+
			'  0   0   .1  0   0   0;'+
			'  0   0   0 100   0   0;'+
			'  0   0   0   0  .1   0;'+
			'  0   0   0   0   0  .1'
		)

		self.delta_t = interval

		self.transmission = numpy.matrix([
			[1, self.delta_t, self.delta_t**2/2.0, 0,            0,                   0],
			[0,            1,        self.delta_t, 0,            0,                   0],
			[0,            0,                   1, 0,            0,                   0],
			[0,            0,                   1, 1, self.delta_t, self.delta_t**2/2.0],
			[0,            0,                   1, 0,            1,        self.delta_t],
			[0,            0,                   1, 0,            0,                   1]
		])
		                            
		self.transmission_t = self.transmission.transpose()
		                            
		self.transmission_eps = numpy.matrix(numpy.matrix(
			' .1 0  0  0  0  0;'+
			' 0  .1 0  0  0  0;'+
			' 0  0 25  0  0  0;'+
			' 0  0  0  .1 0  0;'+
			' 0  0  0  0  .1 0;'+
			' 0  0  0  0  0 25')
		)
		                                            
		self.emission = numpy.matrix(
			'1 0 0 0 0 0;' +
			'0 0 0 1 0 0'
		)
		                        
		self.emission_t = self.emission.transpose()
		                        
		variance_parameter = 25

		self.emission_eps = numpy.matrix([
			[variance_parameter, 0],
			[0, variance_parameter]
		])
		                             
		self.state_now = self.state_not
		self.identity = numpy.identity(6)
		self.kalmans = {}
		self.epsilons = {0:self.epsilon_not}
		self.FEtFTpluses = {}
		self.tankStates = {}
		self.tankObservations = {}

	def _run(self):
		while True:
			now = time.time()

			if config.debugLevelEnabled(config.DEBUG):
				print 'KalmanFilter: filtering'

			next_wakeup = now + self.delta_t
			self._doPredictions()
			sleepLength = next_wakeup - time.time()

			time.sleep(sleepLength)

	def _doPredictions(self):
		observations = ""
		while not self.obsQueue.empty():
			observations = self.obsQueue.get()
		if observations != "":
			prediction = self.predictEnemyPositions(observations)
			self.predQueue.put(prediction)

	def predictEnemyPositions(self, enemyList):
		enemyList = [e for e in enemyList if e.color == self.enemy]
		predictions = []
		for e in enemyList:
			state_now = self.tankStates.get(e.callsign, self.state_not)
			iteration = self.tankObservations.setdefault(e.callsign, 0)
			i = (iteration % self.iteration_count) + 1
			state_next = self.filterObservation(e.x, e.y, state_now, i)
			prediction = self.predictFuturePosition(state_next)
			predictions.append((prediction[0,0], prediction[3,0]))
			self.tankObservations[e.callsign] += 1
			self.tankStates[e.callsign] = state_next
		return predictions

	def calculate_FEtFTplus(self, i):
		epsilon_now = self.epsilons[i-1]
		FEtFTplus = (self.transmission * epsilon_now * self.transmission_t) + self.transmission_eps
		return FEtFTplus

	def calculate_kalman(self, FEtFTplus):
		kalman_next = FEtFTplus * self.emission_t * numpy.linalg.inv((self.emission * FEtFTplus * self.emission_t) + self.emission_eps)
		return kalman_next

	def calculate_epsilon(self, FEtFTplus, kalman_next):
		epsilon_next = (self.identity - (kalman_next * self.emission))*FEtFTplus
		return epsilon_next

	def filterObservation(self, observation_x, observation_y, state_now, i):
		observation = numpy.matrix([[observation_x],[observation_y]])
		if i not in self.FEtFTpluses:
			FEtFTplus = self.calculate_FEtFTplus(i)
			self.FEtFTpluses[i] = FEtFTplus
		else:
			FEtFTplus = self.FEtFTpluses[i]

		if i not in self.kalmans:
			kalman_next = self.calculate_kalman(FEtFTplus)
			self.kalmans[i] = kalman_next
		else:
			kalman_next = self.kalmans[i]

		if i not in self.epsilons:
			epsilon_next = self.calculate_epsilon(FEtFTplus, kalman_next)
			self.epsilons[i] = epsilon_next
		else:
			epsilon_next = self.epsilons[i]

		state_next = (self.transmission * state_now) + (kalman_next * (observation - (self.emission * self.transmission * state_now)))
		return state_next

	def predictFuturePosition(self, state):
		return self.transmission * state

