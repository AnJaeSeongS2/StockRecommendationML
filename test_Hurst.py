import MeanReversionModel
import pandas as pd

df = pd.read_pickle('samsung4.data')
print df['Close']

mrm = MeanReversionModel.MeanReversionModel()


print mrm.calcHurstExponent( df['Close'], 100)

print mrm.calcHalfLife(df['Close'])
print df.loc['2015-02-11','Close']
print df.iloc[0]['Close']
print pd.rolling_mean(df['Close'],5)


print pd.rolling_mean(df.loc['2010-01-01':'2015-02-02','Close'],window=5)
print mrm.determinePosition(df,'Close','2015-02-02',True)
#print mrm.calcHurstExponent2( df['Close'], 100)
if( '2015-01-01'<= df.index[0].strftime('%Y-%m-%d')) :
	print 'asdf'

	print df.index[0]
#print mrm.calcHurstExponent( df['Close'], 400)
#print mrm.calcHurstExponent2( df['Close'], 400)

