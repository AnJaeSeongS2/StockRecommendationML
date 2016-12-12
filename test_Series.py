from pandas import Series, DataFrame

obj = Series([1,3,5,7,7])
obj2 = Series([2,4,6,8])

print obj==7
print obj[obj==7].index



test = {'aaaa':[1,2,3,4] , 'bbbb':[5,6,7,8]}
print test
df = DataFrame(test)
print df
print obj
print obj2
