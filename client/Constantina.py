#!/usr/bin/env python

from argparse import ArgumentParser
from multiprocessing import Queue, Process

import config
from KalmanClient import KalmanClient
from ArtemisClient import ArtemisClient
from net.server import ServerProxy
from agency.fieldagency import FieldAgency

def _get_parser():
	parser = ArgumentParser(description='Run a BZRFlags client.')
	parser.add_argument('url')
	parser.add_argument('-p', '--port', type=int, required=True)
	parser.add_argument('-c', '--color', required=True)
	parser.add_argument('-d', '--debuglevel')

	return parser

def startKalman(obsQueue, predQueue, args, interval):
	KalmanClient(obsQueue, predQueue, args, interval)

if __name__ == "__main__":
	parser = _get_parser()
	args = parser.parse_args()

	if args.debuglevel:
		print "Setting debug level to {}".format(args.debuglevel)
		config.setDebugLevelFromString(args.debuglevel)

	obsQueue = Queue()
	predQueue = Queue()

	interval = 3

	if config.debugLevelEnabled(config.INFO):
		print 'Constantina: Starting child processes'

	p = Process(target=startKalman, args=(obsQueue, predQueue, args, interval))
	p.start()

	ArtemisClient(obsQueue, predQueue, args, interval)
