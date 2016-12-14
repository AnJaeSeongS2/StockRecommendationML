import ConfigParser


class test4:
	def __init__(self):
		self.a = 5
		self.config = ConfigParser.ConfigParser()
		self.config.read('config.conf')
		print self.config.get('Predictors','start_date')
	def geta(self):
		return self.a




b = test4()
print b.geta()
