# algorithm calculations

# Calculating 14 Day RSI
def rsi(data, period):

    delta = data.diff().dropna()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss

    return 100 - (100 / (1 + rs))

# Calculating 14 Day Momentum
def mom(data, period):
    return data-data.shift(period)*period
    
# Calculating 50 SMA
def sma(data):
    return data.rolling(window=50).mean()

