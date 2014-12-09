#!/usr/bin/env python

import sys
import os.path

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

import bzrsocket
import config

from data.base import Base
from data.bullet import Bullet
from data.constants import Constants
from data.enemytank import EnemyTank
from data.flag import Flag
from data.friendlytank import FriendlyTank
from data.obstacle import Obstacle
from data.occgrid import OccGrid
from data.team import Team

class ServerProxy(object):

	def __init__(self, url, port):
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
		if config.debugLevelEnabled(config.TRACE):
			print 'ServerProxy: Ordering tank {0} to shoot'.format(tank)

		response = self.socket.sendExpectStandardResponse('shoot {0}'.format(tank))

		if config.debugLevelEnabled(config.TRACE):
			print 'ServerProxy: Response for shoot order = {0}'.format(response)
		elif not response.isOk() and config.debugLevelEnabled(config.WARN):
			print 'ServerProxy: Attempted to shoot tank {0}, but it hasn\'t reloaded yet'.format(tank)

		return response


	def setVelocity(self, tank, speed):
		if config.debugLevelEnabled(config.TRACE):
			print 'ServerProxy: Ordering tank {0} to set velocity to {1}'.format(tank, speed)

		if speed > 1:
			print 'ServerProxy: Limiting tank speed to 1'
			speed = 1
		elif speed < -1:
			print 'ServerProxy: Limiting tank speed to -1'
			speed = -1

		response = self.socket.sendExpectStandardResponse('speed {0} {1}'.format(tank, speed))

		if config.debugLevelEnabled(config.TRACE):
			print 'ServerProxy: Response for setVelocity order = {0}'.format(response)

		return response


	def setTurnRate(self, tank, rate):
		if config.debugLevelEnabled(config.TRACE):
			print 'ServerProxy: Ordering tank {0} to set turn rate to {1}'.format(tank, rate)

		if rate > 1:
			print 'ServerProxy: Limiting tank turn rate to 1'
			rate = 1
		elif rate < -1:
			print 'ServerProxy: Limiting tank turn rate to -1'
			rate = -1

		response = self.socket.sendExpectStandardResponse('angvel {0} {1}'.format(tank, rate))

		if config.debugLevelEnabled(config.TRACE):
			print 'ServerProxy: Response for setTurnRate order = {0}'.format(response)


	def listTeams(self):
		if config.debugLevelEnabled(config.TRACE):
			print 'ServerProxy: Sending listTeams request'

		response = self.socket.sendExpectListResponse('teams')

		if config.debugLevelEnabled(config.TRACE):
			print 'ServerProxy: Response for listTeams request = {0}'.format(response)

		return Team.parseList(response.getList())


	def listObstacles(self):
		if config.debugLevelEnabled(config.TRACE):
			print 'ServerProxy: Sending listObstacles request'

		response = self.socket.sendExpectListResponse('obstacles')

		if config.debugLevelEnabled(config.TRACE):
			print 'ServerProxy: Response for listObstacles request = {0}'.format(response)

		return Obstacle.parseList(response.getList())


	def listBases(self):
		if config.debugLevelEnabled(config.TRACE):
			print 'ServerProxy: Sending listBases request'

		response = self.socket.sendExpectListResponse('bases')

		if config.debugLevelEnabled(config.TRACE):
			print 'ServerProxy: Response for listBases request = {0}'.format(response)

		return Base.parseList(response.getList())


	def listFlags(self):
		if config.debugLevelEnabled(config.TRACE):
			print 'ServerProxy: Sending listFlags request'

		response = self.socket.sendExpectListResponse('flags')

		if config.debugLevelEnabled(config.TRACE):
			print 'ServerProxy: Response for listFlags request = {0}'.format(response)

		return Flag.parseList(response.getList())


	def listShots(self):
		if config.debugLevelEnabled(config.TRACE):
			print 'ServerProxy: Sending listShots request'

		response = self.socket.sendExpectListResponse('shots')

		if config.debugLevelEnabled(config.TRACE):
			print 'ServerProxy: Response for listShots request = {0}'.format(response)

		return Bullet.parseList(response.getList())


	def listFriendlyTanks(self):
		if config.debugLevelEnabled(config.TRACE):
			print 'ServerProxy: Sending listFriendlyTanks request'

		response = self.socket.sendExpectListResponse('mytanks')

		if config.debugLevelEnabled(config.TRACE):
			print 'ServerProxy: Response for listFriendlyTanks request = {0}'.format(response)

		return FriendlyTank.parseList(response.getList())


	def listEnemyTanks(self):
		if config.debugLevelEnabled(config.TRACE):
			print 'ServerProxy: Sending listEnemyTanks request'

		response = self.socket.sendExpectListResponse('othertanks')

		if config.debugLevelEnabled(config.TRACE):
			print 'ServerProxy: Response for listEnemyTanks request = {0}'.format(response)

		return EnemyTank.parseList(response.getList())


	def listConstants(self):
		if config.debugLevelEnabled(config.TRACE):
			print 'ServerProxy: Sending listContants request'

		response = self.socket.sendExpectListResponse('constants')

		if config.debugLevelEnabled(config.TRACE):
			print 'ServerProxy: Response for listConstants request = {0}'.format(response)

		return Constants.parseList(response.getList())


	def getSurroundings(self, tank):
		if config.debugLevelEnabled(config.TRACE):
			print 'ServerProxy: Sending getSurroundings request'

		response = self.socket.sendExpectListResponse('occgrid {0}'.format(tank))

		if config.debugLevelEnabled(config.TRACE):
			print 'ServerProxy: Response for listConstants request = {0}'.format(response)

		occList = response.getList()
		if len(occList) > 0:
			return OccGrid.parseList(response.getList())
		else:
			return None

