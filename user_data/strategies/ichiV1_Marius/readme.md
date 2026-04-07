我会先在代码库里定位 ichiV1_Marius 策略源码与相关配置，然后逐段阅读并提炼它的交易逻辑、信号条件和全部可调参数，最后给你一份结构化的中文解读。

Searched for text `ichiV1_Marius`, 20 results

Read memory [](file:///home/watson/.vscode-server/data/User/workspaceStorage/b54667ae71add81eb2af90b537bd8a19/GitHub.copilot-chat/memory-tool/memories/repo/freqtrade-notes.md)

我已经定位到策略源码，下一步会读取策略主文件和对应参数文件，整理出“指标计算→开仓→风控→平仓”的完整链路，并把所有可调参数按用途分类。

Read [](file:///home/watson/work/freqtrd/user_data/strategies/ichiV1_Marius/ichiV1_Marius.py#1-1), lines 1 to 320

Read [](file:///home/watson/work/freqtrd/user_data/strategies/ichiV1_Marius/optimization.md)

目前已经拿到核心代码前半段，包含超参数、DCA、杠杆与风控骨架。接下来我会补读后半段（入场/出场条件与指标计算）并确认是否存在独立参数文件。

Read [](file:///home/watson/work/freqtrd/user_data/strategies/ichiV1_Marius)

Read [](file:///home/watson/work/freqtrd/user_data/strategies/ichiV1_Marius/ichiV1_Marius.py#321-321), lines 321 to 760

Read [](file:///home/watson/work/freqtrd/user_data/strategies/ichiV1_Marius/ichiV1_Marius.py#761-761), lines 761 to 940

我已经拿到完整策略逻辑，接着再读同目录的参数导出文件，确认你当前实际在用的是哪些参数值，再给你一份“默认值 vs 优化值”的对照。

Read [](file:///home/watson/work/freqtrd/user_data/strategies/ichiV1_Marius/ichiV1_Marius-sell.json)

Read [](file:///home/watson/work/freqtrd/user_data/strategies/ichiV1_Marius/compare.md)

Searched for regex `class ichiV1_Marius|buy_params =|sell_params =|buy_minimum_conditions|short_enabled|position_adjustment_enable|max_dca_orders|max_dca_multiplier|dca_stake_multiplier|def leverage|def custom_stake_amount|def adjust_trade_position|pump_period = IntParameter|pump_limit = IntParameter|pump_recorver_price = DecimalParameter|pump_pause_duration = IntParameter|max_slip = DecimalParameter|buy_btc_safe = IntParameter|buy_btc_safe_1d = DecimalParameter|antipump_threshold = DecimalParameter|antipump_threshold_2 = DecimalParameter|buy_min_fan_magnitude_gain = DecimalParameter|buy_threshold = DecimalParameter|minimal_roi =|stoploss =|window_buy = IntParameter|bandwidth_buy = IntParameter|mult_buy = DecimalParameter|timeframe =|informative_timeframe =|inf_15m =|startup_candle_count|use_exit_signal =|ignore_roi_if_entry_signal =|pHSL = DecimalParameter|ProfitMargin1 = DecimalParameter|ProfitLoss1 = DecimalParameter|ProfitMargin2 = DecimalParameter|ProfitLoss2 = DecimalParameter|slippage_protection =|def custom_exit|def custom_stoploss|def confirm_trade_exit|def informative_pairs|def informative_1h_indicators|def informative_15m_indicators|def normal_tf_indicators|def populate_indicators|def confirm_trade_entry|def populate_buy_trend|def populate_entry_trend|def populate_sell_trend|def populate_exit_trend|def pct_change` (`**/user_data/strategies/ichiV1_Marius/ichiV1_Marius.py`), 20 results

Searched for regex `pump_pause_duration = IntParameter|max_slip = DecimalParameter|buy_btc_safe = IntParameter|buy_btc_safe_1d = DecimalParameter|antipump_threshold = DecimalParameter|antipump_threshold_2 = DecimalParameter|buy_min_fan_magnitude_gain = DecimalParameter|buy_threshold = DecimalParameter|minimal_roi =|stoploss =|window_buy = IntParameter|bandwidth_buy = IntParameter|mult_buy = DecimalParameter|timeframe =|informative_timeframe =|inf_15m =|startup_candle_count|use_exit_signal =|ignore_roi_if_entry_signal =|pHSL = DecimalParameter|ProfitMargin1 = DecimalParameter|ProfitLoss1 = DecimalParameter|ProfitMargin2 = DecimalParameter|ProfitLoss2 = DecimalParameter|slippage_protection =|def custom_exit|def custom_stoploss|def confirm_trade_exit|def informative_pairs|def informative_1h_indicators|def informative_15m_indicators|def normal_tf_indicators|def populate_indicators|def confirm_trade_entry|def populate_buy_trend|def populate_entry_trend|def populate_sell_trend|def populate_exit_trend|tesla_|telsa_` (`**/user_data/strategies/ichiV1_Marius/ichiV1_Marius.py`), 47 results

源码和参数文件都已核对完成，我现在整理成一份详细解读：会先讲策略执行链路，再给参数总表，并标出几个“看起来可疑/未生效”的参数点，方便你后续优化。这个策略的定位可以先一句话概括：

它是一个 5m 主周期的多周期趋势策略，核心是 Ichimoku + EMA 趋势结构，叠加 BTC 风险过滤、15m 抽水检测、滑点保护、杠杆与 DCA、分段自定义止损，属于“趋势进场 + 强风控管理”的实盘化版本。  
核心源码在 ichiV1_Marius.py，当前参数导出在 ichiV1_Marius-sell.json。

**工作原理**
1. 数据层与时间框架
1. 主周期是 5m: ichiV1_Marius.py。
2. 额外使用 1h 和 15m 的同币种数据，以及 BTC 的 1m/5m/1d 数据做宏观过滤: ichiV1_Marius.py。
3. 启动需要 499 根 K 线，说明它依赖长窗口统计（比如 rolling 499）: ichiV1_Marius.py。

2. 指标层（你可以理解为“信号原料”）
1. 趋势类: 多组 EMA、HMA、Ichimoku 云、fan_magnitude/fan_magnitude_gain。
2. 动量类: RSI、MFI。
3. 风险类:
- BTC 5m 与 1d 的相对变化，用来判断市场是否处于风险段。
- pump_strength_2（EMA50 vs EMA200 差值比例）做反拉盘过滤。
- 15m 的流量价格指标 max_flow_price/flow_price 检测“是否刚经历拉盘后回落”。
4. 这些都在 ichiV1_Marius.py、ichiV1_Marius.py、ichiV1_Marius.py、ichiV1_Marius.py。

3. 入场逻辑（做多）
1. 先过保护门槛（is_protection）: ichiV1_Marius.py
- BTC 1d 相对变化不太差（阈值 buy_btc_safe_1d）
- pump_strength_2 小于 antipump_threshold_2
- buy_ok 为真（即没触发抽水警报）
- 成交量 > 0
2. 再过趋势门槛（tesla 条件）:
- RSI(5m) > RSI(1h)
- 多组 trend_close / trend_open 呈多头结构
- trend_close_1h > ema55，ema21 > trend_close_4h
- MFI < 70
- fan_magnitude_gain 达标且 fan_magnitude > 0.99
3. 满足后打 buy=1，并打标签 tesla_。

4. 入场逻辑（做空，可选）
1. 策略声明支持做空: ichiV1_Marius.py。
2. 但默认 short_enabled=False，做空默认关闭: ichiV1_Marius.py。
3. 若开启，做空条件基本是做多条件的反向版本: ichiV1_Marius.py。

5. 持仓管理与仓位
1. 固定杠杆 2x: ichiV1_Marius.py。
2. 支持 DCA 加仓:
- 最多 2 次加仓: ichiV1_Marius.py
- 每次加仓规模 = 首单成本 × 1.25: ichiV1_Marius.py
- 仅在浮亏超过 -5% 时才考虑加仓
- 多单要求“价格开始回升”才补，空单要求“价格重新下行”才补
3. 若 stake_amount=unlimited，会自动把单次初始仓位按 max_open_trades 和 DCA 预留进行缩放: ichiV1_Marius.py。

6. 出场与止损
1. ROI 表: ichiV1_Marius.py。
2. 全局硬止损: stoploss=-0.275。
3. 自定义动态止损启用: ichiV1_Marius.py, ichiV1_Marius.py。
4. 自定义止损是三段式并按杠杆缩放（关键）:
$$
SL(p)=
\begin{cases}
PL2,& p>PM2\\
PL1+\frac{(p-PM1)(PL2-PL1)}{PM2-PM1},& PM1<p\le PM2\\
HSL,& p\le PM1
\end{cases}
$$
其中 $p$ 为当前收益率，且 $HSL,PM1,PM2,PL1,PL2$ 都会乘以杠杆。
5. 额外离场控制:
- 开仓超过 1440 分钟可触发 unclog 清仓: ichiV1_Marius.py
- confirm_trade_exit 会在某些走势条件下拒绝卖出，并带滑点重试保护: ichiV1_Marius.py

---

**参数总表（你最关心的）**

下面按“当前导出值”为准（来自 ichiV1_Marius-sell.json），并结合源码解释作用。

1. 基础交易参数
- timeframe: 5m
- informative_timeframe: 1h
- inf_15m: 15m
- can_short: true（但 short_enabled 默认 false）
- max_open_trades: 5
- leverage: 固定 2.0

2. ROI / 止损 / 跟踪
- minimal_roi: {0: 0.215, 40: 0.032, 87: 0.016, 201: 0}
- stoploss: -0.275
- trailing_stop: false
- trailing_stop_positive: null
- trailing_stop_positive_offset: 0.0
- trailing_only_offset_is_reached: false

3. 自定义止损参数（sell 空间）
- pHSL: -0.118（导出值）
- ProfitMargin1: 0.019
- ProfitLoss1: 0.005
- ProfitMargin2: 0.079
- ProfitLoss2: 0.023

4. 买入与风控参数（buy 空间）
- short_enabled: false
- buy_minimum_conditions: 1
- max_slip: 0.668（入场允许最大滑点百分比）
- buy_threshold: 0.012（BTC 5m 快速下跌过滤阈值）
- buy_btc_safe_1d: -0.236（BTC 日级过滤）
- buy_btc_safe: -213（当前代码里基本未参与关键判断）
- antipump_threshold: 0.265（当前主路径基本未用）
- antipump_threshold_2: 0.133（关键过滤项）
- pump_period: 14
- pump_limit: 1000
- pump_pause_duration: 192
- pump_recorver_price: 1.1
- buy_min_fan_magnitude_gain: 1.002
- window_buy: 500（当前主路径未见直接使用）
- bandwidth_buy: 8（当前主路径未见直接使用）
- mult_buy: 3（当前主路径未见直接使用）

5. 仓位与 DCA
- position_adjustment_enable: true
- max_dca_orders: 2
- max_dca_multiplier: 1.25
- dca_stake_multiplier: 1.25

---

**你需要注意的几个实现细节（非常重要）**
1. 策略里有一个拼写不一致点:  
买入标签写的是 tesla_，但退出检查里有 telsa_ 分支，见 ichiV1_Marius.py 和 ichiV1_Marius.py。  
这会导致该分支几乎永远不触发。

2. 参数 buy_min_fan_magnitude_gain 的声明区间是 70 到 90，但默认值和导出值约 1.002，见 ichiV1_Marius.py。  
从量纲看这很可疑，像是区间写错了。

3. 你当前配置里 use_exit_signal=false 且 ignore_roi_if_entry_signal=true，意味着它主要依赖 ROI + 自定义止损体系，不是传统“卖出信号主导”。

4. 部分参数在当前主逻辑里影响很弱或未直接使用（如 buy_btc_safe、window_buy、bandwidth_buy、mult_buy、antipump_threshold），后续调参时可优先聚焦真正生效的参数，避免“调了但没作用”。

---

如果你愿意，我下一步可以直接给你两份内容，方便你实操：
1. 一份“优先调参清单”（先调哪 6-8 个参数最有收益）。  
2. 一份“参数瘦身建议”（把当前疑似无效/弱效参数标记出来，减少过拟合和调参时间）。