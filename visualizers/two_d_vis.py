from abc import ABC, abstractmethod
import matplotlib as mpl 
from matplotlib import pyplot as plt
import pandas as pd
from visualizers.visualization import Visualization
class TwoDVis (Visualization):
	def __init__(self, dep_name, dist_arr, user_name, file):
		self.dep = file[dep_name].values#array-like
		self.depth = []
		for i in range(len(self.dep)):
			self.depth.append(self.dep[i] * -1)#*-1#array-like
		self.user = file[user_name].values#array-like
		self.dist = dist_arr#array-like
		self.dep_n = dep_name#str
		self.user_n = user_name#str
	def plot (self):
		plt.figure()
		plt.xlabel("Distance")
		plt.ylabel(self.dep_n)
		cmap = mpl.cm.jet
		axis = plt.scatter(self.dist, (self.depth), c=self.user, cmap = cmap)
		cb_title = plt.colorbar(axis)
		cb_title.set_label(self.user_n)
		plt.show()

