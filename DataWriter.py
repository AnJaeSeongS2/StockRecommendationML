#!/usr/bin/python
#-*- coding: utf-8 -*-

import MySQLdb
import sys
import StockPrice
import datetime

def updateCodesToDB():
	try:
		# INSERT
		# 디비 연결
		db = MySQLdb.connect("localhost","dev","aA99426383","StockRecommendationML" )
		db.set_character_set('utf8')
		# prepare a cursor object 
		cursor = db.cursor()
		cursor.execute('SET NAMES utf8;')
		cursor.execute('SET CHARACTER SET utf8;')
		cursor.execute('SET character_set_connection=utf8;')

		# download Stock's Code from Koscom
		print "Starting Downloading Stock Codes from Koscom."
		codes =StockCode.StockCode()
		codes.parseCodeHTML(codes.downloadCode(1),1)
		codes.parseCodeHTML(codes.downloadCode(2),2)

		sqlAddCode = """insert into codes (last_update, code, full_code, market_type, company) values (now(),%s,%s,%s,%s)"""
		for key, value in codes.iterItems():
			if( len(key) == 0 ):
				continue
			dataCode = (key, value.full_code,value.market_type, value.company)
			cursor.execute(sqlAddCode, dataCode)	
		db.commit()
		
	finally:
		db.close()


def updatePricesToDB(market_type, dateTime1, dateTime2,start_id = 0):
	try:
		# INSERT
		# 디비 연결
		db = MySQLdb.connect("localhost","dev","aA99426383","StockRecommendationML")
		db.set_character_set('utf8')
		# prepare a cursor object 
		cursor = db.cursor()
		cursor.execute('SET NAMES utf8;')
		cursor.execute('SET CHARACTER SET utf8;')
		cursor.execute('SET character_set_connection=utf8;')


		# downlodat Stock's data from Yahoo
		print "Starting Downloading Stock Data from Yahoo. market_type: %s , %s ~ %s" % (market_type, dateTime1.isoformat() , dateTime2.isoformat() )
		sqlGetCode = "select * from codes"
		sqlGetCode += " where market_type =%s" % (market_type)
		if start_id  >0 :
			sqlGetCode +=" and id >%s" %(start_id)
		cursor.execute(sqlGetCode)
		rows =cursor.fetchall()
		#cursor.beginTrans()
		print len(rows)
		
		index = 1
		for a_row in rows:
			code = a_row[2]
			company = a_row[5]
			#data_count = db.getDataCount(code)
			#if data_count == 0:
			print "... %s of %s : Downloading %s 's data " % (index, len(rows), company)
				
			file_name = 'stockData/(%s)' %(index)
			file_name += a_row[5]
			file_name += ".data"
			print 'filename : %s , company : %s , code : %s' %(file_name, company, code)
			df_data =StockPrice.downloadStockData(file_name, code, dateTime1, dateTime2)
			if df_data is not None:
				#DB로 전송
				for i in range(0,len(df_data.index)):
					if(df_data.Volume[i] != 0): #주식 거래량이 0이 아닌 것만  DB갱신
						sqlAddPrice = """insert into prices (last_update, price_date, code, price_open, price_close, price_low, price_high, price_adj_close, volume) values (now(), %s, %s, %s, %s, %s, %s, %s , %s)"""
						dataPrice = (df_data.index[i].strftime('%Y-%m-%d %H:%M:%S'), a_row[2], df_data.Open[i], df_data.Close[i], df_data.Low[i], df_data.High[i], df_data.iloc[i]['Adj Close'], df_data.Volume[i] )
						cursor.execute(sqlAddPrice, dataPrice)
			# end if df_data is not None
			index+=1
			db.commit()
			print "... %s of %s : %s 's data Committed to DB" % (index, len(rows), company)
		# end for a_row in rows
	
		db.commit()
	finally:
		db.close()
		print "End data Crwaling"
	
