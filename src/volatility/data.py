"""Price-data normalization and return calculation.

No network calls are made on import. All returns in this module are decimal;
models that require percent returns should multiply by 100 explicitly.
"""

import numpy as np
import pandas as pd


def extract_close(prices: pd.DataFrame, ticker: str = "^GSPC") -> pd.Series:
    """Extract a one-dimensional Close price series from yfinance output.

    Supports both flat and two-level MultiIndex columns, including versions
    that place the ticker at either column level.
    """
    if not isinstance(prices, pd.DataFrame) or prices.empty:
        raise ValueError("prices must be a non-empty DataFrame")

    if isinstance(prices.columns, pd.MultiIndex):
        candidates = [
            c for c in prices.columns
            if "Close" in c and ticker in c
        ]
        if not candidates:
            candidates = [c for c in prices.columns if "Close" in c]
        if len(candidates) != 1:
            raise ValueError("Cannot uniquely identify Close column for ticker")
        close = prices[candidates[0]]
    else:
        if "Close" not in prices.columns:
            raise ValueError("Missing Close price column")
        close = prices["Close"]

    if not isinstance(close, pd.Series):
        raise ValueError("Expected a one-dimensional Close series")
    close = pd.to_numeric(close, errors="coerce").sort_index()
    close = close.loc[~close.index.duplicated(keep="last")].dropna()
    if close.empty or not np.isfinite(close.to_numpy()).all() or (close <= 0).any():
        raise ValueError("Close prices must be finite and positive")
    return close.rename("close")


def log_returns(close: pd.Series) -> pd.Series:
    """Compute decimal daily log returns; first NA observation is removed."""
    if not isinstance(close, pd.Series) or close.empty:
        raise ValueError("close must be a non-empty Series")
    if not np.isfinite(close.to_numpy()).all() or (close <= 0).any():
        raise ValueError("close must contain finite positive prices")
    returns = np.log(close / close.shift(1)).dropna()
    return returns.rename("log_return")
