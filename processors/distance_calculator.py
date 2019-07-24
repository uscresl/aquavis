from abc import ABC
import utm 
import numpy as np
from processors.processor import Processor


class DistanceCalculator(Processor):
	def __init__(self, lat_name, long_name, file):
		"""
		Calculates the distance from the original point to each of the other points based on longitude and latitude
	
		@type lat_name: str
		@param lat_name: the name of the latitude column in the csv file
		@type long_name: str
		@param long_name: the name of the longitude column in the csv file
		@type Pandas DataFrame
		@param file: the pandas dataframe that holds all of the read data from the csv file
		"""

		self.lat_list = file[lat_name].values
		self.lon_list = file[long_name].values

	def process(self):
		"""
		Uses latitude and longitude data to calculate the distance from the first point to the others

		@rtype: array_like
		@returns: the array containing each point's distance from the first point, to be used for graphing 
		"""

		utm_arr = []
		for i in range(len(self.lat_list)):
			utm_arr.append(utm.from_latlon(self.lat_list[i], self.lon_list[i]))
		NEdist = []
		for i in range(len(utm_arr)):
			NEdist.append([(utm_arr[i])[0], (utm_arr[i])[1]])
		OE = NEdist[0][0]
		ON = NEdist[0][1]
		dist = []
		for i in range(len(NEdist)):
			CE = np.abs(NEdist[i][0] - OE)
			CN = np.abs(NEdist[i][1] - ON)
			dist.append(float(np.abs(np.sqrt((CE ** 2) + (CN ** 2)))))
		return dist



