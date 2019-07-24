from abc import ABC, abstractmethod
from sklearn import svm
from sklearn.metrics import mean_squared_error
import pandas as pd
import numpy as np
from models.model import Model


class SV(Model):
	def __init__(self, dist_arr, user_name, dep_name, length, file, lat_n, lon_n, dims):
		"""
		Creates a Support Vector Regression-based model to interpolate data 
		
		@type dist_arr: array-like
		@param dist_arr: the array that contains each point's distance from the original point
		@type user_name: str
		@param user_name: the name of column of the additional data set selected by the user
		@type dep_name: str
		@param dep_name: the name of the depth column in the csv file
		@type length: int
		@param length: the number of points per row/column that will be displayed on the graph
		@type file: Pandas DataFrame
		@param file: the pandas dataframe containing all of the read data from the csv file
		@type lat_n: str
		@param lat_n: the name of the latitude column in the csv file
		@type lon_n: str
		@param lon_n: the name of the longitude column in the csv file
		@type dims: int
		@param dims: the desired dimensions of the graph representing the interpolations of the GPR
		"""

		self.dist = dist_arr
		self.user = file[user_name].values
		self.dimensions = int(dims)
		self.depth = file[dep_name].values.tolist()
		self.is_fit = False
		self._clf = svm.SVR(kernel = 'poly', gamma = 'scale')
		self.dimns = length

		if self.dimensions == 2:
			self.x_coor = np.linspace(min(self.dist), max(self.dist), self.dimns)
			self.y_coor = np.linspace(min(self.depth), max(self.depth), self.dimns)
			self.xx, self.yy = np.meshgrid(self.x_coor, self.y_coor)
			self.x = []
			self.y = []
			self.xy = []
			for i in range(len(self.xx)):
				for j in range(len(self.xx[i])):
					self.xy.append([self.xx[i][j], self.yy[i][j]])
					self.x.append(self.xx[i][j])
					self.y.append(self.yy[i][j])
			self.x_arr = []
			for i in range(len(self.depth)):
				self.x_arr.append([self.dist[i], self.depth[i]])
			

		else:
			self.lat = file[lat_n].values
			self.lon = file[lon_n].values
			self.fit_array = []
			for i in range(len(self.lat)):
				self.fit_array.append([self.lat[i], self.lon[i], self.depth[i]])	
			self.x_set = np.linspace(min(self.lat), max(self.lat), self.dimns)
			self.y_set = np.linspace(min(self.lon), max(self.lon), self.dimns)
			self.z_set = np.linspace(min(self.depth), max(self.depth), self.dimns)
			self.xxx, self.yyy, self.zzz = np.meshgrid(self.x_set, self.y_set, self.z_set)
	
	@property 
	def clf(self):
		"""
		Checks to see if the model is fit whenever referenced, and, if not, fits the model

		@rtype: SVR
		@returns: the fit model
		"""

		if self.is_fit == False:  
			if self.dimensions == 2:
				self._clf.fit(self.x_arr, self.user)
			else:
				self._clf.fit(self.fit_array, self.user)
		return self._clf

	def fit(self):
		"""
		Gives access to the fit SVR model (used in model_manager class)
		
		@rtype: SVR
		@returns: the fit SVR model
		"""

		return self.clf
	
	def predict(self):
		"""
		Makes a prediction for interpolated datapoints
		
		@rtype: array-like
		@returns: a list containing the xy coordinates and the predicted values at the interpolation points
		"""

		return ([self.x, self.y, self.clf.predict(self.xy)])
	
	def mse(self):
		"""
		Calculates the mean squared error of the predicted vs actual data at known datapoints
		
		@rtype: float
		@returns: the mean squared error between the predicted vs actual data at known datapoints
		"""

		actual = []
		if self.dimensions == 2:
			for i in range(len(self.dist)):
				actual.append([self.dist[i], self.depth[i]])
			predicted = self.clf.predict(actual)
		else:
			for i in range(len(self.lat)):
				actual.append([self.lat[i], self.lon[i], self.depth[i]])
			predicted = self.clf.predict(actual)
		
		return mean_squared_error(self.user, predicted)
	
	def predict3d(self):
		"""
		Makes a prediction for interpolated datapoints fit to a 3D visualization
		
		@rtype: array-like
		@returns: a list containing the xyz coordinates and the predicted values at the interpolation points
		"""

		x_coordinates = []
		y_coordinates = []
		z_coordinates = []
		xyz_coordinates = []
		for i in range(len(self.xxx)):
			for j in range(len(self.xxx[i])):
				for k in range(len(self.xxx[i][j])):
					x_coordinates.append(self.xxx[i][j][k])
					y_coordinates.append(self.yyy[i][j][k])
					z_coordinates.append(self.zzz[i][j][k])
					xyz_coordinates.append([self.xxx[i][j][k], self.yyy[i][j][k], self.zzz[i][j][k]])
		return ([x_coordinates, y_coordinates, z_coordinates, self.clf.predict(xyz_coordinates)])

