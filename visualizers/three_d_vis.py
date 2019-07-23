import matplotlib as mpl 
from matplotlib import pyplot as plt 
from mpl_toolkits import mplot3d
from abc import ABC, abstractmethod 
import pandas as pd
from visualizers.visualization import Visualization


class ThreeDVis(Visualization):
	def __init__(self, dep_name, dist_arr, user_name, lat_name, lon_name, file):
		"""
		Creates and plots a 3D visualization of the hard data 
		
		@type dept_name: str
		@param dep_name: the name of the depth column in the csv file
		@type dist_arr: array-like
		@param dist_arr: the array that contains each point's distance from the original point
		@type user_name: str
		@param user_name: the name of the column of the user-selected data in the csv file
		@type lat_name: str
		@param lat_name: the name of the latitude column in the csv file
		@type lon_name: str
		@param lon_name: the name of the longitude column in the csv file
		@type file: Pandas DataFrame
		@param file: the pandas dataframe containing the read data from the csv file
		"""

		self.depth = file[dep_name].values.tolist()
		self.user = file[user_name].values
		self.dist = dist_arr
		self.lat = file[lat_name].values
		self.lon = file[lon_name].values
		self.lat_n = lat_name
		self.lon_n = lon_name
		self.user_n = user_name
		self.dep_n = dep_name

	def plot(self):
		"""
		Plots and shows a 3D graph of the hard data
		"""

		fig = plt.figure()
		cmap = mpl.cm.jet
		ax = fig.add_subplot(111, projection = '3d')
		for i in range(len(self.depth)):
			self.depth[i] = (self.depth[i] * -1)
		axis = ax.scatter(self.lat, self.lon, (self.depth), c = self.user, cmap = cmap)
		ax.set_xlabel(self.lat_n)
		ax.set_ylabel(self.lon_n)
		ax.set_zlabel(self.dep_n)
		cb = plt.colorbar(axis)
		cb.set_label(self.user_n)
		plt.show()
