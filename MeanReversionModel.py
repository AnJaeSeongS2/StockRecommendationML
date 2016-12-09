#!/usr/bin/python
#-*- coding: utf-8 -*-
import pandas as pd
import statsmodels.tsa.stattools as tsa
import numpy as np
import datetime
HOLD = 'HOLD'
SHORT = 'SHORT'
LONG = 'LONG'
DELETED = "DELETED"

class MeanReversionModel:
	#Naming Mangling 으로 외부에서 파악 불가능하게 함.
	__insCount = 0
	window_size = 5	
	threshold = 1
	
	def __init__(self):
		MeanReversionModel.__insCount +=1
	
	def instanceCount(cls):
		print ("MRM Instance Count : %s" % cls.__insCount)
		return cls.__insCount

	# 평균회기 모델 확인용
	# ADF : Augmented Dickey-Fuller Test
	# df : DataFrame  ex: df_samsung["Close"]
	# return (adf_statistic, adf_critical_values 1,5,10%)
	# Based on MacKinnon (2010) ADF
	def calcADF(self, df):
		adf_result = tsa.adfuller(df)
		critical_values = adf_result[4]
		return adf_result[0], critical_values['1%'], critical_values['5%'], critical_values['10%']

	# 아래calcHurstExpoent2는사용하지 마시오.  수학적 계산상으로 문제가 없는데, 기대 이하의 이상한 값만 나와데서 개발 포기	
	def calcHurstExponent2(self, df, lags_count = 100):
		lags = range(1, lags_count)

		sum1 = 0

		for i in lags :
			sum1 += df[i]

		sum1 = sum1/lags_count
		print 'mean2 %s'%sum1
		mean = np.mean(df)
		print 'mean %s'%mean		
		x = [df[lag] - mean for lag in lags]
		Y = [np.sum(x[:lag+1]) for lag in lags]
		R = np.max(Y) - np.min(Y)
		s = [np.std(df[:(lag+1)]) for lag in lags]
		
		print 'h : '
		print df
		print 'x : '
		print x
		
		for i in lags:
			print '%s %s'% (i, df[i]-mean)
		print 'mean : %s'%mean
		print 'max : %s'%np.max(Y)
		print 'min : %s'%np.min(Y)
		print s
		print np.log(R/s)
		poly = np.polyfit(np.log(lags), np.log(R/s), 1)
		return poly[0]
	
	# 평균회기 모델 확인용
	# I recommend input (n**2) at lags_count
	def calcHurstExponent(self, df, lags_count =100):
		lags = range(1, lags_count)
		ts = np.log(df)
		# calculate array of the variances of the lagged differences	
		tau = [np.sqrt(np.std(np.subtract(ts[lag:], ts[:-lag]))) for lag in lags]
		
		#numpy.polyfit( weight, value, n차방정식) n==1 -> return:  [ 기울기, y절편]
		#print np.log(lags)
		#print 'asdfadsfadsf'
		#print np.log(tau)
		poly = np.polyfit(np.log(lags), np.log(tau), 1)
		result = poly[0]*2.0
		return result
	
	# 평균회기 모델 확인용
	def calcHalfLife(self, df):
		price = pd.Series(df)

		#bfill : shift로 인해 남은 index에 해당하는 값은 이동이전 값으로 매칭 
		lagged_price =price.shift(1).fillna(method = "bfill")
		
		#delta : 시간지남에 따라 변한 값
		delta = price - lagged_price
		
		#beta : polyfit 결과로 1차방정식을 만들어 기울기 값
		beta = np.polyfit(lagged_price, delta, 1)[0]
		half_life = (-1*np.log(2)/beta)
		return half_life

	#row_index : 해당 시점에서의 determine direction
	# 이 함수는 사용하기 앞서 해당 df가 평균회기모델이라고 판단되었을 때만 사용할 것.
	def determineDirection(self, df, column,row_date, verbose=False):
		row_index = 0
		row_datetime = datetime.datetime.strptime(row_date, "%Y-%m-%d")
		
		for a in range(len(df)):
			if df['date'].iloc[row_index] >= row_datetime :
				if df['date'].iloc[row_index] >row_datetime:
						row_index-=1
				break
			row_index+=1
		
		if( row_index >= len(df)):
			row_index = len(df)-1
			return DELETED

		current_price = df.iloc[row_index][column]
			
		#rolling_mean : 이동평균 window: 이동평균 낼 범위 ex window=5 -> 5개의 값으로 계산.
		df_moving_average = df.iloc[0:row_index+1][column].rolling(window= self.window_size).mean()
		df_moving_average_std = df.iloc[0:row_index+1][column].rolling(window= self.window_size).std()
		# nan값 가진 row는 제거
		df_moving_average= df_moving_average[df_moving_average.isnull() != True]
		df_moving_average_std= df_moving_average_std[(df_moving_average_std.isnull()!=True)]
		
		moving_average = df_moving_average.iloc[row_index-self.window_size+1]
		moving_average_std = df_moving_average_std.iloc[row_index-self.window_size+1]
	
		price_arbitrage = current_price - moving_average

		if verbose:
			print "diff=%s, current_price=%s, moving_average=%s, moving_average_std=%s, price_arbitrage=%s"%(price_arbitrage, current_price, moving_average, moving_average_std, price_arbitrage)

		# 현재 위치가 threshold*표준편차 범위 바깥에 있는지 확인. 후에 주가방향예측.. 	
		if abs(price_arbitrage) > moving_average_std*self.threshold:
			if np.sign(price_arbitrage)>0:
				return SHORT
			else :
				return LONG
		return HOLD

