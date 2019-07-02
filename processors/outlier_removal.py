from abc import ABC, abstractmethod
import numpy as np
import pandas as pd
from processors.processor import Processor
class GaussOutlierRemoval(Processor):
	def __init__(self, tolerance, user_name, file):
		self.tol = float(tolerance)#float
		self.user = file[user_name].values#array-like
		self.new_file = file.copy()
		self.extra_copy = file.copy()
	def process(self):
		mean = np.mean(self.user)
		dropped = 0
		for i in range(len(self.user)):
			if np.abs(self.user[i] - mean) > self.tol:
				self.new_file.drop([self.extra_copy.index[i - dropped]])
				dropped += 1
		return self.new_file


