#-*- coding:utf-8 -*-
#!/usr/bin/python

import pandas as pd
from  DataReadWriter import DataReader, DataWriter
from PortfolioBuilder import PortfolioBuilder
import numpy as np
import time
import datetime
import sys
#Long타입은 아래처럼 datetime으로 변환 가능.
#print datetime.datetime.fromtimestamp(1447977600).strftime('%Y-%m-%d')

start_time = time.time()
try:

	dw = DataWriter()
	dr = DataReader()

	#해당날짜부터  평균회귀 성향 확인후 저장.
	#current_date = raw_input("MeanReversionTest진행할 날짜: xxxx-xx-xx형태 :")
	
	start_date = raw_input("MeanReversionTest를 진행하여, 평균회귀 성향을 확인하고 stockTestedData/에 저장합니다. \n해당 테스트는 1일당 50분정도 소요됩니다.\n진행할 날짜 : xxxx-xx-xx ~ 2016-12-07 . input xxxx-xx-xx :")
	#start_date ="2016-01-11"
	df_price =dr.loadPrices("000020")
	index_date = 0
	for index in range(0, len(df_price)):
		if(df_price['date'][index].strftime("%Y-%m-%d")>= start_date):
			index_date = index
			break
	

	for index in range(index_date,len(df_price)):
		
		current_date = df_price['date'][index].strftime("%Y-%m-%d")	
		end_date = '2016-12-07'
		target_column = 'price_close'
		limit = 0

		
		portfolio = PortfolioBuilder()
	
		try:
			#mean_reversion_test 스킵하려면 아래 파일 불러오기.
			print "load Mean Reversion Test Data from stockTestedData/%s(limit=0).data"%current_date
			df_mean_reversion = pd.read_pickle('stockTestedData/%s(limit=0).data'%current_date)
		except:
			#mean_reversion_test 1일당 50분 가량 소요 ,stockTestedData폴더에 해당 df저장.
			print "file is not exist. \nstart Mean Reversion Test"
			df_mean_reversion, next_date= portfolio.doMeanReversionTest('price_close',current_date,end_date,100,limit)
		
		#ranking mean_reversion score part
		df_rank = portfolio.rankMeanReversion(df_mean_reversion)
		#1300개중 평균회귀 상위 9할만 파악함.
		mean_reversion_codes = portfolio.buildUniverse(df_rank,'rank',0.9)
		
		#create direction of mean_reversion_ Stocks
		#해당날짜의 평균회귀 성향이 높은 주식들만 방향 예측
		mean_reversion_direction = {'price_date':[],'code':[],'company':[],'target_column':[],'direction':[], 'rank_score':[]}

		for index in range(len(mean_reversion_codes)):
			mean_reversion_direction['price_date'].append(current_date)
			mean_reversion_direction['code'].append(mean_reversion_codes['code'].iloc[index])
			mean_reversion_direction['company'].append(mean_reversion_codes['company'].iloc[index])
			mean_reversion_direction['target_column'].append(target_column)
			mean_reversion_direction['direction'].append(portfolio.determineMeanReversionDirection(mean_reversion_codes['code'].iloc[index], target_column, current_date, verbose=True) )
			mean_reversion_direction['rank_score'].append(mean_reversion_codes['rank_score'].iloc[index])


			print 'price_date: %s, code: %s, company: %s, column: %s, direction: %s, rank_score: %s'%(mean_reversion_direction['price_date'][index], mean_reversion_direction['code'][index], mean_reversion_direction['company'][index], mean_reversion_direction['target_column'][index], mean_reversion_direction['direction'][index] , mean_reversion_direction['rank_score'][index])
			
		df_mean_reversion_direction = pd.DataFrame(mean_reversion_direction)
		dw.updateDirectionsToDB(df_mean_reversion_direction)


	
finally:
	end_time = time.time()- start_time
	print "---------------- 수행 시간(초)----------------"
	print end_time

	#print time.strftime("%s시간: %s분 :%s초 소요",round(end_time,0)/3600 , round(end_time,0)/60, round(end_time,0))
