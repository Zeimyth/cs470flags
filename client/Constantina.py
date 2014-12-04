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
	parser.add_argument('-w', '--watcher', type=int, required=True)
	parser.add_argument('-c', '--color', required=True)
	parser.add_argument('-d', '--debuglevel')

	return parser

def startKalman(comQueue, args):
	server = ServerProxy(args.url, args.watcher)
	KalmanClient(comQueue, args, server)

if __name__ == "__main__":
	parser = _get_parser()
	args = parser.parse_args()

	comQueue = Queue()
	p = Process(target=startKalman, args=(comQueue, args))
	p.start()
	if args.debuglevel:
		config.setDebugLevelFromString(args.debuglevel)

	ArtemisClient(comQueue, args)