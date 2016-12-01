#!/usr/bin/python
#-*-coding : utf-8 -*-



class MachineLearningModel:
	#Naming Mangling 으로 외부에서 파악 불가능하게 함.
	__insCount = 0
	window_size = 5	
	threshold = 2
	
	def __init__(self):
		MachineLearningModel.__insCount +=1
	
	def instanceCount(cls):
		print ("MRM Instance Count : %s" % cls.__insCount)
		return cls.__insCount
	
	def calcScore(self, split_ratio=0.75, time_lags =10):
		return self.predictor.trainAll(split_ratio=split_ratio, time_lags= time_lags)

	def determinePosition(self, code, df, column, row_index, verbose=False):
		if( row_index <= df.index[0].strftime("%Y-%m-%d")) :
			return HOLD
		current_price = df.loc[row_index-1,column]
		prediction_result =0
		for a_predictor in ['logistic','rf','svm'] :
			predictor = self.predictor.get(code,a_predictor)
			pred = predictor.predict([current_price])
			pred_prob = predictor.predict([current_price])
			prediction_rewult += pred[0]

			if prediction_result >1 :
				return LONG
			else :
				return SHORT

