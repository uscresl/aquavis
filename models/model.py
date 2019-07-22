from abc import ABC, abstractmethod


class Model(ABC):
	def fit(self):
		pass

	def predict(self):
		pass
		
	def mse(self):
		pass
