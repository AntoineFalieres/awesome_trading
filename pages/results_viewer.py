import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from trendflow.strategies import StrategyManager, StrategyExecutor, StrategyExecutionError


def show_results():
    """Display backtest results and analysis."""
    st.title("📊 Backtest Results")
    
    manager = StrategyManager()
    saved_strategies = manager.list()
    
    if not saved_strategies:
        st.info("No saved strategies found. Create one in the Strategy Editor.")
        return
    
    # Strategy selection
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Check if a strategy was selected from editor
        selected_strategy = st.session_state.get("selected_strategy")
        if selected_strategy and selected_strategy in saved_strategies:
            strategy_name = selected_strategy
        else:
            strategy_name = st.selectbox("Select a strategy to backtest", saved_strategies)
    
    with col2:
        run_backtest = st.button("▶️ Run Backtest", use_container_width=True)
    
    if run_backtest or "backtest_results" in st.session_state:
        if "backtest_results" not in st.session_state or st.session_state.get("current_strategy") != strategy_name:
            st.session_state.current_strategy = strategy_name
            
            with st.spinner("Running backtest..."):
                try:
                    strategy = manager.load(strategy_name)
                    executor = StrategyExecutor(strategy)
                    results = executor.execute()
                    st.session_state.backtest_results = results
                    st.session_state.current_strategy = strategy_name
                except StrategyExecutionError as e:
                    st.error(f"❌ Backtest failed: {e}")
                    return
                except FileNotFoundError as e:
                    st.error(f"❌ Strategy not found: {e}")
                    return
                except Exception as e:
                    st.error(f"❌ Unexpected error: {e}")
                    return
        
        results = st.session_state.backtest_results
        
        # Display Results
        st.success("✅ Backtest completed!")
        
        # Performance Metrics
        st.subheader("📈 Performance Metrics")
        
        metrics = results['metrics']
        
        # Create metric columns
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_return = metrics.get('Total Return', 0)
            st.metric(
                "Total Return",
                f"{total_return:.2%}",
                delta=f"{total_return:.2%}"
            )
        
        with col2:
            sharpe = metrics.get('Sharpe Ratio', 0)
            st.metric("Sharpe Ratio", f"{sharpe:.2f}")
        
        with col3:
            max_dd = metrics.get('Max Drawdown', 0)
            st.metric("Max Drawdown", f"{max_dd:.2%}")
        
        with col4:
            win_rate = metrics.get('Win Rate', 0)
            st.metric("Win Rate", f"{win_rate:.2%}")
        
        # Additional Metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            ann_return = metrics.get('Annualized Return', 0)
            st.metric("Annualized Return", f"{ann_return:.2%}")
        
        with col2:
            sortino = metrics.get('Sortino Ratio', 0)
            st.metric("Sortino Ratio", f"{sortino:.2f}")
        
        with col3:
            volatility = metrics.get('Annualized Volatility', 0)
            st.metric("Annualized Volatility", f"{volatility:.2%}")
        
        with col4:
            num_trades = metrics.get('Total Trades', 0)
            st.metric("Total Trades", int(num_trades) if num_trades else 0)
        
        # Comparison to Buy & Hold
        if 'Buy & Hold Return' in metrics:
            col1, col2 = st.columns(2)
            with col1:
                bh_return = metrics['Buy & Hold Return']
                st.metric("Buy & Hold Return", f"{bh_return:.2%}")
            with col2:
                excess = metrics['Excess Return vs B&H']
                color = "normal" if excess > 0 else "inverse"
                st.metric(
                    "Excess Return vs B&H",
                    f"{excess:.2%}",
                    delta_color=color
                )
        
        st.divider()
        
        # Equity Curve Chart
        st.subheader("💹 Equity Curve")
        
        data = results['data']
        
        fig = go.Figure()
        
        # Strategy equity curve
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data['equity_curve'],
            name='Strategy',
            line=dict(color='#1f77b4', width=2),
            fill='tozeroy'
        ))
        
        # Buy and hold equity curve
        if 'buy_hold_equity' in data.columns:
            fig.add_trace(go.Scatter(
                x=data.index,
                y=data['buy_hold_equity'],
                name='Buy & Hold',
                line=dict(color='#ff7f0e', width=2, dash='dash')
            ))
        
        fig.update_layout(
            title="Strategy vs Buy & Hold Performance",
            xaxis_title="Date",
            yaxis_title="Equity ($)",
            hovermode='x unified',
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.divider()
        
        # Drawdown Chart
        st.subheader("📉 Drawdown Analysis")
        
        # Calculate drawdown
        equity = data['equity_curve']
        running_max = equity.expanding().max()
        drawdown = (equity - running_max) / running_max
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=data.index,
            y=drawdown * 100,
            name='Drawdown',
            fill='tozeroy',
            line=dict(color='#d62728'),
            fillcolor='rgba(214, 39, 40, 0.3)'
        ))
        
        fig.update_layout(
            title="Drawdown Over Time",
            xaxis_title="Date",
            yaxis_title="Drawdown (%)",
            hovermode='x',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.divider()
        
        # Trade-by-Trade Breakdown
        st.subheader("🔄 Trade-by-Trade Breakdown")
        
        trades = results['trades']
        
        if trades:
            trades_df = pd.DataFrame(trades)
            trades_df['entry_date'] = pd.to_datetime(trades_df['entry_date']).dt.strftime('%Y-%m-%d')
            trades_df['exit_date'] = pd.to_datetime(trades_df['exit_date']).dt.strftime('%Y-%m-%d')
            trades_df['entry_price'] = trades_df['entry_price'].apply(lambda x: f"${x:.2f}")
            trades_df['exit_price'] = trades_df['exit_price'].apply(lambda x: f"${x:.2f}")
            trades_df['pnl'] = trades_df['pnl'].apply(lambda x: f"${x:.2f}")
            trades_df['pnl_pct'] = trades_df['pnl_pct'].apply(lambda x: f"{x:.2f}%")
            
            st.dataframe(trades_df, use_container_width=True)
            
            st.info(f"Total trades executed: {len(trades)}")
        else:
            st.info("No completed trades in this period.")
        
        st.divider()
        
        # Daily Returns Distribution
        st.subheader("📊 Daily Returns Distribution")
        
        returns = data['strategy_returns'].dropna() * 100
        
        fig = go.Figure()
        fig.add_trace(go.Histogram(
            x=returns,
            nbinsx=50,
            name='Daily Returns',
            marker_color='#2ca02c'
        ))
        
        fig.update_layout(
            title="Distribution of Daily Strategy Returns",
            xaxis_title="Daily Return (%)",
            yaxis_title="Frequency",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Summary Statistics Table
        st.subheader("📋 Summary Statistics")
        
        summary_stats = {
            'Metric': [
                'Total Return',
                'Annualized Return',
                'Annualized Volatility',
                'Sharpe Ratio',
                'Sortino Ratio',
                'Max Drawdown',
                'Win Rate',
                'Positive Days',
                'Negative Days',
                'Total Trade Days'
            ],
            'Value': [
                f"{metrics.get('Total Return', 0):.2%}",
                f"{metrics.get('Annualized Return', 0):.2%}",
                f"{metrics.get('Annualized Volatility', 0):.2%}",
                f"{metrics.get('Sharpe Ratio', 0):.2f}",
                f"{metrics.get('Sortino Ratio', 0):.2f}",
                f"{metrics.get('Max Drawdown', 0):.2%}",
                f"{metrics.get('Win Rate', 0):.2%}",
                f"{int(metrics.get('Positive Days', 0))}",
                f"{int(metrics.get('Negative Days', 0))}",
                f"{int(metrics.get('Total Trade Days', 0))}"
            ]
        }
        
        summary_df = pd.DataFrame(summary_stats)
        st.dataframe(summary_df, use_container_width=True, hide_index=True)
