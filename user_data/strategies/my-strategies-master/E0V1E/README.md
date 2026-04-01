# my strategies

## command

```sh
source .venv/bin/activate && freqtrade hyperopt --strategy E0V1E --config user_data/config-E0V1E.json --spaces buy sell trailing --timerange 20240101-20260131 -e 300 -j 8 --hyperopt-loss SharpeHyperOptLoss --analyze-per-epoch

```

## The optimized parameters are stored in E0V1E.json.

## hyperopt process show

```
                                  ┏━━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━┓
                                  ┃ Best   ┃  Epoch ┃ Trades ┃  Win  Draw  Loss  Win% ┃ Avg profit ┃                    Profit ┃ Avg duration ┃ Objective ┃      Max Drawdown (Acct) ┃
                                  ┡━━━━━━━━╇━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━┩
                                  │ * Best │  3/500 │   1225 │ 1126     0    99  91.9 │      0.01% │  -199.500 USDT  (-39.50%) │      4:59:00 │   0.55029 │  781.496 USDT   (74.74%) │
                                  │ * Best │  4/500 │      3 │    2     0     1  66.7 │     -1.45% │   -25.182 USDT   (-4.99%) │      3:37:00 │   0.41138 │                       -- │
                                  │ * Best │  5/500 │   1252 │ 1150     0   102  91.9 │      0.13% │   631.965 USDT  (125.14%) │      4:09:00 │  -0.94139 │ 1376.340 USDT   (62.77%) │
                                  │ * Best │  8/500 │      5 │    4     0     1  80.0 │      1.70% │    43.898 USDT    (8.69%) │      0:35:00 │  -2.07054 │                       -- │
                                  │ * Best │ 10/500 │     11 │    9     0     2  81.8 │      2.21% │   132.756 USDT   (26.29%) │      0:54:00 │  -2.17570 │    2.534 USDT    (0.40%) │
                                  │ * Best │ 22/500 │    442 │  384     0    58  86.9 │      0.62% │  3917.091 USDT  (775.66%) │      3:25:00 │  -2.81709 │ 4528.847 USDT   (67.37%) │
                                  │ Best   │ 41/500 │    312 │  277     0    35  88.8 │      0.92% │ 5130.193 USDT (1,015.88%) │      2:45:00 │  -3.18003 │  704.429 USDT   (21.32%) │
                                  └────────┴────────┴────────┴────────────────────────┴────────────┴───────────────────────────┴──────────────┴───────────┴──────────────────────────┘
Epochs ━━━━━━━━━━━━━━━━━╺━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  49/500  10% • 2:07:29 • 0:00:07
User interrupted..
2024-12-29 19:24:53,706 - freqtrade.optimize.hyperopt.hyperopt - INFO - 49 epochs saved to 'C:\git-program\freqtrade\user_data\hyperopt_results\strategy_hyper_E0V1E_test_2024-12-29_17-16-59.fthypt'.
2024-12-29 19:24:53,903 - freqtrade.optimize.hyperopt_tools - INFO - Dumping parameters to C:\git-program\freqtrade\user_data\strategies\hyper_E0V1E_test.json

Best result:

    41/500:    312 trades. 277/0/35 Wins/Draws/Losses. Avg profit   0.92%. Median profit   1.54%. Total profit 5130.19274320 USDT (1015.88%). Avg duration 2:45:00 min. Objective: -3.180
```

## backtesting:

2026-03-30 17:32:36,660 - freqtrade.misc - INFO - dumping json to
"/home/watson/work/freqtrd/user_data/backtest_results/backtest-result-2026-03-30_17-32-36.meta.json"
Result for strategy E0V1E
BACKTESTING REPORT  
┏━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Pair ┃ Trades ┃ Avg Profit % ┃ Tot Profit USDT ┃ Tot Profit % ┃ Avg Duration ┃ Win Draw Loss Win% ┃
┡━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━┩
│ BCH/USDT:USDT │ 78 │ 2.38 │ 181.013 │ 18.1 │ 1 day, 14:17:00 │ 65 0 13 83.3 │
│ DOGE/USDT:USDT │ 104 │ 1.26 │ 129.570 │ 12.96 │ 1 day, 3:36:00 │ 72 0 32 69.2 │
│ XRP/USDT:USDT │ 72 │ 1.16 │ 82.729 │ 8.27 │ 1 day, 11:27:00 │ 52 0 20 72.2 │
│ ETH/USDT:USDT │ 60 │ 1.11 │ 64.842 │ 6.48 │ 3 days, 1:22:00 │ 41 0 19 68.3 │
│ ADA/USDT:USDT │ 83 │ 0.5 │ 37.569 │ 3.76 │ 1 day, 3:27:00 │ 57 0 26 68.7 │
│ BNB/USDT:USDT │ 58 │ 0.6 │ 33.190 │ 3.32 │ 2 days, 19:41:00 │ 46 0 12 79.3 │
│ BTC/USDT:USDT │ 33 │ 0.42 │ 11.808 │ 1.18 │ 4 days, 11:07:00 │ 25 0 8 75.8 │
│ HYPE/USDT:USDT │ 81 │ 0.1 │ 8.260 │ 0.83 │ 23:24:00 │ 56 0 25 69.1 │
│ TRX/USDT:USDT │ 43 │ 0.13 │ 5.333 │ 0.53 │ 2 days, 13:15:00 │ 33 0 10 76.7 │
│ SOL/USDT:USDT │ 89 │ 0.06 │ 4.761 │ 0.48 │ 1 day, 8:00:00 │ 57 0 32 64.0 │
│ TOTAL │ 701 │ 0.82 │ 559.074 │ 55.91 │ 1 day, 18:42:00 │ 504 0 197 71.9 │
└────────────────┴────────┴──────────────┴─────────────────┴──────────────┴──────────────────┴────────────────────────┘
LEFT OPEN TRADES REPORT  
┏━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Pair ┃ Trades ┃ Avg Profit % ┃ Tot Profit USDT ┃ Tot Profit % ┃ Avg Duration ┃ Win Draw Loss Win% ┃
┡━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━┩
│ HYPE/USDT:USDT │ 1 │ 1.46 │ 1.452 │ 0.15 │ 2:00:00 │ 1 0 0 100 │
│ TOTAL │ 1 │ 1.46 │ 1.452 │ 0.15 │ 2:00:00 │ 1 0 0 100 │
└────────────────┴────────┴──────────────┴─────────────────┴──────────────┴──────────────┴────────────────────────┘
ENTER TAG STATS  
┏━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Enter Tag ┃ Entries ┃ Avg Profit % ┃ Tot Profit USDT ┃ Tot Profit % ┃ Avg Duration ┃ Win Draw Loss Win% ┃
┡━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━┩
│ short_1 │ 466 │ 0.88 │ 400.495 │ 40.05 │ 2 days, 2:34:00 │ 341 0 125 73.2 │
│ buy_1 │ 164 │ 0.99 │ 159.729 │ 15.97 │ 1 day, 4:19:00 │ 116 0 48 70.7 │
│ buy_new │ 14 │ 1.81 │ 24.885 │ 2.49 │ 8:34:00 │ 12 0 2 85.7 │
│ short_new │ 57 │ -0.44 │ -26.034 │ -2.6 │ 1 day, 4:07:00 │ 35 0 22 61.4 │
│ TOTAL │ 701 │ 0.82 │ 559.074 │ 55.91 │ 1 day, 18:42:00 │ 504 0 197 71.9 │
└───────────┴─────────┴──────────────┴─────────────────┴──────────────┴─────────────────┴────────────────────────┘
EXIT REASON STATS  
┏━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Exit Reason ┃ Exits ┃ Avg Profit % ┃ Tot Profit USDT ┃ Tot Profit % ┃ Avg Duration ┃ Win Draw Loss Win% ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━┩
│ fastk_profit_sell_short │ 161 │ 1.8 │ 282.135 │ 28.21 │ 2 days, 5:45:00 │ 161 0 0 100 │
│ trailing_stop_loss │ 491 │ 0.34 │ 161.548 │ 16.15 │ 1 day, 17:14:00 │ 294 0 197 59.9 │
│ fastk_profit_sell │ 48 │ 2.41 │ 113.940 │ 11.39 │ 21:22:00 │ 48 0 0 100 │
│ force_exit │ 1 │ 1.46 │ 1.452 │ 0.15 │ 2:00:00 │ 1 0 0 100 │
│ TOTAL │ 701 │ 0.82 │ 559.074 │ 55.91 │ 1 day, 18:42:00 │ 504 0 197 71.9 │
└─────────────────────────┴───────┴──────────────┴─────────────────┴──────────────┴─────────────────┴────────────────────────┘
MIXED TAG STATS  
┏━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Enter Tag ┃ Exit Reason ┃ Trades ┃ Avg Profit % ┃ Tot Profit USDT ┃ Tot Profit % ┃ Avg Duration ┃ Win Draw Loss Win% ┃
┡━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━┩
│ short_1 │ fastk_profit_sell_sho… │ 150 │ 1.82 │ 266.970 │ 26.7 │ 2 days, 3:16:00 │ 150 0 0 100 │
│ short_1 │ trailing_stop_loss │ 315 │ 0.44 │ 132.073 │ 13.21 │ 2 days, 2:23:00 │ 190 0 125 60.3 │
│ buy_1 │ fastk_profit_sell │ 44 │ 2.54 │ 110.218 │ 11.02 │ 21:35:00 │ 44 0 0 100 │
│ buy_1 │ trailing_stop_loss │ 120 │ 0.43 │ 49.510 │ 4.95 │ 1 day, 6:46:00 │ 72 0 48 60.0 │
│ buy_new │ trailing_stop_loss │ 10 │ 2.17 │ 21.163 │ 2.12 │ 4:24:00 │ 8 0 2 80.0 │
│ short_new │ fastk_profit_sell_sho… │ 11 │ 1.42 │ 15.164 │ 1.52 │ 3 days, 15:27:00 │ 11 0 0 100 │
│ buy_new │ fastk_profit_sell │ 4 │ 0.93 │ 3.722 │ 0.37 │ 19:00:00 │ 4 0 0 100 │
│ short_1 │ force_exit │ 1 │ 1.46 │ 1.452 │ 0.15 │ 2:00:00 │ 1 0 0 100 │
│ short_new │ trailing_stop_loss │ 46 │ -0.89 │ -41.198 │ -4.12 │ 13:56:00 │ 24 0 22 52.2 │
│ TOTAL │ │ 701 │ 0.82 │ 559.074 │ 55.91 │ 1 day, 18:42:00 │ 504 0 197 71.9 │
└───────────┴────────────────────────┴────────┴──────────────┴─────────────────┴──────────────┴──────────────────┴────────────────────────┘
SUMMARY METRICS  
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Metric ┃ Value ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Backtesting from │ 2024-01-01 00:00:00 │
│ Backtesting to │ 2026-01-31 00:00:00 │
│ Trading Mode │ Isolated Futures │
│ Max open trades │ 5 │
│ │ │
│ Total/Daily Avg Trades │ 701 / 0.92 │
│ Starting balance │ 1000 USDT │
│ Final balance │ 1559.074 USDT │
│ Absolute profit │ 559.074 USDT │
│ Total profit % │ 55.91% │
│ CAGR % │ 23.74% │
│ Sortino │ 6.66 │
│ Sharpe │ 2.52 │
│ Calmar │ 14.45 │
│ SQN │ 3.78 │
│ Profit factor │ 1.38 │
│ Expectancy (Ratio) │ 0.80 (0.11) │
│ Avg. daily profit │ 0.735 USDT │
│ Avg. stake amount │ 98.17 USDT │
│ Total trade volume │ 137479.575 USDT │
│ │ │
│ Long / Short trades │ 178 / 523 │
│ Long / Short profit % │ 18.46% / 37.45% │
│ Long / Short profit USDT │ 184.614 / 374.461 │
│ │ │
│ Best Pair │ BCH/USDT:USDT 18.10% │
│ Worst Pair │ SOL/USDT:USDT 0.48% │
│ Best trade │ BNB/USDT:USDT 13.35% │
│ Worst trade │ DOGE/USDT:USDT -10.08% │
│ Best day │ 31.749 USDT │
│ Worst day │ -35.152 USDT │
│ Days win/draw/lose │ 247 / 387 / 126 │
│ Min/Max/Avg. Duration Winners │ 0d 01:00 / 25d 22:00 / 1d 15:59 │
│ Min/Max/Avg. Duration Losers │ 0d 00:00 / 12d 23:00 / 2d 01:39 │
│ Max Consecutive Wins / Loss │ 23 / 6 │
│ Rejected Entry signals │ 114 │
│ Entry/Exit Timeouts │ 0 / 0 │
│ │ │
│ Min balance │ 930.261 USDT │
│ Max balance │ 1559.074 USDT │
│ Max % of account underwater │ 9.81% │
│ Absolute drawdown │ 116.465 USDT (9.72%) │
│ Drawdown duration │ 25 days 11:00:00 │
│ Profit at drawdown start │ 198.687 USDT │
│ Profit at drawdown end │ 82.222 USDT │
│ Drawdown start │ 2024-11-09 04:00:00 │
│ Drawdown end │ 2024-12-04 15:00:00 │
│ Market change │ 77.47% │
└───────────────────────────────┴─────────────────────────────────┘

Backtested 2024-01-01 00:00:00 -> 2026-01-31 00:00:00 | Max open trades : 5
STRATEGY SUMMARY  
┏━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┓
┃ Strategy ┃ Trades ┃ Avg Profit % ┃ Tot Profit USDT ┃ Tot Profit % ┃ Avg Duration ┃ Win Draw Loss Win% ┃ Drawdown ┃
┡━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━┩
│ E0V1E │ 701 │ 0.82 │ 559.074 │ 55.91 │ 1 day, 18:42:00 │ 504 0 197 71.9 │ 116.465 USDT 9.72% │
└──────────┴────────┴──────────────┴─────────────────┴──────────────┴─────────────────┴────────────────────────┴─────────────────────┘
(.venv) watson@u24:~/work/freqtrd$
