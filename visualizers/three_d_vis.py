import matplotlib as mpl 
from matplotlib import pyplot as plt 
from mpl_toolkits import mplot3d
from abc import ABC, abstractmethod 
import pandas as pd
from visualizers.visualization import Visualization
class ThreeDVis(Visualization):
	def __init__(self, dep_name, dist_arr, user_name, lat_name, lon_name, file):
		self.dep = file[dep_name].values#array-like
		self.depth = []
		for i in range(len(self.dep)):
			self.depth.append(self.dep[i] * -1)#*-1#array-like
		self.user = file[user_name].values#array-like
		self.dist = dist_arr#array-like
		self.lat = file[lat_name].values#array-like
		self.lon = file[lon_name].values#array-like
		self.lat_n = lat_name#str
		self.lon_n = lon_name#str
		self.user_n = user_name#str
		self.dep_n = dep_name#str
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
