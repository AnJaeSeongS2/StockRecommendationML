#!/usr/bin/python
#-*- coding: utf-8 -*-
import BeautifulSoup
import requests
import pandas_datareader.data as web
from pandas_datareader._utils import RemoteDataError



#Item자체가 가지는 4가지 속성을 가짐
# market_type(marketBit) : 주식종목 1==거래소 2==코스닥 , code : 6자리주식코드 , full_code : 12자리주식코드 company : 회사이름
class StockCodeItem:
	def __init__(self, market_type, code, full_code , company):
		self.market_type = market_type
		self.code = code
		self.full_code = full_code
		self.company = company


#StockCode를 관리해줄 클래스
class StockCode:
	def __init__(self):
		self.items = {}
	
	def countItems(self):
		return len(self.items)

	def clearAll(self):
		self.items.clear()
	
	def addItem(self,market_type, code, full_code, company):
		a_item = StockCodeItem(market_type, code, full_code, company)
		self.items[code] = a_item
		
	def getItem(self, code):
		return self.items[code]

	def removeItem(self, code):
		del self.items[code]

	def iterItems(self):
		return self.items.iteritems()

	def dumpAll(self):
		i =0
		for key, value in self.items.iteritems():
			print "index=%s : Market Type=%s, Code=%s, Full Code=%s, Company=%s" %(i , value.market_type, key, value.full_code, value.company)
			i= i+1

	#Koscom DataMall에서 주식고유코드, 주식이름이 적힌 html문서를 가져옴.
	def downloadCode(self,market_type):
		url = 'http://datamall.koscom.co.kr/servlet/infoService/SearchIssue'
		html = requests.post(url, data={'flag':'SEARCH' , 'marketDisabled': 'null', 'marketBit':market_type})
		return html.content

	#HTML내용에서 원하는 Stock들의 code, company부분만 가져옴
	def parseCodeHTML(self, html, market_type):
		soup = BeautifulSoup.BeautifulSoup(html)
		options = soup.findAll('option')
		for a_option in options:
			if len(a_option)==0:
				continue #잘못 된 값은 무시
			text =a_option.text
			i_code1 = text.find('(')
			i_code2 = text.find(')')
			code = a_option.text[i_code1:i_code2]
			company = a_option.text[i_code2+1:]
			full_code = a_option.get('value')
			
			#크롤링 해오는 게 폐지안된 주식주식만 add
			if( company.rfind('(폐지)')!= -1):
				self.addItem(market_type, code, full_code, company)
		return self

	#주식 종목코드(code)로 yahoo에서 주식일일거래데이터 가져옴.
	def downloadPrice(file_name,  code, dateTime1, dateTime2):

		df = web.DataReader("%s.KS" % (code), "yahoo", dateTime1, dateTime2)
		df.to_pickle(file_name)
		return df


