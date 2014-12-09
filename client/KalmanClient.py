#!/usr/bin/env python

from net.server import ServerProxy
from kalman.KalmanFilter import KalmanFilter

class KalmanClient:

	def __init__(self, obsQueue, predQueue, args, interval):
		KalmanFilter(args.color, obsQueue, predQueue, interval)