
'''

In this code, I have filtered the real dataset by calculating the mean values of x/y/z-values by grouping them with same timestamp values

Input:
"11.367645","3.2071228","-10.736221","04-09-2017 07:31:29","Dummy shake"
"13.016296","3.7335358","-14.26683","04-09-2017 07:31:29","Dummy shake"
"13.074921","4.1271667","-12.783279","04-09-2017 07:31:29","Dummy shake"
"14.641022","2.5467072","-9.657059","04-09-2017 07:31:29","Dummy shake"
"17.297058","-0.37612915","-4.5639343","04-09-2017 07:31:29","Dummy shake"
"22.89148","-5.385498","-0.78567505","04-09-2017 07:31:29","Dummy shake"
"31.342926","-12.469452","-0.9220581","04-09-2017 07:31:29","Dummy shake"
"34.23584","-25.504364","3.5070496","04-09-2017 07:31:29","Dummy shake"
"24.491074","-27.095581","14.680344","04-09-2017 07:31:29","Dummy shake"
"16.514603","-20.682816","23.671371","04-09-2017 07:31:29","Dummy shake"
"13.315399","-15.648315","32.35971","04-09-2017 07:31:29","Dummy shake"
"11.28389","-12.858292","31.089127","04-09-2017 07:31:29","Dummy shake"
"8.658966","-10.504944","23.606766","04-09-2017 07:31:29","Dummy shake"
"8.658966","-7.748413","14.449432","04-09-2017 07:31:29","Dummy shake"
"6.221878","-7.7579956","14.449432","04-09-2017 07:31:29","Dummy shake"
"11.48848","-14.3789215","6.233673","04-09-2017 07:31:29","Dummy shake"
"21.246414","-12.150009","3.6984863","04-09-2017 07:31:29","Dummy shake"
"25.09047","-10.094574","4.494095","04-09-2017 07:31:29","Dummy shake"
"32.57881","-4.6221924","5.3507233","04-09-2017 07:31:29","Dummy shake"
"29.840225","-6.206238","4.709442","04-09-2017 07:31:29","Dummy shake"
"25.659973","-9.688995","-1.7655334","04-09-2017 07:31:29","Dummy shake"
"24.019684","-8.918503","-10.013596","04-09-2017 07:31:29","Dummy shake"
"23.152298","-5.996872","-11.687363","04-09-2017 07:31:29","Dummy shake"
"21.077713","-4.9069366","-11.001831","04-09-2017 07:31:29","Dummy shake"
"19.00792","-3.4401398","-12.55835","04-09-2017 07:31:29","Dummy shake"
"17.330551","-2.6086273","-12.929245","04-09-2017 07:31:29","Dummy shake"
"16.110214","-2.3837128","-10.79245","04-09-2017 07:31:29","Dummy shake"

Output:
19.0227672593,-8.06714772778,2.14208245741,04-09-2017 07:31:29,Dummy shake

Run : python filter.py 20170904

'''

import pandas as pd
import numpy as np
import sys

#if (len(sys.argv)==''):
#	print 'Run as python filter.py 20170904'


if(len(sys.argv)!=2):
	print 'Run : python filter.py 20170904'	
	sys.exit(0)
	
_date = str(sys.argv[1])
input_df = pd.read_csv('/home/abhisek/Documents/abhisek-workspace/codes/activity sensor/datasets/AccSensor_Data_' + _date + '.csv',delimiter=',')
print input_df.head()
output_file = '/home/abhisek/Documents/abhisek-workspace/codes/activity sensor/datasets/filter_' + _date + '.csv'

with open(output_file, 'w') as f:
	f.write('x-value' + ',' + 'y-value' + ',' + 'z-value' + ',' + 'timestamp' + ',' + 'travel_mode' + '\n')
	f.close

unique_timestamps = np.unique(input_df[['timestamp']].values)
#print unique_timestamps

for _timestamp in unique_timestamps:
	mean_x = input_df.loc[input_df['timestamp'] == _timestamp]['x-value'].median()
	mean_y = input_df.loc[input_df['timestamp'] == _timestamp]['y-value'].median()
	mean_z = input_df.loc[input_df['timestamp'] == _timestamp]['z-value'].median()
	timestamp = _timestamp
	# four spaces provide to get travel mode from following string (first split by \n and then split by 4spaces)
	#"2915    Walk
	#Name: travel-mode, dtype: object"
	travel_mode = str(input_df.loc[input_df['timestamp'] == _timestamp]['travel-mode'].head(1)).split('\n')[0].split('    ')[1]
	with open(output_file, 'a') as f:
		f.write(str(mean_x) + ',' + str(mean_y) + ',' + str(mean_z) + ',' + str(timestamp) + ',' + str(travel_mode) + '\n')
		f.close
		

output_df = pd.read_csv('/home/abhisek/Documents/abhisek-workspace/codes/activity sensor/datasets/filter_' + _date + '.csv',delimiter=',')
print output_df.head()



    # uniquevalues = np.unique(input[['timestamp']].values)
    # print uniquevalues
    # input.loc[input['timestamp']=='04-09-2017 07:31:24']['x-value']
    # input.loc[input['timestamp']=='04-09-2017 07:31:24']['x-value'].mean()
