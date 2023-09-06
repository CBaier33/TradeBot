import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from alpaca_trade_api import REST
import calculator as calc
import time

class backtester():

    def __init__(self):
        self.symbol = input("Please enter stock ticker: " )
        print("\nPlease enter a backtest date range in 'year-month-day' format below...")
        self.start_date = input("Start Date: ") 
        self.end_date = input("End Date: ")
        self.data = yf.download(self.symbol, start=self.start_date, end=self.end_date)
        self.spy = yf.download('SPY', start=self.start_date, end=self.end_date)

    def backtest(self):
    
        self.data['SMA_50'] = calc.sma(self.data['Close'])
        self.data['MOM'] = calc.mom(self.data['Close'], 14)
        self.data['RSI'] = calc.rsi(self.data['Close'], 14) 
        self.data['Daily_Return'] = self.data['Close'].pct_change()
        self.spy['SPY_Daily_Return'] = self.spy['Close'].pct_change()

        # SPY
        self.spy['SPY_Cumulative_Return'] = (1 + self.spy['SPY_Daily_Return']).cumprod()

        # Backtesting RSI
        self.data['RSI_Signal'] = 0
        self.data.loc[self.data['RSI'] < 30, 'RSI_Signal'] = 1
        self.data.loc[self.data['RSI'] > 70, 'RSI_Signal'] = -1

        self.data['RSI_Strategy_Return'] = self.data['Daily_Return'] * self.data['RSI_Signal'].shift(1)
        self.data['RSI_Cumulative_Return'] = (1 + self.data['RSI_Strategy_Return']).cumprod()


        # Backtesting SMA
        self.data['SMA_Signal'] = np.where(self.data['Close'] > self.data['SMA_50'], 1, 0)
        self.data['SMA_Strategy_Return'] = self.data['Daily_Return'] * self.data['SMA_Signal'].shift(1)
        self.data['SMA_Cumulative_Return'] = (1 + self.data['SMA_Strategy_Return']).cumprod()
        
        # Backtesting Momentum
        self.data['MOM_Signal'] = 0 
        self.data.loc[self.data['MOM'] > 100, 'MOM_Signal'] = 1
        self.data.loc[self.data['MOM'] < 100, 'MOM_Signal'] = -1

        self.data['MOM_Strategy_Return'] = self.data['Daily_Return'] * self.data['MOM_Signal'].shift(1)
        self.data['MOM_Cumulative_Return'] = (1 + self.data['MOM_Strategy_Return']).cumprod()

    def plot(self):
        plt.figure(figsize=(12,6))
        plt.plot(self.data.index, self.data['SMA_Cumulative_Return'], label='SMA')
        plt.plot(self.data.index, self.data['RSI_Cumulative_Return'], label='RSI')
        plt.plot(self.data.index, self.data['MOM_Cumulative_Return'], label='Momentum')
        plt.plot(self.spy.index, self.spy['SPY_Cumulative_Return'], label='SPY')
        plt.xlabel(self.symbol)
        plt.ylabel('Cumulative Returns')
        plt.legend() 
        plt.show()

if __name__ == '__main__':

    while True: 

        bt = backtester()
        bt.backtest()
        bt.plot()

        restart = input('Would you like to backtest another stock? (Y/n) ')

        if restart == 'n':
            break
        else:
            continue

