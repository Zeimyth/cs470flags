from argparse import ArgumentParser

import config
from net.server import ServerProxy
from agent.blindpigeon import BlindPigeon

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
	agents = [BlindPigeon()]
	while True:
		tankData = server.listFriendlyTanks()
		for i in range(len(agents)):
			action = agents[i].getAction(tankData[i])
			if action is not None:
				if 'speed' in action:
					server.setVelocity(i, action['speed'])
				if 'angle' in action:
					server.setTurnRate(i, action['angle'])
				if 'shoot' in action:
					server.shoot(i)