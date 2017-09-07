import pandas as pd
import numpy as np
import sys
import math
_date='20170907'
#_date = str(sys.argv[1])
input_df = pd.read_csv('/home/abhisek/Documents/abhisek-workspace/codes/activity sensor/datasets/filter_' + _date + '.csv',delimiter=',')
print '\n----------------- Input ------------------'	
print input_df.head()
output_file = '/home/abhisek/Documents/abhisek-workspace/codes/activity sensor/datasets/displacement_' + _date + '.csv'


with open(output_file, 'w') as f:
	f.write('x-value' + ',' + 'y-value' + ',' + 'z-value' + ',' + 'timestamp' + ',' + 'travel_mode' + ',' + 'disp(cm)' +  '\n')
	f.close
	
for row in input_df.itertuples():
	x = row[1]
	y = row[2]
	z = row[3]
	#Acceleration is calculated as,
	# a = sqrt(x^2 + y^2 + z^2)
	a = x*x + y*y + z*z
	a_sqrt = a**(0.5)
	#Displacement is calculated as,
	#disp = (u * t) + (0.5 * a * t * t) 	here u=0, t=1s, a = a_sqrt
	disp = 0.5 * a_sqrt * 1 * 1
	with open(output_file, 'a') as f:
		f.write(str(x) + ',' + str(y) + ',' + str(z) + ',' + str(row[4]) + ',' + str(row[5]) + ',' + str(disp) + '\n')
		f.close
	
	

output_df = pd.read_csv('/home/abhisek/Documents/abhisek-workspace/codes/activity sensor/datasets/displacement_' + _date + '.csv',delimiter=',')
print '\n----------------- Output ------------------'	
print output_df.head()
