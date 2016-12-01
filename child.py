from parent import parent

class child(parent):
	parent_num = 30
	__insCount = 0
	def __init__(self):
		parent.__init__(self)
		child.__insCount +=1
		print pd.read_pickle('samsung4.data')
	def printChildNum(self):
		print self.parent_num


	
	
