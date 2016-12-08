#-*- coding:utf-8 -*-
#!/usr/bin/python

import pandas as pd
from  DataReadWriter import DataReader
from PortfolioBuilder import PortfolioBuilder
import numpy as np
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


portfolio = PortfolioBuilder()
#해당날짜의 평균회귀 성향 확인
current_date = '2015-11-20'
target_column = 'price_close'
df_mean_reversion = portfolio.doMeanReversionTest('price_close',current_date,100,30)
df_rank = portfolio.rankMeanReversion(df_mean_reversion)
mean_reversion_codes = portfolio.buildUniverse(df_rank,'rank',0.8)
#해당날짜의 평균회귀 성향이 높은 주식들만 방향 예측
mean_reversion_direction = {'date':[],'code':[],'company':[],'direction':[]}
for index in range(len(mean_reversion_codes)):
	mean_reversion_direction['date'].append(current_date)
	mean_reversion_direction['code'].append(mean_reversion_codes['code'].iloc[index])
	mean_reversion_direction['company'].append(mean_reversion_codes['company'].iloc[index])
	mean_reversion_direction['direction'].append(portfolio.determineMeanReversionDirection(mean_reversion_codes['code'].iloc[index], target_column, current_date, verbose=True) )
	
	
	print 'date: %s, code: %s, company: %s, direction: %s'%(mean_reversion_direction.iloc[index]['date'], mean_reversion_direction.iloc[index]['code'], mean_reversion_direction.iloc[index]['company'], mean_reversion_direction.iloc[index]['direction'], )
	



'''
testC = {'2010-01-04':'1234' ,'2011-01-01':'2345', '2013-02-02':'4444'}
df_testC = pd.DataFrame(testC.items() , columns=['code','company'])
print df_testC.loc[0]
print df_testC['2010-01-04']
print df_testC['2010-01-04':'2013-02-03']
'''

#print pd.read_pickle('samsung2.data')['Close'].shift(5)

