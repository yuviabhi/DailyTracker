import pandas as pd
import numpy as np
import sys

_date='20170907'
#_date = str(sys.argv[1])
input_df = pd.read_csv('/home/abhisek/Documents/abhisek-workspace/codes/activity sensor/datasets/displacement_' + _date + '.csv',delimiter=',')
#print input_df.head()
output_file = '/home/abhisek/Documents/abhisek-workspace/codes/activity sensor/datasets/disp_analysis_' + _date + '.csv'

'''
with open(output_file, 'w') as f:
	f.write('x-value' + ',' + 'y-value' + ',' + 'z-value' + ',' + 'timestamp' + ',' + 'travel_mode' + '\n')
	f.close
'''

unique_travel_mode = np.unique(input_df[['travel_mode']].values)
#print unique_travel_mode


for _travel_mode in unique_travel_mode:
	_sum = input_df.loc[input_df['travel_mode'] == _travel_mode]['disp(cm)'].sum()
	_count = 	input_df.loc[input_df['travel_mode'] == _travel_mode]['disp(cm)'].count()
	print 'Today you have been ',_travel_mode , ' for ',_count , ' sec and covered ' , _sum,' c.m.'
