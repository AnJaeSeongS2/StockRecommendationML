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

	

	#return [Code,Company]
	def loadCodes(self,market_type, limit =0):
		sqlGetCode = "select * from codes"	
		sqlGetCode += " where market_type = %s"%market_type
		if( limit !=0) :
			sqlGetCode += " limit %s;"%limit
		self.cursor.execute(sqlGetCode)
		rows = self.cursor.fetchall()
        #self.db.commit()

		seriesCode = pd.Series(name='code')
		seriesCompany = pd.Series(name= 'company')

		for a_index in range(0,limit):
			seriesCode = seriesCode.set_value(a_index,rows[a_index][2])
			seriesCompany = seriesCompany.set_value(a_index,rows[a_index][5])
	
		#print seriesCode.to_frame().iloc[0]['code']
		#self.db.close()	
		return pd.concat([seriesCode,seriesCompany], axis=1)
		
		
		



