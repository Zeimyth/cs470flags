#!/usr/bin/env python

class ServerProxy:

	def __init__(self, port):
		self.port = port

		print('Attempting to connect to BZRFlag server at port {0}'.format(port))