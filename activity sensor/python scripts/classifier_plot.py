'''
Plotting the distribution 
RUN : python distribution.py date

development under process...
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

def main():	
	
	if(len(sys.argv)==1):
		_date='20170907'
		print 'Default file taken : 20170907'

	if(len(sys.argv)==2):
		_date = str(sys.argv[1])

	input_df = pd.read_csv('/home/abhisek/Documents/abhisek-workspace/codes/activity sensor/datasets/displacement_' + _date + '.csv',delimiter=',')
	#print input_df.head()
	output_file = '/home/abhisek/Documents/abhisek-workspace/codes/activity sensor/datasets/distribution_' + _date + '.csv'

	#results are taken from path/activity sensor/Results.ods
	x_axis = ['Mean', 'SD','Accuracy', 'Precision', 'F1', 'Recall', 'Jaccard Similarity']

	#######################
	#USER1
	#######################
	knn = [0.560137819734,0.0461159443865,0.760869565217,0.448717948718,0.432098765432,0.416666666667,0.760869565217]
	lsvm = [0.889460740621,0.022388511895,0.913043478261,0.75,0.808333333333,0.952380952381,0.913043478261]
	rbfsvm = [0.702952894147,0.0141950484923,0.913043478261,0.45652173913,0.477272727273,0.5,0.913043478261]
	decTree = [0.906481646544,0.0270188425703,0.978260869565,0.9,0.938420348059,0.988095238095,0.978260869565]
	RFor = [0.918984347568,0.0348957764017,0.934782608696,0.785714285714,0.845117845118,0.964285714286,0.934782608696]
	NeuNet = [0.582532074656,0.169772398409,0.45652173913,0.568965517241,0.409347714432,0.702380952381,0.45652173913]
	ABoost = [0.62462313967,0.111028901752,0.521739130435,0.576923076923,0.455913978495,0.738095238095,0.521739130435]
	NBayes = [0.906719741782,0.0210610919274,0.913043478261,0.75,0.808333333333,0.952380952381,0.913043478261]


	#######################
	#USER2
	#######################
	#knn = [0.8389755519,0.0596000851,0.7419354839,0.7386363636,0.7280701754,0.7243589744,0.7419354839]
	#lsvm = [0.9227422003,0.0423485716,0.935483871,0.95,0.9320175439,0.9230769231,0.935483871]
	#rbfsvm = [0.6264869549,0.006977206,0.5806451613,0.2903225806,0.3673469388,0.5,0.5806451613]
	#decTree = [1,0,1,1,1,1,1]
	#RFor = [0.974461777,0.0332140419,0.935483871,0.95,0.9320175439,0.9230769231,0.935483871]
	#NeuNet = [0.6662333516,0.1699219899,0.4838709677,0.724137931,0.4095238095,0.5555555556,0.4838709677]
	#ABoost = [1,0,1,1,1,1,1]
	#NBayes = [0.8899288451,0.0468803115,0.9032258065,0.90625,0.9028213166,0.9166666667,0.9032258065]



	N = 7
	ind = np.arange(N)  # the x locations for the groups
	width = 0.11       # the width of the bars

	fig = plt.figure()
	ax = plt.subplot(111)
	
	knn = ax.bar(ind, knn, width, color='r')
	lsvm = ax.bar(ind+width, lsvm, width, color='g')
	rbfsvm = ax.bar(ind+width*2, rbfsvm, width, color='b')
	decTree = ax.bar(ind+width*3, decTree, width, color='c')
	RFor = ax.bar(ind+width*4, RFor, width, color='m')
	NeuNet = ax.bar(ind+width*5, NeuNet, width, color='k')
	ABoost = ax.bar(ind+width*6, ABoost, width, color='y')
	NBayes = ax.bar(ind+width*7, NBayes, width, color='#795548')	

	ax.set_ylabel('Activity')
	ax.set_xlabel('Classifiers')
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

	ax.legend(('KNN','Linear SVM','RBF SVM','Decision Tree','Random Forest','Neural Network','AdaBoost','Naive Bayes'))	
	def autolabel(rects):
		for rect in rects:
			h = rect.get_height()
			#ax.text(rect.get_x()+rect.get_width()/2., 1.05*h, '%d'%int(h),
			 #   ha='center', va='bottom')

	autolabel(knn)
	autolabel(lsvm)
	autolabel(rbfsvm)
	autolabel(decTree)
	autolabel(RFor)
	autolabel(NeuNet)
	autolabel(ABoost)
	autolabel(NBayes)

	plt.show()

if __name__ == "__main__":
	main()
