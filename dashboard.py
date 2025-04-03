import streamlit as st
import pandas as pd
import json

# Streamlit app
st.title("Paper Trading Bot Dashboard")

# Load trades from trades.json
try:
    with open('trades.json', 'r') as f:
        trades = json.load(f)
except FileNotFoundError:
    trades = []
    st.warning("No trades found. Please run the trading bot to generate trades.")
except json.JSONDecodeError:
    trades = []
    st.error("Error reading trades.json. The file may be corrupted.")

# Display trades in a table
if trades:
    df = pd.DataFrame(trades)
    st.subheader("Recent Trades")
    st.dataframe(df)
else:
    st.write("No trades to display.")