# ichiV4 Buy-Only Optimization Summary (fee=0.0025)

## Decision
- Keep baseline parameters in ichiV4.
- Do not promote ichiV4BuyOpt parameters to production.

## Scope
- Strategy: ichiV4 (baseline) vs ichiV4BuyOpt (buy-only optimized).
- Backtest range: 20240101-20260131.
- Fee setting: 0.0025 (strict/high-cost assumption).

## Final Comparison (highest fee)
- Baseline result: user_data/backtest_results/backtest-result-2026-04-02_06-10-39.zip
- Re-optimized result: user_data/backtest_results/backtest-result-2026-04-02_07-57-56.zip

| Metric | Baseline ichiV4 | Re-optimized ichiV4BuyOpt | Delta (opt - base) |
|---|---:|---:|---:|
| total_trades | 18142 | 17812 | -330 |
| winrate | 0.8030537 | 0.8038401 | +0.0007864 |
| profit_total_abs (USDT) | 27985.2214 | 27500.5594 | -484.6620 |
| profit_total | 279.8522 | 275.0056 | -4.8466 |
| cagr | 13.9406 | 13.8164 | -0.1242 |
| sharpe | 358.4213 | 351.5530 | -6.8684 |
| sortino | 479.0769 | 467.3095 | -11.7674 |
| calmar | 203551.3204 | 196620.4353 | -6930.8852 |
| sqn | 105.9931 | 104.9205 | -1.0726 |
| profit_factor | 5.0758 | 5.0688 | -0.0070 |
| max_drawdown_account | 0.0034516 | 0.0035114 | +0.0000598 |
| max_relative_drawdown | 0.1977002 | 0.1978042 | +0.0001041 |
| rejected_signals | 1618 | 1604 | -14 |

## Hyperopt Outcome
- Hyperopt log: logs/ichiV4BuyOpt_hyperopt_buy_fee025.log
- Result artifact: user_data/hyperopt_results/strategy_ichiV4BuyOpt_2026-04-02_06-40-58.fthypt
- Best buy params:
  - buy_fan_magnitude_shift_value: 2
  - buy_min_fan_magnitude_gain: 1.002
  - buy_trend_above_senkou_level: 2
  - buy_trend_bullish_level: 6
  - leverage_long_value: 5

## Conclusion
- Fee-aligned re-optimization fixed the earlier collapse under high fees.
- However, baseline still has better profit and risk-adjusted metrics.
- Baseline ichiV4 remains the recommended configuration.
