import pandas as pd
import numpy as np
from data.fetcher import get_financials, calculate_key_metrics

def analyze_revenue(ticker: str) -> dict:
    financials = get_financials(ticker)
    income     = financials['income']

    if income.empty:
        return {}

    revenue = income.loc['Total Revenue'] if 'Total Revenue' in income.index else None

    if revenue is None:
        return {}

    revenue_growth = revenue.pct_change(-1) * 100

    return {
        'latest_revenue':  revenue.iloc[0],
        'prev_revenue':    revenue.iloc[1] if len(revenue) > 1 else 0,
        'revenue_growth':  round(revenue_growth.iloc[0], 2) if len(revenue_growth) > 0 else 0,
        'revenue_series':  revenue
    }

def analyze_profitability(ticker: str) -> dict:
    financials = get_financials(ticker)
    income     = financials['income']

    gross_profit  = income.loc['Gross Profit']  if 'Gross Profit'  in income.index else None
    net_income    = income.loc['Net Income']     if 'Net Income'    in income.index else None
    total_revenue = income.loc['Total Revenue']  if 'Total Revenue' in income.index else None

    return {
        'gross_margin':  round((gross_profit.iloc[0]  / total_revenue.iloc[0]) * 100, 2) if gross_profit  is not None else 0,
        'net_margin':    round((net_income.iloc[0]    / total_revenue.iloc[0]) * 100, 2) if net_income    is not None else 0,
        'net_income':    net_income.iloc[0] if net_income is not None else 0
    }

def analyze_balance_sheet(ticker: str) -> dict:
    financials = get_financials(ticker)
    balance    = financials['balance']

    total_assets  = balance.loc['Total Assets']       if 'Total Assets'       in balance.index else None
    total_liab    = balance.loc['Total Liabilities Net Minority Interest'] if 'Total Liabilities Net Minority Interest' in balance.index else None
    total_equity  = balance.loc['Stockholders Equity'] if 'Stockholders Equity' in balance.index else None

    return {
        'total_assets':  total_assets.iloc[0]  if total_assets  is not None else 0,
        'total_liab':    total_liab.iloc[0]    if total_liab    is not None else 0,
        'total_equity':  total_equity.iloc[0]  if total_equity  is not None else 0,
        'debt_ratio':    round((total_liab.iloc[0] / total_assets.iloc[0]) * 100, 2) if total_liab is not None and total_assets is not None else 0
    }

def analyze_cashflow(ticker: str) -> dict:
    financials = get_financials(ticker)
    cashflow   = financials['cashflow']

    operating  = cashflow.loc['Operating Cash Flow']       if 'Operating Cash Flow'       in cashflow.index else None
    capex      = cashflow.loc['Capital Expenditure']       if 'Capital Expenditure'       in cashflow.index else None
    free_cf    = cashflow.loc['Free Cash Flow']            if 'Free Cash Flow'            in cashflow.index else None

    return {
        'operating_cf': operating.iloc[0] if operating is not None else 0,
        'capex':        capex.iloc[0]     if capex     is not None else 0,
        'free_cf':      free_cf.iloc[0]   if free_cf   is not None else 0
    }

def run_full_analysis(ticker: str) -> dict:
    return {
        'metrics':       calculate_key_metrics(ticker),
        'revenue':       analyze_revenue(ticker),
        'profitability': analyze_profitability(ticker),
        'balance_sheet': analyze_balance_sheet(ticker),
        'cashflow':      analyze_cashflow(ticker)
    }