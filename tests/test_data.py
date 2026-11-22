import numpy as np
import pandas as pd
import pytest

from volatility.data import extract_close, log_returns


def test_extract_close_from_flat_columns():
    frame = pd.DataFrame({"Close": [100.0, 101.0], "Volume": [2, 3]})
    assert extract_close(frame).tolist() == [100.0, 101.0]


def test_extract_close_from_yfinance_multiindex():
    cols = pd.MultiIndex.from_tuples([("Close", "^GSPC"), ("Volume", "^GSPC")])
    frame = pd.DataFrame([[100, 2], [101, 3]], columns=cols)
    assert extract_close(frame).tolist() == [100, 101]


def test_log_returns_are_decimal():
    close = pd.Series([100.0, 110.0, 121.0])
    result = log_returns(close)
    assert len(result) == 2
    assert np.allclose(result.to_numpy(), np.log(1.1))


def test_reject_nonpositive_prices():
    with pytest.raises(ValueError):
        log_returns(pd.Series([100.0, 0.0]))
