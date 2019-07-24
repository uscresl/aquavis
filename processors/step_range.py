from abc import ABC, abstractmethod
from processors.processor import Processor 


class StepRange:
	def __init__(self, step_name, step_min, step_max, file):
		"""
		Trims the data set to only contain data within the user's desired step range

		@type step_name: str
		@param step_name: the name of the column in the csv file that holds current step data
		@type step_min: int
		@param step_min: the first step in the range to be examined
		@type step_max: int 
		@param step_max: the last step in the range to be examined
		@type file: Pandas DataFrame
		@param file: the pandas dataframe containing the read data from the csv file
		"""

		self.step = file[step_name].values.tolist()
		step_min = int(step_min)
		step_max = int(step_max)
		self.start = self.step.index(step_min)
		if (step_max == max(self.step)):
			self.end = len(self.step) - 1
		else:
			self.end = self.step.index(step_max + 1) - 1
		self.cop = file.copy()

	def process(self):
		"""
		Removes all data that is not within the selected step range

		@rtype: Pandas DataFrame
		@returns: the dataframe containing only the data from the selected step range
		"""

		return (self.cop[self.start:self.end + 1])

