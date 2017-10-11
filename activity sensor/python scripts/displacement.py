
'''
CALCULATING DISPLACEMENT 
RUN : python displacement.py

'''

import pandas as pd
import numpy as np
import sys
import math
from diff_of_timestamps	 import *


if(len(sys.argv)==1):
	_date='20170907'
	print 'Default file taken : 20170907'

if(len(sys.argv)==2):
	_date = str(sys.argv[1])


input_df = pd.read_csv('/home/abhisek/Documents/abhisek-workspace/codes/activity sensor/datasets/filter_' + _date + '.csv',delimiter=',')
print '\n----------------- Input ------------------'	
print input_df.head()
output_file = '/home/abhisek/Documents/abhisek-workspace/codes/activity sensor/datasets/displacement_' + _date + '.csv'


with open(output_file, 'w') as f:
	f.write('x-value' + ',' + 'y-value' + ',' + 'z-value' + ',' + 'timestamp' + ',' + 'travel_mode' + ',' + 'disp(mtr)' + ',' + 'speed(m/s)' + ',' + 'aggr_acc' +  '\n')
	f.close


prev_ts = 0
u = 0
t = 1
for row in input_df.itertuples():
	x = row[1]
	y = row[2]
	z = row[3]
	
	#Current timestamp
	crnt_ts = row[4]
	
	#Acceleration is calculated as, a = sqrt(x^2 + y^2 + z^2)
	a = x*x + y*y + z*z
	a_sqrt = a**(0.5)	

	
	#Updating the velocity as, v = u + ft
	if(prev_ts == 0 or difference_bw_timestamps(prev_ts,crnt_ts) > 60):
		u = 0 
	else:
		u = u + (a_sqrt * t)
		
	#Displacement is calculated as, disp = (u * t) + (0.5 * a * t * t) 	here u=0, t=1s, a = a_sqrt
	disp = (u * t) + 0.5 * a_sqrt * t * t
	
	
	with open(output_file, 'a') as f:
		f.write(str(x) + ',' + str(y) + ',' + str(z) + ',' + str(row[4]) + ',' + str(row[5]) + ',' + str(disp) + ',' + str(u) + ','+ str(a_sqrt) +'\n')
		f.close
	
	prev_ts = row[4]

output_df = pd.read_csv(output_file,delimiter=',')
print '\n----------------- Output ------------------'	
print output_df.head(100)
