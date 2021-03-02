#!/usr/bin/python3
import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsClassifier

class KNN():
	data = None
	knn_unit = None

	def __init__(self, fileName, k):
		self.data = pd.read_csv(fileName)
		Y = self.data.segmento
		X = self.data.drop('segmento', axis=1)
		self.knn_unit = KNeighborsClassifier(k)
		self.knn_unit.fit(X, Y)

	def classifier(self, ncm):
		X_test = np.array([ncm])
		X_test = X_test.reshape(1,-1)
		return self.knn_unit.predict(X_test)
	
def main():
	fileName = "train_NCM.csv"
	# fileName = "partial_eNCM.csv"
	knn = KNN(fileName, 1)

	print(knn.classifier(int(input("NCM: "))))
	# print(input("NCM: ")[0:4])

if __name__ == "__main__":
	main()