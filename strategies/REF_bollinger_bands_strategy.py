import pandas as pd

def strategy(data, ticker, stock_holdings, cash, short_window=20, long_window=50):
    """
    Moving Average Crossover Trading Strategy.

    Parameters:
        data (pd.DataFrame): Stock data containing prices and dates.
        stock_holdings (int): Current stock holdings.
        cash (float): Current cash available.
        ticker (str): Ticker symbol for the stock.
        short_window (int): Window for the short-term moving average.
        long_window (int): Window for the long-term moving average.

    Returns:
        tuple: Final cash, stock holdings, and trade log with actions ('BUY', 'SELL') for the stock.
    """
    # Calculate moving averages
    data['Short_MA'] = data['Adj Close'].rolling(window=short_window).mean()
    data['Long_MA'] = data['Adj Close'].rolling(window=long_window).mean()

    trade_log = []

    # Simulate trading
    for date, row in data.iterrows():
        if pd.isna(row['Short_MA']) or pd.isna(row['Long_MA']):
            continue  # Skip rows without enough data for MAs

        price = row['Adj Close']
        short_ma = row['Short_MA']
        long_ma = row['Long_MA']

        # Buy signal: Short_MA crosses above Long_MA
        if short_ma > long_ma and stock_holdings == 0:
            num_shares = int(cash // price)
            if num_shares > 0:
                stock_holdings += num_shares
                cash -= num_shares * price
                trade_log.append((date, ticker, 'BUY', num_shares, price))

        # Sell signal: Short_MA crosses below Long_MA
        elif short_ma < long_ma and stock_holdings > 0:
            cash += stock_holdings * price
            trade_log.append((date, ticker, 'SELL', stock_holdings, price))
            stock_holdings = 0

    # Return remaining cash and stock holdings as the final state
    return cash, stock_holdings, trade_log
