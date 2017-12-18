# Correction Matrix Plot
import matplotlib.pyplot as plt
import pandas
import numpy
import sys

def real_data(filename):
	#####################################
	# For real distribution
	#####################################
	url = '/home/abhisek/Documents/abhisek-workspace/codes/activity sensor/datasets/distribution_'+filename+'.csv'
	names = ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5', 'Day 6', 'Day 7']
	data = pandas.read_csv(url, names=names)
	correlations = data.corr()
	# plot correlation matrix
	fig = plt.figure()
	ax = fig.add_subplot(111)
	cax = ax.matshow(correlations, vmin=-1, vmax=1)
	fig.colorbar(cax)
	ticks = numpy.arange(0,7,1)
	ax.set_xticks(ticks)
	ax.set_yticks(ticks)
	ax.set_xticklabels(names)
	ax.set_yticklabels(names)
	plt.show()

def simulated_data():
	#####################################
	# For simulated distribution
	#####################################
	url = '/home/abhisek/Documents/abhisek-workspace/codes/activity sensor/datasets/distribution_simulate_irregular.csv'
	names = ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5', 'Day 6', 'Day 7', 'Target Day']
	data = pandas.read_csv(url, names=names)
	correlations = data.corr()
	# plot correlation matrix
	fig = plt.figure()
	ax = fig.add_subplot(111)
	cax = ax.matshow(correlations, vmin=-1, vmax=1)
	fig.colorbar(cax)
	ticks = numpy.arange(0,8,1)
	ax.set_xticks(ticks)
	ax.set_yticks(ticks)
	ax.set_xticklabels(names)
	ax.set_yticklabels(names)
	plt.show()

if __name__ == "__main__":

	if(len(sys.argv)==1):
		simulated_data()		
		print 'Simulated'

	elif(len(sys.argv)==2):
		_date = str(sys.argv[1])
		real_data(_date)


