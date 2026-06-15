import streamlit as st
from pathlib import Path
import sys

# Add parent directory to path so we can import trendflow
sys.path.insert(0, str(Path(__file__).parent))

# Configure Streamlit app
st.set_page_config(
    page_title="TrendFlow - Trading Strategy Backtester",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Navigation in sidebar
st.sidebar.title("🔗 Navigation")
page_options = ["Home", "Strategy Editor", "View Results", "About"]
if "current_page" not in st.session_state or st.session_state["current_page"] not in page_options:
    st.session_state["current_page"] = "Home"

page = st.sidebar.radio(
    "Select Page",
    page_options,
    index=page_options.index(st.session_state["current_page"])
)

if page != st.session_state["current_page"]:
    st.session_state["current_page"] = page

# Page routing
if page == "Home":
    st.title("📈 TrendFlow - Trading Strategy Backtester")
    st.markdown("""
    Welcome to TrendFlow! A powerful platform to backtest your trading strategies.
    
    ### Features
    - 📊 **Multiple Indicators**: Moving Averages, Volume, RSI, MACD
    - 🔄 **Flexible Strategy Rules**: Define custom entry and exit conditions
    - 💾 **Save Strategies**: Store your strategies and reuse them anytime
    - 📉 **Comprehensive Metrics**: Sharpe Ratio, Max Drawdown, Win Rate, and more
    - 📈 **Visual Results**: Interactive charts and trade-by-trade breakdown
    
    ### Quick Start
    1. Go to **Strategy Editor** to create a new strategy
    2. Configure your indicators and entry/exit conditions
    3. Run the backtest to see historical performance
    4. Check **View Results** to analyze the performance metrics
    5. Save your strategy for future use
    
    ### Supported Indicators
    - **Moving Averages**: SMA, EMA, WMA (customizable periods)
    - **Volume**: Volume moving average and ratio
    - **RSI**: Relative Strength Index (default 14-period)
    - **MACD**: Moving Average Convergence Divergence
    
    ### Example Use Cases
    - MA Crossover: Buy when 10-day MA crosses above 30-day MA
    - Mean Reversion: Buy when RSI < 30, sell when RSI > 70
    - Trend Following: Buy on MACD histogram crossover
    """)

elif page == "Strategy Editor":
    # Import here to avoid issues with page structure
    from pages.strategy_editor import show_editor
    show_editor()

elif page == "View Results":
    from pages.results_viewer import show_results
    show_results()

elif page == "About":
    st.title("About TrendFlow")
    st.markdown("""
    ## TrendFlow - Trading Strategy Backtesting Platform
    
    TrendFlow is a Python-based backtesting framework designed to help traders and investors
    test their strategies against historical market data.
    
    ### Technology
    - **Language**: Python 3
    - **Web Framework**: Streamlit
    - **Data Source**: yfinance
    - **Analysis**: Pandas, NumPy
    - **Visualization**: Plotly
    
    ### Key Components
    
    **Indicators Module** (`trendflow.indicators`)
    - Extensible indicator system with base class
    - Built-in indicators: MA, Volume, RSI, MACD
    - Easy to add custom indicators
    
    **Data Module** (`trendflow.data`)
    - Fetches real market data via yfinance
    - Caches data locally to optimize API calls
    - Supports stocks and cryptocurrencies
    
    **Backtest Engine** (`trendflow.backtest`)
    - Vectorized backtesting for performance
    - Comprehensive metrics: Sharpe, Sortino, Max Drawdown, etc.
    - Commission support
    
    **Strategy System** (`trendflow.strategies`)
    - JSON-based strategy configuration
    - Strategy persistence (save/load)
    - Condition evaluation engine
    
    ### Disclaimer
    This tool is for educational and research purposes only. Past performance does not 
    guarantee future results. Always do your own research and consult with a financial 
    advisor before making investment decisions.
    
    ### License
    MIT License - See LICENSE file for details
    """)
