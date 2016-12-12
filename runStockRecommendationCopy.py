#-*- coding:utf-8 -*-
#!/usr/bin/python

import pandas as pd
from  DataReadWriter import DataReader, DataWriter
from PortfolioBuilder import PortfolioBuilder
import numpy as np
import time
import datetime
import sys

'''
#print pd.read_pickle('samsung2.data')['Close'].pct_change()
df =pd.read_pickle('samsung2.data')
#df =pd.read_pickle('samsung2.data')['Close']
#print df
#print df.index[0]
#print df.shape[0]-1
#print df.index[df.shape[0]-1]
print df['Close'].iloc[0]
print df['Close']
'''



'''

portfoliotest = PortfolioBuilder()
portfoliotest.determineMeanReversionDirection(df,'Close','2015-11-20',True)
'''

'''
def testSplit(df, input_column_array):
	df2 = df[input_column_array]
	print df2
	print df2.index[0]
	print df2.shape[0]

testSplit(df, ["Close","Adj_Close"])


print df.index.get_level_values("Date")
print df.loc["2015-01-05"]
print df.iloc[1]
print df.index.get_level_values("Date")
'''

'''
dr = DataReader()
testcodes =dr.loadCodes(1,10)
print testcodes['code']
for a_index in range(testcodes.shape[0]):
	print testcodes.iloc[a_index]['code']
	print testcodes.iloc[a_index]['company']


testPrices = dr.loadPrices("005110",0)
print testPrices['price_close']

testPercentile = np.percentile( testPrices['price_close'] , np.arange(0,100,10))
print testPercentile
print len(testcodes), len(testPrices)
'''
'''
# test dictionary to dataframe
test_dict = {'a':[], 'b':[]}
test_dict['a'].append(1)
test_dict['b'].append(2)
test_dict['a'].append(11)
test_dict['b'].append(22)
print test_dict
print 'adfadsfadsfadsfdsfasdfkjnasndflandslfnadslfmal;sdmf;aldsmf %s '%test_dict['a'][0]
print pd.DataFrame(test_dict)
'''
#Long타입은 아래처럼 datetime으로 변환 가능.
#print datetime.datetime.fromtimestamp(1447977600).strftime('%Y-%m-%d')

start_time = time.time()
try:

	dw = DataWriter()
	dr = DataReader()

	#해당날짜의 평균회귀 성향 확인
	current_date = '2016-01-04'
	end_date = '2016-12-07'
	target_column = 'price_close'
	limit = 0
	#get index from dataframe with column, value
	#print dr.loadDirectionsByDate(current_date)['price_date'][dr.loadDirectionsByDate(current_date)['price_date'] == '2015-11-20'].index.tolist()[0]

	portfolio = PortfolioBuilder()
	
	
	'''
	#mean_reversion_test part
	print "start Mean Reversion Test"
	#df와 다음날짜 가져옴."
	df_mean_reversion, next_date= portfolio.doMeanReversionTest('price_close',current_date,end_date,100,limit)
	
	#ranking mean_reversion score part
	df_rank = portfolio.rankMeanReversion(df_mean_reversion)
	mean_reversion_codes = portfolio.buildUniverse(df_rank,'rank',0.8)
	
	#create direction of mean_reversion_ Stocks
	#해당날짜의 평균회귀 성향이 높은 주식들만 방향 예측
	mean_reversion_direction = {'price_date':[],'code':[],'company':[],'target_column':[],'direction':[]}

	for index in range(len(mean_reversion_codes)):
		mean_reversion_direction['price_date'].append(current_date)
		mean_reversion_direction['code'].append(mean_reversion_codes['code'].iloc[index])
		mean_reversion_direction['company'].append(mean_reversion_codes['company'].iloc[index])
		mean_reversion_direction['target_column'].append(target_column)
		mean_reversion_direction['direction'].append(portfolio.determineMeanReversionDirection(mean_reversion_codes['code'].iloc[index], target_column, current_date, verbose=True) )

		print 'price_date: %s, code: %s, company: %s, column: %s, direction: %s'%(mean_reversion_direction['price_date'][index], mean_reversion_direction['code'][index], mean_reversion_direction['company'][index], mean_reversion_direction['target_column'][index], mean_reversion_direction['direction'][index] )
	df_mean_reversion_direction = pd.DataFrame(mean_reversion_direction)
	dw.updateDirectionsToDB(df_mean_reversion_direction)
	'''

	#show Hit Ratio and save Correct Ratio, count True,False,All
	codes = dr.loadCodes(1,limit)	
	seriesCode = pd.Series(name= 'code')
	seriesCompany = pd.Series(name='company')
	seriesTargetColumn = pd.Series(name= 'target_column')
	seriesCountTrue = pd.Series(name='count_true')
	seriesCountFalse = pd.Series(name='count_false')
	seriesCountAll = pd.Series(name='count_all')
	for index in range(len(codes)):
		#show Hit Ratio
		df_direction = dr.loadDirectionsByCode(codes.iloc[index]['code'] )
		if (df_direction.empty ==False) :
			c_code, c_company, c_target_column,c_count_true,c_count_false,c_count_all =portfolio.showHitRatio(dr.loadDirectionsByCode(codes.iloc[index]['code']),target_column)
			#맞는 날짜값이 없으면 c_code=0으로 돌려줌	
			if( c_code != 0):
				print c_code
				seriesCode = seriesCode.set_value('code',c_code)
				seriesCompany= seriesCompany.set_value('company',c_company)
				seriesTargetColumn = seriesTargetColumn.set_value('target_column',c_target_column)
				seriesCountTrue = seriesCountTrue.set_value('count_true',c_count_true)
				seriesCountFalse = seriesCountFalse.set_value('count_false',c_count_false)
				seriesCountAll = seriesCountAll.set_value('count_all',c_count_all)
				
	df_count = pd.concat([seriesCode, seriesCompany,seriesTargetColumn, seriesCountTrue, seriesCountFalse, seriesCountAll],axis=1)
	dw.updatePredictionToDB(df_count)
	current_date = next_date



	'''
	testC = {'2010-01-04':'1234' ,'2011-01-01':'2345', '2013-02-02':'4444'}
	df_testC = pd.DataFrame(testC.items() , columns=['code','company'])
	print df_testC.loc[0]
	print df_testC['2010-01-04']
	print df_testC['2010-01-04':'2013-02-03']
	'''

	#print pd.read_pickle('samsung2.data')['Close'].shift(5)

finally:
	end_time = time.time()- start_time
	print "---------------- 수행 시간(초)----------------"
	print end_time

	#print time.strftime("%s시간: %s분 :%s초 소요",round(end_time,0)/3600 , round(end_time,0)/60, round(end_time,0))
