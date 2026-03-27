import yfinance as yf
import pandas as pd
import numpy as np
from fredapi import Fred
import os
from dotenv import load_dotenv

load_dotenv()

def get_stock_data(ticker: str) -> dict:
    stock = yf.Ticker(ticker)
    info = stock.info

    return {
        'name':             info.get('longName', ticker),
        'sector':           info.get('sector', 'N/A'),
        'industry':         info.get('industry', 'N/A'),
        'market_cap':       info.get('marketCap', 0),
        'current_price':    info.get('currentPrice', 0),
        'pe_ratio':         info.get('trailingPE', 0),
        'pb_ratio':         info.get('priceToBook', 0),
        'dividend_yield':   info.get('dividendYield', 0),
        'beta':             info.get('beta', 0),
        'fifty_two_high':   info.get('fiftyTwoWeekHigh', 0),
        'fifty_two_low':    info.get('fiftyTwoWeekLow', 0),
        'description':      info.get('longBusinessSummary', 'N/A')
    }

def get_financials(ticker: str) -> dict:
    stock = yf.Ticker(ticker)

    income    = stock.financials
    balance   = stock.balance_sheet
    cashflow  = stock.cashflow
    history   = stock.history(period='2y')

    return {
        'income':    income,
        'balance':   balance,
        'cashflow':  cashflow,
        'history':   history
    }

def get_price_history(ticker: str) -> pd.DataFrame:
    stock = yf.Ticker(ticker)
    df    = stock.history(period='1y')
    df.reset_index(inplace=True)
    df['Date'] = pd.to_datetime(df['Date'])
    df['Daily_Return'] = df['Close'].pct_change()
    return df

def calculate_key_metrics(ticker: str) -> dict:
    stock    = yf.Ticker(ticker)
    info     = stock.info
    history  = stock.history(period='1y')

    returns      = history['Close'].pct_change().dropna()
    sharpe       = (returns.mean() / returns.std()) * np.sqrt(252)
    cumulative   = (1 + returns).cumprod()
    rolling_max  = cumulative.cummax()
    drawdown     = (cumulative - rolling_max) / rolling_max
    max_dd       = drawdown.min()
    annual_return = returns.mean() * 252

    return {
        'revenue':        info.get('totalRevenue', 0),
        'gross_margin':   info.get('grossMargins', 0),
        'profit_margin':  info.get('profitMargins', 0),
        'roe':            info.get('returnOnEquity', 0),
        'roa':            info.get('returnOnAssets', 0),
        'debt_to_equity': info.get('debtToEquity', 0),
        'current_ratio':  info.get('currentRatio', 0),
        'sharpe_ratio':   round(sharpe, 2),
        'max_drawdown':   round(max_dd * 100, 2),
        'annual_return':  round(annual_return * 100, 2)
    }