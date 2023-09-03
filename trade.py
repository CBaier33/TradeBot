import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from alpaca_trade_api import REST
import time

api_key = 'PKOK81QGPPHPOUS8FNFP'
api_secret = 't1wQoMGlLOb4YsecfkBBLXG2YVOXE2vl9BAfg3Pz'
base_url = 'https://paper-api.alpaca.markets'
api = REST(api_key, api_secret, base_url)


# Fetching historical data
symbol = 'GOOG'
start_date = '2015-01-01' 
end_date = '2022-12-31'
data = yf.download(symbol, start=start_date, end=end_date)

# Calculating the 50-day SMA
data['SMA_50'] = data['Close'].rolling(window=50).mean()

# Implementing the trading strategy
data['Signal'] = np.where(data['Close'] > data['SMA_50'], 1, 0)
data['Daily_Return'] = data['Close'].pct_change()
data['Strategy_Return'] = data['Daily_Return'] * data['Signal'].shift(1)
data['Cumulative_Return'] = (1 + data['Strategy_Return']).cumprod()

# Fetch historical data for SPY
spy_data = yf.download('SPY', start=start_date, end=end_date)

# Calculate daily returns and cumulative returns for SPY
spy_data['Daily_Return'] = spy_data['Close'].pct_change()
spy_data['Cumulative_Return'] = (1 + spy_data['Daily_Return']).cumprod()

# plot both cumulative returns on the same chart
plt.figure(figsize=(12,6))
plt.plot(data.index, data['Cumulative_Return'], label='SMA Strategy')
plt.plot(spy_data.index, spy_data['Cumulative_Return'], label='SPY')
plt.xlabel('Date')
plt.ylabel('Cumulative_Return')
plt.legend() 
plt.show()

def check_positions(symbol):
    positions = api.list_positions()
    for position in positions:
        if positions.symbol == symbol:
            return int(positions.qty)
    return 0

def trade(symbol, qty):
    current_price = api.get_latest_trade(symbol).price
    historical_data = yf.download(symbol, start=start_date, end=end_date, interval='1D')
    historical_data['SMA_50'] = historical_data['Close'].rolling(window=50).mean()
    if current_price > historical_data['SMA_50'][-1]:
        if check_positions(symbol) == 0:
                api.submit_order(symbol=symbol, qty=qty, side='buy', type='market', time_in_force='gtc')
                print("Buy order placed for", symbol)
        else:
            print("Holding", symbol)


symbol = 'GOOG' 
qty = 10
while True:
    trade(symbol, qty)
    time.sleep(60)
