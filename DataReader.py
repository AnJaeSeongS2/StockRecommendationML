#-*- coding: utf-8 -*-
#!/usr/bin/python
import MySQLdb
import sys
import StockPrice
import datetime

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
	def loadCodes(self,market_type):
		sqlGetCode = "select * from codes"
		sqlGetCode += "where market_type =%s"%market_type
		self.cursor.execute(sqlGetCode)
		rows = cursor.fetchall()
		self.db.commit()
		print rows[2],rows[5]
		return pd.concat([rows[2],rows[5]], axis=1)
		
		
		



