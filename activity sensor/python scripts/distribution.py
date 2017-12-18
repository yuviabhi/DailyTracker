
'''
Plotting the distribution 
RUN : python distribution.py date



'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import date2num
from matplotlib.ticker import FuncFormatter
import datetime
import scipy.stats  as stats
import sys
from diff_of_timestamps	 import *
from feature_extraction import *



def divide_each_element_by_max(walk_axis,run_axis,workout_axis,cycle_axis,biking_axis,bus_car_axis,train_axis,dummy_shake_axis,somethingelse_axis):
	max_no = np.amax(walk_axis)
	max_no = max_no + np.amax(run_axis)
	max_no = max_no + np.amax(workout_axis)
	max_no = max_no + np.amax(cycle_axis)
	max_no = max_no + np.amax(biking_axis)
	max_no = max_no + np.amax(bus_car_axis)
	max_no = max_no + np.amax(train_axis)
	max_no = max_no + np.amax(dummy_shake_axis)
	max_no = max_no + np.amax(somethingelse_axis)
	
	print max_no
	if(max_no !=0):
		walk_axis[:] = [x / float(max_no) for x in walk_axis]
		run_axis[:] = [x / float(max_no) for x in run_axis]
		workout_axis[:] = [x / float(max_no) for x in workout_axis]
		cycle_axis[:] = [x / float(max_no) for x in cycle_axis]
		biking_axis[:] = [x / float(max_no) for x in biking_axis]
		bus_car_axis[:] = [x / float(max_no) for x in bus_car_axis]
		train_axis[:] = [x / float(max_no) for x in train_axis]
		dummy_shake_axis[:] = [x / float(max_no) for x in dummy_shake_axis]
		somethingelse_axis[:] = [x / float(max_no) for x in somethingelse_axis]
	#print arr
	#return arr
	
	
	
def main():	
	
	if(len(sys.argv)==1):
		_date='20170907'
		print 'Default file taken : 20170907'

	if(len(sys.argv)==2):
		_date = str(sys.argv[1])

	input_df = pd.read_csv('/home/abhisek/Documents/abhisek-workspace/codes/activity sensor/datasets/displacement_' + _date + '.csv',delimiter=',')
	#print input_df.head()
	output_file = '/home/abhisek/Documents/abhisek-workspace/codes/activity sensor/datasets/distribution_' + _date + '.csv'



	#
	##################################
	#	
	#fair_coin_flips = stats.binom.rvs(n=10,        # Number of flips per trial
	#                                p=0.5,       # Success probability
	#                                size=10000)  # Number of trials
	#                                
	#unfair_coin_flips = stats.binom.rvs(n=10,        # Number of flips per trial
	#	                              p=0.9,       # Success probability
	#	                              size=10000)  # Number of trials
	#print fair_coin_flips
	#print(pd.crosstab(index="counts", columns= fair_coin_flips))	
	#pd.DataFrame(fair_coin_flips,unfair_coin_flips).hist(range=(-0.5,10.5), bins=11)
	#
	##################################
	#
	#x = [datetime.datetime(2011, 1, 4, 0, 0),
	#datetime.datetime(2011, 1, 5, 0, 0),
	#datetime.datetime(2011, 1, 6, 0, 0)]
	#print x
	#x = date2num(x)	
	#print x
	#y = [4, 9, 2]
	#z = [1,2,3]
	#k = [11,12,13]
	#ax = plt.subplot(111)
	#w = 0.3
	#ax.bar(x-w, y,width=w,color='b',align='center')
	#ax.bar(x, z,width=w,color='g',align='center')
	#ax.bar(x+w, k,width=w,color='r',align='center')
	#ax.xaxis_date()
	#ax.autoscale(tight=True)	
	#plt.show()
	#
	##################################
	
	x_axis = []
	walk_axis = []
	run_axis = []
	workout_axis = []
	cycle_axis = []
	biking_axis = []
	bus_car_axis = []
	train_axis = []
	dummy_shake_axis = []
	somethingelse_axis = []
	
	day=0
	
	input_df_timestamp = input_df[['timestamp']].values
	df_dates = np.apply_along_axis(lambda a: (a[0].split(' ')[0]),1,input_df_timestamp)
	unique_dates = np.unique(df_dates)
	
	for _a_date in unique_dates :

		day = day + 1
		#print '\n----------- ', _a_date, ' --------------'
	
		df_date_wise_chunk = input_df.loc[input_df['timestamp'].str.contains(_a_date)]
	
		'''
		Walk = 1
		Run = 2
		Work-out = 3
		Cycling = 4
		Biking = 5
		Travel by bus/car = 6
		Travel by train = 7
		Dummy shake = 8
		Something else = 9
		'''
		
		count_walk = 0
		count_run = 0
		count_workout = 0
		count_cycling = 0
		count_biking = 0
		count_bus_car = 0
		count_train = 0
		count_dummy_shake = 0
		count_something_else = 0

	
		for row in df_date_wise_chunk.itertuples():
			#timestamp = row[4]
			#timestamp = timestamp.split(" ")
			#date = timestamp[0]
			#time = timestamp[1].split(":")
			#hour = int(time[0])
			#labelled_time_of_day = time_of_day(hour)
			#print labelled_time_of_day
		
		
			activity = getActivityLabel(row[5])
		
			if(activity==1):
				count_walk = count_walk + 1 
			elif(activity==2):
				count_run = count_run + 1
			elif(activity==3):
				count_workout = count_workout + 1
			elif(activity==4):
				count_cycling = count_cycling + 1	
			elif(activity==5):
				count_biking = count_biking + 1
			elif(activity==6):
				count_bus_car = count_bus_car + 1
			elif(activity==7):
				count_train = count_train + 1
			elif(activity==8):
				count_dummy_shake = count_dummy_shake + 1
			elif(activity==9):
				count_something_else = count_something_else + 1
				
		x_axis.append(day)
		walk_axis.append(count_walk)
		run_axis.append(count_run)
		workout_axis.append(count_workout)
		cycle_axis.append(count_cycling)
		biking_axis.append(count_biking)
		bus_car_axis.append(count_bus_car)
		train_axis.append(count_train)
		dummy_shake_axis.append(count_dummy_shake)
		somethingelse_axis.append(count_something_else)
		
	print x_axis
	print walk_axis
	print run_axis 
	print workout_axis 
	print cycle_axis 
	print biking_axis
	print bus_car_axis
	print train_axis
	print dummy_shake_axis
	print somethingelse_axis
	
	divide_each_element_by_max(walk_axis,run_axis,workout_axis,cycle_axis,biking_axis,bus_car_axis,train_axis,dummy_shake_axis,somethingelse_axis)
	
	print 'Write all arrays to a file'
	a = np.asarray([ walk_axis, run_axis, workout_axis, cycle_axis,biking_axis,bus_car_axis,train_axis,dummy_shake_axis,somethingelse_axis ])
	np.savetxt(output_file, a, delimiter=',')
	
	N = day
	ind = np.arange(N)  # the x locations for the groups
	width = 0.11       # the width of the bars

	fig = plt.figure()
	ax = plt.subplot(111)
	
	rects_walk = ax.bar(ind, walk_axis, width, color='r')
	rects_run = ax.bar(ind+width, run_axis, width, color='g')
	rects_workout = ax.bar(ind+width*2, workout_axis, width, color='b')
	rects_cycle = ax.bar(ind+width*3, cycle_axis, width, color='c')
	rects_bike = ax.bar(ind+width*4, biking_axis, width, color='m')
	rects_buscar = ax.bar(ind+width*5, bus_car_axis, width, color='w')
	rects_train = ax.bar(ind+width*6, train_axis, width, color='k')
	rects_dummy = ax.bar(ind+width*7, dummy_shake_axis, width, color='y')
	rects_somethingelse = ax.bar(ind+width*8, somethingelse_axis, width, color='#795548')

	ax.set_ylabel('Activity')
	ax.set_xlabel('Day')
	ax.set_xticks(ind+width)
	ax.set_xticklabels( x_axis )
	ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.0%}'.format(y)))

	# Shrink current axis's height by 10% on the bottom
	box = ax.get_position()
	ax.set_position([box.x0, box.y0 + box.height * 0.1,
		           box.width, box.height * 0.9])

	# Put a legend below current axis
	ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
		    fancybox=True, shadow=True, ncol=7)

	ax.legend(('Walking', 'Running','Work-out', 'Cycling', 'Biking', 'Bus/Car', 'Train', 'Dummy', 'Something else'))	

	def autolabel(rects):
		for rect in rects:
			h = rect.get_height()
			#ax.text(rect.get_x()+rect.get_width()/2., 1.05*h, '%d'%int(h),
			 #   ha='center', va='bottom')

	autolabel(rects_walk)
	autolabel(rects_run)
	autolabel(rects_workout)
	autolabel(rects_cycle)
	autolabel(rects_bike)
	autolabel(rects_buscar)
	autolabel(rects_train)
	autolabel(rects_dummy)
	autolabel(rects_somethingelse)

	plt.show()

if __name__ == "__main__":
	main()
