#-*- coding: utf-8 -*-
import pandas as pd
import pandas_datareader.data as web
import datetime
import matplotlib.pyplot as plt
from  pandas.tools.plotting import scatter_matrix, autocorrelation_plot
import numpy as np	
import statsmodels.tsa.stattools as tsa
import pprint

def download_stock_data(file_name, company_code, year1, month1, date1, year2, month2, date2):
	start = datetime.datetime(year1,month1,date1)
	end = datetime.datetime(year2,month2,date2)
	df = web.DataReader("%s.KS" % (company_code), "yahoo", start, end)
	df.to_pickle(file_name)
	return df

def load_stock_data(file_name):
	df = pd.read_pickle(file_name)
	return df


def describe_stock_data(file_name):
	df = load_stock_data(file_name)
	print df.describe()


def show_quantile(file_name):
	df = load_stock_data(file_name)
	print df.quantile([0.25,0.5,0.75])

def show_histogram(file_name, value):
	df = load_stock_data(file_name)
	(n, bins, patched) = plt.hist(df[value])
	plt.axvline(df[value].mean(), color = 'red')
	plt.show()


	
def show_scatter_matrix(file_name):
	df = load_stock_data(file_name)
	scatter_matrix(df[['Open','High','Low','Close']], alpha= 0.2, figsize= (6,6), diagonal = 'kde')
	plt.show()

def show_box(file_name):
	df = load_stock_data(file_name)
	df[['Open','High','Low','Close','Adj Close']].plot(kind='box')
	plt.show()

# value : Open / Close / Adj Close / Volume ~
def print_covariance(file1,file2, value):
	df1= load_stock_data(file1)
	df2 = load_stock_data(file2)
	print df1[value].cov(df2[value])

def print_correlation(file1,file2, value):
	df1= load_stock_data(file1)
	df2 = load_stock_data(file2)
	print df1[value].corr(df2[value])
	
def show_autocorr(file_name,value):
	df = load_stock_data(file_name)
	fig , axs = plt.subplots(2,1)
	df[value].plot(ax=axs[0])
	autocorrelation_plot(df[value], ax= axs[1])
	plt.show()

def get_autocorr_dataframe(series):
	def r(h):
		return ((data[:n -h] -mean) * (data[h:]-mean)).sum() /float(n) /c0
	n = len(series)
	data = np.asarray(series)
	mean == np.mean(data)
	c0= np.sum((data-mean) **2) /float(n)
	x = np.arange(n) +1
	y = lmap(r,x)
	df = pd.DataFrame(y, index=x)
	return df

def show_correlogram(file_name, value):
	df = load_stock_data(file_name)
	df_autocorr_frame = get_autocorr_dataframe(df[value])
	fig, axs = plt.subplots(2,1)
	axs[1].xaxis.set_visible(False)
	df[value].plot(ax=axs[0])
	df_autocorr_frame[0].plot(kind='bar', ax= axs[1])
	plt.show()

def pprint_adf(file_name,value):
	df = load_stock_data(file_name)
	adf_result = tsa.adfuller(df[value])
	pprint.pprint(adf_result)


def get_hurst_exponent(df):
	lags = range(2,100)
	ts = np.log(df)
	tau = [np.sqrt(np.std(np.subtract(ts[lag:], ts[:-lag]))) for lag in lags]
	poly = np.polyfit(np.log(lags), np.log(tau), 1)
	result = poly[0]*2.0

	return result

def print_hurst_exponent(file1,file2,value):
	df1 = load_stock_data(file1)
	df2 = load_stock_data(file2)
	hurst1 = get_hurst_exponent(df1[value])
	hurst2 = get_hurst_exponent(df2[value])
	print "Hurst Exponent : ", file1 , "%s "%hurst1 , file2, "%s "%hurst2 


def make_dataset( df, time_lags =5):
	df_lag = pd.DataFrame(index=df.index)
	df_lag["Close"] = df["Close"]
	df_lag["Volume"] = df["Volume"]
	df_lag["Close_Lag%s" % str(time_lags)] =df["Close"].shift(time_lags)
	df_lag["Close_Lag%s_Change" % str(time_lags)] = df_lag["Close_Lag%s" % str(time_lags)]pct_change() *100.0
	df_lag["Volume_Lag%s" % str(time_lags)] = df["Volume"].shift(time_lags)
	df_lag["Volume_Lag%s_Change" % str(time_lags)] = df_lag["Volume_Lag%s" % str(time_lags)].pct_change() *100.0

	df_lag["Close_Direction"] = np.sign(df_lag["Close_Lag%s_Change"% str(time_lags)])
	df_lag["Volume_Direction"] = np.sign(df_lag["Volume_Lag%s_Change" % str(time_lags)])

	return df_lag.dropna(how='any')
