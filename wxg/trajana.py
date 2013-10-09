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
		self.pos = pos[0:2]
		self.v = v

	def spatial_dist_to(self, x):
		"""
		Spatial distance to another node
		Defined by Euclidean distance

		This is the function `h` in Wang[06]
		"""
		d = self.pos - x.pos
		return np.sqrt(d.dot(d))

	def feature_dist_to(self, x):
		"""
		Feature distance to another node

		This is the function `d` in Wang[06]
		"""

		return 0

	def dist_to(self, x):
		return self.spatial_dist_to(x) + 1 * self.feature_dist_to(x)

	def to_string(self):
		rst = 'x=%d, y=%d' % (self.x, self.y)
		return rst

	def nearest_node_in(self, trajectory):
		"""
		Finds the index of the node in a trajectory that is
		nearest to this node

		This is the `phi` function in Wang[06]
		"""
		dists = [self.dist_to(node) for node in trajectory.nodes]
		return np.argmin(dists)

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

	def dist_to(self, trajectory):
		"""
		Returns the distance between 'self' and 'x'
		"""
		dists = []
		for i in range(len(self.nodes)):
			nodeA = self.nodes[i]
			nodeB = nodeA.nearest_node_in(trajectory)
			dists.append(nodeA.dist_to(nodeB)

		return np.average(dists)

# end class Trajectory


class AnalysisEngine(object):
	"""
	Analysis Engine, contains utilities that analysis trajectory corpus
	"""

	pass