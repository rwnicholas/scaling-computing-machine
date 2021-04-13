#!/usr/bin/python3
import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsClassifier

class KNN():
	'''
	Class to create and retrieve KNN predict
	
	Functions
	----------
	classifier : str
	'''
	data = None
	knn_unit = None

	def __init__(self, fileName, k):
		self.data = pd.read_csv(fileName)
		Y = self.data.segment
		X = self.data.drop('segment', axis=1)
		self.knn_unit = KNeighborsClassifier(k)
		self.knn_unit.fit(X, Y)

	def classifier(self, ncm):
		'''
		Predicts the segment based on ncm.
		
		Parameters
		----------
		ncm : integer
		
		Returns
		-------
		segment : str
		'''
		X_test = np.array([ncm])
		X_test = X_test.reshape(1,-1)
		return self.knn_unit.predict(X_test)
