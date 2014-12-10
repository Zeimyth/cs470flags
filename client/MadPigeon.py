from argparse import ArgumentParser

import random

import config
from net.server import ServerProxy
import time

def _get_parser():
	parser = ArgumentParser(description='Run a BZRFlags client.')
	parser.add_argument('url')
	parser.add_argument('-p', '--port', type=int, required=True)
	parser.add_argument('-d', '--debuglevel')

	return parser


if __name__ == "__main__":
	parser = _get_parser()
	args = parser.parse_args()

	if args.debuglevel:
		config.setDebugLevelFromString(args.debuglevel)

	server = ServerProxy(args.url, args.port)
	forward = 1
	turn = 1
	while True:
		if random.random() < .10:
			turn *= -1
		server.setTurnRate(0, turn)
		time.sleep(.1)
		if random.random() < .05:
			forward *= -1
		server.setVelocity(0, forward)
		time.sleep(.1)