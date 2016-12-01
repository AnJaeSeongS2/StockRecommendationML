#!/usr/bin/python
#-*- coding: utf-8 -*-

import pandas_datareader.data as web

def downloadStockData(file_name,  code, dateTime1, dateTime2):

	df = web.DataReader("%s.KS" % (code), "yahoo", dateTime1, dateTime2)
	df.to_pickle(file_name)
	return df



