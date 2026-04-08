import streamlit as st

from data.fetcher import get_stock_data
from report.analyzer import run_full_analysis
from report.pdf_builder import build_pdf
from report.writer import (
    generate_executive_summary,
    generate_investment_thesis,
    generate_risk_assessment,
)

st.set_page_config(
    page_title="AI Financial Report Generator",
    layout="wide",
    page_icon="📄",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .stApp {
        background: radial-gradient(circle at 0% 0%, #10203b 0%, #0b1220 38%, #070b12 100%);
        color: #e6edf7;
    }
    .hero-card {
        padding: 1.3rem 1.5rem;
        border-radius: 16px;
        background: linear-gradient(135deg, rgba(49, 130, 246, 0.35), rgba(147, 51, 234, 0.25));
        border: 1px solid rgba(148, 163, 184, 0.4);
        margin-bottom: 1rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    .tag {
        display: inline-block;
        padding: 0.2rem 0.65rem;
        border-radius: 999px;
        background: rgba(30, 41, 59, 0.85);
        border: 1px solid rgba(125, 211, 252, 0.45);
        margin-right: 0.35rem;
        font-size: 0.82rem;
    }
    .section-card {
        background: rgba(15, 23, 42, 0.72);
        border: 1px solid rgba(71, 85, 105, 0.45);
        border-radius: 14px;
        padding: 1rem 1.15rem;
        margin-bottom: 0.8rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero-card">
      <h1 style="margin:0;">📄 AI Financial Report Generator</h1>
      <p style="margin:0.4rem 0 0.7rem 0; font-size:1.04rem;">
        Build investor-ready equity memos with AI-assisted analysis, risk narrative, and investment thesis.
      </p>
      <span class="tag">Institutional Style</span>
      <span class="tag">Auto Metrics</span>
      <span class="tag">PDF Export</span>
    </div>
    """,
    unsafe_allow_html=True,
)

st.sidebar.title("⚙️ Portfolio Report Settings")
ticker = st.sidebar.text_input("Stock Ticker", value="RELIANCE.NS")
st.sidebar.caption("Try: RELIANCE.NS, TCS.NS, HDFCBANK.NS, AAPL, MSFT")

generate = st.sidebar.button("🚀 Generate Report", type="primary", use_container_width=True)


def _safe_num(value, default=0.0):
    try:
        if value is None:
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


if generate:
    progress = st.progress(0, text="Starting pipeline...")

    with st.spinner("Fetching market and company data..."):
        stock_info = get_stock_data(ticker)
        analysis = run_full_analysis(ticker)
    progress.progress(35, text="Data fetched. Computing report sections...")

    name = stock_info.get("name", ticker)
    st.success(f"Data fetched for {name}")

    metrics = analysis.get("metrics", {})

    price = _safe_num(stock_info.get("current_price"))
    market_cap = _safe_num(stock_info.get("market_cap"))
    pe_ratio = stock_info.get("pe_ratio", "N/A")
    sharpe = metrics.get("sharpe_ratio", "N/A")
    profit_margin = _safe_num(metrics.get("profit_margin")) * 100
    annual_return = metrics.get("annual_return", "N/A")
    max_drawdown = metrics.get("max_drawdown", "N/A")
    roe = _safe_num(metrics.get("roe")) * 100

    st.markdown("### 📊 KPI Snapshot")
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Current Price", f"₹{price:,.2f}")
    k2.metric("Market Cap", f"₹{market_cap/1e9:.1f}B")
    k3.metric("P/E Ratio", pe_ratio)
    k4.metric("Sharpe Ratio", sharpe)

    k5, k6, k7, k8 = st.columns(4)
    k5.metric("Profit Margin", f"{profit_margin:.1f}%")
    k6.metric("Annual Return", f"{annual_return}%")
    k7.metric("Max Drawdown", f"{max_drawdown}%")
    k8.metric("ROE", f"{roe:.1f}%")

    with st.spinner("Generating AI narrative..."):
        executive_summary = generate_executive_summary(stock_info, metrics)
        risk_assessment = generate_risk_assessment(stock_info, metrics)
        investment_thesis = generate_investment_thesis(stock_info, metrics, analysis.get("revenue", {}))
    progress.progress(75, text="AI sections generated. Building PDF...")

    ai_content = {
        "executive_summary": executive_summary,
        "risk_assessment": risk_assessment,
        "investment_thesis": investment_thesis,
    }

    tab1, tab2, tab3 = st.tabs(["📋 Executive Summary", "⚠️ Risk Assessment", "💡 Investment Thesis"])

    with tab1:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.write(executive_summary)
        st.markdown("</div>", unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.write(risk_assessment)
        st.markdown("</div>", unsafe_allow_html=True)

    with tab3:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.write(investment_thesis)
        st.markdown("</div>", unsafe_allow_html=True)

    with st.spinner("Building PDF report..."):
        pdf_path = build_pdf(ticker, stock_info, analysis, ai_content)

    with open(pdf_path, "rb") as f:
        st.download_button(
            label="📥 Download Full PDF Report",
            data=f,
            file_name=f"{ticker}_Financial_Report.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

    progress.progress(100, text="Done — your portfolio-grade report is ready.")
    st.success("✅ Report ready. Download it above.")
else:
    st.info("Pick a ticker and click **Generate Report** to build your portfolio-style report.")
