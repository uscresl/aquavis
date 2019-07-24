from abc import ABC, abstractmethod
import matplotlib as mpl 
from matplotlib import pyplot as plt
import pandas as pd
from visualizers.visualization import Visualization


class TwoDVis (Visualization):
	def __init__(self, dep_name, dist_arr, user_name, file):
		"""
		Creates and plots a 2D visualization of the hard data 
		
		@type dep_name: str
		@param dep_name: the name of the depth column in the csv file
		@type dist_arr: array-like
		@param dist_arr: the array that contains each point's distance from the original point
		@type user_name: str
		@param user_name: the name of the column of the user-selected data in the csv file
		@type file: Pandas DataFrame
		@param file: the pandas dataframe containing the read data from the csv file
		"""

		self.depth = file[dep_name].values.tolist()
		self.user = file[user_name].values
		self.dist = dist_arr
		self.dep_n = dep_name
		self.user_n = user_name

	def plot (self):
		"""
		Plots and shows a 2D graph of the hard data
		"""

		plt.figure()
		plt.xlabel("Distance")
		plt.ylabel(self.dep_n)
		cmap = mpl.cm.jet
		for i in range(len(self.depth)):
			self.depth[i] = (self.depth[i] * -1)
		axis = plt.scatter(self.dist, self.depth, c=self.user, cmap = cmap)
		cb_title = plt.colorbar(axis)
		cb_title.set_label(self.user_n)
		plt.show()

