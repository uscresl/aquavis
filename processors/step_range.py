from abc import ABC, abstractmethod
from processors.processor import Processor 


class StepRange:
	def __init__(self, step_name, step_min, step_max, file):
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
		return (self.cop[self.start:self.end + 1])

