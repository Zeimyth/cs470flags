#!/usr/bin/env python

import socket
import sys

class ServerProxy:

	def __init__(self, url, port):
		self.socket = Socket(url, port)
		self._debug = True



class Socket:
	RECV_SIZE = 1024

	def __init__(self, url, port):
		self.url = url
		self.port = port
		self._debug = True

		self._initialize_socket()


	def _initialize_socket(self):
		if self._debug:
			print 'Socket: Establishing connection to server {0} at port {1}'.format(self.url, self.port)

		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		try:
			self.socket.connect((self.url, self.port))

			greeting = self.socket.recv(self.RECV_SIZE).strip()

			if greeting != 'bzrobots 1':
				print ('Socket: Invalid greeting received from server {0} at port {1}: {2}'
					.format(self.url, self.port, greeting))
			else:
				message = 'agent 1'
				self.send(message, False)

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


	def send(self, message, listen=True):
		if self._debug:
			print 'Socket: Sending "{0}"'.format(message)

		self.socket.send(message)

		if not listen:
			return
		else:
			data = self.socket.recv(1024)

			if self._debug:
				print 'Socket: Received "{0}"'.format(data)

			return message


	def __del__(self):
		self._close_socket()
