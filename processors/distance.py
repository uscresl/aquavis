from abc import ABC
import utm 
import numpy as np
from processors.processor import Processor
class Distance(Processor):
	def __init__(self, lat_name, long_name, file):
		self.lat_list = file[lat_name].values#str
		self.lon_list = file[long_name].values#str

	def process(self):
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



