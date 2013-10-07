import sys
sys.path.append('../utilities')
from frames import *
from parseTrackletXML import *
from scipy import stats
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import re
import os
import fnmatch
import pickle

"""
Trajectory Analysis
Implementation of 
Xiaogang Wang [06]
`Learning Semantic Scene Models by Trajectory Analysis`, ECCV
"""

class Node(object):
	"""
	Node is the component of trajectory.
	A node is a two-dimensional point, together with some features
	"""

	def __init__(self, pos, v):
		self.pos = pos
		self.v = v

	def to_string(self):
		rst = 'x=%d, y=%d' % (self.x, self.y)
		return rst

# end class Node

class Trajectory(object):
	"""
	Trajactory comprises of several nodes.
	Initialize a trajectory from a tracklet that contains several observations
	"""

	nodes = None		# list of node's
	firstFrame = None	# first frame of this trajectory
	nFrames = None		# number of frames

	def __init__(self, tracklet):
		self.nodes = [Node(t, v) for t, v in zip(tracklet.trans, tracklet.velos)]
		self.firstFrame = tracklet.firstFrame
		self.nFrames = tracklet.nFrames

	def __sub__(self, x):
		"""
		Returns the distance between `self` and `x`
		"""
		return self.dist_to(x)

	def dist_to(self, x):
		"""
		Returns the distance between 'self' and 'x'
		"""
		return 3

# end class Trajectory


class AnalysisEngine(object):
	"""
	Analysis Engine, contains utilities that analysis trajectory corpus
	"""

	pass