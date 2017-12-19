
#import pandas as pd
#import numpy as np
#import sys

def difference_bw_timestamps(tsa,tsb):

	ts_a = tsa.split(' ')
	a = str(ts_a[1])
	#print a.split(":")
	a = a.split(":") 

	ts_b = tsb.split(' ')
	b = str(ts_b[1])
	#print b.split(":")
	b = b.split(":")

	sec = 0
	
	if(len(b)==2 and len(a)==2):
		b.append("0")
		a.append("0")

	if(int(b[2]) > int(a[2]) or int(b[2]) == int(a[2])):		
		sec = int(b[2]) - int(a[2])
		#print sec
	elif(int(b[2]) < int(a[2])):
		b[2] = int(b[2]) + 60
		b[1] = int(b[1]) - 1
		sec += int(b[2]) - int(a[2])
		#print sec
	if(int(b[1]) > int(a[1]) or int(b[1]) == int(a[1])):
		sec+= int(b[1])*60 - int(a[1])*60
		#print sec
	elif(int(b[1]) < int(a[1])):
		b[1] = int(b[1]) + 60
		b[0] = int(b[0]) - 1
		sec+= int(b[1])*60 - int(a[1])*60

	return sec

if __name__ == "__main__":
	#tsa is the smaller one, tsb is the bigger one
	tsa = '07-09-2017 10:03:37'
	#tsa = '07-09-2017 09:57:30'
	tsb = '07-09-2017 11:02:05'
	print difference_bw_timestamps(tsa,tsb)
