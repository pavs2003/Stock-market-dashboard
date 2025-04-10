import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from datetime import date, timedelta

# Page settings
st.set_page_config(page_title="Stock Market Dashboard", layout="wide")

# Title
st.title("📈 Stock Market Dashboard")

# Sidebar for input
st.sidebar.header("🔍 Stock Selection")
symbol = st.sidebar.text_input("Enter Stock Symbol (e.g., AAPL, INFY, TSLA)", value="AAPL")

# Date range selection
st.sidebar.markdown("Select Date Range:")
end_date = st.sidebar.date_input("End Date", date.today())
start_date = st.sidebar.date_input("Start Date", end_date - timedelta(days=180))

# Fetch stock data
try:
    stock = yf.Ticker(symbol)
    data = stock.history(start=start_date, end=end_date)

    if data.empty:
        st.error("⚠️ No data found. Please check the stock symbol or date range.")
    else:
        # Display stock name
        st.subheader(f"📊 {stock.info.get('longName', symbol)} ({symbol.upper()})")

        # Line chart of closing prices
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Close'))
        fig.update_layout(title="Closing Price Over Time",
                          xaxis_title="Date", yaxis_title="Price (USD)",
                          template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)

        # Stock stats
        st.markdown("### 📌 Stock Info")
        cols = st.columns(3)
        cols[0].metric("Current Price", stock.info.get("currentPrice", "N/A"))
        cols[1].metric("Open", stock.info.get("open", "N/A"))
        cols[2].metric("Previous Close", stock.info.get("previousClose", "N/A"))

        cols = st.columns(3)
        cols[0].metric("Day High", stock.info.get("dayHigh", "N/A"))
        cols[1].metric("Day Low", stock.info.get("dayLow", "N/A"))
        cols[2].metric("Volume", stock.info.get("volume", "N/A"))

except Exception as e:
    st.error("❌ An error occurred while fetching stock data. Please try again.")
