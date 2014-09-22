#!/usr/bin/env python

from argparse import ArgumentParser

from net.server import ServerProxy
from plotter.plotter import plot

def _get_parser():
	parser = ArgumentParser(description='Run a BZRFlags client.')
	parser.add_argument('url')
	parser.add_argument('-p', '--port', type=int, required=True)

	return parser


if __name__ == "__main__":
	parser = _get_parser()
	args = parser.parse_args()

	server = ServerProxy(args.url, args.port)
	obstacles = server.listObstacles()
	obs = [ob.toTupleList() for ob in obstacles]
	print obs
	plot(obs)
