#!/usr/bin/env python

from argparse import ArgumentParser

import config
from net.server import ServerProxy
from agency.fieldagency import FieldAgency

def _get_parser():
	parser = ArgumentParser(description='Run a BZRFlags client.')
	parser.add_argument('url')
	parser.add_argument('-p', '--port', type=int, required=True)
	parser.add_argument('-c', '--color', required=True)
	parser.add_argument('-d --debuglevel')

	return parser


if __name__ == "__main__":
	parser = _get_parser()
	args = parser.parse_args()

	if hasattr(args, 'debuglevel'):
		config.setDebugLevelFromString(args.debuglevel)

	server = ServerProxy(args.url, args.port)
	FieldAgency(server, args.color)
