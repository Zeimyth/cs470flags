#!/usr/bin/env python

class ServerProxy:

	def __init__(self, url, port):
		self.url = url
		self.port = port

		print('Attempting to connect to BZRFlag server {0} at port {1}'.format(url, port))