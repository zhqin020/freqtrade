status: open
owner: copilot
created: 2026-04-02
target_fix_time: 2026-04-02

# Task

Run ichiV4 stability analysis from 20240101 to current data range using 5-week windows.

# Scope

- Strategy: ichiV4
- Timeframe: 5m
- Window size: 35 days
- Metrics: trade count, trades/day, profit, winrate, Sharpe, Sortino, Profit Factor, drawdown

# Deliverables

- Rolling backtest result summary CSV/JSON
- Stability markdown report under docs/optimization/
- Archived result zips for each window

# Relevant Files

- user_data/config_ichiv4_backtest.json
- user_data/strategies/ichiV1/ichiV4.py
- user_data/strategies/ichiV1/ichiV4.json
