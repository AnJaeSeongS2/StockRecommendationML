#!/usr/bin/python
#-*-coding : utf-8 -*-
from DataReadWriter import DataReader




#머신러닝에 3가지 방법 로지스틱회귀, 랜덤포레스트, SVM사용
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


class Predictors:

	def __init__(self):
		self.dbreader = DataReader()
		
	
	def trainAll(self, time_lags=5, split_ratio= 0.75):
		rows_code = self.dbreader.loadCodes(self.config.get('data_limit'))
		test_result= {'code':[], 'company':[], 'logistic':[], 'rf':[], 'svm':[]}
		index =1
		
		
		for a_row_code in rows_code:
			code = a_row_code[0]
			company = a_row_code[1]
		print "... $s of $s : Training Machine Learning on %s %s" %s (index, len(rows_code), code, company)
		df_dataset = self.makeLaggedDataset(code,self.config.get('start_date'), self.config.get('end_date'), self.config.get('input_column'), self.config.get('output_column'), time_lags=time_lags)
		if df_dataset.shape[0]>0:
			test_result['code'].append(code)
			test_result['company'].append(company)

			X_train,X_test,Y_train,Y_test = self.splitDataset(df_dataset, 'price_date', [self.config.get('input_column')], self.config.get('output_column'), split_ratio)

			for a_clasifier in ['logistic', 'rf', 'svm']:
				predictor = self.createPredictor(a_clasifier)
				self.add(code,a_clasifier,predictor)
				predictor.train(X_train, Y_train)
				score = predictor.score(X_test,Y_test)
				test_result[a_clasifier].append(score)
				print " predictor=%s, score=%s" %(a_clasifier,score)
		index+=1
	df_result = pd.DataFrame(test_result)
	return df_result
	
	#Data (7 days ago~ now)를 이용한 주가방향 예측용 데이터셋 생성
	def makeLaggedDataset(self, code, start_date, enddate, input_column, output_column, time_lags=5):
		return df_dataset
	def splitDataset(self, input_dataset, column, input_column, output_column, split_ratio=0.75):
		return output_dataset

