import sys
import pandas as pd
import numpy as np
import datetime
import calendar




def time_of_day(hour):

	'''
	12-4am - Mid Night (Label 1)
	4-8am - Early Morning (Label 2)
	8am-12pm - Morning (Label 3)
	12-4pm - Afternoon (Label 4)
	4-8pm - Evening (Label 5)
	8pm-12am - Night (Label 6)
	'''
	if(hour >= 0 and hour < 4):
		return 1
	elif(hour >= 4 and hour < 8):
		return 2
	elif(hour >= 8 and hour < 12):
		return 3
	elif(hour >= 12 and hour < 16):
		return 4
	elif(hour >= 16 and hour < 20):
		return 5
	elif(hour >= 20 and hour < 24):
		return 6


def count_letters(word):  return len(filter(lambda x: x not in " ", word))

		
def day_of_week(date):
	'''
	Sun =	0,	Mon =	1,	Tues = 2,	Wed = 3,	Thurs = 4,	Fri = 5,	Sat = 6
	'''
	#when format is 15-10-2017
	if(count_letters(date)==10):
		ts_date = datetime.datetime.strptime(str(date), '%d-%m-%Y')
	#when format is 15-10-17	
	elif(count_letters(date)==8):
		ts_date = datetime.datetime.strptime(str(date), '%d-%m-%y')
	#print ts_date.weekday()
	#print calendar.day_name[ts_date.weekday()]	
	return int(ts_date.weekday()) + 1



def getActivityLabel(act):
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
	if(act == 'Walk'):
		return 1
	elif(act == 'Run'):
		return 2
	elif(act == 'Work-out'):
		return 3
	elif(act == 'Cycling'):
		return 4
	elif(act == 'Biking'):
		return 5
	elif(act == 'Travel by bus/car'):
		return 6
	elif(act == 'Travel by train'):
		return 7
	elif(act == 'Dummy shake'):
		return 8
	elif(act == 'Something else'):
		return 9



def main():		
	if(len(sys.argv)==1):
		_date='20170907'
	print 'Default file taken : 20170907'

	if(len(sys.argv)==2):
		_date = str(sys.argv[1])

	input_df = pd.read_csv('/home/abhisek/Documents/abhisek-workspace/codes/activity sensor/datasets/displacement_' + _date + '.csv',delimiter=',')
	print '\n----------------- Input ------------------'	
	print input_df.head()
	output_file = '/home/abhisek/Documents/abhisek-workspace/codes/activity sensor/datasets/feature_extraction_' + _date + '.csv'

	output_file_labelled = '/home/abhisek/Documents/abhisek-workspace/codes/activity sensor/datasets/labelled_' + _date + '.csv'
	
	fv = []
	feature_vector = np.array([])
	feature_vector.reshape(1,-1)

	label = []
	label_np = np.array([])
	label_np.reshape(1,-1)

	#Creating Feature Vector
	fv.append(['time_of_day','day_of_week','disp','velocity','acc'])
	for row in input_df.itertuples():
		timestamp = row[4]
		timestamp = timestamp.split(" ")
		labelled_day_of_week = day_of_week(timestamp[0])
		time = timestamp[1].split(":")
		hour = int(time[0])
		labelled_time_of_day = time_of_day(hour)
		disp = int(row[6])	
		velocity = int(row[7])
		aggr_acc = int(row[8])
	
		fv.append([labelled_time_of_day , labelled_day_of_week		, disp, velocity, aggr_acc])
		#print labelled_time_of_day , labelled_day_of_week		, disp, velocity, aggr_acc


	#Label extraction from the dataset
	label.append(['activity-label'])
	for row in input_df.itertuples():
		act_label = getActivityLabel(str(row[5]))
		label.append([act_label])

	try :
		feature_vector= np.array([fv])
		#print feature_vector
	
		#write feature-vector into file
		print '\nExtracting feature-vector...'	
		with open(output_file,'w') as f:
			for row in feature_vector:
				np.savetxt(f, row, delimiter=',', fmt='%s')
	
		#read feature-vector from file
		with open(output_file) as f:print f.read()

		#write label-data into file
		print '\nExtracting label-data...'	
		label_np = np.array([label])
		with open(output_file_labelled,'w') as f:
			for row in label_np:
				np.savetxt(f, row, delimiter=',', fmt='%s')

	except Exception,e:
		print str(e)
	
	
if __name__ == "__main__":
	main()

	
	
	
	
	
	
	
	
	
	
