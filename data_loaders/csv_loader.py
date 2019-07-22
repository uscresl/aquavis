from abc import ABC, abstractmethod
import pandas as pd
from data_loaders.data_loader import DataLoader


class CsvLoader(DataLoader):
	def __init__(self, name, delimiter):
		self.name1 = name
		self.delim = delimiter

	def load(self):
		return (pd.read_csv(self.name1, self.delim))
