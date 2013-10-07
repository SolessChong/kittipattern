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

class Node:
	"""
	Node is the component of trajectory.
	A node is a two-dimensional point, together with some features
	"""

	def __init__(self, obj):
		self.obj = obj
		
		
	def 