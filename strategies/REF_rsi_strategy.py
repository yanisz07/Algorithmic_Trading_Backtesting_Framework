import pandas as pd

def strategy(data, ticker, stock_holdings, cash, rsi_period=14, overbought=70, oversold=30):
    """
    RSI (Relative Strength Index) Trading Strategy.

    Parameters:
        data (pd.DataFrame): Stock data containing prices and dates.
        stock_holdings (int): Current stock holdings.
        cash (float): Current cash available.
        ticker (str): Ticker symbol for the stock.
        rsi_period (int): Lookback period for RSI calculation.
        overbought (int): RSI threshold above which the stock is considered overbought (sell signal).
        oversold (int): RSI threshold below which the stock is considered oversold (buy signal).

    Returns:
        tuple: Final cash, stock holdings, and trade log with actions ('BUY', 'SELL') for the stock.
    """
    # Calculate RSI
    delta = data['Adj Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=rsi_period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=rsi_period).mean()
    rs = gain / loss
    data['RSI'] = 100 - (100 / (1 + rs))

    trade_log = []

    # Simulate trading
    for date, row in data.iterrows():
        if pd.isna(row['RSI']):
            continue  # Skip rows without enough data for RSI

        price = row['Adj Close']
        rsi = row['RSI']

        # Buy signal: RSI crosses below the oversold threshold
        if rsi < oversold and stock_holdings == 0:
            num_shares = int(cash // price)
            if num_shares > 0:
                stock_holdings += num_shares
                cash -= num_shares * price
                trade_log.append((date, ticker, 'BUY', num_shares, price))

        # Sell signal: RSI crosses above the overbought threshold
        elif rsi > overbought and stock_holdings > 0:
            cash += stock_holdings * price
            trade_log.append((date, ticker, 'SELL', stock_holdings, price))
            stock_holdings = 0

    # Return remaining cash and stock holdings as the final state
    return cash, stock_holdings, trade_log
