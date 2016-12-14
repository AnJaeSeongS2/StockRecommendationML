#!/usr/bin/python
#-*- coding: utf-8 -*-

class AlphaModel:
	__insCount = 0
	def __init__(self):
		AlphaModel.__insCount += 1
	
	def instanceCount(cls):
		print ("AlpahModel Instance Count : %s"%cls.__insCount)
		return cls.__insCount

	def determinePosition(self):
		print "create determinePosition func in Inherited Class"
		
