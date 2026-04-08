import os
import time

from dotenv import load_dotenv
from openai import APIConnectionError, APIError, OpenAI, RateLimitError

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def _call_llm(prompt: str, max_tokens: int, retries: int = 2) -> str:
    last_error = None
    for attempt in range(retries + 1):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
            )
            return (response.choices[0].message.content or "").strip()
        except RateLimitError as error:
            last_error = error
            # Handles request rate limits and insufficient_quota gracefully.
            if attempt < retries:
                time.sleep(1.5 * (2**attempt))
                continue
            return (
                "AI analysis is temporarily unavailable because the OpenAI API is "
                "rate-limited or out of quota. Please verify billing/usage limits "
                "and try again shortly."
            )
        except (APIConnectionError, APIError) as error:
            last_error = error
            if attempt < retries:
                time.sleep(1.0 * (2**attempt))
                continue
            return (
                "AI analysis is temporarily unavailable due to an API/network issue. "
                "Please try again in a few moments."
            )
        except Exception as error:
            last_error = error
            break

    return f"AI analysis could not be generated right now: {last_error}"


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
    return _call_llm(prompt=prompt, max_tokens=500)


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
    return _call_llm(prompt=prompt, max_tokens=300)


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
    return _call_llm(prompt=prompt, max_tokens=300)