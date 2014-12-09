#!/usr/bin/env python

from argparse import ArgumentParser

import config
from net.server import ServerProxy
from agency.ArtemisAgency import ArtemisAgency

class ArtemisClient:

	def __init__(self, obsQueue, predQueue, args, interval):
		server = ServerProxy(args.url, args.port)
		ArtemisAgency(server, args.color, obsQueue, predQueue, interval)