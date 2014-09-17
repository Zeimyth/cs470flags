#!/usr/bin/env python

def _get_parser():
	parser = ArgumentParser(description='Run a BZRFlags client.')
	parser.add_argument('-p', '--port', type=int, required=True)

	return parser


if __name__ == "__main__":
	from argparse import ArgumentParser

	parser = _get_parser()
	args = parser.parse_args()

	print 'port {0}'.format(args.port)
