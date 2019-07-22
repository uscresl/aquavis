import matplotlib as mpl 
from matplotlib import pyplot as plt 
from mpl_toolkits import mplot3d
from abc import ABC, abstractmethod 
import pandas as pd
from visualizers.visualization import Visualization


class ThreeDVis(Visualization):
	def __init__(self, dep_name, dist_arr, user_name, lat_name, lon_name, file):
		self.dep = file[dep_name].values
		self.depth = []
		for i in range(len(self.dep)):
			self.depth.append(self.dep[i] * -1)
		self.user = file[user_name].values
		self.dist = dist_arr
		self.lat = file[lat_name].values
		self.lon = file[lon_name].values
		self.lat_n = lat_name
		self.lon_n = lon_name
		self.user_n = user_name
		self.dep_n = dep_name

	def plot(self):
		fig = plt.figure()
		cmap = mpl.cm.jet
		ax = fig.add_subplot(111, projection = '3d')
		axis = ax.scatter(self.lat, self.lon, (self.depth), c = self.user, cmap = cmap)
		ax.set_xlabel(self.lat_n)
		ax.set_ylabel(self.lon_n)
		ax.set_zlabel(self.dep_n)
		cb = plt.colorbar(axis)
		cb.set_label(self.user_n)
		plt.show()
