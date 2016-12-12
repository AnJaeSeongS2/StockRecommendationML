#!/usr/bin/python
#-*- coding: utf-8 -*-

from MeanReversionModel import MeanReversionModel
#from MachineLearningModel import MachineLearningModel
from DataReadWriter import DataReader
import pandas as pd
import numpy as np
import datetime
from pandas.tools.plotting import scatter_matrix, autocorrelation_plot
import matplotlib.pyplot as plt
import sys
import os

class PortfolioBuilder:

	def __init__(self):
		self.dbreader = DataReader()
		self.mean_reversion_model = MeanReversionModel() 
		#시간이 모자라서 머신러닝 파트는  구현 못할 듯.
		#self.machine_learning_model = MachineLearningModel() 
	
	def getIndexsDateTime(self, series_DateTime, dateTime):
		return series_DateTime[series_DateTime == dateTime].index
		


	#평균회귀 성향을 파악하고, 결과냄.
	#column : 원하는 column으로 검사 진행. ex) price_close
	# adf_1,5,10 : 기각값 1,5,10 인 adf
	def doMeanReversionTest(self, column, target_date,end_date,lags_count=100 ,code_count_limit =0):
		#rows_code = self.dbreader.loadCodes(limit = self.config.get('data_limit'))
		rows_code = self.dbreader.loadCodes(market_type = 1, limit= code_count_limit)

		#return해줄 df양식
		test_result = {'code':[],'company':[], 'adf_statistic':[], 'adf_1':[], 'adf_5':[], 'adf_10':[], 'hurst':[], 'halflife':[]}
		a_index = 1

		target_datetime = datetime.datetime.strptime(target_date, "%Y-%m-%d")		
		
		#next_date 변수 변경값 갱신 잘해줘야함.
		next_date ="2016-12-31"
		if(os.path.isfile("stockTestedData/%s(limit=%s).data"%(target_date, code_count_limit))):
			return pd.read_pickle("stockTestedData/%s(limit=%s).data"%(target_date, code_count_limit)), next_date
		else:
			for a_index in range(0,len(rows_code)) :
				code = rows_code.iloc[a_index][0]
				company = rows_code.iloc[a_index][1]
				print "... %s of %s : Testing Mean Reversion Model %s on %s %s " % (a_index, len(rows_code), target_date, code, company)
				a_df = self.dbreader.loadPrices(code)
				target_index = 0
				
				print a_df
				# a_df를 검사를 원하는 날짜 폭으로 df변환.	
				for a in range(len(a_df)):
					if a_df['date'].iloc[target_index] >= target_datetime :
						if a_df['date'].iloc[target_index] >target_datetime:
								target_index-=1
						break
					target_index+=1
				
				if( target_index >= len(a_df)):
					target_index = len(a_df)-1
				a_df = a_df.iloc[0:target_index+1]
			
				print "target_index = %s"%target_index
				a_df_column = a_df[column]
				if(a_index == 0):
					if(target_index+1 < len(a_df)):
						next_date = a_df['date'].iloc[target_index+1]

				#print a_df_column
				if a_df_column.shape[0]>0 :
					try:
						adf_statistic, adf_1, adf_5, adf_10= self.mean_reversion_model.calcADF(a_df_column)	
						hurst = self.mean_reversion_model.calcHurstExponent(a_df_column,lags_count)
						halflife = self.mean_reversion_model.calcHalfLife(a_df_column)
						print "adf_statistic: %s, adf_1기각값: %s, adf_5기각값: %s, adf_10기각값: %s" %(adf_statistic,adf_1,adf_5,adf_10) 
						print "hurst exponent: %s, half life: %s" %(hurst,halflife)
							
						test_result['code'].append(code)
						test_result['company'].append(company)
						test_result['hurst'].append(hurst)
						test_result['halflife'].append(halflife)	
						test_result['adf_statistic'].append(adf_statistic)
						test_result['adf_1'].append(adf_1)
						test_result['adf_5'].append(adf_5)
						test_result['adf_10'].append(adf_10)
					except :
						print "except in MeanReversionModels' calc"
						print sys.exc_info()[0]
				
				a_index+=1
			df_result = pd.DataFrame(test_result)
			df_result.to_pickle("stockTestedData/%s(limit=%s).data"%(target_date, code_count_limit))
			return df_result, next_date

	def determineMeanReversionDirection(self, code, column, row_date, verbose=False):
		df_price = self.dbreader.loadPrices(code)
		print df_price
		return self.mean_reversion_model.determineDirection(df_price,column,row_date,verbose)


	#종목별 적합도 순위표 리턴
	def rankMeanReversion(self,df_mean_reversion):
		df_mean_reversion['rank_adf'] = 0
		df_mean_reversion['rank_hurst'] = 0
		df_mean_reversion['rank_halflife'] = 0

		halflife_percentile = np.percentile(df_mean_reversion['halflife'], np.arange(0,100,2))
		for row_index in range(df_mean_reversion.shape[0]):

			df_mean_reversion.loc[row_index, 'rank_adf'] = self.estimateADF(df_mean_reversion.loc[row_index, 'adf_statistic'], df_mean_reversion.loc[row_index,'adf_1'], df_mean_reversion.loc[row_index, 'adf_5'], df_mean_reversion.loc[row_index, 'adf_10'])

			df_mean_reversion.loc[row_index,'rank_hurst']= self.estimateHurst(df_mean_reversion.loc[row_index, 'hurst'])
			df_mean_reversion.loc[row_index, 'rank_halflife'] = self.estimateHalflife(halflife_percentile, df_mean_reversion.loc[row_index,'halflife'])
			
		df_mean_reversion['rank'] = df_mean_reversion['rank_adf']+ df_mean_reversion['rank_hurst'] + df_mean_reversion['rank_halflife']
		print df_mean_reversion['rank'],df_mean_reversion['rank_adf'], df_mean_reversion['rank_hurst'], df_mean_reversion['rank_halflife']

		return df_mean_reversion

	#적합도 순위 결과로 meanReversion 판정된 주식 목록 리턴  .ex) ratio 0.7 : 순위로 상위70%이상인 주식의 목록 dataframe 반환
	def buildUniverse(self, df_mean_reversion, column, ratio):
		#백분위수 0, 10, ... , 100에 해당하는 column값
		percentile_column = np.percentile(df_mean_reversion[column], np.arange(0,100,10))
		ratio_index = np.trunc(ratio * (len(percentile_column)))
		universe = {}

		#가진 날자 동안 진행.
		for row_index in range(df_mean_reversion.shape[0]) :
			percentile_index = self.getPercentileIndex(percentile_column, df_mean_reversion.loc[row_index,column])
			if percentile_index >= ratio_index:
				universe[df_mean_reversion.loc[row_index,'code']] = df_mean_reversion.loc[row_index,'company']

		return pd.DataFrame(universe.items(), columns=['code','company'])
	
	def getPercentileIndex( self, percentile , target):
		for a_index in range(len(percentile)-1, -1, -1):
			if percentile[a_index]<= target :
				return a_index
		return 0
		
	# estimate함수들은 0~1사이 실수값으로 숫자가 높을 수록 평균회귀 성향이 있음을 나타냄.
	def estimateADF(self, adf_statistic, adf_1, adf_5, adf_10):
		if (adf_statistic < adf_1 or adf_statistic < adf_5 or adf_statistic < adf_10):
			return (adf_statistic/adf_1 + adf_statistic/adf_5 + adf_statistic/adf_10)/4
		else :
			return 0

	def estimateHurst(self, hurst):
		if (hurst <0.5):
			return 1-hurst
		else :
			return 0

	def estimateHalflife(self, percentile, halflife):
		for index in range(len(percentile) ):
			#print "estimateHalflife : %s , halflife : %s, percentile : %s"%(index,halflife,percentile[index])
			if halflife <= percentile[index]:
				return round(float(len(percentile)-index)/len(percentile), 2)	
		
		return 0

	#얼마나 맞췄는지 파악함. 해당 주식의 방향 맞춘다.
	def showHitRatio(self, df_directions, target_column, start_date="2016-01-01", end_date ="2016-12-10"):
		
		count_true = 0
		count_false = 0
		count_all = 0
		print target_column
		print df_directions
		
		df_prices = self.dbreader.loadPrices(df_directions.iloc[0]['code'])
		print df_prices
		date_list = df_directions['price_date'].values.tolist()
		
		print date_list
		#index_list =df_directions['price_date'][df_directions['price_date']== '2015-11-20'].index.tolist()

		for a_date_long in date_list:
			#long타입 날짜 를 변환함.
			a_converted_date_long = a_date_long/1000000000		
			a_datetime =datetime.datetime.fromtimestamp(a_converted_date_long)
			a_date = a_datetime.strftime("%Y-%m-%d")
			do_flag = True;
		
			#make do_flag
			for index in range(0,len(df_prices['date'])):
				if(df_prices['date'].iloc[index] == a_date):
					break;
				if(index == len(df_prices['date'])-1):
					do_flag= False;
			if(do_flag):
				i = df_prices['date'][df_prices['date']== a_date].index.tolist()[0]
				i_direction = df_directions['price_date'][df_directions['price_date']==a_date].index.tolist()[0]
				#print i
				#print df_prices.iloc[i]['date']
				#print i_direction
				
				if df_prices.iloc[i+1][target_column] -df_prices.iloc[i][target_column] > 0 and df_directions.iloc[i_direction]['direction']=='LONG' :
					count_true+=1
				if  df_prices.iloc[i+1][target_column] -df_prices.iloc[i][target_column] <= 0 and df_directions.iloc[i_direction]['direction']=='LONG' :				
					count_false+=1
				if df_prices.iloc[i+1][target_column] -df_prices.iloc[i][target_column] >= 0 and df_directions.iloc[i_direction]['direction']=='SHORT' :
					count_false+=1
				if df_prices.iloc[i+1][target_column] -df_prices.iloc[i][target_column] < 0 and df_directions.iloc[i_direction]['direction']=='SHORT' :
					count_true+=1


		if( count_true+count_false >0):	
		
			print " Correct Ratio: %s, all_count: %s,  code: %s, target_column: %s "%(round(float(count_true)/(count_true+count_false),2) , (count_true+count_false) ,  df_directions.iloc[0]['code'],target_column )
		else :
			print " Correct Ratio: %s, all_count: %s,  code: %s, target_column: %s "%(round(float(count_true)/1,2) , (count_true+count_false) ,  df_directions.iloc[0]['code'],target_column )
		
		return df_directions.iloc[0]['code'], df_directions.iloc[0]['company'], target_column, count_true, count_false, count_all

		#fig = plt.plot()

		#df_price[target_column].plot()
		#plt.show()
		
		#print "show End"
		

'''
			if df_prices.loc[df_directions.iloc[i+1]['price_date']][target_column] -df_prices.loc[df_directions.iloc[i]['price_date']][target_column] > 0 and df_directions.iloc[i][target_column]=='HOLD' :
				count_true+=1
			if df_prices.loc[df_directions.iloc[i+1]['price_date']][target_column] -df_prices.loc[df_directions.iloc[i]['price_date']][target_column] <= 0 and df_directions.iloc[i][target_column]=='HOLD' :
				count_false+=1
			if df_prices.loc[df_directions.iloc[i+1]['price_date']][target_column] -df_prices.loc[df_directions.iloc[i]['price_date']][target_column] >= 0 and df_directions.iloc[i][target_column]=='SHORT' :
				count_false+=1
			if df_prices.loc[df_directions.iloc[i+1]['price_date']][target_column] -df_prices.loc[df_directions.iloc[i]['price_date']][target_column] < 0 and df_directions.iloc[i][target_column]=='SHORT' :
				count_true+=1
'''				

	
		

'''

class MessTrader():
	def setPortfolio(self, portfolio):
		self.protfolio = portfolio

	def add(self, model, code, row_index, position):
		if self.find(code) is None:
			self.items[code] = []

		a_item = TradeItem(model, code, row_index, position)
		self.items[code].append(a_item)

	def dump(self):
		print "----Portfolio.dump----"
		for key in self.items.keys():
			for a_item in self.items[key]:
				print "... model=%s, code=%s, row_index=%s, position=%s" %(a_item.model, a_item.code, a_item.row_index, a_item.position)
			print "----Done----"

'''

