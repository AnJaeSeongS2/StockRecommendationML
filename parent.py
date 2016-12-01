import pandas as pd

class parent:
	parent_num = 10

	__insCount = 0
	def __init__(self):
		parent.__insCount +=1
		pass	

	
	def printClsCount(self):
		print self.__insCount

	def printParentNum(self):
		print self.parent_num


