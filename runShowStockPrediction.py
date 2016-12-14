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
	# test by file
	#df_count = pd.read_pickle("stockPredictionData201612121506/predictionData.data")
	#df_count = pd.read_pickle("stockPredictionData/predictionData.data")
	
	dr = DataReader()
	df_count =dr.loadTopCountPrediction(limit =0)
	
	count_true =0
	count_all =0 
	money_diff = 0

	start_date = '2016-01-04'
	end_date = '2016-xx-xx'
	
	print"Tatal Prediction Show"
	for index in range(0,len(df_count)):
		
		count_true += df_count['count_true'][index]
		count_all += df_count['count_all'][index]
		money_diff += df_count['money_diff'][index]
		money_total = count_all*100000

	if( count_all != 0):
		print "[%s ~ %s] correct_ratio:%s,  count_true:%s, count_all:%s\n               benefit_ratio:%s, money_diff:%s, money_used:%s"%(start_date,end_date,round(float(count_true)*100/count_all,3) ,count_true, count_all, round(float(money_total+money_diff)/money_total,3), money_diff, money_total)
	else:
		print "[%s ~ %s] correct_ratio:%s,  count_true:%s, count_all:%s\n               benefit_ratio:%s, money_diff:%s, money_used:%s"%(start_date,end_date,0 ,count_true, count_all, round(float(money_total+money_diff)/money_diff,3), money_diff, money_total)
	


	while(1):
		input_date = raw_input('search Recommend Direction By Date. Input Date: (xxxx-xx-xx):')
		df_direction = dr.loadDirectionsByDate(input_date)
		df_direction =df_direction.sort_values(by='rank_score', ascending =False)
		df_direction =df_direction.reset_index(drop ='True')
		#print df_direction
		#df_direction.sort_values(by=['rank_score'],ascending =False)
		print "(하강예측)"
		for index in range(0,len(df_direction)):
			if( df_direction['direction'][index] == 'SHORT'):
				print "rank_score:%s, target_column:%s, code:%s, company:%s"%(df_direction['rank_score'][index],df_direction['target_column'][index],df_direction['code'][index],df_direction['company'][index])
		print "(상승예측)"
		#df_direction.sort_values(by=['rank_score'],ascending =False)
		
		for index in range(0,len(df_direction)):
			if( df_direction['direction'][index] == 'LONG'):
				print "rank_score:%s, target_column:%s, code:%s, company:%s"%(df_direction['rank_score'][index], df_direction['target_column'][index], df_direction['code'][index],df_direction['company'][index])
			
			
	


finally:
	end_time = time.time()- start_time
	print "---------------- 수행 시간(초)----------------"
	print end_time

	#print time.strftime("%s시간: %s분 :%s초 소요",round(end_time,0)/3600 , round(end_time,0)/60, round(end_time,0))
