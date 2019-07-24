from abc import ABC, abstractmethod
from processors.drop_close import DropClose
from processors.outlier_removal import OutlierRemoval
from processors.distance_calculator import DistanceCalculator
from processors.step_range import StepRange
from processors.processor import Processor
from data_loaders.csv_loader import CsvLoader
from data_loaders.data_loader import DataLoader  
from models.gpr import GPR
from models.svr import SV
from models.model_manager import ModelManager
from models.model import Model
from visualizers.visualization import Visualization
from visualizers.two_d_vis import TwoDVis
from visualizers.three_d_vis import ThreeDVis
import matplotlib as mpl 
from matplotlib import pyplot as plt
import argparse
import json


def set_defaults():
	"""
	Gives variables default values

	@rtype: tuple
	@returns: a tuple containing key variables for future methods
	"""

	delimiter = ","
	lat = "Latitude"
	lon = "Longitude"
	dep = "Depth"
	range_name = "Current Step"
	tol = 0.0001
	outlier_tol = 3
	range_min = 0
	range_max = 1
	ans = 'n'
	tol_mse = 0.01
	ans1 = 1
	length = 20
	ans2 = 2
	ans3 = 2
	return (delimiter, lat, lon, dep, range_name, tol, outlier_tol, range_min, range_max, ans, tol_mse, ans1, length, ans2, ans3)

def arg_parse_and_json(tup):
	"""
	Parses user-inputted arguments and reads possible json file
	
	@type tup: tuple
	@param tup: the necessary variables for the functions of this method
	@rtype: tuple
	@returns: a tuple containing key variables for future methods
	"""

	parser = argparse.ArgumentParser(description = "This program takes a csv file and displays the data in a useful way.")
	parser.add_argument('--json', '-j', help = "name of json file (default = no file)")
	parser.add_argument('--file', '-f', required = True, help = "name of csv file")
	parser.add_argument('--extra_data', '-e', required = True, help = "name of column of user-selected data")
	parser.add_argument('--delimiter', '-d', help = "delimiter separating the column names in the file (make this first in json file) (default = ',')")
	parser.add_argument('--latitude', '-l', help = "name of latitude column (default = 'Latitude')")
	parser.add_argument('--longitude', '-lo', help = "name of longitude column (default = 'Longitude')")
	parser.add_argument('--depth', '-de', help = "name of depth column (default = 'Depth')")
	parser.add_argument('--current_step', '-c', help = "name of current step column (default = 'Current Step')")
	parser.add_argument('--dist_tol', '-dt', help = "tolerance for points being too close together on chart (default = 0.0001)")
	parser.add_argument('--outlier_tol', '-o', help = "tolerance for outliers (in standard deviations) (default = 3)")
	parser.add_argument('--first', '-fi', help = "first step in range being examined (default = 0)")
	parser.add_argument('--last', '-la', help = "last step in range being examined (default = 1)")
	parser.add_argument('--predictor', '-p', help = "whether or not to use a predictor model to interpolate (default = no)", action = 'store_true')
	parser.add_argument('--mse_tol', '-t', help = "tolerance for MSE (default = 0.01)")
	parser.add_argument('--model', '-m', help = "type of model to preferably use(1(GPR)/2(SVR)) (default = 1)")
	parser.add_argument('--size', '-s', help = "number of points per row/column in the square/cubic grid that represents the model (default = 20)")
	parser.add_argument('--dimension', '-di', help = "dimensions of model (default = 2)")
	parser.add_argument('--plot', '-pl', help = "dimensions of hard data plot (default = 2)")
	args = parser.parse_args()

	file_name = args.file 
	user = args.extra_data

	delimiter = tup[0]
	lat = tup[1] 
	lon = tup[2]
	dep = tup[3]
	range_name = tup[4]
	tol = tup[5]
	outlier_tol = tup[6]
	range_min = tup[7]
	range_max = tup[8]
	ans = tup[9]
	tol_mse = tup[10]
	ans1 = tup[11]
	length = tup[12]
	ans2 = tup[13]
	ans3 = tup[14]

	if args.json != None:
		with open(arg.json) as f:
	  		data = json.load(f)
		json_file = []
		for key, value in data.items():
			json_file.append([key, value])
		for i in range(len(json_file)):
			if jason_file[i][0] == "delimiter":
				delimiter = json_file[i][1]
			elif jason_file[i][0] == "latitude":
				lat = json_file[i][1]
			elif jason_file[i][0] == "longitude":
				lon = json_file[i][1]
			elif jason_file[i][0] == "depth":
				dep = json_file[i][1]
			elif jason_file[i][0] == "current_step":
				range_name = json_file[i][1]
			elif jason_file[i][0] == "dist_tol":
				tol = float(json_file[i][1])
			elif jason_file[i][0] == "outlier_tol":
				outlier_tol = float(json_file[i][1])
			elif jason_file[i][0] == "first":
				range_min = int(json_file[i][1])
			elif jason_file[i][0] == "last":
				range_max = int(json_file[i][1])
			elif jason_file[i][0] == "predictor":
				if bool(jason_file[i][1]) == True:
					ans = 'y'
			elif jason_file[i][0] == "mse_tol":
				tol_mse = float(json_file[i][1])
			elif jason_file[i][0] == "model":
				ans1 = int(json_file[i][1])
			elif jason_file[i][0] == "size":
				length = int(json_file[i][1])
			elif jason_file[i][0] == "dimension":
				ans2 = int(json_file[i][1])
			else:
				ans3 = int(json_file[i][1])
	
	if args.delimiter != None:
		delimiter = args.delimiter
	if args.latitude != None:
		lat = args.latitude
	if args.depth != None:
		dep = args.depth
	if args.current_step != None:
		range_name = args.current_step
	if args.dist_tol != None:
		tol = float(args.dist_tol)
	if args.outlier_tol != None:
		outlier_tol = float(args.outlier_tol)
	if args.first != None:
		range_min = int(args.first)
	if args.last != None:
		range_max = int(args.last)
	if bool(args.predictor) == True:
		ans = 'y'
	if args.mse_tol != None:
		tol_mse = float(args.mse_tol)
	if args.model != None:
		ans1 = int(args.model)
	if args.size != None:
		length = int(args.size)
	if args.dimension != None:
		ans2 = int(args.dimension)
	if args.plot != None:
		ans3 = int(args.plot)

	return (delimiter, lat, lon, dep, range_name, tol, outlier_tol, range_min, range_max, ans, tol_mse, ans1, length, ans2, ans3, user, file_name)

def set_up(tup):
	"""
	Processes and sets up data for models/graphing

	@type tup: tuple
	@param tup: the necessary variables for the functions of this method
	@rtype: tuple
	@returns: a tuple containing key variables for future methods
	"""

	delimiter = tup[0]
	lat = tup[1] 
	lon = tup[2]
	dep = tup[3]
	range_name = tup[4]
	tol = tup[5]
	outlier_tol = tup[6]
	range_min = tup[7]
	range_max = tup[8]
	ans = tup[9]
	tol_mse = tup[10]
	ans1 = tup[11]
	length = tup[12]
	ans2 = tup[13]
	ans3 = tup[14]
	user = tup[15]
	file_name = tup[16]

	file = CsvLoader(name = file_name, delimiter = delimiter)
	read_file = file.load()

	distance = DistanceCalculator(lat_name = lat, long_name = lon, file = read_file)
	distance_arr = distance.process()

	file_ranger = StepRange(step_name = range_name, step_min = range_min, step_max = range_max, file = read_file)
	file_ranged = file_ranger.process()

	close_dropper = DropClose(dep_name = dep, dist_arr = distance_arr, tolerance = tol, file = file_ranged)
	close_dropped = close_dropper.process()

	outlier_remover = OutlierRemoval(tolerance = outlier_tol, user_name = user, file = close_dropped)
	outlier_removed = outlier_remover.process()

	distance = DistanceCalculator(lat_name = lat, long_name = lon, file = outlier_removed)
	distance_arr = distance.process()

	return (lat, lon, dep, ans, tol_mse, ans1, length, ans2, ans3, distance_arr, outlier_removed, user)

def execute_model(tup):
	"""
	Creates a fit model and graphs predicted interpolation data

	@type tup: tuple
	@param tup: the necessary variables for the functions of this method
	@rtype: tuple
	@returns: a tuple containing key variables for future methods
	"""

	lat = tup[0]
	lon = tup[1]
	dep = tup[2]
	ans = tup[3]
	tol_mse = tup[4]
	ans1 = tup[5]
	length = tup[6]
	ans2 = tup[7]
	ans3 = tup[8]
	distance_arr = tup[9]
	outlier_removed = tup[10]
	user = tup[11]


	if ans == "y":

		Gauss = GPR(dist_array = distance_arr, user_name = user, dep_name = dep, length = length, file = outlier_removed, lat_n = lat, lon_n = lon, dims = ans2)
		svr_mod = SV(dist_arr = distance_arr, user_name = user, dep_name = dep, length = length, file = outlier_removed, lat_n = lat, lon_n = lon, dims = ans2)
		if ans1 == 1:
			model_manager = ModelManager(primary = Gauss, secondary = svr_mod, tolerance = tol_mse, dimension = ans2)
			x = model_manager.fit()
		else:
			model_manager = ModelManager(primary = svr_mod, secondary = Gauss, tolerance = tol_mse, dimension = ans2)
			x = model_manager.fit()
		if ans2 == 2:
			gridpoints = model_manager.predict()
			plt.figure()
			cmap = mpl.cm.jet;
			plt.xlabel("Distance (m)")
			plt.ylabel(dep)
			for i in range(len(gridpoints[1])):
				gridpoints[1][i] = gridpoints[1][i] * -1
			cb = plt.colorbar(plt.scatter(gridpoints[0], gridpoints[1], c = gridpoints[2], cmap = cmap))
			cb.set_label(user)
			if len(gridpoints) == 4:
				plt.figure()
				plt.xlabel("Distance (m)")
				plt.ylabel(dep)
				cb1 = plt.colorbar(plt.scatter(gridpoints[0], gridpoints[1], c = gridpoints[3], cmap = cmap))
				cb1.set_label("Variance (" + str(user) + ")")
			plt.show()
		else:
			cmap = mpl.cm.jet
			gridpoints = model_manager.predict()
			fig = plt.figure()
			ax = fig.add_subplot(111, projection = '3d')
			ax.set_xlabel(lat)
			ax.set_ylabel(lon)
			ax.set_zlabel(dep)
			for i in range(len(gridpoints[2])):
				gridpoints[2][i] = gridpoints[2][i] * -1
			cb = plt.colorbar(ax.scatter(gridpoints[0], gridpoints[1], gridpoints[2], c = gridpoints[3], cmap = cmap))
			cb.set_label(user)
			if len(gridpoints) == 5:
				fig1 = plt.figure()
				axis = fig1.add_subplot(111, projection = '3d')
				axis.set_xlabel(lat)
				axis.set_ylabel(lon)
				axis.set_zlabel(dep)
				cb1 = plt.colorbar(axis.scatter(gridpoints[0], gridpoints[1], gridpoints[2], c = gridpoints[4], cmap = cmap))
				cb1.set_label("Variance (" + str(user) + ")")
			plt.show()
		return (lat, lon, dep, ans3, distance_arr, outlier_removed, user)
def plot_data(tup):
	"""
	Plots and shows the hard data

	@type tup: tuple
	@param tup: the necessary variables for the functions of this method
	"""

	lat = tup[0]
	lon = tup[1]
	dep = tup[2]
	ans3 = tup[3]
	distance_arr = tup[4]
	outlier_removed = tup[5]
	user = tup[6]
	if ans3 == 2:
		graph = TwoDVis(dep_name = dep, dist_arr = distance_arr, user_name = user, file = outlier_removed)
		graph.plot()
	else:
		graph = ThreeDVis(dep_name = dep, dist_arr = distance_arr, user_name = user, lat_name = lat, lon_name = lon, file = outlier_removed)
		graph.plot()

def main():
	"""
	Executes all methods in the class
	"""

	a = set_defaults()
	b = arg_parse_and_json(a)
	c = set_up(b)
	d = execute_model(c)
	plot_data(d)

main()