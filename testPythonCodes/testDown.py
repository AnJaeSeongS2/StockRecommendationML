import touch_stock as ts
import datetime

#df = ts.download_stock_data('samsung3.data','005930',2015,1,1,2015,1,3)
#print df
df = ts.download_stock_data('samsung4.data','005930',datetime.datetime(2015,1,1),datetime.datetime(2015,12,31))
#
#for key,value in df.it

print len(df.index)
print df.index[23].strftime('%Y-%m-%d %H:%M:%S')
print df.Open[1]

print df.iloc[1]
print df.iloc[1]['Open']
print df.get_value('2015-01-02','Open')
#print df.Adj__Close[1]
#print df['2015-01-02'].tolist()


