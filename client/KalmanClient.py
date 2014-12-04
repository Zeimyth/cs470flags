#!/usr/bin/env python

from net.server import ServerProxy
from kalman.KalmanFilter import KalmanFilter

class KalmanClient:

	def __init__(self, comQueue, args, server):
		KalmanFilter(server, args.color, comQueue)