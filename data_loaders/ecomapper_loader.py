from abc import ABC, abstractmethod
import pandas as pd
from data_loaders.data_loader import DataLoader 
class EcomapperLoader(DataLoader):
	def __init__(self, name, delimiter):
		self.nm = name#str
		self.dl = delimiter#str
	def load(self):
		return (pd.read_csv(self.nm, self.dl))
