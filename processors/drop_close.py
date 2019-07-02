from abc import ABC, abstractmethod
import numpy as np
import pandas as pd
from processors.processor import Processor
class DropClose(Processor):
	def __init__(self, dep_name, d, tolerance, file):
		self.dep = file[dep_name].values#array-like
		self.depth = []
		for i in range(len(self.dep)):
			self.depth.append(self.dep[i] * -1)#str
		self.distance = d#array-like
		self.tol = float(tolerance)#float
		self.trimmed = file.copy()#pandas DataFrame
	def process(self):
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



