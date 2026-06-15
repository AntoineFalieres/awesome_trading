import streamlit as st
import json
from trendflow.strategies import Strategy, StrategyManager
import datetime


def show_editor():
    """Display the strategy editor interface."""
    st.title("📝 Strategy Editor")
    
    st.markdown("""
    Create and configure your trading strategy here. Define indicators, entry conditions, and exit conditions.
    """)
    
    # Strategy Manager
    manager = StrategyManager()
    
    # Tabs for Create/Edit vs Load
    tab1, tab2 = st.tabs(["Create New Strategy", "Load Existing Strategy"])
    
    with tab1:
        show_create_strategy(manager)
    
    with tab2:
        show_load_strategy(manager)


def show_create_strategy(manager):
    """Show form to create a new strategy."""
    st.subheader("Create New Strategy")
    
    with st.form("strategy_form", clear_on_submit=True):
        # Basic Info
        col1, col2 = st.columns(2)
        with col1:
            strategy_name = st.text_input(
                "Strategy Name",
                help="Unique name for your strategy (e.g., 'MA Crossover 10-30')"
            )
            symbol = st.text_input(
                "Symbol",
                value="AAPL",
                help="Stock ticker or crypto symbol (e.g., AAPL, BTC-USD)"
            )
        
        with col2:
            description = st.text_area(
                "Description",
                help="Brief description of what this strategy does",
                height=100
            )
        
        # Date Range
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input(
                "Start Date",
                value=datetime.date.today() - datetime.timedelta(days=365)
            )
        with col2:
            end_date = st.date_input(
                "End Date",
                value=datetime.date.today()
            )
        
        st.divider()
        
        # Indicators Section
        st.subheader("📊 Indicators")
        
        indicators = []
        num_indicators = st.number_input("Number of Indicators", min_value=1, max_value=5, value=1)
        
        for i in range(int(num_indicators)):
            with st.expander(f"Indicator {i+1}", expanded=(i==0)):
                ind_name = st.text_input(f"Indicator {i+1} Name", key=f"ind_name_{i}")
                ind_type = st.selectbox(
                    f"Indicator {i+1} Type",
                    ["moving_average", "volume", "rsi", "macd"],
                    key=f"ind_type_{i}"
                )
                
                params = {}
                if ind_type == "moving_average":
                    col1, col2 = st.columns(2)
                    with col1:
                        params["period"] = st.number_input(
                            f"Period {i+1}",
                            value=10,
                            min_value=2,
                            key=f"ma_period_{i}"
                        )
                    with col2:
                        params["ma_type"] = st.selectbox(
                            f"MA Type {i+1}",
                            ["sma", "ema", "wma"],
                            key=f"ma_type_{i}"
                        )
                
                elif ind_type == "rsi":
                    params["period"] = st.number_input(
                        f"RSI Period {i+1}",
                        value=14,
                        min_value=2,
                        key=f"rsi_period_{i}"
                    )
                
                elif ind_type == "macd":
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        params["fast"] = st.number_input("Fast", value=12, key=f"macd_fast_{i}")
                    with col2:
                        params["slow"] = st.number_input("Slow", value=26, key=f"macd_slow_{i}")
                    with col3:
                        params["signal"] = st.number_input("Signal", value=9, key=f"macd_signal_{i}")
                
                if ind_name and ind_type:
                    indicators.append({
                        "name": ind_name,
                        "type": ind_type,
                        "params": params
                    })
        
        st.divider()
        
        # Entry Conditions
        st.subheader("📈 Entry Conditions")
        entry_conditions = []
        num_entries = st.number_input("Number of Entry Conditions", min_value=1, max_value=3, value=1)
        
        indicator_names = [ind["name"] for ind in indicators]
        
        for i in range(int(num_entries)):
            with st.expander(f"Entry Condition {i+1}", expanded=(i==0)):
                cond_type = st.selectbox(
                    f"Condition {i+1} Type",
                    ["crossover", "crossunder", "threshold"],
                    key=f"entry_cond_type_{i}"
                )
                
                cond = {"type": cond_type}
                
                if cond_type == "crossover" or cond_type == "crossunder":
                    col1, col2 = st.columns(2)
                    with col1:
                        cond["fast_indicator"] = st.selectbox(
                            f"Fast Indicator {i+1}",
                            indicator_names,
                            key=f"entry_fast_{i}"
                        )
                    with col2:
                        cond["slow_indicator"] = st.selectbox(
                            f"Slow Indicator {i+1}",
                            indicator_names,
                            key=f"entry_slow_{i}"
                        )
                
                elif cond_type == "threshold":
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        cond["indicator"] = st.selectbox(
                            f"Indicator {i+1}",
                            indicator_names,
                            key=f"entry_thresh_ind_{i}"
                        )
                    with col2:
                        cond["comparison"] = st.selectbox(
                            f"Comparison {i+1}",
                            ["above", "below", "above_or_equal", "below_or_equal"],
                            key=f"entry_comp_{i}"
                        )
                    with col3:
                        cond["value"] = st.number_input(
                            f"Value {i+1}",
                            value=50.0,
                            key=f"entry_value_{i}"
                        )
                
                if all(k in cond for k in ["type"]):
                    entry_conditions.append(cond)
        
        st.divider()
        
        # Exit Conditions
        st.subheader("📉 Exit Conditions")
        exit_conditions = []
        num_exits = st.number_input("Number of Exit Conditions", min_value=1, max_value=3, value=1)
        
        for i in range(int(num_exits)):
            with st.expander(f"Exit Condition {i+1}", expanded=(i==0)):
                cond_type = st.selectbox(
                    f"Exit Condition {i+1} Type",
                    ["crossover", "crossunder", "threshold"],
                    key=f"exit_cond_type_{i}"
                )
                
                cond = {"type": cond_type}
                
                if cond_type == "crossover" or cond_type == "crossunder":
                    col1, col2 = st.columns(2)
                    with col1:
                        cond["fast_indicator"] = st.selectbox(
                            f"Exit Fast Indicator {i+1}",
                            indicator_names,
                            key=f"exit_fast_{i}"
                        )
                    with col2:
                        cond["slow_indicator"] = st.selectbox(
                            f"Exit Slow Indicator {i+1}",
                            indicator_names,
                            key=f"exit_slow_{i}"
                        )
                
                elif cond_type == "threshold":
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        cond["indicator"] = st.selectbox(
                            f"Exit Indicator {i+1}",
                            indicator_names,
                            key=f"exit_thresh_ind_{i}"
                        )
                    with col2:
                        cond["comparison"] = st.selectbox(
                            f"Exit Comparison {i+1}",
                            ["above", "below", "above_or_equal", "below_or_equal"],
                            key=f"exit_comp_{i}"
                        )
                    with col3:
                        cond["value"] = st.number_input(
                            f"Exit Value {i+1}",
                            value=50.0,
                            key=f"exit_value_{i}"
                        )
                
                if all(k in cond for k in ["type"]):
                    exit_conditions.append(cond)
        
        st.divider()
        
        # Backtest Parameters
        st.subheader("⚙️ Backtest Parameters")
        col1, col2 = st.columns(2)
        with col1:
            initial_capital = st.number_input(
                "Initial Capital ($)",
                value=10000,
                min_value=1000,
                step=1000
            )
        with col2:
            commission = st.number_input(
                "Commission (as decimal, e.g., 0.001 for 0.1%)",
                value=0.001,
                min_value=0.0,
                max_value=0.1,
                step=0.0001
            )
        
        st.divider()
        
        # Submit Button
        submitted = st.form_submit_button("✅ Create Strategy", use_container_width=True)
        
        if submitted:
            if not strategy_name or not symbol:
                st.error("Strategy name and symbol are required")
            elif not indicators:
                st.error("At least one indicator is required")
            elif not entry_conditions:
                st.error("At least one entry condition is required")
            elif not exit_conditions:
                st.error("At least one exit condition is required")
            else:
                try:
                    strategy = Strategy(
                        name=strategy_name,
                        symbol=symbol,
                        start_date=start_date.isoformat(),
                        end_date=end_date.isoformat(),
                        description=description,
                        indicators=indicators,
                        entry_conditions=entry_conditions,
                        exit_conditions=exit_conditions,
                        backtest_params={
                            "initial_capital": initial_capital,
                            "commission": commission
                        }
                    )
                    
                    errors = strategy.validate()
                    if errors:
                        st.error(f"Strategy validation failed: {'; '.join(errors)}")
                    else:
                        manager.save(strategy, overwrite=False)
                        st.success(f"✅ Strategy '{strategy_name}' created and saved!")
                        st.info("You can now run this strategy from the home page or execute it here.")
                        
                        # Show strategy preview
                        with st.expander("View Strategy JSON"):
                            st.json(strategy.to_dict())
                
                except FileExistsError as e:
                    st.error(f"Error: {e}")
                except Exception as e:
                    st.error(f"Error creating strategy: {e}")


def show_load_strategy(manager):
    """Show interface to load and edit existing strategies."""
    st.subheader("Load & Edit Existing Strategy")
    
    saved_strategies = manager.list()
    
    if not saved_strategies:
        st.info("No saved strategies found. Create one in the 'Create New Strategy' tab.")
    else:
        strategy_name = st.selectbox("Select a strategy", saved_strategies)
        
        if strategy_name:
            strategy = manager.load(strategy_name)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("📊 Run Backtest", use_container_width=True):
                    st.session_state.selected_strategy = strategy_name
                    st.switch_page("pages/results_viewer.py")
            
            with col2:
                if st.button("📋 View JSON", use_container_width=True):
                    st.session_state.show_json = True
            
            with col3:
                if st.button("🗑️ Delete", use_container_width=True):
                    manager.delete(strategy_name)
                    st.success(f"Deleted strategy: {strategy_name}")
                    st.rerun()
            
            if st.session_state.get("show_json"):
                st.json(strategy.to_dict())
