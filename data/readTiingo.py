import os
from datetime import datetime

from tiingo import TiingoClient
os.environ["TIINGO_API_KEY"]= "e39ce9305ed69d18a27c62860cd44ce2b3f7cfff"

client = TiingoClient()

# Get Ticker
ticker_metadata = client.get_ticker_metadata("GOOGL")
# Get latest prices, based on 3+ sources as JSON, sampled weekly
ticker_price = client.get_ticker_price("GOOGL", frequency="weekly")
# Get historical GOOGL prices from August 2017 as JSON, sampled daily
historical_prices = client.get_ticker_price("GOOGL",
                                            fmt='json',
                                            startDate='2000-08-01',
                                            endDate='2017-08-03',
                                            frequency='daily')
print(historical_prices)
