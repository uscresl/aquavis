from abc import ABC, abstractmethod
import numpy as np
import pandas as pd
from processors.processor import Processor


class OutlierRemoval(Processor):
	def __init__(self, tolerance, user_name, file):
		"""
		Removes outliers from the data set with a user-selected tolerance

		@type tolerance: 
		@param tolerance: the user's tolerance for outliers
		@param user_name: the name of the column of the user-selected data in the csv file
		@param file: the pandas dataframe that holds all the data from the csv file 
		"""

		self.tol = float(tolerance)
		self.user = file[user_name].values
		self.new_file = file.copy()
	def process(self):
		"""
		Calculates and removes the oulying points

		@rtype Pandas DataFrame
		@returns: a new pandas dataframes ridden of outliers
		"""

		mean = np.mean(self.user)
		std = np.std(self.user)
		dropped = 0
		for i in range(len(self.user)):
			if np.abs(self.user[i] - mean) > (std*self.tol):
				self.new_file.drop([file.index[i - dropped]])
				dropped += 1
		return self.new_file


