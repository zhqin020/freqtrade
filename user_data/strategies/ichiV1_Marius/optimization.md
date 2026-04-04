1. 增加杠杆：
2026-04-03 23:56:34,215 - freqtrade.optimize.backtesting - INFO - Backtesting with data from 2024-01-01 00:00:00 up to 
2026-04-02 15:05:00 (822 days).
/home/watson/work/freqtrd/freqtrade/data/metrics.py:77: FutureWarning: The default fill_method='pad' in DataFrame.pct_change is deprecated and will be removed in a future version. Either fill in any non-leading NA values prior to calling pct_change or specify 'fill_method=None' to not fill NA values.
  rel_mean = df_comb.pct_change().mean(axis=1).fillna(0).cumsum()
2026-04-03 23:57:08,763 - freqtrade.misc - INFO - dumping json to 
"/home/watson/work/freqtrd/user_data/backtest_results/backtest-result-2026-04-03_23-57-08.meta.json"
Result for strategy ichiV1_Marius
                                                BACKTESTING REPORT                                                 
┏━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┓
┃           Pair ┃ Trades ┃ Avg Profit % ┃ Tot Profit USDT ┃ Tot Profit % ┃ Avg Duration ┃  Win  Draw  Loss  Win% ┃
┡━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━┩
│  ADA/USDT:USDT │     42 │         2.48 │         154.507 │        15.45 │      0:57:00 │   33     0     9  78.6 │
│ PEPE/USDT:USDT │    143 │         2.31 │         139.764 │        13.98 │      0:50:00 │  101     0    42  70.6 │
│  SUI/USDT:USDT │     83 │         2.34 │         129.213 │        12.92 │      0:48:00 │   62     0    21  74.7 │
│ ATOM/USDT:USDT │     24 │         2.42 │         102.240 │        10.22 │      1:01:00 │   20     0     4  83.3 │
│ NEAR/USDT:USDT │     89 │         2.23 │          48.529 │         4.85 │      1:01:00 │   70     1    18  78.7 │
│  ETC/USDT:USDT │     19 │         2.02 │          44.210 │         4.42 │      2:22:00 │   13     3     3  68.4 │
│ AVAX/USDT:USDT │     37 │         1.59 │          41.835 │         4.18 │      1:30:00 │   27     3     7  73.0 │
│  LTC/USDT:USDT │     17 │         2.11 │          35.541 │         3.55 │      0:49:00 │   11     1     5  64.7 │
│  ETH/USDT:USDT │     11 │         2.52 │          33.617 │         3.36 │      0:34:00 │    7     0     4  63.6 │
│  SOL/USDT:USDT │     33 │         2.36 │          32.156 │         3.22 │      1:04:00 │   26     3     4  78.8 │
│  BTC/USDT:USDT │      3 │          3.3 │           9.758 │         0.98 │      0:45:00 │    3     0     0   100 │
│  BNB/USDT:USDT │      2 │         3.39 │           6.761 │         0.68 │      0:55:00 │    2     0     0   100 │
│ DOGE/USDT:USDT │     56 │         1.38 │          -2.830 │        -0.28 │      1:00:00 │   35     0    21  62.5 │
│ LINK/USDT:USDT │     34 │         1.58 │         -59.678 │        -5.97 │      1:13:00 │   25     2     7  73.5 │
│  XRP/USDT:USDT │     36 │         1.65 │        -121.854 │       -12.19 │      2:00:00 │   30     0     6  83.3 │
│          TOTAL │    629 │         2.12 │         593.766 │        59.38 │      1:04:00 │  465    13   151  73.9 │
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
│     OTHER │     629 │         2.12 │         593.766 │        59.38 │      1:04:00 │  465    13   151  73.9 │
│     TOTAL │     629 │         2.12 │         593.766 │        59.38 │      1:04:00 │  465    13   151  73.9 │
└───────────┴─────────┴──────────────┴─────────────────┴──────────────┴──────────────┴────────────────────────┘
                                                  EXIT REASON STATS                                                   
┏━━━━━━━━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┓
┃        Exit Reason ┃ Exits ┃ Avg Profit % ┃ Tot Profit USDT ┃ Tot Profit % ┃ Avg Duration ┃  Win  Draw  Loss  Win% ┃
┡━━━━━━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━┩
│                roi │   283 │         2.19 │        1225.789 │       122.58 │      1:57:00 │  260    13    10  91.9 │
│ trailing_stop_loss │   346 │         2.06 │        -632.023 │        -63.2 │      0:21:00 │  205     0   141  59.2 │
│              TOTAL │   629 │         2.12 │         593.766 │        59.38 │      1:04:00 │  465    13   151  73.9 │
└────────────────────┴───────┴──────────────┴─────────────────┴──────────────┴──────────────┴────────────────────────┘
                                                    MIXED TAG STATS                                                    
┏━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┓
┃           ┃                ┃        ┃              ┃                 ┃              ┃              ┃      Win  Draw ┃
┃ Enter Tag ┃    Exit Reason ┃ Trades ┃ Avg Profit % ┃ Tot Profit USDT ┃ Tot Profit % ┃ Avg Duration ┃     Loss  Win% ┃
┡━━━━━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━┩
│           │            roi │    283 │         2.19 │        1225.789 │       122.58 │      1:57:00 │      260    13 │
│           │                │        │              │                 │              │              │       10  91.9 │
│           │ trailing_stop… │    346 │         2.06 │        -632.023 │        -63.2 │      0:21:00 │      205     0 │
│           │                │        │              │                 │              │              │      141  59.2 │
│     TOTAL │                │    629 │         2.12 │         593.766 │        59.38 │      1:04:00 │      465    13 │
│           │                │        │              │                 │              │              │      151  73.9 │
└───────────┴────────────────┴────────┴──────────────┴─────────────────┴──────────────┴──────────────┴────────────────┘
                         SUMMARY METRICS                          
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Metric                        ┃ Value                          ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Backtesting from              │ 2024-01-01 00:00:00            │
│ Backtesting to                │ 2026-04-02 15:05:00            │
│ Trading Mode                  │ Isolated Futures               │
│ Max open trades               │ 5                              │
│                               │                                │
│ Total/Daily Avg Trades        │ 629 / 0.77                     │
│ Starting balance              │ 1000 USDT                      │
│ Final balance                 │ 1593.766 USDT                  │
│ Absolute profit               │ 593.766 USDT                   │
│ Total profit %                │ 59.38%                         │
│ CAGR %                        │ 22.99%                         │
│ Sortino                       │ 0.45                           │
│ Sharpe                        │ 0.83                           │
│ Calmar                        │ 5.08                           │
│ SQN                           │ 1.43                           │
│ Profit factor                 │ 1.38                           │
│ Expectancy (Ratio)            │ 0.94 (0.07)                    │
│ Avg. daily profit             │ 0.722 USDT                     │
│ Avg. stake amount             │ 191.355 USDT                   │
│ Total trade volume            │ 723492.046 USDT                │
│                               │                                │
│ Best Pair                     │ ADA/USDT:USDT 15.45%           │
│ Worst Pair                    │ XRP/USDT:USDT -12.19%          │
│ Best trade                    │ PEPE/USDT:USDT 16.53%          │
│ Worst trade                   │ AVAX/USDT:USDT -16.41%         │
│ Best day                      │ 139.704 USDT                   │
│ Worst day                     │ -179.195 USDT                  │
│ Days win/draw/lose            │ 169 / 617 / 26                 │
│ Min/Max/Avg. Duration Winners │ 0d 00:05 / 1d 00:50 / 0d 01:01 │
│ Min/Max/Avg. Duration Losers  │ 0d 00:00 / 0d 12:50 / 0d 00:49 │
│ Max Consecutive Wins / Loss   │ 22 / 8                         │
│ Rejected Entry signals        │ 19                             │
│ Entry/Exit Timeouts           │ 0 / 0                          │
│                               │                                │
│ Min balance                   │ 870.325 USDT                   │
│ Max balance                   │ 1608.929 USDT                  │
│ Max % of account underwater   │ 27.18%                         │
│ Absolute drawdown             │ 407.091 USDT (27.18%)          │
│ Drawdown duration             │ 48 days 02:25:00               │
│ Profit at drawdown start      │ 497.913 USDT                   │
│ Profit at drawdown end        │ 90.822 USDT                    │
│ Drawdown start                │ 2024-12-02 19:30:00            │
│ Drawdown end                  │ 2025-01-19 21:55:00            │
│ Market change                 │ -2.38%                         │
└───────────────────────────────┴────────────────────────────────┘

Backtested 2024-01-01 00:00:00 -> 2026-04-02 15:05:00 | Max open trades : 5
                                                   STRATEGY SUMMARY                                                    
┏━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┓
┃               ┃        ┃              ┃    Tot Profit ┃              ┃              ┃     Win  Draw ┃               ┃
┃      Strategy ┃ Trades ┃ Avg Profit % ┃          USDT ┃ Tot Profit % ┃ Avg Duration ┃    Loss  Win% ┃      Drawdown ┃
┡━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━┩
│ ichiV1_Marius │    629 │         2.12 │       593.766 │        59.38 │      1:04:00 │     465    13 │  407.091 USDT │
│               │        │              │               │              │              │     151  73.9 │        27.18% │
└───────────────┴────────┴──────────────┴───────────────┴──────────────┴──────────────┴───────────────┴───────────────┘
(.venv) watson@u2404:~/work/freqtrd$ 



2. 支持空单
