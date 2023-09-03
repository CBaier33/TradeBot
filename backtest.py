import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from alpaca_trade_api import REST
import time

''' DATA '''

# Fetching historical stock data
symbol = 'QQQ'
start_date = '2022-09-01' 
end_date = '2023-09-01'
data = yf.download(symbol, start=start_date, end=end_date)


''' CALCULATIONS '''

# Calculating the 50-day SMA
data['SMA_50'] = data['Close'].rolling(window=50).mean()

# Calculating RSI
def rsi(data, period):
    delta = data.diff().dropna()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss

    return 100 - (100 / (1 + rs))


''' BACKTESTING '''

# Backtesting RSI
data['RSI'] = rsi(data['Close'], 14)
data['RSI_Signal'] = 0
data.loc[data['RSI'] < 30, 'RSI_Signal'] = 1
data.loc[data['RSI'] > 70, 'RSI_Signal'] = -1

data['RSI_Daily_Return'] = data['Close'].pct_change()
data['RSI_Strategy_Return'] = data['RSI_Daily_Return'] * data['RSI_Signal'].shift(1)
data['RSI_Cumulative_Return'] = (1 + data['RSI_Strategy_Return']).cumprod()

# Backtesting SMA
data['SMA_Signal'] = np.where(data['Close'] > data['SMA_50'], 1, 0)
data['SMA_Daily_Return'] = data['Close'].pct_change()
data['SMA_Strategy_Return'] = data['SMA_Daily_Return'] * data['SMA_Signal'].shift(1)
data['SMA_Cumulative_Return'] = (1 + data['SMA_Strategy_Return']).cumprod()

# Buy and Hold Strategy
data['BAH_Daily_Return'] = data['Close'].pct_change()
data['BAH_Cumulative_Return'] = (1 + data['BAH_Daily_Return']).cumprod()


''' PLOTTING '''

# plot both cumulative returns on the same chart
plt.figure(figsize=(12,6))
plt.plot(data.index, data['BAH_Cumulative_Return'], label='Buy and Hold')
plt.plot(data.index, data['SMA_Cumulative_Return'], label='SMA Strategy')
plt.plot(data.index, data['RSI_Cumulative_Return'], label='RSI Strategy')
plt.xlabel('Date')
plt.ylabel('Cumulative Return')
plt.legend() 
plt.show()

