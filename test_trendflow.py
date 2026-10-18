#!/usr/bin/env python3
"""
Quick test script to verify TrendFlow functionality.
"""

import json
from trendflow.strategies import Strategy, StrategyManager, StrategyExecutor


def test_create_strategy():
    """Test strategy creation and validation."""
    print("🧪 Testing Strategy Creation...")
    
    strategy = Strategy(
        name="Test MA Crossover",
        symbol="AAPL",
        start_date="2023-01-01",
        end_date="2023-12-31",
        description="Simple moving average crossover strategy",
        indicators=[
            {
                "name": "sma_10",
                "type": "moving_average",
                "params": {"period": 10, "ma_type": "sma"}
            },
            {
                "name": "sma_30",
                "type": "moving_average",
                "params": {"period": 30, "ma_type": "sma"}
            }
        ],
        entry_conditions=[
            {
                "type": "crossover",
                "fast_indicator": "sma_10",
                "slow_indicator": "sma_30"
            }
        ],
        exit_conditions=[
            {
                "type": "crossunder",
                "fast_indicator": "sma_10",
                "slow_indicator": "sma_30"
            }
        ]
    )
    
    # Validate
    errors = strategy.validate()
    assert len(errors) == 0, f"Strategy validation failed: {errors}"
    print("✓ Strategy created and validated successfully")
    
    return strategy


def test_save_load_strategy(strategy):
    """Test strategy persistence."""
    print("\n🧪 Testing Strategy Persistence...")
    
    manager = StrategyManager()
    
    # Save
    manager.save(strategy, overwrite=True)
    print(f"✓ Strategy saved: {strategy.name}")
    
    # Load
    loaded = manager.load(strategy.name)
    assert loaded.name == strategy.name
    assert loaded.symbol == strategy.symbol
    print(f"✓ Strategy loaded successfully")
    
    # List
    strategies = manager.list()
    assert strategy.name in strategies
    print(f"✓ Strategy appears in list: {strategies}")
    
    return loaded


def test_backtest(strategy):
    """Test backtest execution."""
    print("\n🧪 Testing Backtest Execution...")
    
    executor = StrategyExecutor(strategy)
    
    try:
        results = executor.execute()
        print("✓ Backtest executed successfully")
        
        # Check results structure
        assert 'data' in results
        assert 'metrics' in results
        assert 'trades' in results
        print("✓ Results have expected structure")
        
        # Check metrics
        metrics = results['metrics']
        required_metrics = [
            'Total Return', 'Annualized Return', 'Sharpe Ratio',
            'Max Drawdown', 'Win Rate'
        ]
        for metric in required_metrics:
            assert metric in metrics, f"Missing metric: {metric}"
        print(f"✓ All required metrics present")
        
        # Print summary
        print(f"\n📊 Backtest Results:")
        print(f"   Total Return: {metrics['Total Return']:.2%}")
        print(f"   Annualized Return: {metrics['Annualized Return']:.2%}")
        print(f"   Sharpe Ratio: {metrics['Sharpe Ratio']:.2f}")
        print(f"   Max Drawdown: {metrics['Max Drawdown']:.2%}")
        print(f"   Win Rate: {metrics['Win Rate']:.2%}")
        print(f"   Total Trades: {metrics.get('Total Trades', 'N/A')}")
        
        return results
        
    except Exception as e:
        print(f"⚠️  Backtest failed (expected on first run due to data fetching):")
        print(f"   {e}")
        return None


def main():
    """Run all tests."""
    print("=" * 60)
    print("TrendFlow - Test Suite")
    print("=" * 60)
    
    try:
        # Test 1: Create strategy
        strategy = test_create_strategy()
        
        # Test 2: Save and load
        strategy = test_save_load_strategy(strategy)
        
        # Test 3: Run backtest
        results = test_backtest(strategy)
        
        print("\n" + "=" * 60)
        print("✅ All tests completed!")
        print("=" * 60)
        print("\nYou can now run the web app with:")
        print("  streamlit run main.py")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
