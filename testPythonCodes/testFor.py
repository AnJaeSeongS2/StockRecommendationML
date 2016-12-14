import numpy as np
import pandas as pd
lags = range(1,2)
df = pd.read_pickle('samsung4.data')
ts = df['Close']


print ts[2:]
print ts[:-2]



print [np.std(np.subtract(ts[lag:],ts[:-lag])) for lag in lags]


