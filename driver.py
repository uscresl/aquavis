from abc import ABC, abstractmethod
from processors.drop_close import DropClose
from processors.outlier_removal import GaussOutlierRemoval
from processors.distance import Distance
from processors.step_range import StepRange
from processors.processor import Processor
from data_loaders.ecomapper_loader import EcomapperLoader
from data_loaders.data_loader import DataLoader  
from data_loaders.json_loader import JsonLoader
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



parser = argparse.ArgumentParser()
parser.add_argument('--json', '-j', help = "name of json file")
parser.add_argument('--file', '-f', required = True, help = "name of csv file")
parser.add_argument('--extra_data', '-e', required = True, help = "name of column of user-selected data")
parser.add_argument('--delimiter', '-d', help = "delimiter separating the column names in the file (make this first in json file)")
parser.add_argument('--latitude', '-l', help = "name of latitude column")
parser.add_argument('--longitude', '-lo', help = "name of longitude column")
parser.add_argument('--depth', '-de', help = "name of depth column")
parser.add_argument('--current_step', '-c', help = "name of current step column")
parser.add_argument('--dist_tol', '-dt', help = "tolerance for points being too close together on chart")
parser.add_argument('--outlier_tol', '-o', help = "tolerance for outliers (unit same as selected data type)")
parser.add_argument('--first', '-fi', help = "first step in range being examined")
parser.add_argument('--last', '-la', help = "last step in range being examined")
parser.add_argument('--predictor', '-p', help = "whether or not to use a predictor model to interpolate (y/n)")
parser.add_argument('--mse_tol', '-t', help = "tolerance for MSE")
parser.add_argument('--model', '-m', help = "type of model to preferably use(1(GPR)/2(SVR))")
parser.add_argument('--size', '-s', help = "number of points per row/column in the square/cubic grid that represents the model")
parser.add_argument('--dimension', '-di', help = "dimensions of model")
parser.add_argument('--plot', '-pl', help = "dimensions of hard data plot")



args = parser.parse_args()
file_name = args.file 
user = args.extra_data
#file_name = input("What is the name of the file (make sure file is csv and is downloaded)? ")
#user = input("What is the name of the column of the additional data that you would like to examine? ")

delimiter = ","
lat = "Latitude"
lon = "Longitude"
dep = "Depth"
rg_n = "Current Step"
tol = 0.0001
outlier_tol = 7
rg_min = 0
rg_max = 1
ans = "y"
tol_mse = 0.01
ans1 = 1
length = 20
ans2 = 2
ans3 = 2

if args.json != None:
	json_f = JsonLoader(file_name = args.json)
	json_file = json_f.process
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
			rg_n = json_file[i][1]
		elif jason_file[i][0] == "dist_tol":
			tol = json_file[i][1]
		elif jason_file[i][0] == "outlier_tol":
			outlier_tol = json_file[i][1]
		elif jason_file[i][0] == "first":
			rg_min = json_file[i][1]
		elif jason_file[i][0] == "last":
			rg_max = json_file[i][1]
		elif jason_file[i][0] == "predictor":
			ans = json_file[i][1]
		elif jason_file[i][0] == "mse_tol":
			tol_mse = json_file[i][1]
		elif jason_file[i][0] == "model":
			ans1 = json_file[i][1]
		elif jason_file[i][0] == "size":
			length = json_file[i][1]
		elif jason_file[i][0] == "dimension":
			ans2 = json_file[i][1]
		else:
			ans3 = json_file[i][1]

if args.delimiter != None:
	delimiter = args.delimiter
if args.latitude != None:
	lat = args.latitude
if args.depth != None:
	dep = args.depth
if args.current_step != None:
	rg_n = args.current_step
if args.dist_tol != None:
	tol = args.dist_tol
if args.outlier_tol != None:
	outlier_tol = args.outlier_tol
if args.first != None:
	rg_min = args.first
if args.last != None:
	rg_max = args.last
if args.predictor != None:
	ans = args.predictor
if args.mse_tol != None:
	tol_mse = args.mse_tol
if args.model != None:
	ans1 = args.model
if args.size != None:
	length = args.size
if args.dimension != None:
	ans2 = args.dimension
if args.plot != None:
	ans3 = args.plot


file = EcomapperLoader(name = file_name, delimiter = delimiter)
read_file = file.load()

distance = Distance(lat_name = lat, long_name = lon, file = read_file)
distance_arr = distance.process()

file_ranger = StepRange(step_name = rg_n, step_min = rg_min, step_max = rg_max, file = read_file)
file_ranged = file_ranger.process()

close_dropper = DropClose(dep_name = dep, d = distance_arr, tolerance = tol, file = file_ranged)
close_dropped = close_dropper.process()

outlier_remover = GaussOutlierRemoval(tolerance = outlier_tol, user_name = user, file = close_dropped)
outlier_removed = outlier_remover.process()

distance = Distance(lat_name = lat, long_name = lon, file = outlier_removed)
distance_arr = distance.process()

if ans == "y":

	Gauss = GPR(dist_array = distance_arr, user_name = user, dep_name = dep, length = length, file = outlier_removed, lat_n = lat, lon_n = lon)
	svr_mod = SV(dist_arr = distance_arr, user_name = user, dep_name = dep, length = length, file = outlier_removed, lat_n = lat, lon_n = lon)
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
if ans3 == 2:
	graph = TwoDVis(dep_name = dep, dist_arr = distance_arr, user_name = user, file = outlier_removed)
	graph.plot()
else:
	graph = ThreeDVis(dep_name = dep, dist_arr = distance_arr, user_name = user, lat_name = lat, lon_name = lon, file = outlier_removed, )
	graph.plot()
