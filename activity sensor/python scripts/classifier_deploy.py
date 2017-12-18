#!/usr/bin/env python 
'''
Classifier deployment
'''

import sys
import pandas as pd
import numpy as np
from sklearn.svm import SVC
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
import sklearn.metrics
from sklearn.cross_validation import train_test_split
import sklearn.model_selection

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 
    
if(len(sys.argv)==1):
	_date='20170907'
	print 'Default file taken : 20170907'

if(len(sys.argv)==2):
	_date = str(sys.argv[1])


######## TRAIN DATA INPUTS	[Model fit by data 20170904. Best Accuracy for RBF SVM]
input_train_features = pd.read_csv('/home/abhisek/Documents/abhisek-workspace/codes/activity sensor/datasets/feature_extraction_' + _date + '.csv',delimiter=',',skiprows=1,header=None)

input_train_labels = pd.read_csv('/home/abhisek/Documents/abhisek-workspace/codes/activity sensor/datasets/labelled_' + _date + '.csv',delimiter=',',skiprows=1,header=None)



######## DEPLOY : TEST DATA INPUTS
_date = '20170904'

input_test_features = pd.read_csv('/home/abhisek/Documents/abhisek-workspace/codes/activity sensor/datasets/feature_extraction_' + _date + '.csv',delimiter=',',skiprows=1,header=None)

input_test_labels = pd.read_csv('/home/abhisek/Documents/abhisek-workspace/codes/activity sensor/datasets/labelled_' + _date + '.csv',delimiter=',',skiprows=1,header=None)


try:

	train_data = input_train_features
	train_labels = input_train_labels
	train_labels = train_labels.values.ravel()
	
	test_data = input_test_features
	test_labels = input_test_labels


	names = ["KNN", "Linear SVM", "RBF SVM","Decision Tree", "Random Forest", "Neural Network", "AdaBoost", "Naive Bayes"]
	
	classifiers = [
		KNeighborsClassifier(3),
		SVC(kernel="linear", C=0.025),
		SVC(gamma=2, C=1),
		DecisionTreeClassifier(max_depth=5),
		RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1),
		MLPClassifier(alpha=1),
		AdaBoostClassifier(),
		GaussianNB()]	

	for name, model in zip(names, classifiers):
	
		print ' '
		print '=========== ',name,' ==========='
		print ' '
		
		#Cross-validation
		Train_data = np.array(train_data)
		Train_labels = np.array(train_labels)
		Train_labels = np.ndarray.flatten(train_labels)
		cv_score = sklearn.model_selection.cross_val_score(model,Train_data, Train_labels, cv=10)	
		print 'Cross-validation : ',cv_score
		print 'Mean : ',cv_score.mean()
		print 'SD : ',cv_score.std()
		
		#Fitting the model
		model.fit(train_data,train_labels)
	
		#Predicting the output
		predicted_labels = model.predict(test_data)
	
		#print 'test labels'	
		#print test_labels
		#print 'predicted labels'
		#print predicted_labels


		#Scores
		accuracy_score = sklearn.metrics.accuracy_score(test_labels,predicted_labels)
		precision_score = sklearn.metrics.precision_score(test_labels,predicted_labels, average='macro')
		f1_score = sklearn.metrics.f1_score(test_labels,predicted_labels, average='macro')
		recall_score = sklearn.metrics.recall_score(test_labels,predicted_labels, average='macro')
		jaccard_similarity_score = sklearn.metrics.jaccard_similarity_score(test_labels, predicted_labels)
		
		print 'Accuracy Score : ',accuracy_score
		print 'Precision Score : ',precision_score	
		print 'F1 Score : ',f1_score
		print 'Recall Score : ',recall_score
		print 'Jaccard Similarity Score : ',jaccard_similarity_score


except Exception,e:
		print str(e)

