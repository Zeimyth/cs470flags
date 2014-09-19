#!/usr/bin/env python

import bzrsocket

class ServerProxy(object):

	def __init__(self, url, port):
		self._debug = True

		self.socket = bzrsocket.Socket(url, port)


	""" Orders tank #(tank) to shoot.
		If the tank shoots, the server sends back a standard acknowledge response, e.g.

		ack <timestamp> shoot <tank>
		ok

		This response is received regardless of whether a valid tank was asked to shoot.

		When a tank is asked to shoot too quickly after the last time it fired, an empty
		Fail response is received.
	"""
	def shoot(self, tank):
		if self._debug:
			print 'ServerProxy: Ordering tank {0} to shoot'.format(tank)

		response = self.socket.sendExpectStandardResponse('shoot {0}'.format(tank))

		if self._debug:
			print 'ServerProxy: Response for shoot order = {0}'.format(response)
		elif not response.isOk():
			print 'ServerProxy: Attempted to shoot tank {0}, but it hasn\'t reloaded yet'.format(tank)

		return response


	def setVelocity(self, tank, speed):
		if self._debug:
			print 'ServerProxy: Ordering tank {0} to set velocity to {1}'.format(tank, speed)

		if speed > 1:
			print 'ServerProxy: Limiting tank speed to 1'
			speed = 1
		elif speed < -1:
			print 'ServerProxy: Limiting tank speed to -1'
			speed = -1

		response = self.socket.sendExpectStandardResponse('speed {0} {1}'.format(tank, speed))

		if self._debug:
			print 'ServerProxy: Response for setVelocity order = {0}'.format(response)

		return response


	def setTurnRate(self, tank, rate):
		if self._debug:
			print 'ServerProxy: Ordering tank {0} to set turn rate to {1}'.format(tank, rate)

		if rate > 1:
			print 'ServerProxy: Limiting tank turn rate to 1'
			rate = 1
		elif rate < -1:
			print 'ServerProxy: Limiting tank turn rate to -1'
			rate = -1

		response = self.socket.sendExpectStandardResponse('angvel {0} {1}'.format(tank, rate))

		if self._debug:
			print 'ServerProxy: Response for setTurnRate order = {0}'.format(response)
