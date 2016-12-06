import pandas as pd
from  DataReadWriter import DataReader
#print pd.read_pickle('samsung2.data')['Close'].pct_change()
df =pd.read_pickle('samsung2.data')['Close']
print df
print df.index[0]
print df.shape[0]-1
print df.index[df.shape[0]-1]

def testSplit(df, input_column_array):
	df2 = df[input_column_array]
	print df2
	print df2.index[0]
	print df2.shape[0]

testSplit(df, ["Close","Adj_Close"])


print df.index.get_level_values("Date")
print df.loc["2015-01-05"]
print df.iloc[1]
print df.index.get_level_values("Date")


dr = DataReader()
testcodes =dr.loadCodes(1,10)
print testcodes['Code']
for a_index in range(testcodes.shape[0]):
	print testcodes.iloc[a_index]['Code']
	print testcodes.iloc[a_index]['Company']


testPrices = dr.loadPrices("005110",0)
print testPrices['Close']




#print pd.read_pickle('samsung2.data')['Close'].shift(5)

