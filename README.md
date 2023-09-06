# TradeBot

<p>A basic bot for algo trading using the Alpaca API.<p>

<p> ```backtest.py``` pulls stock data for a specified time using the yfinance library, then uses matplotlibto display the returns that could've been realized using several different strategies including 14 Day Momentum, 50 Day SMA, and the 14 Day RSI.<p>

<p>`trade.py` uses the calculations to determine whether to buy, hold, or sell a stock. When a condition is met, an order is placed using the Alpaca API. The specific trading algorithm used will iterate every 24 hours, but this can easily be changed. Note that a different dataset would need to downloaded to match the desired interval.<p>

## Disclaimer
<p>The goal of this project is to practice data visualizations and manipulations. It is by no means financial advice and I would recommend using paper trading for this experiment, and investing your money in other ways. 
