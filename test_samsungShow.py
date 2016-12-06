import pandas as pd
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
	print df2.columns()
	

testSplit(df, ["Close","Adj_Close"])

#print pd.read_pickle('samsung2.data')['Close'].shift(5)

