# Freqtrade Setup and Verification Walkthrough

I have successfully set up the Freqtrade environment and verified that the bot is operational.

## Changes Made

- Created a virtual environment using `uv`.
- Installed Freqtrade dependencies in editable mode.
- Adjusted [user_data/config.json](file:///home/watson/work/freqtrd/user_data/config.json) to allow backtesting (set `stake_amount` to 100 and switched to `StaticPairList` for `BTC/USDT:USDT`).
- **Automated .venv Activation**: Updated [.vscode/settings.json](file:///home/watson/work/freqtrd/.vscode/settings.json) and [.vscode/terminal-init.sh](file:///home/watson/work/freqtrd/.vscode/terminal-init.sh) to automatically activate the `.venv` in any new VS Code terminal.
- **Fixed WebUI Startup Error**: Refactored `freqtrade/rpc/api_server/webserver.py` to use the modern FastAPI `lifespan` pattern, resolving an `AttributeError` caused by deprecated startup/shutdown event handlers in recent FastAPI versions.

## Verification Results

### 1. Installation Check

The bot version and dependencies were verified:

```bash
Freqtrade Version: freqtrade 2025.12-dev-6848f9197
Python Version: Python 3.13.9
CCXT Version: 4.5.45
```

### 2. Data Download

Sample data for `BTC/USDT:USDT` (futures) was downloaded for the range `20240101-20240102`.

```bash
freqtrade download-data --exchange okx --trading-mode futures --pairs BTC/USDT:USDT ETH/USDT:USDT --timerange 20260101-  -v

or:
freqtrade download-data  -t 1m 15m 5m 1h 2h 4h 1d --exchange okx --trading-mode futures  --timerange 20200101-  -v -c user_data/config-down.json --prepend

freqtrade list-data  --show-timerange

```

## 未来数据分析
freqtrade lookahead-analysis   --config user_data/config_ichiv1.json   --strategy ichiV1   --strategy-path user_data/freqtrade-strategies/strategies/ichiV1   --timerange 20240101-20260131


### 3. Backtesting


A backtest was successfully run using `SampleStrategy`:

```bash
freqtrade backtesting --config user_data/config.json --strategy SampleStrategy --strategy-path user_data/strategies --pairs BTC/USDT:USDT --timerange 20240101-20240102 --cache none
```

The backtest executed without errors, confirming the engine is working correctly.

## How to Proceed

1. **Open a New Terminal**:
   Simply open a new terminal in VS Code (`Ctrl + ~`), and it will automatically activate the `.venv`. You should see:

   ```bash
   ✓ freqtrade .venv activated
   ```

2. **Run Backtesting**:

   ```bash
   freqtrade backtesting --config user_data/config.json --strategy <StrategyName>
   ```

3. **Start Dry-run Trading (Starts UI automatically)**:

   ```bash
   freqtrade trade --config user_data/config.json --strategy <StrategyName>
   ```

4. **Start Web UI Only (Without Trading)**:

   ```bash
   freqtrade webserver --config user_data/config.json
   ```

5. **Access the WebUI**:
   Once the bot is running, open your browser and go to `http://127.0.0.1:8080`.
   - **Username**: `freqtrader`
   - **Password**: `freqtrader`

6. **参数调优（Hyperopt）**

目标：先优化 short 参数，同时保持 long 参数不变且继续参与交易。

前置设置（策略中）：
- `optimize_side = 'both'`
- `enable_long_entries = True`
- `enable_short_entries = True`

快速冒烟（先确认命令可跑）：

```bash
source .venv/bin/activate && freqtrade hyperopt \
   --strategy NostalgiaForInfinityX \
   --strategy-path user_data/freqtrade-strategies/strategies/NostalgiaForInfinityX \
   --config user_data/config.json \
   --hyperopt-loss SharpeHyperOptLossDaily \
   --timerange 20250101-20260402 \
   --spaces buy sell \
   --epochs 5 \
   --print-all
```

正式优化（建议）：

```bash
source .venv/bin/activate && freqtrade hyperopt \
   --strategy NostalgiaForInfinityX \
   --strategy-path user_data/freqtrade-strategies/strategies/NostalgiaForInfinityX \
   --config user_data/config.json \
   --hyperopt-loss SharpeHyperOptLossDaily \
   --timerange 20250101-20260402 \
   --spaces buy sell \
   --epochs 80 \
   --random-state 42 \
   --print-all
```

参数说明：
- `--spaces buy sell`：会覆盖 short 入场与 short 退出参数（它们已被定义为 Parameter），long 参数不参与搜索。
- `--hyperopt-loss SharpeHyperOptLossDaily`：在你的长区间数据上更稳定，适合作为第一轮目标函数。
- `--random-state 42`：保证可复现，便于不同轮次对比。

结果导出到策略：

```bash
source .venv/bin/activate && freqtrade hyperopt-show \
   --strategy NostalgiaForInfinityX \
   --config user_data/config.json \
   --best
```


> [!NOTE]
> If you are accessing this from another machine, you may need to update the `listen_ip_address` in `user_data/config.json` to `0.0.0.0`.
