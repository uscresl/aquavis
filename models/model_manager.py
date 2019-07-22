from abc import ABC, abstractmethod
from models.model import Model
from models.gpr import GPR 
from models.svr import SV


class ModelManager(Model):
	def __init__(self, primary, secondary, tolerance, dimension):
		'''
		Manages which model is more fit to graph based on MSE, user preference, and user-selected MSE tolerance
		
		@param primary: the user's preferred type of model
		@param secondary: the user's non-preferred type of model
		@param tolerance: the user's tolerance for MSE
		@param dimension: the user's selected dimensions for the visualization of the model (2D/3D)

		'''
		self.tol = float(tolerance)
		self.pri = primary
		self.sec = secondary
		self.mod = 0
		self.dim = dimension

	def fit(self):
		'''

		Picks the model based on MSE, user preference, and user-selected MSE tolerance
		
		@return the GPR or SVR object fit to the known data 

		'''
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

	def predict(self):
		'''

		Predicts the interpolated data based on the pre-selected model and dimensions

		@return a list that contains all the data needed to graph

		'''
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
		'''
		
		Calculates the mean squared error of the predicted data set vs. the actual data set

		@return the float value of mse

		'''
		if self.mod == 0:
			return self.pri.mse()
		else:
			return self.sec.mse()

