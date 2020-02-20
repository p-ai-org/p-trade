from pandas_datareader import data, wb, iex
import pandas_datareader
import os
from datetime import datetime


os.environ["IEX_API_KEY"]= "pk_97758c21082d45939a04a9430d438c64"

start = datetime(2016, 9, 1)
end = datetime(2018, 9, 1)
f = pandas_datareader.iex.daily.IEXDailyReader(symbols='GOOG', start = start, end = end).read()
print(f)