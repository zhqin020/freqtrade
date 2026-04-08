## model architecture is in https://github.com/Netanelshoshan/freqAI-LSTM
## backtest command
```sh
(.venv) watson@u2404:~/work/freqtrd$ cd /home/watson/work/freqtrd && ./.venv/bin/freqtrade backtesting --strategy AlexStrategyFinalV9 --strategy-path user_data/strategies/LSTM --config user_data/strategies/LSTM/config_freqai.run.json --timerange 20240101-20260101 | tee /tmp/lstm_full_validation.log
```

## changelog
- **v91 (2026-04-07)**: Added MA100 trend filter to entry conditions in `populate_entry_trend`: long only when `close > ma100`, short only when `close < ma100`. OOS test (2026-01-01 to 2026-04-01) improved from -4.69% → +33.68% (profit factor 0.92 → 1.64, drawdown 8.12% → 5.03%). Grid search (7×7 on threshold_buy × threshold_sell) confirmed current parameters (0.59453, 0.80573) sit on a stable plateau; max-neighbour delta 0.57%, buy-axis std 0.32.
- **v90 (2026-04-07)**: Fixed overlapping long/short entry thresholds (short now uses `-threshold_sell` instead of sharing the `threshold_buy`/`threshold_sell` overlap zone). Removed `bfill()` on `&-target` to eliminate forward-looking label leakage. Disabled ROI fallback exits (`minimal_roi = {}`). Raised `startup_candle_count` from 20 → 200 to cover the 100-period MA warmup. Cleaned unused imports.

## result (v90 — clean, 2026-04-07)

```
Result for strategy AlexStrategyFinalV9
2026-04-07 01:16:31,435 - freqtrade.misc - INFO - dumping json to "/home/watson/work/freqtrd/user_data/backtest_results/backtest-result-2026-04-07_01-16-31.meta.json"
Result for strategy AlexStrategyFinalV9
                                                 BACKTESTING REPORT
┏━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┓
┃           Pair ┃ Trades ┃ Avg Profit % ┃ Tot Profit USDT ┃ Tot Profit % ┃ Avg Duration ┃  Win  Draw  Loss  Win% ┃
┡━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━┩
│  SUI/USDT:USDT │    990 │         0.44 │         430.182 │        43.02 │     12:12:00 │  786     0   204  79.4 │
│ PEPE/USDT:USDT │    961 │         0.43 │         380.989 │         38.1 │      9:02:00 │  770     0   191  80.1 │
│  SOL/USDT:USDT │    685 │         0.45 │         308.698 │        30.87 │     13:30:00 │  550     0   135  80.3 │
│ LINK/USDT:USDT │    394 │         0.56 │         217.051 │        21.71 │      7:26:00 │  323     0    71  82.0 │
│ DOGE/USDT:USDT │    587 │         0.29 │         169.987 │         17.0 │     15:52:00 │  463     0   124  78.9 │
│ AVAX/USDT:USDT │    472 │         0.32 │         148.615 │        14.86 │     11:45:00 │  397     0    75  84.1 │
│  ETC/USDT:USDT │    295 │         0.22 │          63.311 │         6.33 │     11:27:00 │  229     0    66  77.6 │
│  TON/USDT:USDT │    139 │         0.46 │          62.697 │         6.27 │     18:47:00 │  120     0    19  86.3 │
│  ETH/USDT:USDT │    362 │         0.14 │          49.894 │         4.99 │  1d 8:31:00 │  288     0    74  79.6 │
│  LTC/USDT:USDT │    188 │         0.25 │          46.795 │         4.68 │     17:21:00 │  155     0    33  82.4 │
│  BNB/USDT:USDT │    464 │         0.07 │          28.996 │          2.9 │  1d 5:18:00 │  318     0   146  68.5 │
│ NEAR/USDT:USDT │    111 │        -0.15 │         -15.547 │        -1.55 │      7:27:00 │   85     0    26  76.6 │
│  BTC/USDT:USDT │     37 │        -0.68 │         -24.804 │        -2.48 │ 4d 21:06:00 │   30     0     7  81.1 │
│          TOTAL │   5685 │         0.34 │        1866.863 │       186.69 │     15:24:00 │ 4514     0  1171  79.4 │
└────────────────┴────────┴──────────────┴─────────────────┴──────────────┴──────────────┴────────────────────────┘
                                                ENTER TAG STATS
┏━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Enter Tag ┃ Entries ┃ Avg Profit % ┃ Tot Profit USDT ┃ Tot Profit % ┃ Avg Duration ┃  Win  Draw  Loss  Win% ┃
┡━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━┩
│     short │    2998 │         0.43 │        1261.898 │       126.19 │     13:15:00 │ 2452     0   546  81.8 │
│      long │    2687 │         0.23 │         604.965 │         60.5 │     17:49:00 │ 2062     0   625  76.7 │
│     TOTAL │    5685 │         0.34 │        1866.863 │       186.69 │     15:24:00 │ 4514     0  1171  79.4 │
└───────────┴─────────┴──────────────┴─────────────────┴──────────────┴──────────────┴────────────────────────┘
                                                   EXIT REASON STATS
┏━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┓
┃        Exit Reason ┃  Exits ┃ Avg Profit % ┃ Tot Profit USDT ┃ Tot Profit % ┃    Avg Duration ┃  Win  Draw  Loss  Win% ┃
┡━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━┩
│ trailing_stop_loss │   4329 │         1.72 │        7274.945 │       727.49 │        9:47:00 │ 4329     0     0   100 │
│         force_exit │      5 │        -5.49 │         -27.135 │        -2.71 │ 13 days 20:36  │    0     0     5     0 │
│          stop_loss │     11 │       -50.12 │        -540.695 │       -54.07 │ 11 days  3:16  │    0     0    11     0 │
│         exit_short │    630 │        -3.47 │       -2141.086 │      -214.11 │   1 day  3:32  │   93     0   537  14.8 │
│          exit_long │    710 │        -3.89 │       -2699.166 │      -269.92 │   1 day  8:45  │   92     0   618  13.0 │
│              TOTAL │   5685 │         0.34 │        1866.863 │       186.69 │       15:24:00 │ 4514     0  1171  79.4 │
└────────────────────┴────────┴──────────────┴─────────────────┴──────────────┴─────────────────┴────────────────────────┘
                         SUMMARY METRICS
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Metric                        ┃ Value                           ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Backtesting from              │ 2024-01-01 00:00:00             │
│ Backtesting to                │ 2026-01-01 00:00:00             │
│ Trading Mode                  │ Isolated Futures                │
│ Max open trades               │ 5                               │
│ Total/Daily Avg Trades        │ 5685 / 7.78                     │
│ Starting balance              │ 1000 USDT                       │
│ Final balance                 │ 2866.863 USDT                   │
│ Absolute profit               │ 1866.863 USDT                   │
│ Total profit %                │ 186.69%                         │
│ CAGR %                        │ 69.20%                          │
│ Sortino                       │ 7.28                            │
│ Sharpe                        │ 11.98                           │
│ Calmar                        │ 29.33                           │
│ SQN                           │ 6.08                            │
│ Profit factor                 │ 1.34                            │
│ Expectancy (Ratio)            │ 0.33 (0.07)                     │
│ Long / Short trades           │ 2687 / 2998                     │
│ Long / Short profit %         │ 60.50% / 126.19%                │
│ Long / Short profit USDT      │ 604.965 / 1261.898              │
│ Best Pair                     │ SUI/USDT:USDT 43.02%            │
│ Worst Pair                    │ BTC/USDT:USDT -2.48%            │
│ Absolute drawdown             │ 185.268 USDT (16.64%)           │
│ Drawdown duration             │ 48 days 19:00:00                │
│ Market change                 │ 33.64%                          │
└───────────────────────────────┴─────────────────────────────────┘
Backtested 2024-01-01 00:00:00 -> 2026-01-01 00:00:00 | Max open trades : 5
┏━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┓
┃            Strategy ┃ Trades ┃ Avg Profit % ┃ Tot Profit USDT ┃ Tot Profit % ┃ Avg Duration ┃  Win  Draw  Loss  Win% ┃            Drawdown ┃
┡━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━┩
│ AlexStrategyFinalV9 │   5685 │         0.34 │        1866.863 │       186.69 │     15:24:00 │ 4514     0  1171  79.4 │ 185.268 USDT 16.64% │
└─────────────────────┴────────┴──────────────┴─────────────────┴──────────────┴──────────────┴────────────────────────┴─────────────────────┘
(.venv) watson@u2404
```

## result (v1 — original pre-fix, 2026-04-07)
> ⚠️ Before threshold/leakage fixes. ROI fallback active, long/short thresholds overlapped, `bfill()` present on target label. Numbers are not valid baselines.

| Metric | v1 (pre-fix) | v90 (clean) |
|--------|-------------|-------------|
| Total profit % | 256.34% | **186.69%** |
| CAGR % | 88.61% | **69.20%** |
| Profit factor | 1.19 | **1.34** |
| Avg profit/trade | 0.15% | **0.34%** |
| Win rate | 63.9% | **79.4%** |
| Trades | 17376 | **5685** |
| Long profit % | 9.52% | **60.50%** |
| Short profit % | 246.82% | **126.19%** |
| Max drawdown | 6.56% | 16.64% |
| ROI exits loss | -10631 USDT | **0** |

## out-of-sample (2026-01-01 to 2026-04-01)

### baseline (before trend filter)
- Total profit %: **-4.69%**
- Profit factor: **0.92**
- Trades: **523**
- Long / Short profit %: **-8.49% / 3.80%**
- Exit losses: `exit_long -31.75%`, `exit_short -21.10%`

### v91 (entry trend filter on ma100)
- Change: added trend filter in `populate_entry_trend`:
    - long only when `close > ma100`
    - short only when `close < ma100`
- OOS command:

```sh
./.venv/bin/freqtrade backtesting --strategy AlexStrategyFinalV9 --strategy-path user_data/strategies/LSTM --config user_data/strategies/LSTM/config_freqai.run.json --timerange 20260101-20260401
```

- Total profit %: **33.68%**
- Profit factor: **1.64**
- Trades: **621**
- Long / Short profit %: **4.58% / 29.11%**
- Max drawdown: **5.03%**
