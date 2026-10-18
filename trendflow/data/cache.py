import os
import pandas as pd
from pathlib import Path
from datetime import datetime
from trendflow.data.fetcher import fetch_data as fetch_data_from_api


class DataCache:
    """Manages local caching of market data to avoid repeated API calls."""

    def __init__(self, cache_dir: str = ".cache/market_data"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _get_cache_path(self, ticker: str, start_date: str, end_date: str) -> Path:
        """Generate cache file path based on ticker and date range."""
        cache_file = f"{ticker}_{start_date}_{end_date}.csv"
        return self.cache_dir / cache_file

    def _is_cache_valid(self, cache_path: Path, max_age_hours: int = 24) -> bool:
        """Check if cached file exists and is fresh enough."""
        if not cache_path.exists():
            return False
        
        file_age_hours = (datetime.now() - datetime.fromtimestamp(
            cache_path.stat().st_mtime
        )).total_seconds() / 3600
        
        return file_age_hours < max_age_hours

    def get(self, ticker: str, start_date: str, end_date: str, 
            force_refresh: bool = False, max_age_hours: int = 24) -> pd.DataFrame:
        """
        Get market data with caching.
        
        Args:
            ticker: Stock ticker symbol (e.g., 'AAPL')
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            force_refresh: If True, always fetch fresh data
            max_age_hours: Max age of cached data in hours
            
        Returns:
            DataFrame with OHLCV data
        """
        cache_path = self._get_cache_path(ticker, start_date, end_date)
        
        # Try to load from cache if valid and not forcing refresh
        if not force_refresh and self._is_cache_valid(cache_path, max_age_hours):
            try:
                data = pd.read_csv(cache_path, index_col=0, parse_dates=True)
                print(f"Loaded {ticker} from cache")
                return data
            except Exception as e:
                print(f"Failed to load cache: {e}, fetching fresh data")
        
        # Fetch fresh data from API
        print(f"Fetching fresh data for {ticker}")
        data = fetch_data_from_api(ticker, start_date, end_date)
        
        # Save to cache
        try:
            data.to_csv(cache_path)
            print(f"Cached data for {ticker} to {cache_path}")
        except Exception as e:
            print(f"Failed to cache data: {e}")
        
        return data

    def clear_cache(self, ticker: str = None, start_date: str = None, 
                    end_date: str = None) -> None:
        """
        Clear cache files.
        
        Args:
            ticker: If specified, only clear cache for this ticker
            start_date: If specified (with ticker), only clear specific date range
            end_date: If specified (with ticker), only clear specific date range
        """
        if ticker is None:
            # Clear entire cache
            import shutil
            shutil.rmtree(self.cache_dir)
            self.cache_dir.mkdir(parents=True, exist_ok=True)
            print(f"Cleared all cached data")
        elif start_date is not None and end_date is not None:
            # Clear specific cache file
            cache_path = self._get_cache_path(ticker, start_date, end_date)
            if cache_path.exists():
                cache_path.unlink()
                print(f"Cleared cache for {ticker} ({start_date} to {end_date})")
        else:
            # Clear all cache for a ticker
            for cache_file in self.cache_dir.glob(f"{ticker}_*.csv"):
                cache_file.unlink()
            print(f"Cleared all cache for {ticker}")


# Default global cache instance
_default_cache = DataCache()


def get_market_data(ticker: str, start_date: str, end_date: str,
                   force_refresh: bool = False, cache: DataCache = None) -> pd.DataFrame:
    """
    Convenience function to get market data with caching.
    
    Args:
        ticker: Stock ticker symbol
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        force_refresh: If True, always fetch fresh data
        cache: Custom DataCache instance. If None, uses default.
        
    Returns:
        DataFrame with OHLCV data
    """
    if cache is None:
        cache = _default_cache
    
    return cache.get(ticker, start_date, end_date, force_refresh=force_refresh)
