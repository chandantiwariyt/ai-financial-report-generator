import streamlit as st
import os
from data.fetcher import get_stock_data, calculate_key_metrics
from report.analyzer import run_full_analysis
from report.writer import generate_executive_summary, generate_risk_assessment, generate_investment_thesis
from report.pdf_builder import build_pdf

st.set_page_config(page_title="AI Financial Report Generator", layout="wide", page_icon="📄")

st.title("📄 AI Financial Report Generator")
st.caption("Institutional-grade analyst reports generated in seconds")

st.sidebar.title("⚙️ Report Settings")
ticker   = st.sidebar.text_input("Stock Ticker", value="RELIANCE.NS")
st.sidebar.markdown("**Examples:**")
st.sidebar.code("RELIANCE.NS\nTCS.NS\nHDFCBANK.NS\nAAPL\nMSFT")

generate = st.sidebar.button("🚀 Generate Report", type="primary")

if generate:
    with st.spinner("Fetching financial data..."):
        stock_info = get_stock_data(ticker)
        analysis   = run_full_analysis(ticker)

    st.success(f"Data fetched for {stock_info['name']}")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Current Price",  f"₹{stock_info['current_price']:,.2f}")
    col2.metric("Market Cap",     f"₹{stock_info['market_cap']/1e9:.1f}B")
    col3.metric("P/E Ratio",      stock_info['pe_ratio'])
    col4.metric("Sharpe Ratio",   analysis['metrics']['sharpe_ratio'])

    col5, col6, col7, col8 = st.columns(4)
    col5.metric("Profit Margin",  f"{analysis['metrics']['profit_margin']*100:.1f}%")
    col6.metric("Annual Return",  f"{analysis['metrics']['annual_return']}%")
    col7.metric("Max Drawdown",   f"{analysis['metrics']['max_drawdown']}%")
    col8.metric("ROE",            f"{analysis['metrics']['roe']*100:.1f}%")

    with st.spinner("Generating AI analysis..."):
        executive_summary  = generate_executive_summary(stock_info, analysis['metrics'])
        risk_assessment    = generate_risk_assessment(stock_info, analysis['metrics'])
        investment_thesis  = generate_investment_thesis(stock_info, analysis['metrics'], analysis['revenue'])

    ai_content = {
        'executive_summary': executive_summary,
        'risk_assessment':   risk_assessment,
        'investment_thesis': investment_thesis
    }

    st.subheader("📋 Executive Summary")
    st.write(executive_summary)

    st.subheader("⚠️ Risk Assessment")
    st.write(risk_assessment)

    st.subheader("💡 Investment Thesis")
    st.write(investment_thesis)

    with st.spinner("Building PDF report..."):
        pdf_path = build_pdf(ticker, stock_info, analysis, ai_content)

    with open(pdf_path, 'rb') as f:
        st.download_button(
            label="📥 Download Full PDF Report",
            data=f,
            file_name=f"{ticker}_Financial_Report.pdf",
            mime="application/pdf"
        )

    st.success("Report ready! Click above to download.")