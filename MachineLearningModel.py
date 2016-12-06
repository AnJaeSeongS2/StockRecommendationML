#!/usr/bin/python
#-*-coding : utf-8 -*-
from DataReadWriter import DataReader
from sklearn import LogisticRegression, RandomForestClassifier
from sklearn.svm import SVC




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
		for a_predictor in ['LR','RF','SVM'] :
			predictor = self.predictor.get(code,a_predictor)
			pred = predictor.predict([current_price])
			pred_prob = predictor.predict([current_price])
			prediction_result += pred[0]

			if prediction_result >1 :
				return LONG
			else :
				return SHORT


class Predictors:

	def __init__(self):
		self.dbreader = DataReader()
		
	
	def trainAll(self, time_lags=5, split_ratio= 0.75):
		rows_code = self.dbreader.loadCodes(self.config.get('data_limit'))
		test_result= {'code':[], 'company':[], 'LR':[], 'RF':[], 'SVM':[]}
		index =1:

		for a_row_code in rows_code:
			code = a_row_code[0]
			company = a_row_code[1]
			print "... $s of $s : Training Machine Learning on %s %s" %s (index, len(rows_code), code, company)
			df_dataset = self.makeLaggedDataset(code,self.config.get('start_date'), self.config.get('end_date'), self.config.get('input_column'), self.config.get('output_column'), time_lags=time_lags)
			if df_dataset.shape[0]>0:
				test_result['code'].append(code)
				test_result['company'].append(company)

				X_train,X_test,Y_train,Y_test = self.splitDataset(df_dataset, 'price_date', [self.config.get('input_column')], self.config.get('output_column'), split_ratio)

				for a_classifier in ['LR', 'RF', 'SVM']:
					predictor = self.createPredictor(a_classifier)
					self.add(code,a_classifier,predictor)
					#predictor.train(X_train, Y_train)
					predictor.fit(X_train, Y_train)
					score = predictor.score(X_test,Y_test)
					test_result[a_classifier].append(score)
					print " predictor=%s, score=%s" %(a_classifier,score)
			index+=1
		df_result = pd.DataFrame(test_result)
		return df_result
	

	def createPredictor( s_classifier):
		if s_classifier=='LR':
			return LogisticRegression()
		if s_classifier=='RF':
			return RandomForestClassifier()
		if s_classifier=='SVM':
			return SVC()
		return 0

	#Data (7 days ago~ now)를 이용한 주가방향 예측용 데이터셋 생성
	def makeLaggedDataset(df, time_lags= 5):
		df_lag = pd.DataFrame(index= df.index)
		df_lag["Close"] = df["Close"]
		df_lag["Volume"] = df["Volume"]
		df_lag["Close_Lag%s" % str(time_lags)] = df["Close"].shift(time_lags)
		#데이터 변화율 퍼센트1
		df_lag["Close_Lag%s_Change" %str(time_lags)] = df_lag["Close_Lag%s"%str(time_lags)].pct_change()*100.0
		df_lag["Close_Direction"] = np.sign(df_lag["Close_lag%s_Change"%str(time_lags)])
		
		
		df_lag["Volume_Lag%s" % str(time_lags)] = df["Volume"].shift(time_lags)
		#데이터 변화율 퍼센트1
		df_lag["Volume_Lag%s_Change" %str(time_lags)] = df_lag["Volume_Lag%s"%str(time_lags)].pct_change()*100.0
		df_lag["Volume_Direction"] = np.sign(df_lag["Volume_lag%s_Change"%str(time_lags)])
		
		#shift해서 lagged데이터를 만들었으니, 누락된 데이터 부분을 제외해서 리턴.
		return df_lag.dropna(how='any')

	def makeLaggedDataset(self, code, start_date, end_date, input_column_array, output_column, time_lags=5):
		return df_dataset
	def splitDataset(self, input_dataset, column, input_column, output_column, split_ratio=0.75):
		#나눌 기준이 될  date구함.
		split_date = getDateByPercent(df, split_ratio)
		
		input_data = df[input_column_array]
		output_data = df[output_column]
		
		X_train = input_data[input_data.index < split_date]
		Y_train = output_data[output_data.index <split_date]
		X_test = input_data[input_data.index >= split_date]
		Y_test = output_data[output_data.index >= split_date]

		return X_train, Y_train, X_test, Y_test
	
	def getDateByPercent(df,percent = 0.75):
		a_index = df.shape[0]* percent
		if( a_index-1 >=0):
			a_index -=1
		return df.index[a_index]


		
		
		
		return output_dataset

