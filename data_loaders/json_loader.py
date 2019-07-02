from abc import ABC 
from data_loaders.data_loader import DataLoader
import json

class JsonLoader(DataLoader):
	def __init__(self, file_name):
		self.file = file_name
	def load(self):
		with open(self.file) as f:
  			data = json.load(f)
		r = []
		for key, value in data.items():
			r.append([key, value])
		return r
 

