#!/usr/bin/python
#-*- coding:utf-8 -*-
class PortfolioBuilder:
	
class MessTrader(BaseCollection):
	def setPortfolio(self, portfolio):
		self.protfolio = portfolio

	def add(self, model, code, row_index, position):
		if self.find(code) is None:
			self.items[code] = []

		a_item = TradeItem(model, code, row_index, position)
		self.items[code].append(a_item)

	def dump(self):
		print "----Portfolio.dump----"
		for key in self.items.keys():
			for a_item in self.items[key]:
				print "... model=%s, code=%s, row_index=%s, position=%s" %(a_item.model, a_item.code, a_item.row_index, a_item.position)
			print "----Done----"



class Predictors:
	def trainAll(self, time_lags=5, split_ratio= 0.75):
		rows_code = self.dbreader.loadCodes(self.config.get('data_limit'))
		test_result= {'code':[], 'company':[], 'logistic':[], 'rf':[], 'svm':[]}
		index =1
		
		
		for a_row_code in rows_code:
			code = a_row_code[0]
			company = a_row_code[1]
		print "... $s of $s : Training Machine Learning on %s %s" %s (index, len(rows_code), code, company)
		df_dataset = self.makeLaggedDataset(code,self.config.get('start_date'), self.config.get('end_date'), self.config.get('input_column'), self.config.get('output_column'), time_lags=time_lags)
		if df_dataset.shape[0]>0:
			test_result['code'].append(code)
			test_result['company'].append(company)

			X_train,X_test,Y_train,Y_test = self.splitDataset(df_dataset, 'price_date', [self.config.get('input_column')], self.config.get('output_column'), split_ratio)

			for a_clasifier in ['logistic', 'rf', 'svm']:
				predictor = self.createPredictor(a_clasifier)
				self.add(code,a_clasifier,predictor)
				predictor.train(X_train, Y_train)
				score = predictor.score(X_test,Y_test)
				test_result[a_clasifier].append(score)
				print " predictor=%s, score=%s" %(a_clasifier,score)
		index+=1
	df_result = pd.DataFrame(test_result)
	return df_result

