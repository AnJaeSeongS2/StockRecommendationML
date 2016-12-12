#!/usr/bin/python
#-*- coding:utf-8 -*-

from DataReadWriter import DataWriter
from datetime import datetime

dw = DataWriter()
start_time =datetime.now()
dw.updateCodesToDB()
print "Update Codes To DB 시간소요 : "+str(datetime.now()-start_time)
start_time = datetime.now()
dw.updatePricesToDB(1,datetime(2014,1,1),datetime(2016,12,10))
print "Update Prices To DB 시간소요 : "+str(datetime.now()-start_time)
