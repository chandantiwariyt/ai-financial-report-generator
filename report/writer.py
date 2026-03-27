from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_executive_summary(stock_info: dict, metrics: dict) -> str:
    prompt = f"""
    You are a senior equity research analyst at a top investment bank.
    Write a professional executive summary for {stock_info['name']} ({stock_info['sector']}).
    
    Key Data:
    - Current Price: {stock_info['current_price']}
    - Market Cap: {stock_info['market_cap']}
    - P/E Ratio: {stock_info['pe_ratio']}
    - Revenue: {metrics['revenue']}
    - Profit Margin: {metrics['profit_margin']}
    - Sharpe Ratio: {metrics['sharpe_ratio']}
    - Annual Return: {metrics['annual_return']}%
    - Max Drawdown: {metrics['max_drawdown']}%
    
    Write 3 paragraphs covering: business overview, financial performance, investment outlook.
    Use professional investment banking language.
    """
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500
    )
    return response.choices[0].message.content

def generate_risk_assessment(stock_info: dict, metrics: dict) -> str:
    prompt = f"""
    You are a senior risk analyst at a hedge fund.
    Write a risk assessment for {stock_info['name']}.
    
    Risk Data:
    - Beta: {stock_info['beta']}
    - Max Drawdown: {metrics['max_drawdown']}%
    - Debt to Equity: {metrics['debt_to_equity']}
    - Current Ratio: {metrics['current_ratio']}
    - Sharpe Ratio: {metrics['sharpe_ratio']}
    
    Write 2 paragraphs covering key risks and risk mitigation factors.
    Use professional risk management language.
    """
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300
    )
    return response.choices[0].message.content

def generate_investment_thesis(stock_info: dict, metrics: dict, revenue: dict) -> str:
    prompt = f"""
    You are a portfolio manager at a top PE firm.
    Write an investment thesis for {stock_info['name']}.
    
    Data:
    - Revenue Growth: {revenue.get('revenue_growth', 0)}%
    - Gross Margin: {metrics['gross_margin']}%
    - ROE: {metrics['roe']}%
    - P/E Ratio: {stock_info['pe_ratio']}
    - Annual Return: {metrics['annual_return']}%
    
    Write a compelling 2 paragraph buy/hold/sell thesis with price target reasoning.
    Use PE/VC investment committee language.
    """
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300
    )
    return response.choices[0].message.content