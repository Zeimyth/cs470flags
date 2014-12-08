from argparse import ArgumentParser

import config
import random
from net.server import ServerProxy

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
	direction = 1
	while True:
		randomTurn = random.random() * direction
		server.setTurnRate(0,randomTurn)
		if random.random() > .85:
			direction *= -1
		randomVelocity = random.random() * direction
		server.setVelocity(0, randomVelocity)