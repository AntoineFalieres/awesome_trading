import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from trendflow.data.fetcher import get_data
from trendflow.strategies.crossover import crossover_strategy
from trendflow.backtest.engine import run_backtest

st.title("TrendFlow")

st.write("Welcome to TrendFlow, your application for backtesting trading strategies.")

st.sidebar.header("Data")
ticker = st.sidebar.text_input("Ticker", "AAPL")
start_date = st.sidebar.text_input("Start Date", "2023-01-01")
end_date = st.sidebar.text_input("End Date", "2024-01-01")

st.sidebar.header("Strategy")
short_window = st.sidebar.number_input("Short SMA Window", min_value=1, max_value=200, value=40)
long_window = st.sidebar.number_input("Long SMA Window", min_value=1, max_value=200, value=100)
initial_capital = st.sidebar.number_input("Initial Capital", min_value=1000, max_value=1000000, value=10000)


if st.sidebar.button("Run Backtest"):
    st.subheader(f"Data for {ticker}")
    data = get_data(ticker, start_date, end_date)
    if not data.empty:
        signals = crossover_strategy(data, short_window, long_window)
        
        # Run backtest
        backtest_results = run_backtest(initial_capital, data, signals)

        # Display performance metrics
        st.subheader("Backtest Performance")
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Total Return", f"{backtest_results['total_return']:.2%}")
        col2.metric("Number of Trades", backtest_results['num_trades'])
        col3.metric("Winning Trades", backtest_results['num_wins'])
        col4.metric("Losing Trades", backtest_results['num_losses'])
        col5.metric("Win Rate", f"{backtest_results['win_rate']:.2f}%")

        # Display portfolio value over time
        st.subheader("Portfolio Value Over Time")
        st.line_chart(backtest_results['portfolio']['total'])


        # Create a plotly chart for price and signals
        fig = go.Figure()

        fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Close'))
        fig.add_trace(go.Scatter(x=signals.index, y=signals['short_mavg'], mode='lines', name='Short SMA'))
        fig.add_trace(go.Scatter(x=signals.index, y=signals['long_mavg'], mode='lines', name='Long SMA'))

        # Add buy signals
        buy_signals = signals[signals['positions'] == 1.0]
        fig.add_trace(go.Scatter(x=buy_signals.index, y=data.loc[buy_signals.index]['Close'], 
                                 mode='markers', name='Buy Signal', marker=dict(color='green', size=10, symbol='triangle-up')))

        # Add sell signals
        sell_signals = signals[signals['positions'] == -1.0]
        fig.add_trace(go.Scatter(x=sell_signals.index, y=data.loc[sell_signals.index]['Close'], 
                                  mode='markers', name='Sell Signal', marker=dict(color='red', size=10, symbol='triangle-down')))

        fig.update_layout(title=f"{ticker} Price with Crossover Strategy",
                          xaxis_title="Date",
                          yaxis_title="Price")

        st.plotly_chart(fig)

        st.subheader("Raw Data")
        st.write(data)
        st.subheader("Signals")
        st.write(signals)
        st.subheader("Portfolio")
        st.write(backtest_results['portfolio'])

    else:
        st.write("No data found for the given ticker and date range.")

