from abc import ABC, abstractmethod
from models.model import Model
from models.gpr import GPR 
from models.svr import SV
class ModelManager(Model):
	def __init__(self, primary, secondary, tolerance, dimension):
		self.tol = float(tolerance)
		self.pri = primary
		self.sec = secondary
		self.mod = 0
		self.dim = dimension
	def fit(self):
		if self.dim == 2:
			if self.pri.mse() > self.tol:
				print ("Your selected model did not fit your selected tolerance. Checking the other model...")
				if self.sec.mse() > self.tol:
					print ("The other model did not fit your selected tolerance either. Using the closest one...")
					dif = self.pri.mse() - self.tol 
					dif1 = self.sec.mse() - self.tol
					if dif <= dif1:
						print ("Your selected model was used")
						return self.pri.fit()
					else:
						print ("The other model was used")
						self.mod += 1
						return self.sec.fit() 
				else:
					print ("The other model fits your selected tolerance. Using the other model...")
					self.mod += 1
					return self.sec.fit()

			else:
				print ("Your selected model fit your selected tolerance.")
				return self.pri.fit()
		else:
			if self.pri.mse3d() > self.tol:
				print ("Your selected model did not fit your selected tolerance. Checking the other model...")
				if self.sec.mse3d() > self.tol:
					print ("The other model did not fit your selected tolerance either. Using the closest one...")
					dif = self.pri.mse3d() - self.tol 
					dif1 = self.sec.mse3d() - self.tol
					if dif <= dif1:
						print ("Your selected model was used")
						return self.pri.fit3d()
					else:
						print ("The other model was used")
						self.mod += 1
						return self.sec.fit3d() 
				else:
					print ("The other model fits your selected tolerance. Using the other model...")
					self.mod += 1
					return self.sec.fit3d()

			else:
				print ("Your selected model fit your selected tolerance.")
				return self.pri.fit3d()
	def predict(self):
		if self.dim == 2:
			if self.mod == 0:
				return self.pri.predict()
			else:
				return self.sec.predict()
		else:
			if self.mod == 0:
				return self.pri.predict3d()
			else:
				return self.sec.predict3d()
	def mse(self):
		if self.dim == 2:
			if self.mod == 0:
				return self.pri.mse()
			else:
				return self.sec.mse()
		else:
			if self.mod == 0:
				return self.pri.mse3d()
			else:
				return self.sec.mse3d()
