
'''
ANALYZING THE MEASURED DISPLACEMENT 
RUN : python disp_analysis.py

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

'''
with open(output_file, 'w') as f:
	f.write('x-value' + ',' + 'y-value' + ',' + 'z-value' + ',' + 'timestamp' + ',' + 'travel_mode' + '\n')
	f.close
'''

unique_travel_mode = np.unique(input_df[['travel_mode']].values)
#print unique_travel_mode



for _travel_mode in unique_travel_mode:
	sec = 0
	prev_ts = 0
	_sum = input_df.loc[input_df['travel_mode'] == _travel_mode]['disp(mtr)'].sum()
	#_count = 	input_df.loc[input_df['travel_mode'] == _travel_mode]['disp(mtr)'].count()	
	df_ts =  input_df.loc[input_df['travel_mode'] == _travel_mode]
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
