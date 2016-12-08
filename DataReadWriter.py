#-*- coding: utf-8 -*-
#!/usr/bin/python
import MySQLdb
import sys
import StockPrice
import datetime
import pandas as pd

class DataReader:
	db = 0
	cursor = 0

	#Naming Mangling 으로 외부에서 파악 불가능하게 함.
	__insCount = 0
		
	def __init__(self):
		DataReader.__insCount +=1
		# 디비 연결
		self.db = MySQLdb.connect("localhost","dev","aA99426383","StockRecommendationML" )
		self.db.set_character_set('utf8')
		# prepare a cursor object 
		self.cursor = self.db.cursor()
		self.cursor.execute('SET NAMES utf8;')
		self.cursor.execute('SET CHARACTER SET utf8;')
		self.cursor.execute('SET character_set_connection=utf8;')
		
	def __del__(self):
		self.db.close()

	def instanceCount(cls):
		print ("DataReader Instance Count : %s" % cls.__insCount)
		return cls.__insCount

	
	#return dataFrame_codes from db
	def loadCodes(self,market_type, limit =0):
		sqlGetCode = "select * from codes"	
		sqlGetCode += " where market_type = %s"%market_type
		if( limit !=0) :
			sqlGetCode += " limit %s;"%limit
		else :
			sqlGetCode += ";"
		self.cursor.execute(sqlGetCode)
		rows = self.cursor.fetchall()
        #self.db.commit()
		seriesCode = pd.Series(name='code')
		seriesCompany = pd.Series(name= 'company')
		
		for a_index in range(0,len(rows)):
			seriesCode = seriesCode.set_value(a_index,rows[a_index][2])
			seriesCompany = seriesCompany.set_value(a_index,rows[a_index][5])
		
		
		#self.db.close()	
		

		return pd.concat([seriesCode,seriesCompany], axis=1)
		
	
	#return dataFrame_prices from db
	def loadPrices(self, code, limit=0):
		sqlGetCode = "select * from prices"	
		sqlGetCode += " where code = %s"%code
		if( limit !=0) :
			sqlGetCode += " limit %s;"%limit
		else :
			sqlGetCode += ";"	
		self.cursor.execute(sqlGetCode)
		rows = self.cursor.fetchall()
        #self.db.commit()
		
		seriesDate = pd.Series(name='date')
		seriesCode = pd.Series(name= 'code')
		seriesOpen = pd.Series(name='price_open')
		seriesClose = pd.Series(name= 'price_close')
		seriesHigh = pd.Series(name='price_high')
		seriesLow = pd.Series(name= 'price_low')
		seriesAdjClose = pd.Series(name='price_adj_close')
		seriesVolume = pd.Series(name= 'volume')

	
		for a_index in range(0,len(rows)):
			seriesDate = seriesDate.set_value(a_index,rows[a_index][2])
			seriesCode = seriesCode.set_value(a_index,rows[a_index][3])
			seriesOpen = seriesOpen.set_value(a_index,rows[a_index][4])
			seriesClose = seriesClose.set_value(a_index,rows[a_index][5])
			seriesLow = seriesLow.set_value(a_index,rows[a_index][6])
			seriesHigh = seriesHigh.set_value(a_index,rows[a_index][7])
			seriesAdjClose = seriesAdjClose.set_value(a_index,rows[a_index][8])
			seriesVolume = seriesVolume.set_value(a_index,rows[a_index][9])
		
		#print seriesCode.to_frame().iloc[0]['code']
		#self.db.close()
	
		return pd.concat([seriesDate, seriesCode, seriesOpen, seriesClose, seriesLow, seriesHigh, seriesAdjClose, seriesVolume], axis=1)
		
		
	



