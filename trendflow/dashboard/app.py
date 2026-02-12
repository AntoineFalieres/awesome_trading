import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from trendflow.data.fetcher import fetch_data
from trendflow.strategies.weinstein import WeinsteinStrategy
from trendflow.backtest.engine import Backtester
from trendflow.indicators.ma import MovingAverage

st.set_page_config(layout="wide")

st.title("TrendFlow Strategy Dashboard")

# --- Sidebar Controls ---
st.sidebar.header("Strategy Parameters")
ticker = st.sidebar.text_input("Ticker", "AAPL")
start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2022-01-01"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("2023-01-01"))

st.sidebar.subheader("Weinstein Strategy")
sl_pct = st.sidebar.slider("Stop Loss %", 0.01, 0.2, 0.05, 0.01)
tp_pct = st.sidebar.slider("Take Profit %", 0.05, 0.5, 0.1, 0.01)

use_trend_filter = st.sidebar.checkbox("Use Long-Term Trend Filter")
long_ma_period = st.sidebar.number_input("Long MA Period", 50, 300, 200, 10)
long_ma_type = st.sidebar.selectbox("Long MA Type", ['sma', 'ema', 'wma'])

st.sidebar.subheader("Secondary MA")
show_secondary_ma = st.sidebar.checkbox("Show Secondary MA")
sec_ma_period = st.sidebar.number_input("Secondary MA Period", 10, 200, 50, 10)
sec_ma_type = st.sidebar.selectbox("Secondary MA Type", ['sma', 'ema', 'wma'], index=1)


@st.cache_data
def run_backtest(ticker, start_date, end_date, sl_pct, tp_pct, use_trend_filter, long_ma_period, long_ma_type):
    data = fetch_data(ticker, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))
    
    strategy = WeinsteinStrategy(
        stop_loss_pct=sl_pct,
        take_profit_pct=tp_pct,
        use_trend_filter=use_trend_filter,
        long_ma_period=long_ma_period,
        long_ma_type=long_ma_type
    )
    data_with_signals = strategy.generate_signals(data.copy())
    
    backtester = Backtester()
    results = backtester.run(data_with_signals.copy())
    metrics = backtester.calculate_metrics(results)
    
    return results, metrics

# --- Main App ---
if st.sidebar.button("Run Backtest"):
    results_df, metrics = run_backtest(ticker, start_date, end_date, sl_pct, tp_pct, use_trend_filter, long_ma_period, long_ma_type)

    st.subheader("Performance Metrics")
    st.json(metrics)

    st.subheader("Equity Curve")
    st.line_chart(results_df['equity_curve'])

    st.subheader("Price Chart & Signals")

    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.02, row_heights=[0.7, 0.3])

    # Price Chart
    fig.add_trace(go.Candlestick(x=results_df.index,
                               open=results_df['open'],
                               high=results_df['high'],
                               low=results_df['low'],
                               close=results_df['close'],
                               name='Price'), row=1, col=1)

    # MM30
    fig.add_trace(go.Scatter(x=results_df.index, y=results_df['MM30'], mode='lines', name='MM30', line=dict(color='orange')), row=1, col=1)

    # Secondary MA
    if show_secondary_ma:
        ma_indicator = MovingAverage(period=sec_ma_period, ma_type=sec_ma_type)
        results_df = ma_indicator.calculate(results_df)
        sec_ma_col = f"{sec_ma_type.upper()}_{sec_ma_period}"
        fig.add_trace(go.Scatter(x=results_df.index, y=results_df[sec_ma_col], mode='lines', name=f'Secondary MA ({sec_ma_col})'), row=1, col=1)

    # Buy Signals
    buy_signals = results_df[results_df['signal'] == 1]
    fig.add_trace(go.Scatter(x=buy_signals.index, y=buy_signals['close'], mode='markers', name='Buy Signal',
                               marker=dict(symbol='triangle-up', color='green', size=10)), row=1, col=1)

    # Sell Signals
    sell_signals = results_df[results_df['signal'] == -1]
    fig.add_trace(go.Scatter(x=sell_signals.index, y=sell_signals['close'], mode='markers', name='Sell Signal',
                               marker=dict(symbol='triangle-down', color='red', size=10)), row=1, col=1)

    # Volume Chart
    fig.add_trace(go.Bar(x=results_df.index, y=results_df['volume'], name='Volume'), row=2, col=1)
    
    fig.update_layout(xaxis_rangeslider_visible=False, height=800)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Trade Log")
    st.dataframe(results_df[results_df['signal'] != 0])
