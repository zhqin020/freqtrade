## backtesting
./.venv/bin/freqtrade backtesting --strategy NostalgiaForInfinityNextGen  --config  user_data/strategies/NostalgiaForInfinityNextGen/config_NFI_NextGen.json  --timerange 20240101-20260401


2026-04-07 15:41:23,555 - freqtrade.optimize.backtesting - INFO - Backtesting with data from 2024-01-01 00:00:00 up to 2026-04-01 00:00:00 
(821 days).
2026-04-07 15:41:44,980 - freqtrade.misc - INFO - dumping json to 
"/home/watson/work/freqtrd/user_data/backtest_results/backtest-result-2026-04-07_15-41-44.meta.json"
Result for strategy NostalgiaForInfinityNextGen
                                                BACKTESTING REPORT                                                 
┏━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┓
┃           Pair ┃ Trades ┃ Avg Profit % ┃ Tot Profit USDT ┃ Tot Profit % ┃ Avg Duration ┃  Win  Draw  Loss  Win% ┃
┡━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━┩
│  LTC/USDT:USDT │      4 │         1.81 │           3.307 │         3.31 │      0:02:00 │    4     0     0   100 │
│  SUI/USDT:USDT │      4 │         1.64 │           3.232 │         3.23 │      0:41:00 │    4     0     0   100 │
│ LINK/USDT:USDT │      3 │         0.74 │           1.113 │         1.11 │      2:31:00 │    2     1     0   100 │
│ DOGE/USDT:USDT │      2 │         1.01 │           1.001 │          1.0 │      7:27:00 │    1     1     0   100 │
│  XRP/USDT:USDT │      2 │          1.0 │           0.995 │          1.0 │      2:47:00 │    1     1     0   100 │
│  ETC/USDT:USDT │      1 │         1.25 │           0.604 │          0.6 │      1:22:00 │    1     0     0   100 │
│ PEPE/USDT:USDT │      2 │         0.59 │           0.584 │         0.58 │      2:10:00 │    1     1     0   100 │
│  ETH/USDT:USDT │      1 │          1.2 │           0.576 │         0.58 │      3:12:00 │    1     0     0   100 │
│  BNB/USDT:USDT │      1 │         1.17 │           0.549 │         0.55 │      0:48:00 │    1     0     0   100 │
│  BTC/USDT:USDT │      0 │          0.0 │           0.000 │          0.0 │         0:00 │    0     0     0     0 │
│  SOL/USDT:USDT │      0 │          0.0 │           0.000 │          0.0 │         0:00 │    0     0     0     0 │
│          TOTAL │     20 │         1.24 │          11.960 │        11.96 │      2:02:00 │   16     4     0   100 │
└────────────────┴────────┴──────────────┴─────────────────┴──────────────┴──────────────┴────────────────────────┘
                                         LEFT OPEN TRADES REPORT                                          
┏━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┓
┃  Pair ┃ Trades ┃ Avg Profit % ┃ Tot Profit USDT ┃ Tot Profit % ┃ Avg Duration ┃  Win  Draw  Loss  Win% ┃
┡━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━┩
│ TOTAL │      0 │          0.0 │           0.000 │          0.0 │         0:00 │    0     0     0     0 │
└───────┴────────┴──────────────┴─────────────────┴──────────────┴──────────────┴────────────────────────┘
                                                ENTER TAG STATS                                                
┏━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Enter Tag ┃ Entries ┃ Avg Profit % ┃ Tot Profit USDT ┃ Tot Profit % ┃ Avg Duration ┃  Win  Draw  Loss  Win% ┃
┡━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━┩
│     OTHER │      20 │         1.24 │          11.960 │        11.96 │      2:02:00 │   16     4     0   100 │
│     TOTAL │      20 │         1.24 │          11.960 │        11.96 │      2:02:00 │   16     4     0   100 │
└───────────┴─────────┴──────────────┴─────────────────┴──────────────┴──────────────┴────────────────────────┘
                                                      EXIT REASON STATS                                                       
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                Exit Reason ┃ Exits ┃ Avg Profit % ┃ Tot Profit USDT ┃ Tot Profit % ┃ Avg Duration ┃  Win  Draw  Loss  Win% ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━┩
│ sell_profit_u_bear_1_1 ( ) │     6 │         1.26 │           3.528 │         3.53 │      0:02:00 │    6     0     0   100 │
│ sell_profit_u_bear_3_1 ( ) │     2 │         3.08 │           2.979 │         2.98 │      0:15:00 │    2     0     0   100 │
│ sell_profit_u_bear_1_4 ( ) │     2 │         1.09 │           1.056 │         1.06 │      0:42:00 │    2     0     0   100 │
│     sell_profit_w_2_17 ( ) │     1 │         2.02 │           1.001 │          1.0 │      1:32:00 │    1     0     0   100 │
│ sell_profit_u_bear_2_1 ( ) │     1 │          2.0 │           0.995 │          1.0 │      0:03:00 │    1     0     0   100 │
│ sell_profit_u_bear_1_2 ( ) │     1 │         1.23 │           0.611 │         0.61 │      0:06:00 │    1     0     0   100 │
│     sell_profit_w_1_17 ( ) │     1 │         1.24 │           0.610 │         0.61 │      1:35:00 │    1     0     0   100 │
│      sell_profit_w_1_3 ( ) │     1 │         1.25 │           0.604 │          0.6 │      1:22:00 │    1     0     0   100 │
│                        roi │     5 │         0.24 │           0.576 │         0.58 │      6:46:00 │    1     4     0   100 │
│                      TOTAL │    20 │         1.24 │          11.960 │        11.96 │      2:02:00 │   16     4     0   100 │
└────────────────────────────┴───────┴──────────────┴─────────────────┴──────────────┴──────────────┴────────────────────────┘
                                                              MIXED TAG STATS                                                              
┏━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Enter Tag ┃                Exit Reason ┃ Trades ┃ Avg Profit % ┃ Tot Profit USDT ┃ Tot Profit % ┃ Avg Duration ┃  Win  Draw  Loss  Win% ┃
┡━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━┩
│           │ sell_profit_u_bear_1_1 ( ) │      6 │         1.26 │           3.528 │         3.53 │      0:02:00 │    6     0     0   100 │
│           │ sell_profit_u_bear_3_1 ( ) │      2 │         3.08 │           2.979 │         2.98 │      0:15:00 │    2     0     0   100 │
│           │ sell_profit_u_bear_1_4 ( ) │      2 │         1.09 │           1.056 │         1.06 │      0:42:00 │    2     0     0   100 │
│           │     sell_profit_w_2_17 ( ) │      1 │         2.02 │           1.001 │          1.0 │      1:32:00 │    1     0     0   100 │
│           │ sell_profit_u_bear_2_1 ( ) │      1 │          2.0 │           0.995 │          1.0 │      0:03:00 │    1     0     0   100 │
│           │ sell_profit_u_bear_1_2 ( ) │      1 │         1.23 │           0.611 │         0.61 │      0:06:00 │    1     0     0   100 │
│           │     sell_profit_w_1_17 ( ) │      1 │         1.24 │           0.610 │         0.61 │      1:35:00 │    1     0     0   100 │
│           │      sell_profit_w_1_3 ( ) │      1 │         1.25 │           0.604 │          0.6 │      1:22:00 │    1     0     0   100 │
│           │                        roi │      5 │         0.24 │           0.576 │         0.58 │      6:46:00 │    1     4     0   100 │
│     TOTAL │                            │     20 │         1.24 │          11.960 │        11.96 │      2:02:00 │   16     4     0   100 │
└───────────┴────────────────────────────┴────────┴──────────────┴─────────────────┴──────────────┴──────────────┴────────────────────────┘
                         SUMMARY METRICS                          
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Metric                        ┃ Value                          ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Backtesting from              │ 2024-01-01 00:00:00            │
│ Backtesting to                │ 2026-04-01 00:00:00            │
│ Trading Mode                  │ Isolated Futures               │
│ Max open trades               │ 5                              │
│                               │                                │
│ Total/Daily Avg Trades        │ 20 / 0.02                      │
│ Starting balance              │ 100 USDT                       │
│ Final balance                 │ 111.96 USDT                    │
│ Absolute profit               │ 11.96 USDT                     │
│ Total profit %                │ 11.96%                         │
│ CAGR %                        │ 5.15%                          │
│ Sortino                       │ -100.00                        │
│ Sharpe                        │ 0.68                           │
│ Calmar                        │ -100.00                        │
│ SQN                           │ 6.35                           │
│ Profit factor                 │ 0.00                           │
│ Expectancy (Ratio)            │ 0.60 (100.00)                  │
│ Avg. daily profit             │ 0.015 USDT                     │
│ Avg. stake amount             │ 47.794 USDT                    │
│ Total trade volume            │ 1931.432 USDT                  │
│                               │                                │
│ Best Pair                     │ LTC/USDT:USDT 3.31%            │
│ Worst Pair                    │ BTC/USDT:USDT 0.00%            │
│ Best trade                    │ LTC/USDT:USDT 3.10%            │
│ Worst trade                   │ DOGE/USDT:USDT 0.00%           │
│ Best day                      │ 3.599 USDT                     │
│ Worst day                     │ 0 USDT                         │
│ Days win/draw/lose            │ 9 / 638 / 0                    │
│ Min/Max/Avg. Duration Winners │ 0d 00:01 / 0d 03:12 / 0d 00:37 │
│ Min/Max/Avg. Duration Losers  │ 0d 00:00 / 0d 00:00 / 0d 00:00 │
│ Max Consecutive Wins / Loss   │ 6 / 2                          │
│ Rejected Entry signals        │ 0                              │
│ Entry/Exit Timeouts           │ 0 / 0                          │
│                               │                                │
│ Min balance                   │ 100.502 USDT                   │
│ Max balance                   │ 111.96 USDT                    │
│ Max % of account underwater   │ 0.00%                          │
│ Absolute drawdown             │ 0 USDT (0.00%)                 │
│ Drawdown duration             │ 0 days 00:00:00                │
│ Profit at drawdown start      │ 0 USDT                         │
│ Profit at drawdown end        │ 0 USDT                         │
│ Drawdown start                │ 2024-01-03 12:16:00            │
│ Drawdown end                  │ 2024-01-03 12:16:00            │
│ Market change                 │ 26.90%                         │
└───────────────────────────────┴────────────────────────────────┘

Backtested 2024-01-01 00:00:00 -> 2026-04-01 00:00:00 | Max open trades : 5
                                                               STRATEGY SUMMARY                                                               
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┓
┃                  Strategy ┃ Trades ┃ Avg Profit % ┃ Tot Profit USDT ┃ Tot Profit % ┃ Avg Duration ┃  Win  Draw  Loss  Win% ┃      Drawdown ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━┩
│ NostalgiaForInfinityNext… │     20 │         1.24 │          11.960 │        11.96 │      2:02:00 │   16     4     0   100 │ 0 USDT  0.00% │
└───────────────────────────┴────────┴──────────────┴─────────────────┴──────────────┴──────────────┴────────────────────────┴───────────────┘
(.venv) watson@u2404:~/work/freqtrd$ 

