
'''
ANALYZING THE MEASURED DISPLACEMENT 
RUN : python disp_analysis.py date

development under process...

'''

import pandas as pd
import numpy as np
import sys
from diff_of_timestamps	 import *


if(len(sys.argv)==1):
	_date='20170907'
	print 'Default file taken : 20170907'

if(len(sys.argv)==2):
	_date = str(sys.argv[1])

input_df = pd.read_csv('/home/abhisek/Documents/abhisek-workspace/codes/activity sensor/datasets/displacement_' + _date + '.csv',delimiter=',')
#print input_df.head()
output_file = '/home/abhisek/Documents/abhisek-workspace/codes/activity sensor/datasets/disp_analysis_' + _date + '.csv'


input_df_timestamp = input_df[['timestamp']].values
df_dates = np.apply_along_axis(lambda a: (a[0].split(' ')[0]),1,input_df_timestamp)
unique_dates = np.unique(df_dates)

for _a_date in unique_dates :

	print '\n----------- ', _a_date, ' --------------'
	
	df_date_wise_chunk = input_df.loc[input_df['timestamp'].str.contains(_a_date)]
	
	unique_travel_mode = np.unique(df_date_wise_chunk[['travel_mode']].values)
	
	sec = 0
	_sum=0
		
	for _travel_mode in unique_travel_mode:
		sec = 0
		prev_ts = 0
		_sum = df_date_wise_chunk.loc[df_date_wise_chunk['travel_mode'] == _travel_mode]['disp(mtr)'].sum()
		#_count = 	df_date_wise_chunk.loc[df_date_wise_chunk['travel_mode'] == _travel_mode]['disp(mtr)'].count()	
		df_ts =  df_date_wise_chunk.loc[df_date_wise_chunk['travel_mode'] == _travel_mode]
		#print df_ts
	
	
		for row in df_ts.iterrows():
			crnt_ts = row[1]['timestamp']
			#print crnt_ts
			
			if(prev_ts==0):
				sec = 0
			else:
				sec += difference_bw_timestamps(prev_ts,crnt_ts)
			prev_ts = row[1]['timestamp']
					
	
		print 'Today you have been ',_travel_mode , ' for ',sec , ' sec and covered ' , _sum,' mtr'
