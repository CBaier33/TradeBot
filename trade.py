import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from alpaca_trade_api import REST
from config import api_key, api_secret, base_url
import calculator as calc
import time

api = REST(api_key, api_secret, base_url)

class trader():

    def __init__(self):

        self.symbol = input("Please enter stock ticker: " )
        print("\nPlease enter a historical data range in 'year-month-day' format below...")
        self.start_date = input("Start Date: ") 
        self.end_date = input("End Date: ")
        self.data = yf.download(self.symbol, start=self.start_date, end=self.end_date, interval='1d')
        print(f'Current Price of {self.symbol}: {api.get_latest_trade(self.symbol).price}')
        print('\nTRADE OPTIONS')
        print('*************')
        print('(1) SMA\n(2) RSI\n(3) Momentum')
        self.strategy = int(input("\nWhich strategy would you like to trade with? "))
        self.qty = input("How many shares per trade? ")

    def check_positions(self, symbol):
        positions = api.list_positions()
        for position in positions:
            if position.symbol == symbol:
                return int(position.qty)
        return 0

    def sma_trade(self, symbol, qty, historical_data):
        current_price = api.get_latest_trade(symbol).price
        historical_data['SMA_50'] = calc.sma(historical_data['Close'])

        if current_price > historical_data['SMA_50'][-1] and self.check_positions(symbol) == 0:
            api.submit_order(symbol=symbol, qty=qty, side='buy', type='market', time_in_force='gtc')
            print(f'**Buy order placed for {symbol}**')
        elif current_price <= (historical_data['SMA_50'][-1] - hisorical_data['SMA_50'][-1] * .08):
            if self.check_positions > 0:
                api.submit_order(symbol=symbol, qty=qty, side='sell', type='market', time_in_force='gtc')
                print(f'**Sell order placed for {symbol}**')
        else:
            print(f'**Holding {symbol}**')

    def rsi_trade(self, symbol, qty, data):
        current_rsi = calc.rsi(data['Close'], 14)[-1]
        position_qty = self.check_positions(symbol)
        
        if current_rsi < 30 and position_qty == 0:
            api.submit_order( symbol=symbol, qty=qty, side='buy', type='market', time_in_force='gtc' )
            print(f"**Buy order placed for {symbol}**") 
        elif current_rsi > 70 and position_qty > 0:
            api.submit_order( symbol=symbol, qty=position_qty, side='sell', type='market', time_in_force='gtc' )
            print(f"**Sell order placed for {symbol}**") 

        else: 
            print(f"**Holding {symbol}**")

    def mom_trade(self, symbol, qty, data):
        current_mom = calc.mom(data['Close'], 14)[-1]
        position_qty = self.check_positions(symbol)

        if current_mom > 100 and position_qty == 0:
            api.submit_order( symbol=symbol, qty=qty, side='buy', type='market', time_in_force='gtc' )
            print(f"**Buy order placed for {symbol}**") 
        elif current_mom < -100 and position_qty > 0:
            api.submit_order( symbol=symbol, qty=position_qty, side='sell', type='market', time_in_force='gtc' )
            print(f"**Sell order placed for {symbol}**") 
        
        else:
            print(f"**Holding {symbol}**")
        
    def trade(self):
        print('\n*********TRADE CYCLE START*********\n')
        if self.strategy == 1:
            while True:
                self.sma_trade(self.symbol, self.qty, self.data)
                time.sleep(84600)

        elif self.strategy == 2:
            while True:
                self.rsi_trade(self.symbol, self.qty, self.data)
                time.sleep(84600)

        elif self.strategy == 3:
            while True:
                self.mom_trade(self.symbol, self.qty, self.data)
                time.sleep(84600)


if __name__ == '__main__':

    tr = trader()

    tr.trade()
