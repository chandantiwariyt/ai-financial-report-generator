# 📄 AI Financial Report Generator

An institutional-grade financial report generator that automatically 
produces professional analyst-style PDF reports using AI — 
just like an investment bank analyst would produce.

## 🔍 What It Does
- Fetches live financial data for any stock (NSE, BSE, NYSE)
- Calculates key metrics — Sharpe Ratio, ROE, Profit Margin, Max Drawdown
- Uses GPT-4 to write professional analyst commentary
- Generates a downloadable PDF report in seconds

## 📄 Report Sections
- Executive Summary (AI Generated)
- Key Financial Metrics Table
- Risk Assessment (AI Generated)
- Investment Thesis (AI Generated)

## 🛠 Tech Stack
- Python, Streamlit, OpenAI GPT-4
- yFinance, ReportLab, Pandas, NumPy
- FRED API, Python-dotenv

## 🚀 How to Run
pip install -r requirements.txt
streamlit run app.py

## 📊 Sample Tickers
- Indian Stocks: RELIANCE.NS, TCS.NS, HDFCBANK.NS
- US Stocks: AAPL, MSFT, GOOGL

## ⚙️ Environment Variables
OPENAI_API_KEY=your_openai_key
FRED_API_KEY=your_fred_key
```

Then push to GitHub:
```
git add README.md
git commit -m "Added README"
git push