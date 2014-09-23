#/usr/bin/env python

import os
import sys
import socket

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

import config

from response import *

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

		self._initialize_socket()


	def _initialize_socket(self):
		if config.debugLevelEnabled(config.INFO):
			print 'Socket: Establishing connection to server {0} at port {1}'.format(self.url, self.port)

		try:
			self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.socket.connect((self.url, self.port))

			greeting = self._receive()

			if greeting != Socket.GREETING:
				if config.debugLevelEnabled(config.ERROR):
					print ('Socket: Invalid greeting received from server {0} at port {1}: {2}'
						.format(self.url, self.port, greeting))
				sys.exit(1)
			else:
				message = 'agent 1'
				self.sendExpectNoResponse(message)

		except socket.error as e:
			if config.debugLevelEnabled(config.ERROR):
				print ('Socket: Error occurred while attempting to establish connection with server {0} at port {1}: {2}'
					.format(self.url, self.port, e))

			sys.exit(1)

		if config.debugLevelEnabled(config.INFO):
			print 'Socket: Connection successfully established'


	def _close_socket(self):
		if config.debugLevelEnabled(config.INFO):
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
				if config.debugLevelEnabled(config.WARN):
					print ('Socket: WARN: Received acknowledge line that doesn\'t match message. ' +
						'Message = "{0}", Response = "{1}"').format(message, response)
				return FailResponse([])

		splitResponse = response[responseLine].split(' ', 1)

		if splitResponse[0] == Socket.OK_RESPONSE:
			return OkResponse(splitResponse[1:])
		else:
			return FailResponse(splitResponse[1:])


	def sendExpectListResponse(self, message):
		response = self._handleSend(message, True)
		lines = response.split('\n')

		# Response format:
		# awk ...
		# begin
		# (list elements) ...
		# end
		return ListResponse(lines[2:-1])


	def _handleSend(self, message, listen):
		self._send(message)

		if not listen:
			return
		else:
			return self._receive()


	def _send(self, message):
		if config.debugLevelEnabled(config.DEBUG):
			print 'Socket: Sending "{0}"'.format(message)

		self.socket.send(message + '\n')


	def _receive(self):
		fullResponse = ''

		while 1:
			data = self.socket.recv(self.RECV_SIZE)

			if config.debugLevelEnabled(config.TRACE):
				print 'Socket: Receive loop, received "{0}"'.format(data)

			if not data.startswith(Socket.ACKNOWLEDGE):
				fullResponse += data
				lastLine = data.strip().split('\n')[-1]
				if any([lastLine.startswith(eom) for eom in Socket.END_OF_MESSAGE_LIST]):
					break

		fullResponse = fullResponse.strip()
		if config.debugLevelEnabled(config.DEBUG):
			print 'Socket: Received "{0}"'.format(fullResponse)

		return fullResponse
