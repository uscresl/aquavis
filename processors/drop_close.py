from abc import ABC, abstractmethod
import numpy as np
import pandas as pd
from processors.processor import Processor


class DropClose(Processor):
	def __init__(self, dep_name, dist_arr, tolerance, file):
		"""
		Drops points from the data set that are problematically close together on the graph

		@type dep_name: str
		@param dep_name: the name of the column that represents depth in the csv file
		@type dist_arr: array-like
		@param dist_arr: the array that contains each point's distance from the original point
		@type tolerance: float
		@param tolerance: the user's tolerance for how close points are allowed to be on the graph
		@type file: Pandas DataFrame
		@param file: the read pandas dataframe that holds all of the data from the csv file 
		"""

		self.depth = file[dep_name].values.tolist()
		self.distance = dist_arr
		self.tol = float(tolerance)
		self.trimmed = file.copy()

	def process(self):
		"""
		Removes points from the dataframe that are too close together (based on the user's tolerance)

		@rtype: Pandas DataFrame
		@returns: the new dataframe ridden of problematic data
		"""

		dropped = 0
		for i in range(len(self.depth)):
			k = 0
			OD = self.distance[i]
			ODP = self.depth[i]
			for j in range(len(self.depth)):
				CD = self.distance[j] - OD
				CDP = self.depth[j] - ODP
				dt = float(np.abs(np.sqrt((CD ** 2) + (CDP ** 2))))
				if i != j and dt < self.tol:
					k += 1
			if k != 0:
				self.trimmed.drop([self.trimmed.index[i - dropped]])
				dropped += 1
		return self.trimmed



