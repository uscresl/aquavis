import numpy as np
import pandas as pd
import utm
import matplotlib as mpl
from matplotlib import pyplot as plt
import math
from mpl_toolkits import mplot3d
import sklearn.gaussian_process
from sklearn.gaussian_process.kernels import RBF, ConstantKernel, Matern
from sklearn.gaussian_process import GaussianProcessRegressor
import statistics
import random
from sklearn import svm

file = pd.read_csv('lawnmower_file', delimiter = ';')

n_rows = 6593
lat = (file["Latitude"]).values
longi = (file["Longitude"]).values

UTM_arr = []

for i in range(n_rows):
	UTM_arr.insert(i, utm.from_latlon(lat[i], longi[i]))

ans = input("""Select a column:
0: Sal ppt
1: pH
2: Chl ug/L
3: Chl RFU
4: BGA - PC cells/mL
5: BGA - PC RFU
6: ODOsat %
7: ODO mg/L
8: Temp C
9: SpCond ms/cm
10: Battery volts
""")
cstep = []
for i in range(n_rows):
	cstep.append((file["Current Step"].values)[i])
ans1 = input("Select step range (0 - 67)(use format 'AB - XY'): ")
start = cstep.index(int(ans1[0:2]))
if ans1[5:7] == "67":
	end = 6592
else:
	end = cstep.index(int(ans1[5:7]) + 1) - 1
n_rows = (end - start + 1)
ans = int(ans)

if ans == 1:
		user = ((file["YSI-pH"]).values)
		name = 'pH'
elif ans == 2:
		user = ((file["YSI-Chl ug/L"]).values)
		name = 'Chl ug/L'
elif ans == 3:
		user = ((file["YSI-Chl RFU"]).values)
		name = 'Chl RFU'
elif ans == 4:
		user = ((file["YSI-BGA-PC cells/mL"]).values)
		name = 'BGA-PC cells/mL'
elif ans == 5:
		user = ((file["YSI-BGA-PC RFU"]).values)
		name = 'BGA-PC RFU'
elif ans == 6:
		user = ((file["YSI-ODOsat %"]).values)
		name = 'ODOsat %'
elif ans == 7:
		user = ((file["YSI-ODO mg/L"]).values)
		name = 'ODO mg/L'
		newZ = []
elif ans == 8:
		user = ((file["YSI-Temp C"]).values)
		name = 'Temp C'
elif ans == 9:
		user = ((file["YSI-SpCond mS/cm"]).values)
		name = 'SpCond mS/cm'
elif ans == 0:
		user = ((file["YSI-Sal ppt"]).values)
		name = 'Sal ppt'
else:
		user = ((file["YSI-Battery volts"]).values)
		name = 'Battery volts'

dep = (file["YSI-Depth feet"]).values
OGE = (UTM_arr[0])[0]
OGN = (UTM_arr[0])[1]
z = []
for i in range(start, end + 1):
	z.append(user[i])
x_coor = []

for i in range(start, end + 1):
	Change_E = (UTM_arr[i])[0] - OGE
	Change_N = (UTM_arr[i])[1] - OGN
	x_coor.append(float(abs(math.sqrt((Change_E ** 2) + (Change_N ** 2)))))
all_x = []
for i in range(6593):
	Change_E = (UTM_arr[i])[0] - OGE
	Change_N = (UTM_arr[i])[1] - OGN
	all_x.append(float(abs(math.sqrt((Change_E ** 2) + (Change_N ** 2)))))
#print (len(all_x))
for i in range (n_rows):

	if dep[i] < 0:
		dep[i] = 0
y = []
for i in range (start, end + 1):
	y.append(dep[i] * -1)

x_set = []
y_set = []
for i in range (start, end + 1):
	x_set.append(((file["Latitude"]).values)[i])
	y_set.append(((file["Longitude"]).values)[i])
ans2 = input("Would you like a 2d or 3d plot (2/3)? ")
if ans2 == "2":
	plt.figure()
	plt.xlabel("distance (m)")
	plt.ylabel("depth (feet)")
	plt.scatter(x_coor, y, c=z)
	axis = plt.scatter(x_coor, y, c = z)
	cb_title = plt.colorbar(axis)
	cb_title.set_label(name)
	plt.show()
else:
	z_set = y
	
	fig = plt.figure()
	ax = fig.add_subplot(111, projection = '3d')
	ax.scatter(x_set, y_set, z_set, c=z, marker = 'o')
	ax.set_xlabel("Latitude (degrees)")
	ax.set_ylabel("Longitude (degrees")
	ax.set_zlabel("Depth (feet)")
	axis = ax.scatter(x_set, y_set, z_set, c=z, marker = 'o')
	cb_title = plt.colorbar(axis)
	cb_title.set_label(name)
	plt.show()

#################################################################################################
#################################################################################################

ans3 = input("Would you like to see a GPR - based model (y/n)? ")
if ans3 == "y":
	ans4 = input("Would you like a 2d or 3d model (2/3)? ")
	if ans4 == "2":
		x_digits = np.linspace(min(x_coor), max(x_coor), 20)
		y_digits = np.linspace(min(y), max(y), 20)

		#print ("Min/Max/mean of user selected data: " + str(min(z)))
		#print (max(z))
		#print (np.mean(z))
		#print (z)

		xx, yy = np.meshgrid(x_digits, y_digits)
		xy_coordinates = []
		x_coordinates = []
		y_coordinates = []
		for i in range(len(xx)):
			for j in range(len(xx[i])):
				xy_coordinates.append([xx[i][j], yy[i][j]])
				x_coordinates.append(xx[i][j])
				y_coordinates.append(yy[i][j])

		x_array = []
		newXY = []
		newZ = []
		for i in range(len(x_coor)):
			x_array.append([x_coor[i], y[i]])
		print ("OG length: " + str(len(x_array)))
		for i in range(len(x_coor)):
			k = 0
			for j in range (len(x_coor)):
				dif_x = float(np.abs(x_coor[i] - x_coor[j]))
				dif_y = float(np.abs(y[i] - y[j]))*3.28084
				dist = float(np.abs(math.sqrt(dif_x ** 2 + dif_y ** 2)))
				if i != j and dist <= 0.001:
					k += 1
			if k == 0:
				newXY.append(x_array[i])
				newZ.append(z[i])
		#print ("Min/Max/Mean of trimmed user selected data (XY/Z): ")
		#print (str(min(newXY)) + "             " + str(min(newZ)))
		#print (str(max(newXY)) + "             " + str(max(newZ)))
		#print (str(np.mean(newXY)) + "             " + str(np.mean(newZ)))
		#print (newZ)
		#print (newXY)

		print ("Length of trimmed array: " + str(len(newXY)))
		gp = GaussianProcessRegressor(normalize_y=True, kernel=Matern()+ConstantKernel())
		gp.fit(newXY, newZ)

		z_digits = gp.predict(xy_coordinates, return_std = True)
		mean = z_digits[0]
		#print ("Min/max/mean of means: " + str(min(mean)))
		#print (max(mean))
		#print (np.mean(mean))
		if min(mean) != max(mean):
			#print (mean)
			variance = z_digits[1]
			for i in range(len(variance)):
				variance[i] = (variance[i] ** 2)
			plt.figure()
			#plt.scatter(x_coor, y, c = z)
			plt.xlabel ("Distance (m)")
			plt.ylabel ("Depth (feet)")
			
			cmap = mpl.cm.jet
			cb = plt.colorbar(plt.scatter(x_coordinates, y_coordinates, c = mean, cmap = cmap))

			cb.set_label("Mean " + name)

			plt.figure()
			plt.xlabel("Distance (m)")
			plt.ylabel("Depth (feet)")

			cb1 = plt.colorbar(plt.scatter(x_coordinates, y_coordinates, c = variance, cmap = cmap))
			cb1.set_label("Variance (" + name + ")")
			plt.show()
		else:
			print ("Problematic data set for Gaussian Process Regressor; using SVR instead (no variance grid will be provided)...")
			clf = svm.SVR(kernel = 'poly', gamma = 'scale')
			clf.fit(newXY, newZ)
			mean = clf.predict(xy_coordinates)
			cmap = mpl.cm.jet
			plt.figure()
			plt.xlabel("Distance (m)")
			plt.ylabel("Depth (feet)")
			plt.scatter (x_coor, y, c = z, cmap = cmap)
			cb = plt.colorbar(plt.scatter(x_coordinates, y_coordinates, c = mean, cmap = cmap))
			cb.set_label ("Mean " + name)
			

			plt.show()
	else:
		x_digits = np.linspace(min(x_set), max(x_set), 10)
		y_digits = np.linspace(min(y_set), max(y_set), 10)
		z_digits = np.linspace(min(y), max(y), 10)

		xx, yy, zz = np.meshgrid(x_digits, y_digits, z_digits)
		xyz_coordinates = []
		x_coordinates = []
		y_coordinates = []
		z_coordinates = []
		for i in range(len(xx)):
			for j in range(len(xx[i])):
				for k in range (len(xx[i][j])):
					xyz_coordinates.append([xx[i][j][k], yy[i][j][k], zz[i][j][k]])
					x_coordinates.append(xx[i][j][k])
					y_coordinates.append(yy[i][j][k])
					z_coordinates.append(zz[i][j][k])
		#print (xyz_coordinates)
		#test_arr = []
		#for i in range(len(xyz_coordinates)):
			#test_arr.append(xyz_coordinates[i])
		#print (test_arr)
		x_array = []
		for i in range (len(x_set)):
			x_array.append([x_set[i], y_set[i], y[i]])
		gp = GaussianProcessRegressor(normalize_y=True, kernel=Matern()+ConstantKernel(), alpha = 0.0001)
		gp.fit(x_array, z)



		z_nums = gp.predict(xyz_coordinates, return_std = True)

		mean = z_nums[0]
		#print (mean)
		#test_mean = []
		#for i in range(len(mean)):
			#test_mean.append(mean[i])
		#print (test_mean)
		variance = z_nums[1]
		for i in range(len(variance)):
			variance[i] = variance[i] ** 2
		cmap = mpl.cm.jet
		fig1 = plt.figure()
		axis = fig1.add_subplot(111, projection = '3d')
		axis.set_xlabel ("Latitude (degrees)")
		axis.set_ylabel ("Longitude (degrees)")
		axis.set_zlabel ("Depth (feet)")

		cb = plt.colorbar(axis.scatter(x_coordinates, y_coordinates, z_coordinates, c = mean, cmap = cmap))
		cb.set_label("Mean " + name)
		plt.show()
		fig2 = plt.figure()
		ax2 = fig2.add_subplot (111, projection = '3d')
		ax2.set_xlabel("Latitude (degrees)")
		ax2.set_ylabel("Longitude (degrees)")
		ax2.set_zlabel("Depth (feet)")
		cb1 = plt.colorbar(ax2.scatter(x_coordinates, y_coordinates, z_coordinates, c = variance, cmap = cmap))
		cb1.set_label("Variance (" + name + ")")
		plt.show()

#xx and yy have the set 20 x 20 dimensions, so z_digits is not compatible, since it is based on 
#the length of the user selected data - z_digits roots from the length of 
#2nd graph - mean (predicted value) determines color
#3rd graph - variants determine color
#maybe calculate mean of each of 400 arrays, and variant of each of 400 values - variance is just 
#sqrt of standard deviation but there might just be a method for it built into python, 
#numpy, or scikit-learn#numpy, or scikit-learn  