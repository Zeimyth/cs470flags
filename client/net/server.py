#!/usr/bin/env python

import socket
import sys

from response import *

class ServerProxy(object):

	def __init__(self, url, port):
		self._debug = True

		self.socket = Socket(url, port)


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



class Socket(object):
	RECV_SIZE = 4096

	ACKNOWLEDGE = 'awk'
	GREETING = 'bzrobots 1'
	OK_RESPONSE = 'ok'
	FAIL_RESPONSE = 'fail'
	LIST_END = 'end'

	END_OF_MESSAGE_LIST = [GREETING, OK_RESPONSE, FAIL_RESPONSE, LIST_END]

	def __init__(self, url, port):
		self.url = url
		self.port = port
		self._debug = True

		self._initialize_socket()


	def _initialize_socket(self):
		if self._debug:
			print 'Socket: Establishing connection to server {0} at port {1}'.format(self.url, self.port)

		try:
			self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.socket.connect((self.url, self.port))

			greeting = self._receive()

			if greeting != Socket.GREETING:
				print ('Socket: Invalid greeting received from server {0} at port {1}: {2}'
					.format(self.url, self.port, greeting))
				sys.exit(1)
			else:
				message = 'agent 1'
				self.sendExpectNoResponse(message)

		except socket.error as e:
			print ('Socket: Error occurred while attempting to establish connection with server {0} at port {1}: {2}'
				.format(self.url, self.port, e))

			sys.exit(1)

		if self._debug:
			print 'Socket: Connection successfully established'


	def _close_socket(self):
		if self._debug:
			print 'Socket: Closing connection'

		self.socket.close()


	def sendExpectNoResponse(self, message):
		self._handleSend(message, False)


	def sendIgnoreResponse(self, message):
		self._handleSend(message, True)


	def sendExpectStandardResponse(self, message):
		response = self._handleSend(message, True)
		lines = response.split('\n')

		responseLine = 0
		if lines[responseLine].startswith(Socket.ACKNOWLEDGE):
			# setVelocity or setTurnRate 1 comes back as 1.0
			if lines[responseLine].endswith(message):
				responseLine += 1
			else:
				print ('Socket: ERROR: Received acknowledge line that doesn\'t match message. ' +
					'Message = "{0}", Response = "{1}"').format(message, response)
				return FailResponse([])

		splitResponse = response[responseLine].split(' ', 1)

		if splitResponse[0] == Socket.OK_RESPONSE:
			return OkResponse(splitResponse[1:])
		else:
			return FailResponse(splitResponse[1:])


	def _handleSend(self, message, listen):
		self._send(message)

		if not listen:
			return
		else:
			return self._receive()


	def _send(self, message):
		if self._debug:
			print 'Socket: Sending "{0}"'.format(message)

		self.socket.send(message + '\n')


	def _receive(self):
		fullResponse = ''

		while 1:
			data = self.socket.recv(self.RECV_SIZE)

			if self._debug:
				print 'Socket: Receive loop, received "{0}"'.format(data)

			if not data.startswith(Socket.ACKNOWLEDGE):
				fullResponse += data
				lastLine = data.strip().split('\n')[-1]
				if any([lastLine.startswith(eom) for eom in Socket.END_OF_MESSAGE_LIST]):
					break

		fullResponse = fullResponse.strip()
		if self._debug:
			print 'Socket: Received "{0}"'.format(fullResponse)

		return fullResponse


	def __del__(self):
		self._close_socket()
