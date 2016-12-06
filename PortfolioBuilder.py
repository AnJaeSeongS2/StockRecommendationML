from MeanReversionModel import MeanReversionModel
#from MachineLearningModel import MachineLearningModel
from DataReadWriter import DataReader
import pandas as pd

class PortfolioBuilder:
	def __init__(self):
		self.dbreader = DataReader()
		self.mean_reversion_model = MeanReversionModel() 
		#self.machine_learning_model = MachineLearningModel() 
	def loadDataFrame(self, code):
		return 0

'''
	#머신러닝의 score계산 실행
	def doMachineLearningTest(self, split_ratio = 0.75 , lags_count=10):
		return self.machine_learning_model.calcScore(split_ratio= split_ratio, time_lags = lags_count)
'''
	#평균회귀 성향을 파악하고, 결과냄.
	def doMeanReversionTest(self, column, lags_count = 100):
		#rows_code = self.dbreader.loadCodes(limit = self.config.get('data_limit'))
		rows_code = self.dbreader.loadCodes(market_type = 1, limit = 30)

		#return해줄 df양식
		test_result = {'code':[]. 'company':[], 'adf_statistic':[], 'adf_1':[], 'adf_5':[], 'adf_10':[], 'hurst':[], 'halflife':[]}
		index = 1
		for a_row_code in rows_code :
			code = a_row_code[0]
			company = a_row_code[1]
			print "... %s of %s : Testing Mean Reversion Model on %s %s " % (index, len(rows_code), code, company)
			a_df = self.loadDataFrame(code)
			a_df_column = a_df[column]

			if a_df_column.shape[0]>0 :
				test_result['code'].append(code)
				test_result['company'].append(company)
				test_result['hurst'].append(self.mean_reversion_model.calcHurstExponent(a_df_column, lags_count))
				test_result['halflife'].append(self.mean_reversion_model.calcHalfLief(a_df_column))
				adf_statistic, adf_1, adf_5, adf_10= self.mean_reversion_model.calcADF(a_df_column)
				
				test_result['adf_statistic'].append(adf_statistic)
				test_result['adf_1'].append(adf_1)
				test_result['adf_5'].append(adf_5)
				test_result['adf_10'].append(adf_10)
			
			index+=1

		df_result = pd.DataFrame(test_result)
		return df_result

	#종목별 적합도 순위표 리턴
	def rankMeanReversion(self,df_mean_reversion):
		df_mean_reversion['rank_adf'] = 0
		df_mean_reversion['rank_hurst'] = 0
		df_mean_reversion['rank_halflife'] = 0

		halflife_percentile = np.percentile(df_mean_reversion['halflife'], np.arange(0,100,10))
		for row_index in range(df_mean_reversion.shape[0]):
			df_mean_reversion.loc[row_index, 'rank_adf'] = self.assessADF(df_stationarity.loc[row_index, 'adf_statistic'], df_stationarity.loc[row_index,'adf_1'], df_stationarity.loc[row_index, 'adf_5'], df_stationarity.loc[row_index, 'adf_10'])

			df_mean_reversion.loc[row_index,'rank_hurst']= self.assessHurst(df_stationarity.loc[row_index, 'hurst'])
			df_mean_reversion.loc[row_index, 'rank_halflife'] = self.assessHalflife(halflife_percentile, df_stationarity.loc[row_index,'halflife'])
			
		df_mean_reversion['rank'] = df_stationarity['rank_adf']+ df_stationarity['rank_hurst'] + df_stationarity['rank_halflife']

		return df_mean_reversion

	#적합도 순위 결과로 주식 선정 .ex) ratio 0.7 : 순위로 상위70%이상인 주식의 목록 반환
	def buildUniverse(self, df_mean_reversion, column, ratio):
		#백분위수 0, 10, ... , 100에 해당하는 column값
		percentile_column = np.percentile(df_mean_reversion[column], np.arange(0,101,10))
		ratio_index = np.trunc(ratio * (len(percentile_column)-1))
		universe = {}

		#가진 날자 동안 진행.
		for row_index in range(df_mean_reversion.shape[0]) :
			percentile_index = getPercentileIndex(percentile_column, df_mean_reversion.loc[row_index,column])
			if percentile_index >= ratio_index:
				universe[df_mean_reversion.loc[row_index,'code']] = df_stationarity.loc[row_index,'company']

		return universe
'''

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

'''

