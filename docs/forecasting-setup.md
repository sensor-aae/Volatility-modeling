# Forecasting study setup

Status: **setup only**. This branch does not yet contain rolling forecasts or backtests.

## Research design (initial defaults; revise before evaluating)

- Market data: Yahoo Finance S&P 500 index (`^GSPC`), daily Close with `auto_adjust=True`.
- Data period: 2015-01-01 to 2026-11-01 (**end exclusive**); date window is configurable.
- Model development: observations before 2020-01-01. Out-of-sample: observations from 2020-01-01 onward.
- One-step-ahead forecasts; expanding window and approximate monthly refits (every 21 trading observations) are initial assumptions, not yet implemented.
- All data utilities produce decimal log returns; `arch` models will use returns in **percentage points** (multiply by 100) when implemented. Conditional variances must be converted consistently.
- Evaluate with squared returns as an imperfect proxy for latent daily variance; QLIKE and MSE will be implemented later.
- GARCH Normal, GARCH Student-t, GJR Student-t, EWMA, and rolling historical variance will be compared; this file does not imply any is best.

## Local setup

```bash
git clone https://github.com/sensor-aae/Volatility-modeling.git
cd Volatility-modeling
git switch feature/volatility-forecasting-setup
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e '.[dev]'
pytest -q
```

For Windows PowerShell: activate with `.venv\\Scripts\\Activate.ps1`.

## Next research implementation
1. Download and audit price history; record data provenance and snapshot date.
2. Implement training/test partition with strict no-look-ahead checks.
3. Estimate expanding-window forecasts with configurable refit cadence and simple baselines.
4. Add diagnostics, forecast evaluation, and VaR backtests.

Tracking issue: https://github.com/sensor-aae/Volatility-modeling/issues/1
