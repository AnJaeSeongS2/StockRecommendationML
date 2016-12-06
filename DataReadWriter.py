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

	
	#return df_codes
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
		seriesCode = pd.Series(name='Code')
		seriesCompany = pd.Series(name= 'Company')
		
		a_index = 0
		for row in rows:
			seriesCode = seriesCode.set_value(a_index,rows[a_index][2])
			seriesCompany = seriesCompany.set_value(a_index,rows[a_index][5])
			a_index+=1
		
		#self.db.close()	
		

		return pd.concat([seriesCode,seriesCompany], axis=1)
		
	
	#return df_prices
	def loadPrices(self, code, limit=0):
		sqlGetCode = "select * from prices"	
		sqlGetCode += " where code = %s"%code
		if( limit !=0) :
			sqlGetCode += " limit %s;"%limit
		else :
			sqlGetCode += ";"

		print sqlGetCode
		self.cursor.execute(sqlGetCode)
		rows = self.cursor.fetchall()
        #self.db.commit()
		
		seriesDate = pd.Series(name='Date')
		seriesCode = pd.Series(name= 'Code')
		seriesOpen = pd.Series(name='Open')
		seriesClose = pd.Series(name= 'Close')
		seriesHigh = pd.Series(name='High')
		seriesLow = pd.Series(name= 'Low')
		seriesAdjClose = pd.Series(name='Adj_Close')
		seriesVolume = pd.Series(name= 'Volume')

		a_index = 0
		for row in rows:
			seriesDate = seriesDate.set_value(a_index,rows[a_index][2])
			seriesCode = seriesCode.set_value(a_index,rows[a_index][3])
			seriesOpen = seriesOpen.set_value(a_index,rows[a_index][4])
			seriesClose = seriesClose.set_value(a_index,rows[a_index][5])
			seriesLow = seriesLow.set_value(a_index,rows[a_index][6])
			seriesHigh = seriesHigh.set_value(a_index,rows[a_index][7])
			seriesAdjClose = seriesAdjClose.set_value(a_index,rows[a_index][8])
			seriesVolume = seriesVolume.set_value(a_index,rows[a_index][9])
			a_index+=1
		#print seriesCode.to_frame().iloc[0]['code']
		#self.db.close()	
		return pd.concat([seriesDate, seriesCode, seriesOpen, seriesClose, seriesLow, seriesHigh, seriesAdjClose, seriesVolume], axis=1)
		
		
	



