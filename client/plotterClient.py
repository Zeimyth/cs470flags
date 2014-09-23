#!/usr/bin/env python

from argparse import ArgumentParser

from net.server import ServerProxy
from plotter.plotter2 import plot
from fields.attractive import AttractiveField
from fields.repulsive import RepulsiveField
from math import sqrt

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
	fields = []
	flags = server.listFlags()
	flag = [flag for flag in flags if flag.color == "purple"][0]
	fields.append(AttractiveField(flag.x, flag.y, 10, 200))
		
	for obstacle in obstacles:
		x = 0
		y = 0
		for point in obstacle._points:
			x += point.x
			y += point.y
		x = x / len(obstacle._points)
		y = y / len(obstacle._points)
		radiusx = obstacle._points[0].x - obstacle._points[3].x
		radiusy = obstacle._points[0].y - obstacle._points[3].y
		radius = sqrt(pow(radiusx, 2) + pow(radiusy, 2)) / 2
		spread = 150
		repulsiveField = RepulsiveField(x, y, radius, spread)
		fields.append(repulsiveField)
	plot(obs, fields)
