import sys
sys.path.append('../utilities')
from frames import *
from parseTrackletXML import *
from scipy import stats, signal
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

"""
To Do:

Change Node.feature_dist_to().
	Currently it ranges in [0,2]

"""

# parameters: Lambda, ratio of feature distance and spatial distance
pLambda = 1
# parameters: Sigma, gaussian parameter for converting node distance to similarity
pSigma = 1
# parameters: Sigma 1, gaussian parameter for comparison confidence
pSigma1 = 1

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
		We use cosine similarity for this.

		This is the function `d` in Wang[06]
		"""
		# Feature vector
		fv1 = self.v
		fv2 = x.v
		cos_sim = np.dot(fv1, fv2) / np.sqrt(np.dot(fv1,fv1) * np.dot(fv2, fv2))

		return 1 - cos_sim

	def dist_to(self, x):
		return self.spatial_dist_to(x) + pLambda * self.feature_dist_to(x)

	def similarity_to(self, x):
		return np.exp(-self.dist_to(x)/pSigma)

	def comparison_confidence(self, x):
		return np.exp(self.spatial_dist_to(x)/pSigma1)


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

	def nearest_node_to(self, node):
		dists = [node.spatial_dist_to(n) for n in self.nodes]

		return np.argmin(dists)

	# Similarity Version I
	# def dist_to(self, trajectory):
	# 	"""
	# 	Returns the distance between 'self' and 'x'
	# 	"""
	# 	dists = []
	# 	for i in range(len(self.nodes)):
	# 		nodeA = self.nodes[i]
	# 		nodeB = trajectory.nearest_node_to(nodeA)
	# 		dists.append(nodeA.dist_to(nodeB))

	# 	return np.average(dists)

	# Similarity Version II
	def similarity_to(self, trajectory):
		"""
		Trajectory similarity to

		This is the function S_A_B in Wang[06]
		"""
		sims = []	# similarities
		cons = []	# confidences
		for i in range(len(self.nodes)):
			nodeA = self.nodes[i]
			nodeB = self.nodes[self.nearest_node_to(nodeA)]
			sims.append(nodeA.similarity_to(nodeB))
			cons.append(nodeA.comparison_confidence(nodeB))

		return np.dot(sims, cons) / np.sum(cons)

	def comparison_confidence(self, trajectory):
		"""
		Trajectory comparison confidence to

		This is the function C_A_B in Wang[06]
		"""
		cons = []	# confidences
		for i in range(len(self.nodes)):
			nodeA = self.nodes[i]
			nodeB = self.nodes[self.nearest_node_to(nodeA)]
			cons.append(nodeA.comparison_confidence(nodeB))

		return np.dot(cons, cons) / np.sum(cons)

	def dist_to(self, trajectory):
		"""
		Returns the distance between 'self' and 'x'
		"""
		dists = []
		for i in range(len(self.nodes)):
			nodeA = self.nodes[i]
			nodeB = nodeA.nearest_node_in(trajectory)
			dists.append(nodeA.dist_to(nodeB))

		return np.average(dists)

# end class Trajectory


class AnalysisEngine(object):
	"""
	Analysis Engine, contains utilities that analysis trajectory corpus
	"""

	pass