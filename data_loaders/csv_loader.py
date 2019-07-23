from abc import ABC, abstractmethod
import pandas as pd
from data_loaders.data_loader import DataLoader


class CsvLoader(DataLoader):
	def __init__(self, name, delimiter):
		"""
		Reads the given csv file

		@type name: str
		@param name: the name of the csv file
		@type delimiter: str
		@param delimiter: the delimiter separating the column names in the csv file
		"""

		self.name1 = name
		self.delim = delimiter

	def load(self):
		"""
		Reads the csv file into a dataframe

		@rtype: Pandas DataFrame
		@returns: the pandas dataframe containing the read data from the csv file
		"""

		return (pd.read_csv(self.name1, self.delim))
