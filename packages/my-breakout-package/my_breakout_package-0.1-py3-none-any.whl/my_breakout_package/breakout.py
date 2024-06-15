# my_breakout_package/breakout.py
import numpy as np
import pandas as pd

def calculate_breakout(data, length=20, target=65, n=5):
    window = length
    data = data.copy()
    data['diff'] = data['Close'].diff()
    data['gain'] = np.where(data['diff'] > 0, data['diff'], 0)
    data['loss'] = np.where(data['diff'] < 0, -data['diff'], 0)

    data['avg_gain'] = 0.0
    data['avg_loss'] = 0.0

    for i in range(1, len(data)):
        if i < window:
            data.iloc[i, data.columns.get_loc('avg_gain')] = data['gain'][:i + 1].mean()
            data.iloc[i, data.columns.get_loc('avg_loss')] = data['loss'][:i + 1].mean()
        else:
            data.iloc[i, data.columns.get_loc('avg_gain')] = (
                (data.iloc[i - 1, data.columns.get_loc('avg_gain')] * (window - 1) + data.iloc[i, data.columns.get_loc('gain')]) / window
            )
            data.iloc[i, data.columns.get_loc('avg_loss')] = (
                (data.iloc[i - 1, data.columns.get_loc('avg_loss')] * (window - 1) + data.iloc[i, data.columns.get_loc('loss')]) / window
            )

    data['BI'] = data['avg_gain'] / data['avg_loss']
    data['BIV'] = 100 - (100 / (1 + data['BI']))

    try:
        data["Trade condition"] = False

        for i in range(n, len(data)):
            condition = (
                (data["BIV"].iloc[i] > target) and
                all(data["BIV"].iloc[i - j] < target for j in range(1, n + 1)) and
                (data["Close"].iloc[i] > data["Open"].iloc[i])
            )
            data.loc[data.index[i], "Trade condition"] = condition
    except Exception as e:
        print(f"Error in calculate_trade_conditions: {e}")
        
    return data[['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume', 'Trade condition']]
